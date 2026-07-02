"""
PostgreSQL database helpers for AI Smart Study Risk Predictor.

Design notes:
- Hosted PostgreSQL via Supabase — shared across all devices and developers.
- init_db() is non-destructive: CREATE TABLE IF NOT EXISTS + ALTER TABLE ADD COLUMN IF NOT EXISTS.
- Passwords and security answers are stored as bcrypt hashes. Plaintext is never saved.
- Security questions enable in-app password reset without any email infrastructure.
- All query-result functions return plain dicts so callers never depend on column order.
- All parameterised queries use %s placeholders — psycopg2 escapes values automatically,
  providing full protection against SQL injection.

Data structures returned (stable contract for frontend):

  User Profile dict:
    { id, email, full_name, university, department, semester, target_gpa, created_at }

  Course dict:
    { id, user_id, name, difficulty, workload, study_hours, attendance,
      deadline_days, pass_grade, instructor, notes, created_at }

  Prediction dict:
    { id, user_id, course_id, course_name, risk_level, created_at }

  Study Schedule entry dict:
    { id, user_id, course_id, course_name, study_date, duration_minutes,
      topic, priority, completed, notes, created_at }

Public API summary:
  get_connection()                      — open a DB connection
  init_db()                             — create / migrate schema (idempotent)
  create_user(...)                      — register new user
  get_user_by_email(email)              — raw user row
  verify_user_password(email, password) — bcrypt check
  get_user_profile(user_id)             — profile dict
  update_user_profile(user_id, ...)     — update profile fields
  get_security_question(email)          — security question string
  verify_security_answer(email, answer) — bcrypt check
  reset_password_direct(email, pw)      — set new password hash
  create_course(user_id, name, ...)     — add course, returns id
  get_user_courses(user_id)             — list[dict]
  update_course(course_id, user_id, ...)— update course fields
  delete_course(course_id, user_id)     — delete course
  create_session(user_id)               — persistent login token
  get_session_user(token)               — raw user row for token
  delete_session(token)                 — invalidate token
  save_prediction(user_id, risk, ...)   — store prediction, returns id
  get_user_predictions(user_id, limit)  — list[dict] newest-first
  save_study_schedule(user_id, entries) — INSERT list of schedule entries
  upsert_study_schedule(user_id, entries)— REPLACE all schedule entries atomically
  get_user_schedule(user_id, ...)       — list[dict] filtered by date
  mark_schedule_complete(id, user_id)   — toggle completed flag
  clear_user_schedule(user_id)          — delete all schedule rows
"""

import os
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
import psycopg2
import psycopg2.errors
from dotenv import load_dotenv

_ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env")


# ── Connection ────────────────────────────────────────────────────────────────

def get_connection():
    """Return a psycopg2 connection using DATABASE_URL from .env."""
    load_dotenv(_ENV_PATH, override=True)
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError(
            "DATABASE_URL is not set. "
            "Ensure the .env file exists at the project root with a valid DATABASE_URL."
        )
    return psycopg2.connect(db_url, connect_timeout=5)


# ── Schema initialisation ─────────────────────────────────────────────────────

def init_db():
    """Create all tables and add any missing columns. Safe to call on every startup."""
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                # ── users ────────────────────────────────────────────────────
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
                for col in (
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS security_question    TEXT",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS security_answer_hash TEXT",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS university           TEXT",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS department           TEXT",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS semester             TEXT",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS target_gpa           REAL",
                ):
                    cur.execute(col)

                # ── courses ──────────────────────────────────────────────────
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
                for col in (
                    "ALTER TABLE courses ADD COLUMN IF NOT EXISTS workload_level  TEXT",
                    "ALTER TABLE courses ADD COLUMN IF NOT EXISTS study_hours     INTEGER DEFAULT 0",
                    "ALTER TABLE courses ADD COLUMN IF NOT EXISTS attendance      INTEGER DEFAULT 75",
                    "ALTER TABLE courses ADD COLUMN IF NOT EXISTS deadline_days   INTEGER DEFAULT 7",
                    "ALTER TABLE courses ADD COLUMN IF NOT EXISTS pass_grade      INTEGER DEFAULT 70",
                    "ALTER TABLE courses ADD COLUMN IF NOT EXISTS instructor      TEXT",
                    "ALTER TABLE courses ADD COLUMN IF NOT EXISTS notes           TEXT",
                ):
                    cur.execute(col)

                # Unique course name per user (idempotent via DO block)
                cur.execute("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM pg_constraint
                            WHERE conname = 'uq_courses_user_name'
                              AND conrelid = 'courses'::regclass
                        ) THEN
                            ALTER TABLE courses
                                ADD CONSTRAINT uq_courses_user_name UNIQUE (user_id, name);
                        END IF;
                    END $$
                """)

                # ── pdfs ─────────────────────────────────────────────────────
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS pdfs (
                        id          SERIAL PRIMARY KEY,
                        user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        course_id   INTEGER REFERENCES courses(id) ON DELETE SET NULL,
                        filename    TEXT NOT NULL,
                        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # ── predictions ──────────────────────────────────────────────
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS predictions (
                        id         SERIAL PRIMARY KEY,
                        user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        course_id  INTEGER REFERENCES courses(id) ON DELETE SET NULL,
                        risk_level TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cur.execute(
                    "ALTER TABLE predictions ADD COLUMN IF NOT EXISTS course_name TEXT"
                )

                # ── sessions ─────────────────────────────────────────────────
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS sessions (
                        id         SERIAL PRIMARY KEY,
                        user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        token      TEXT UNIQUE NOT NULL,
                        expires_at TIMESTAMP NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # ── study_schedules ──────────────────────────────────────────
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS study_schedules (
                        id               SERIAL PRIMARY KEY,
                        user_id          INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        course_id        INTEGER REFERENCES courses(id) ON DELETE SET NULL,
                        course_name      TEXT,
                        study_date       DATE NOT NULL,
                        duration_minutes INTEGER NOT NULL DEFAULT 60,
                        topic            TEXT,
                        priority         TEXT DEFAULT 'Medium',
                        completed        BOOLEAN DEFAULT FALSE,
                        notes            TEXT,
                        created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                # Add updated_at column for schedule entries (backward compat)
                cur.execute(
                    "ALTER TABLE study_schedules "
                    "ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
                )
    finally:
        conn.close()


# ── Internal helpers ──────────────────────────────────────────────────────────

def _row_to_profile(row) -> dict:
    return {
        "id":         row[0],
        "email":      row[1],
        "full_name":  row[2],
        "university": row[3],
        "department": row[4],
        "semester":   row[5],
        "target_gpa": row[6],
        "created_at": row[7],
    }


def _row_to_course(row) -> dict:
    diff = row[3] or "Medium"
    wl   = row[4] or "Medium"
    return {
        "id":                    row[0],
        "user_id":               row[1],
        "name":                  row[2],
        # Both aliases kept so risk_prediction.py and my_courses.py both work
        "difficulty":            diff,
        "assignment_difficulty": diff,
        "workload":              wl,
        "workload_level":        wl,
        "study_hours":           row[5] or 0,
        "attendance":            row[6] or 75,
        "deadline_days":         row[7] or 7,
        "pass_grade":            row[8] or 70,
        "instructor":            row[9] or "",
        "notes":                 row[10] or "",
        "created_at":            row[11],
    }


def _row_to_prediction(row) -> dict:
    return {
        "id":          row[0],
        "user_id":     row[1],
        "course_id":   row[2],
        "course_name": row[3],
        "risk_level":  row[4],
        "created_at":  row[5],
    }


def _row_to_schedule(row) -> dict:
    return {
        "id":               row[0],
        "user_id":          row[1],
        "course_id":        row[2],
        "course_name":      row[3],
        "study_date":       row[4],
        "duration_minutes": row[5],
        "topic":            row[6],
        "priority":         row[7] or "Medium",
        "completed":        bool(row[8]),
        "notes":            row[9],
        "created_at":       row[10],
    }


# ── User management ───────────────────────────────────────────────────────────

def create_user(
    email: str,
    password: str,
    full_name: str = None,
    security_question: str = None,
    security_answer: str = None,
    university: str = None,
    department: str = None,
    semester: str = None,
    target_gpa: float = None,
) -> int:
    """Register a new user and return the new user's id.

    Raises ValueError if the email is already registered.
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
                            (email, password_hash, full_name, security_question,
                             security_answer_hash, university, department, semester, target_gpa)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        (email, password_hash, full_name, security_question,
                         answer_hash, university, department, semester, target_gpa),
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


# ── User profile ──────────────────────────────────────────────────────────────

def get_user_profile(user_id: int) -> dict | None:
    """Return the full profile dict for a user, or None if not found."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, email, full_name, university, department, semester,
                       target_gpa, created_at
                FROM users WHERE id = %s
                """,
                (user_id,),
            )
            row = cur.fetchone()
            return _row_to_profile(row) if row else None
    finally:
        conn.close()


def update_user_profile(
    user_id: int,
    full_name: str = None,
    university: str = None,
    department: str = None,
    semester: str = None,
    target_gpa: float = None,
) -> bool:
    """Update profile fields for a user. Only non-None values are written.

    Returns True if any row was updated.
    """
    updates = []
    values = []
    if full_name is not None:
        updates.append("full_name = %s")
        values.append(full_name.strip() or None)
    if university is not None:
        updates.append("university = %s")
        values.append(university.strip() or None)
    if department is not None:
        updates.append("department = %s")
        values.append(department)
    if semester is not None:
        updates.append("semester = %s")
        values.append(semester)
    if target_gpa is not None:
        updates.append("target_gpa = %s")
        values.append(target_gpa)

    if not updates:
        return False

    values.append(user_id)
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"UPDATE users SET {', '.join(updates)} WHERE id = %s",
                    values,
                )
                return cur.rowcount > 0
    finally:
        conn.close()


# ── Security-question password reset ─────────────────────────────────────────

def get_security_question(email: str) -> str | None:
    user = get_user_by_email(email)
    if user is None:
        return None
    return user[4] or None


def verify_security_answer(email: str, plain_answer: str) -> bool:
    user = get_user_by_email(email)
    if user is None or not user[5]:
        return False
    normalised = (plain_answer or "").strip().lower()
    return bcrypt.checkpw(normalised.encode("utf-8"), user[5].encode("utf-8"))


def reset_password_direct(email: str, new_password: str) -> bool:
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


# ── Course CRUD ───────────────────────────────────────────────────────────────

def create_course(
    user_id: int,
    name: str,
    difficulty: str = "Medium",
    workload: str = "Medium",
    study_hours: int = 0,
    attendance: int = 75,
    deadline_days: int = 7,
    pass_grade: int = 70,
    instructor: str = "",
    notes: str = "",
) -> int:
    """Add a course for a user and return the new course id.

    Raises ValueError if the user already has a course with the same name.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        """
                        INSERT INTO courses
                            (user_id, name, difficulty, workload_level,
                             study_hours, attendance, deadline_days,
                             pass_grade, instructor, notes)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        (user_id, name.strip(), difficulty, workload,
                         study_hours, attendance, deadline_days,
                         pass_grade, instructor.strip(), notes.strip()),
                    )
                    return cur.fetchone()[0]
                except psycopg2.errors.UniqueViolation:
                    raise ValueError(
                        f"You already have a course named '{name}'. Choose a different name."
                    )
    finally:
        conn.close()


def get_user_courses(user_id: int) -> list[dict]:
    """Return all courses for a user as a list of dicts, newest first."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, user_id, name, difficulty, workload_level,
                       study_hours, attendance, deadline_days, pass_grade,
                       instructor, notes, created_at
                FROM courses
                WHERE user_id = %s
                ORDER BY created_at DESC
                """,
                (user_id,),
            )
            return [_row_to_course(row) for row in cur.fetchall()]
    finally:
        conn.close()


def update_course(
    course_id: int,
    user_id: int,
    name: str,
    difficulty: str = "Medium",
    workload: str = "Medium",
    study_hours: int = 0,
    attendance: int = 75,
    deadline_days: int = 7,
    pass_grade: int = 70,
    instructor: str = "",
    notes: str = "",
) -> bool:
    """Update a course. Only the owning user can modify it.

    Raises ValueError on duplicate name conflict.
    Returns True if the row was updated.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        """
                        UPDATE courses
                        SET name = %s, difficulty = %s, workload_level = %s,
                            study_hours = %s, attendance = %s, deadline_days = %s,
                            pass_grade = %s, instructor = %s, notes = %s
                        WHERE id = %s AND user_id = %s
                        """,
                        (name.strip(), difficulty, workload,
                         study_hours, attendance, deadline_days,
                         pass_grade, instructor.strip(), notes.strip(),
                         course_id, user_id),
                    )
                    return cur.rowcount > 0
                except psycopg2.errors.UniqueViolation:
                    raise ValueError(
                        f"You already have another course named '{name}'."
                    )
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
    """Create a persistent login session and return the opaque token."""
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
    """Return the raw user row for a non-expired session token, or None."""
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

def save_prediction(
    user_id: int,
    risk_level: str,
    course_id: int = None,
    course_name: str = None,
) -> int:
    """Persist a prediction result and return the new prediction id."""
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO predictions (user_id, course_id, risk_level, course_name)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (user_id, course_id, risk_level, course_name),
                )
                return cur.fetchone()[0]
    finally:
        conn.close()


def get_user_predictions(user_id: int, limit: int = 20) -> list[dict]:
    """Return the most recent predictions for a user as a list of dicts."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT p.id, p.user_id, p.course_id,
                       COALESCE(p.course_name, c.name) AS course_name,
                       p.risk_level, p.created_at
                FROM predictions p
                LEFT JOIN courses c ON c.id = p.course_id
                WHERE p.user_id = %s
                ORDER BY p.created_at DESC
                LIMIT %s
                """,
                (user_id, limit),
            )
            return [_row_to_prediction(row) for row in cur.fetchall()]
    finally:
        conn.close()


# ── Study schedule ────────────────────────────────────────────────────────────

def save_study_schedule(user_id: int, entries: list[dict]) -> int:
    """Append a list of schedule entries for a user.

    Each entry dict may contain:
        course_id (int, optional), course_name (str, optional),
        study_date (date or ISO str), duration_minutes (int),
        topic (str), priority (str: Low/Medium/High),
        completed (bool), notes (str)

    Returns the number of rows inserted.
    Note: prefer upsert_study_schedule() to avoid duplicate entries.
    """
    if not entries:
        return 0
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                rows = [
                    (
                        user_id,
                        e.get("course_id"),
                        e.get("course_name"),
                        e["study_date"],
                        int(e.get("duration_minutes", 60)),
                        e.get("topic"),
                        e.get("priority", "Medium"),
                        bool(e.get("completed", False)),
                        e.get("notes"),
                    )
                    for e in entries
                ]
                cur.executemany(
                    """
                    INSERT INTO study_schedules
                        (user_id, course_id, course_name, study_date,
                         duration_minutes, topic, priority, completed, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    rows,
                )
                return cur.rowcount
    finally:
        conn.close()


def upsert_study_schedule(user_id: int, entries: list[dict]) -> int:
    """Replace ALL schedule entries for a user with the given list.

    This is an atomic delete-then-insert inside a single transaction,
    ensuring no duplicate rows accumulate when the user saves the schedule
    multiple times.

    Each entry dict accepts the same keys as save_study_schedule().
    Returns the number of rows inserted.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                # Delete existing schedule for this user atomically
                cur.execute(
                    "DELETE FROM study_schedules WHERE user_id = %s",
                    (user_id,),
                )
                if not entries:
                    return 0
                rows = [
                    (
                        user_id,
                        e.get("course_id"),
                        e.get("course_name"),
                        e["study_date"],
                        int(e.get("duration_minutes", 60)),
                        e.get("topic"),
                        e.get("priority", "Medium"),
                        bool(e.get("completed", False)),
                        e.get("notes"),
                    )
                    for e in entries
                ]
                cur.executemany(
                    """
                    INSERT INTO study_schedules
                        (user_id, course_id, course_name, study_date,
                         duration_minutes, topic, priority, completed, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    rows,
                )
                return cur.rowcount
    finally:
        conn.close()


def get_user_schedule(
    user_id: int,
    from_date=None,
    to_date=None,
) -> list[dict]:
    """Return study schedule entries for a user.

    Optionally filter by date range (from_date / to_date as date or ISO str).
    Results are ordered by study_date ascending.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            where = "WHERE user_id = %s"
            params: list = [user_id]
            if from_date is not None:
                where += " AND study_date >= %s"
                params.append(from_date)
            if to_date is not None:
                where += " AND study_date <= %s"
                params.append(to_date)
            cur.execute(
                f"""
                SELECT id, user_id, course_id, course_name, study_date,
                       duration_minutes, topic, priority, completed, notes, created_at
                FROM study_schedules
                {where}
                ORDER BY study_date ASC, id ASC
                """,
                params,
            )
            return [_row_to_schedule(row) for row in cur.fetchall()]
    finally:
        conn.close()


def mark_schedule_complete(entry_id: int, user_id: int, completed: bool = True) -> bool:
    """Toggle the completed flag on a schedule entry. Returns True if updated."""
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE study_schedules SET completed = %s WHERE id = %s AND user_id = %s",
                    (completed, entry_id, user_id),
                )
                return cur.rowcount > 0
    finally:
        conn.close()


def clear_user_schedule(user_id: int) -> int:
    """Delete all schedule entries for a user. Returns number of rows deleted."""
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM study_schedules WHERE user_id = %s",
                    (user_id,),
                )
                return cur.rowcount
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
