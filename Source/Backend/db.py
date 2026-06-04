"""
PostgreSQL database helpers for AI Smart Study Risk Predictor.

IMPORTANT: .env must never be committed to version control.
           Copy .env.example to .env and fill in real credentials locally.

Design notes:
- Hosted PostgreSQL is used (e.g. Supabase or Neon) because the app needs a
  shared database accessible from multiple devices and developers. A local
  SQLite file would not be visible to other machines.
- init_db() is non-destructive: it only creates tables that do not already
  exist and will never drop or reset existing data.
- Passwords are stored as bcrypt hashes. Plaintext passwords are never saved.
"""

import os

import bcrypt
import psycopg2
from dotenv import load_dotenv


def get_connection():
    """Return a psycopg2 connection using DATABASE_URL from .env.

    SSL settings embedded in the URL (e.g. ?sslmode=require) are preserved
    automatically by psycopg2 — no extra kwarg needed.

    Raises RuntimeError if DATABASE_URL is not set.
    """
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError(
            "DATABASE_URL is not set. "
            "Copy .env.example to .env and fill in your hosted PostgreSQL credentials."
        )
    return psycopg2.connect(db_url)


def init_db():
    """Create all required tables if they do not already exist.

    Safe to call multiple times — uses CREATE TABLE IF NOT EXISTS so no
    existing data is dropped or modified.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id           SERIAL PRIMARY KEY,
                        email        TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        full_name    TEXT,
                        created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS courses (
                        id         SERIAL PRIMARY KEY,
                        user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        name       TEXT NOT NULL,
                        difficulty TEXT,
                        workload   INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS pdfs (
                        id          SERIAL PRIMARY KEY,
                        user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        course_id   INTEGER REFERENCES courses(id) ON DELETE SET NULL,
                        filename    TEXT NOT NULL,
                        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS predictions (
                        id         SERIAL PRIMARY KEY,
                        user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        course_id  INTEGER REFERENCES courses(id) ON DELETE SET NULL,
                        risk_level TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
    finally:
        conn.close()


def create_user(email: str, password: str, full_name: str = None):
    """Register a new user and return the new user's id.

    - email is trimmed and lowercased before storage.
    - password is hashed with bcrypt; the plaintext is never stored.
    - Raises ValueError if the email is already registered.
    """
    email = (email or "").strip().lower()
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        """
                        INSERT INTO users (email, password_hash, full_name)
                        VALUES (%s, %s, %s)
                        RETURNING id
                        """,
                        (email, password_hash, full_name),
                    )
                    return cur.fetchone()[0]
                except psycopg2.errors.UniqueViolation:
                    raise ValueError(f"Email '{email}' is already registered.")
    finally:
        conn.close()


def get_user_by_email(email: str):
    """Return the user row for the given email, or None if not found.

    email is trimmed and lowercased before the lookup.
    Returns a psycopg2 Row (tuple) or None.
    """
    email = (email or "").strip().lower()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, email, password_hash, full_name, created_at FROM users WHERE email = %s",
                (email,),
            )
            return cur.fetchone()
    finally:
        conn.close()


def verify_user_password(email: str, password: str) -> bool:
    """Return True if the email/password pair is valid, False otherwise.

    Uses bcrypt.checkpw so the comparison is constant-time.
    """
    user = get_user_by_email(email)
    if user is None:
        return False
    password_hash = user[2]  # third column
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def save_prediction(user_id: int, risk_level: str, course_id: int = None) -> int:
    """Persist a prediction result for a user and return the new prediction id."""
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO predictions (user_id, course_id, risk_level)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (user_id, course_id, risk_level),
                )
                return cur.fetchone()[0]
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
