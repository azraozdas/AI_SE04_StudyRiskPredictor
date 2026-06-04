"""
Thin wrapper around streamlit-cookies-controller for session-token cookies.

CookieController is a Streamlit custom component (widget) — it must NOT be
instantiated inside @st.cache_data or @st.cache_resource functions.
A fresh instance is created on each call; the browser holds the actual state.
"""

from streamlit_cookies_controller import CookieController

_COOKIE_KEY = "ai_study_session_token"
_MAX_AGE_DAYS = 30


def _ctrl() -> CookieController:
    return CookieController(key="ai_study_cookie_ctrl")


def get_session_token() -> str | None:
    """Read the persisted session token from the browser cookie, or None."""
    try:
        return _ctrl().get(_COOKIE_KEY) or None
    except Exception:
        return None


def set_session_token(token: str) -> None:
    """Write the session token to a 30-day browser cookie."""
    try:
        _ctrl().set(_COOKIE_KEY, token, max_age=_MAX_AGE_DAYS * 24 * 60 * 60)
    except Exception:
        pass


def clear_session_token() -> None:
    """Delete the session cookie (call on sign-out)."""
    try:
        _ctrl().remove(_COOKIE_KEY)
    except Exception:
        pass
