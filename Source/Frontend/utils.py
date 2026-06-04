import json
import os
import re

import streamlit as st

# Absolute path to the project root (two levels above Source/Frontend/)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUTH_SESSION_PATH = os.path.join(ROOT, "Data", ".auth_session.json")

_AUTH_KEYS = (
    "logged_in",
    "user_email",
    "full_name",
    "student_id",
    "profile_department",
    "profile_semester",
)


def save_auth_session() -> None:
    """Persist login to disk so GET sidebar navigation survives full page reloads."""
    data = {k: st.session_state.get(k) for k in _AUTH_KEYS}
    data["logged_in"] = True
    os.makedirs(os.path.dirname(AUTH_SESSION_PATH), exist_ok=True)
    with open(AUTH_SESSION_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def restore_auth_session() -> bool:
    """Restore login from disk into session_state. Returns True if restored."""
    if st.session_state.get("logged_in"):
        return True
    if not os.path.exists(AUTH_SESSION_PATH):
        return False
    try:
        with open(AUTH_SESSION_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return False
    if not data.get("logged_in"):
        return False
    for k in _AUTH_KEYS:
        if k in data:
            st.session_state[k] = data[k]
    return True


def clear_auth_session() -> None:
    """Remove persisted login (sign out)."""
    if os.path.exists(AUTH_SESSION_PATH):
        try:
            os.remove(AUTH_SESSION_PATH)
        except OSError:
            pass


def render_html(html: str) -> None:
    """Render an HTML fragment inside Streamlit.

    Streamlit uses CommonMark, which terminates an HTML block on a blank line.
    This helper strips blank lines before forwarding to st.markdown so that
    multi-line HTML strings with formatting whitespace render correctly.
    """
    clean = re.sub(r"\n[ \t]*\n", "\n", html)
    st.markdown(clean, unsafe_allow_html=True)
