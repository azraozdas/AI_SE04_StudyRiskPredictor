"""
App startup helpers: session defaults, database init, URL query navigation.
"""

import os
import sys

import streamlit as st

_FRONTEND = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_FRONTEND))
_BACKEND = os.path.join(_ROOT, "Source", "Backend")

if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)

_DB_INIT_ATTEMPTED = False

_SESSION_DEFAULTS = {
    "logged_in": False,
    "current_page": "dashboard",
    "user_id": None,
    "user_email": "",
    "full_name": "",
    "student_id": "",
    "profile_department": "Computer Science",
    "profile_semester": "Semester 6",
    "profile_university": "",
    "profile_target_gpa": None,
    "user_courses": [],
    "prefill_course": {},
    "auth_mode": "Sign In",
    "login_error": None,
    "signup_error": None,
}


def _query_get(name: str) -> str | None:
    """Read a single query-string value (Streamlit 1.30+ or legacy API)."""
    try:
        val = st.query_params.get(name)
        if val is None:
            return None
        if isinstance(val, list):
            return val[0] if val else None
        return str(val)
    except Exception:
        pass
    try:
        params = st.experimental_get_query_params()
        vals = params.get(name)
        if vals:
            return vals[0]
    except Exception:
        pass
    return None


def _drop_query_keys(*keys: str) -> None:
    try:
        remaining = {k: v for k, v in st.query_params.items() if k not in keys}
        st.query_params.clear()
        for k, v in remaining.items():
            st.query_params[k] = v
    except Exception:
        pass


def _restore_remember_me_cookie() -> None:
    """Log in from a valid Remember Me token stored in the browser cookie."""
    if st.session_state.get("logged_in"):
        return
    if st.session_state.get("_remember_me_attempted"):
        return
    st.session_state._remember_me_attempted = True
    try:
        from cookie_session import get_session_token
        from db import get_session_user

        token = get_session_token()
        if not token:
            return
        user = get_session_user(token)
        if not user:
            return
        st.session_state.logged_in = True
        st.session_state.user_id = user[0]
        st.session_state.user_email = user[1]
        st.session_state.full_name = (user[3] or "") if len(user) > 3 else ""
        st.session_state.student_id = user[1]
    except Exception:
        pass


def _flush_pending_session_cookie() -> None:
    token = st.session_state.pop("_pending_session_cookie", None)
    if not token:
        return
    try:
        from cookie_session import set_session_token

        set_session_token(token)
    except Exception:
        pass


def init_session_state() -> None:
    """Ensure required session_state keys exist with safe defaults."""
    for key, value in _SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value

    from utils import restore_auth_session

    restore_auth_session()
    _restore_remember_me_cookie()
    _flush_pending_session_cookie()


def ensure_database() -> None:
    """Create tables if missing. Runs at most once per server process."""
    global _DB_INIT_ATTEMPTED
    if _DB_INIT_ATTEMPTED:
        return
    _DB_INIT_ATTEMPTED = True
    try:
        from db import init_db

        init_db()
    except Exception as e:
        _msg = str(e).lower()
        if "enotfound" in _msg or "tenant" in _msg or "not found" in _msg or "nodename" in _msg:
            st.warning(
                "⚠️ Database is paused. Go to **supabase.com/dashboard** → your project → **Restore project**, "
                "then refresh this page.",
                icon="🔌",
            )
        else:
            st.warning(f"⚠️ Database connection failed: {e}", icon="🔌")


def handle_logout_query() -> None:
    """Process ?logout=1 from sidebar anchor links."""
    if _query_get("logout") != "1":
        return

    try:
        from cookie_session import clear_session_token, get_session_token
        from db import delete_session

        token = get_session_token()
        if token:
            delete_session(token)
        clear_session_token()
    except Exception:
        pass

    from utils import clear_auth_session

    clear_auth_session()

    for key in list(st.session_state.keys()):
        del st.session_state[key]

    init_session_state()
    _drop_query_keys("logout")
    st.rerun()


def handle_nav_query(valid_pages: set[str]) -> None:
    """Process ?nav=<page> from sidebar anchor links."""
    nav = _query_get("nav")
    if not nav or nav not in valid_pages:
        return

    st.session_state.current_page = nav
    _drop_query_keys("nav")
