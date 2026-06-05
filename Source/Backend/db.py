"""
PostgreSQL database helpers for AI Smart Study Risk Predictor.

Design notes:
- Hosted PostgreSQL via Supabase — shared across all devices and developers.
- init_db() is non-destructive: CREATE TABLE IF NOT EXISTS + ALTER TABLE ADD COLUMN IF NOT EXISTS.
- Passwords and security answers are stored as bcrypt hashes. Plaintext is never saved.
- Security questions enable in-app password reset without any email infrastructure.
"""

import os
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
import psycopg2
from dotenv import load_dotenv

# Resolve .env relative to this file so it is found regardless of the
# working directory the app is launched from.
_ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env")


def get_connection():
    """Return a psycopg2 connection using DATABASE_URL from .env."""
    load_dotenv(_ENV_PATH, override=True)
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError(
            "DATABASE_URL is not set. "
            "Ensure the .env file exists at the project root with a valid DATABASE_URL."
        )
    return psycopg2.connect(db_url)


def init_db():
    """Create all tables and add any missing columns. Safe to call on every startup."""
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id                   SERIAL PRIMARY KEY,
                        email                TEXT UNIQUE NOT NULL,
                        password_hash        TEXT NOT NULL,
                        full_name            TEXT,
                        security_question    TEXT,
                        security_answer_hash TEXT,
                        created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                # Migrate existing installations that pre-date security columns
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS security_question TEXT")
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS security_answer_hash TEXT")

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

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS sessions (
                        id         SERIAL PRIMARY KEY,
                        user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        token      TEXT UNIQUE NOT NULL,
                        expires_at TIMESTAMP NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
    finally:
        conn.close()


# ── User management ───────────────────────────────────────────────────────────

def create_user(
    email: str,
    password: str,
    full_name: str = None,
    security_question: str = None,
    security_answer: str = None,
) -> int:
    """Register a new user and return the new user's id.

    - Security answer is normalised (stripped + lowercased) then bcrypt-hashed.
    - Raises ValueError if the email is already registered.
    """
    email = (email or "").strip().lower()
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    answer_hash = None
    if security_answer:
        normalised = (security_answer).strip().lower()
        answer_hash = bcrypt.hashpw(normalised.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        """
                        INSERT INTO users
                            (email, password_hash, full_name, security_question, security_answer_hash)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        (email, password_hash, full_name, security_question, answer_hash),
                    )
                    return cur.fetchone()[0]
                except psycopg2.errors.UniqueViolation:
                    raise ValueError(f"Email '{email}' is already registered.")
    finally:
        conn.close()


def get_user_by_email(email: str):
    """Return the full user row for the given email, or None."""
    email = (email or "").strip().lower()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, email, password_hash, full_name,
                       security_question, security_answer_hash, created_at
                FROM users WHERE email = %s
                """,
                (email,),
            )
            return cur.fetchone()
    finally:
        conn.close()


def verify_user_password(email: str, password: str) -> bool:
    """Return True if the email/password pair is valid."""
    user = get_user_by_email(email)
    if user is None:
        return False
    return bcrypt.checkpw(password.encode("utf-8"), user[2].encode("utf-8"))


# ── Security-question password reset ─────────────────────────────────────────

def get_security_question(email: str) -> str | None:
    """Return the security question for the given email, or None if not set."""
    user = get_user_by_email(email)
    if user is None:
        return None
    return user[4] or None  # security_question column


def verify_security_answer(email: str, plain_answer: str) -> bool:
    """Return True if plain_answer (case-insensitive) matches the stored hash."""
    user = get_user_by_email(email)
    if user is None or not user[5]:  # security_answer_hash column
        return False
    normalised = (plain_answer or "").strip().lower()
    return bcrypt.checkpw(normalised.encode("utf-8"), user[5].encode("utf-8"))


def reset_password_direct(email: str, new_password: str) -> bool:
    """Overwrite the password for the given email. Call only after answer verification."""
    email = (email or "").strip().lower()
    new_hash = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE users SET password_hash = %s WHERE email = %s",
                    (new_hash, email),
                )
                return cur.rowcount > 0
    finally:
        conn.close()


# ── Course CRUD (reserved — not used by current Streamlit UI) ─────────────────

def create_course(user_id: int, name: str, difficulty: str = "Medium", workload: int = 5) -> int:
    """Add a course for a user and return the new course id."""
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO courses (user_id, name, difficulty, workload)
                    VALUES (%s, %s, %s, %s) RETURNING id
                    """,
                    (user_id, name.strip(), difficulty, workload),
                )
                return cur.fetchone()[0]
    finally:
        conn.close()


def get_user_courses(user_id: int) -> list:
    """Return all courses for a user, ordered by creation date."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, difficulty, workload, created_at
                FROM courses WHERE user_id = %s ORDER BY created_at DESC
                """,
                (user_id,),
            )
            return cur.fetchall()
    finally:
        conn.close()


def update_course(course_id: int, user_id: int, name: str, difficulty: str, workload: int) -> bool:
    """Update a course. Only the owning user can modify it."""
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE courses SET name = %s, difficulty = %s, workload = %s
                    WHERE id = %s AND user_id = %s
                    """,
                    (name.strip(), difficulty, workload, course_id, user_id),
                )
                return cur.rowcount > 0
    finally:
        conn.close()


def delete_course(course_id: int, user_id: int) -> bool:
    """Delete a course. Only the owning user can delete it."""
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM courses WHERE id = %s AND user_id = %s",
                    (course_id, user_id),
                )
                return cur.rowcount > 0
    finally:
        conn.close()


# ── Persistent sessions (Remember Me) ────────────────────────────────────────

def create_session(user_id: int, days: int = 30) -> str:
    """Create a 30-day persistent login session and return the opaque token."""
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(days=days)
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO sessions (user_id, token, expires_at) VALUES (%s, %s, %s)",
                    (user_id, token, expires_at),
                )
    finally:
        conn.close()
    return token


def get_session_user(token: str):
    """Return the user row for a non-expired session token, or None."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT u.id, u.email, u.password_hash, u.full_name,
                       u.security_question, u.security_answer_hash, u.created_at
                FROM sessions s
                JOIN users u ON u.id = s.user_id
                WHERE s.token = %s AND s.expires_at > NOW()
                """,
                (token,),
            )
            return cur.fetchone()
    finally:
        conn.close()


def delete_session(token: str) -> None:
    """Invalidate a session on sign-out."""
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM sessions WHERE token = %s", (token,))
    finally:
        conn.close()


# ── Predictions ───────────────────────────────────────────────────────────────

def save_prediction(user_id: int, risk_level: str, course_id: int = None) -> int:
    """Persist a prediction result and return the new prediction id."""
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
