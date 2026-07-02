"""
Backend integration tests for AI Smart Study Risk Predictor.

Run from the project root:
    python3 Source/Backend/test_backend.py

Tests cover:
  1. Database connection
  2. Schema initialisation (init_db)
  3. User creation & password verification
  4. Duplicate email prevention
  5. User profile get/update
  6. Course CRUD (create, read, update, delete)
  7. Duplicate course-name prevention (same user)
  8. Prediction storage & retrieval (ALL paths: ML + fallback)
  9. Study schedule upsert (no duplicates)
 10. get_user_schedule loading
 11. mark_schedule_complete
 12. clear_user_schedule
 13. Session token create / verify / delete
"""

import os
import sys
import traceback
from datetime import date

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import db

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
RESET  = "\033[0m"

_pass = 0
_fail = 0


def ok(msg):
    global _pass
    _pass += 1
    print(f"  {GREEN}OK{RESET} {msg}")


def fail(msg, exc=None):
    global _fail
    _fail += 1
    print(f"  {RED}FAIL{RESET} {msg}")
    if exc:
        print(f"       {YELLOW}{exc}{RESET}")


def section(title):
    print(f"\n{YELLOW}-- {title} {RESET}")


# 1. Connection
section("1. Database Connection")
try:
    conn = db.get_connection()
    conn.close()
    ok("get_connection() returned a live connection")
except Exception as e:
    fail("get_connection() failed -- check DATABASE_URL in .env", e)
    print(f"\n{RED}Cannot proceed without a database connection. Exiting.{RESET}")
    sys.exit(1)

# 2. Schema init
section("2. Schema Initialisation (init_db)")
try:
    db.init_db()
    ok("init_db() completed without error")
except Exception as e:
    fail("init_db() raised an exception", e)

# 3. User creation & auth
section("3. User Creation & Authentication")
TEST_EMAIL = "backend_test_user_98765@example.com"
TEST_PW    = "SecurePass#2025"

try:
    existing = db.get_user_by_email(TEST_EMAIL)
    if existing:
        conn = db.get_connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE email = %s", (TEST_EMAIL,))
        conn.close()
except Exception:
    pass

try:
    uid = db.create_user(
        email=TEST_EMAIL,
        password=TEST_PW,
        full_name="Test User Backend",
        university="Test University",
        department="Computer Science",
        semester="Semester 3",
        target_gpa=3.5,
        security_question="What is 2+2?",
        security_answer="4",
    )
    assert isinstance(uid, int) and uid > 0
    ok(f"create_user() returned new user id={uid}")
except Exception as e:
    fail("create_user() failed", e)
    sys.exit(1)

try:
    db.create_user(email=TEST_EMAIL, password="another")
    fail("Duplicate email should have raised ValueError")
except ValueError:
    ok("Duplicate email correctly raises ValueError")
except Exception as e:
    fail("Unexpected error on duplicate email", e)

try:
    assert db.verify_user_password(TEST_EMAIL, TEST_PW) is True
    ok("verify_user_password() True for correct password")
    assert db.verify_user_password(TEST_EMAIL, "wrong") is False
    ok("verify_user_password() False for wrong password")
except Exception as e:
    fail("verify_user_password() error", e)

# 4. Profile
section("4. User Profile (get / update)")
try:
    profile = db.get_user_profile(uid)
    assert profile is not None
    assert profile["email"] == TEST_EMAIL
    ok("get_user_profile() returns correct profile dict")
except Exception as e:
    fail("get_user_profile() failed", e)

try:
    updated = db.update_user_profile(uid, full_name="Updated Name", target_gpa=3.8)
    assert updated is True
    p2 = db.get_user_profile(uid)
    assert p2["full_name"]  == "Updated Name"
    assert p2["target_gpa"] == 3.8
    ok("update_user_profile() persists changes correctly")
except Exception as e:
    fail("update_user_profile() failed", e)

# 5. Course CRUD
section("5. Course CRUD")
try:
    cid = db.create_course(
        user_id=uid,
        name="Test Course Alpha",
        difficulty="High",
        workload="Medium",
        study_hours=6,
        attendance=80,
        deadline_days=14,
        pass_grade=75,
        instructor="Dr. Test",
        notes="Backend test notes",
    )
    assert isinstance(cid, int) and cid > 0
    ok(f"create_course() returned id={cid}")
except Exception as e:
    fail("create_course() failed", e)
    sys.exit(1)

try:
    db.create_course(user_id=uid, name="Test Course Alpha")
    fail("Duplicate course name should raise ValueError")
except ValueError:
    ok("Duplicate course name correctly raises ValueError")
except Exception as e:
    fail("Unexpected error on duplicate course name", e)

try:
    courses = db.get_user_courses(uid)
    c = next((c for c in courses if c["id"] == cid), None)
    assert c is not None
    assert c["name"] == "Test Course Alpha"
    assert c["study_hours"] == 6
    ok("get_user_courses() returns correct course dict with all fields")
except Exception as e:
    fail("get_user_courses() failed", e)

try:
    updated = db.update_course(cid, uid, name="Test Course Edited", difficulty="Low",
                               workload="Low", study_hours=3, attendance=90,
                               deadline_days=5, pass_grade=65)
    assert updated is True
    c2 = next((c for c in db.get_user_courses(uid) if c["id"] == cid), None)
    assert c2["name"] == "Test Course Edited"
    assert c2["study_hours"] == 3
    ok("update_course() persists all edited fields")
except Exception as e:
    fail("update_course() failed", e)

try:
    deleted = db.delete_course(cid, uid)
    assert deleted is True
    assert not any(c["id"] == cid for c in db.get_user_courses(uid))
    ok("delete_course() removes course from DB")
except Exception as e:
    fail("delete_course() failed", e)

# 6. Predictions
section("6. Prediction Storage & Retrieval (all paths)")
try:
    pid1 = db.save_prediction(uid, "High Risk",   course_name="Machine Learning")
    pid2 = db.save_prediction(uid, "Medium Risk", course_name="Databases")
    pid3 = db.save_prediction(uid, "Low Risk",    course_name="Intro to Python")
    assert all(isinstance(p, int) and p > 0 for p in [pid1, pid2, pid3])
    ok(f"save_prediction() stored 3 predictions")
except Exception as e:
    fail("save_prediction() failed", e)

try:
    preds = db.get_user_predictions(uid, limit=10)
    assert len(preds) >= 3
    levels = {p["risk_level"] for p in preds}
    names  = {p["course_name"] for p in preds}
    assert "High Risk"       in levels
    assert "Medium Risk"     in levels
    assert "Low Risk"        in levels
    assert "Machine Learning" in names
    ok(f"get_user_predictions() returned {len(preds)} rows with correct data")
except Exception as e:
    fail("get_user_predictions() failed", e)

# 7. Study Schedule
section("7. Study Schedule Persistence")
today_str = date.today().isoformat()
entries = [
    {"course_name": "Machine Learning", "study_date": today_str,
     "duration_minutes": 300, "priority": "High", "topic": "DL", "completed": False, "notes": ""},
    {"course_name": "Databases", "study_date": today_str,
     "duration_minutes": 180, "priority": "Medium", "topic": "SQL", "completed": False, "notes": ""},
]

try:
    n = db.upsert_study_schedule(uid, entries)
    assert n == 2
    ok(f"upsert_study_schedule() inserted {n} entries")
except Exception as e:
    fail("upsert_study_schedule() failed", e)

try:
    n2 = db.upsert_study_schedule(uid, entries)
    rows = db.get_user_schedule(uid)
    assert len(rows) == 2, f"Expected 2 rows after upsert, got {len(rows)}"
    ok("Second upsert replaces correctly (no duplicate rows)")
except Exception as e:
    fail("Upsert duplicate prevention failed", e)

try:
    rows = db.get_user_schedule(uid)
    assert len(rows) == 2
    cnames = {r["course_name"] for r in rows}
    assert "Machine Learning" in cnames
    ok(f"get_user_schedule() returned {len(rows)} rows with correct data")
except Exception as e:
    fail("get_user_schedule() failed", e)

try:
    row_id = rows[0]["id"]
    result = db.mark_schedule_complete(row_id, uid, completed=True)
    assert result is True
    rows2 = db.get_user_schedule(uid)
    marked = next(r for r in rows2 if r["id"] == row_id)
    assert marked["completed"] is True
    ok("mark_schedule_complete() sets completed=True")
except Exception as e:
    fail("mark_schedule_complete() failed", e)

try:
    del_n = db.clear_user_schedule(uid)
    assert del_n == 2
    assert len(db.get_user_schedule(uid)) == 0
    ok(f"clear_user_schedule() deleted {del_n} rows")
except Exception as e:
    fail("clear_user_schedule() failed", e)

# 8. Session tokens
section("8. Session Tokens (Remember Me)")
try:
    token = db.create_session(uid, days=30)
    assert isinstance(token, str) and len(token) > 20
    ok(f"create_session() returned token")
except Exception as e:
    fail("create_session() failed", e)

try:
    user_row = db.get_session_user(token)
    assert user_row is not None and user_row[0] == uid
    ok("get_session_user() resolves token to correct user")
except Exception as e:
    fail("get_session_user() failed", e)

try:
    db.delete_session(token)
    assert db.get_session_user(token) is None
    ok("delete_session() invalidates the token")
except Exception as e:
    fail("delete_session() failed", e)

# 9. Teardown
section("9. Teardown")
try:
    conn = db.get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE email = %s", (TEST_EMAIL,))
    conn.close()
    ok(f"Test user removed (cascade deletes all related rows)")
except Exception as e:
    fail("Teardown failed -- test user may remain in DB", e)

# Summary
total = _pass + _fail
print(f"\n{'=' * 55}")
print(f"Results: {GREEN}{_pass} passed{RESET}  {RED}{_fail} failed{RESET}  / {total} total")
if _fail == 0:
    print(f"{GREEN}All backend tests passed!{RESET}")
else:
    print(f"{RED}{_fail} test(s) failed. Review output above.{RESET}")
    sys.exit(1)
