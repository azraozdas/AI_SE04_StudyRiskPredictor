"""Studor: Risk & Performance Predictor — main entry point."""

import base64
import importlib
import os
import sys

# Ensure imports from this directory resolve (pages_, utils, styles, login)
_HERE = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.join(os.path.dirname(_HERE), "Backend")
_LOGO_PATH = os.path.join(_HERE, "assets", "logo.png")
_SIDEBAR_LOGO_SVG = """
<svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
<path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
<path d="M6 12v5c3 3 9 3 12 0v-5"/>
</svg>
"""
for _p in (_HERE, _BACKEND):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import streamlit as st
from streamlit import config as st_config

# Slider active track uses theme primaryColor (inline gradient — not overridable via background-color CSS)
try:
    st_config.set_option("theme.primaryColor", "#3B82F6")
except Exception:
    pass

from utils import render_html, restore_auth_session, save_auth_session
from db import init_db, get_session_user  # noqa: E402
from cookie_session import (  # noqa: E402
    get_session_token,
    set_session_token,
    clear_session_token,
)

st.set_page_config(
    page_title="Studor",
    page_icon="📘",
    layout="wide",
)


# ---------------------------------------------------------------------------
# Database initialisation (once per server process)
# ---------------------------------------------------------------------------

@st.cache_resource
def _init_db_once():
    """Run init_db exactly once per Streamlit server process, not on every rerun."""
    try:
        init_db()
    except Exception:
        pass  # Login page will surface DB errors when the user tries to sign in


_init_db_once()

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------

_DEFAULTS = {
    "logged_in":          False,
    "current_page":       "dashboard",
    "prediction_result":  None,
    "selected_course":    None,
    "user_id":            None,
    "student_id":         None,
    "user_email":         "",
    "full_name":          "",
    "profile_department": "Computer Science",
    "profile_semester":   "Semester 6",
    "_session_token":     None,
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# Restore login after GET nav reload (full page load can reset Streamlit session)
restore_auth_session()

# ---------------------------------------------------------------------------
# Remember Me: write pending cookie (set by login.py after successful login)
# ---------------------------------------------------------------------------

_pending = st.session_state.pop("_pending_session_cookie", None)
if _pending:
    set_session_token(_pending)
    st.session_state._session_token = _pending

# ---------------------------------------------------------------------------
# Remember Me: auto-login from existing browser cookie
# ---------------------------------------------------------------------------

if not st.session_state.logged_in:
    _cookie_token = get_session_token()
    if _cookie_token:
        try:
            _user = get_session_user(_cookie_token)
            if _user:
                st.session_state.logged_in = True
                st.session_state.user_id = _user[0]
                st.session_state.user_email = _user[1]
                st.session_state.full_name = _user[3] or ""
                st.session_state.student_id = _user[1]
                st.session_state._session_token = _cookie_token
                st.rerun()
            else:
                # Token expired or revoked — clear the stale cookie
                clear_session_token()
        except Exception:
            clear_session_token()

# ---------------------------------------------------------------------------
# Handle GET-form navigation (nav param preserved on full page reload)
# ---------------------------------------------------------------------------

_nav = st.query_params.get("nav")
if isinstance(_nav, list):
    _nav = _nav[0] if _nav else None
if _nav:
    _valid = {
        "dashboard", "courses", "risk", "schedule",
        "recommendations", "model", "profile",
    }
    if _nav in _valid:
        st.session_state.current_page = _nav
    st.query_params.clear()
    st.rerun()

# ---------------------------------------------------------------------------
# Login gate
# ---------------------------------------------------------------------------

if not st.session_state.logged_in:
    from login import render_login_page
    render_login_page()
    st.stop()

# Persist auth to disk so GET-form navigation reloads keep the user signed in
save_auth_session()

# ---------------------------------------------------------------------------
# Inject design-system styles
# ---------------------------------------------------------------------------

try:
    from styles import inject_app_styles
    inject_app_styles()
except ImportError:
    # inject_app_styles not implemented yet — app still runs, just unstyled.
    pass

# ---------------------------------------------------------------------------
# SVG icon definitions (Lucide-style, currentColor)
# ---------------------------------------------------------------------------

_ICON = {
    "dashboard": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>""",
    "courses":   """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>""",
    "risk":      """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m10.29 3.86-8.47 14.67A2 2 0 0 0 3.54 21h16.92a2 2 0 0 0 1.72-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>""",
    "schedule":  """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>""",
    "recommendations": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>""",
    "model":     """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>""",
}

NAV_ITEMS = [
    ("dashboard",       "Dashboard"),
    ("courses",         "My Courses"),
    ("risk",            "Risk Prediction"),
    ("schedule",        "Study Schedule"),
    ("recommendations", "Recommendations"),
    ("model",           "Model Results"),
]

# Maps a nav key to the module under pages_/ that implements render()
_PAGE_MODULES = {
    "dashboard":       "dashboard",
    "courses":         "courses",
    "risk":            "risk_prediction",
    "schedule":        "study_schedule",
    "recommendations": "recommendations",
    "model":           "model_results",
    "profile":         "profile",
}


# ---------------------------------------------------------------------------
# Sidebar builder (HTML nav — original design)
# ---------------------------------------------------------------------------

def _sidebar_logo_html() -> tuple[str, str]:
    """Return (logo inner HTML, sb-logo CSS class) for sidebar branding."""
    try:
        if os.path.exists(_LOGO_PATH):
            with open(_LOGO_PATH, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")
            img = (
                f'<img src="data:image/png;base64,{b64}" '
                f'alt="Studor logo" class="sb-logo-img" />'
            )
            return img, "sb-logo sb-logo--custom"
    except OSError:
        pass
    return _SIDEBAR_LOGO_SVG, "sb-logo"


def _nav_item_html(key: str, label: str, active: bool) -> str:
    icon_svg = _ICON.get(key, "")
    icon_html = f'<span class="sb-nav-icon">{icon_svg}</span>'
    label_html = f'<span class="sb-nav-label">{label}</span>'

    if active:
        return (
            f'<div class="sb-nav-item sb-nav-item--active">'
            f'{icon_html}{label_html}'
            f'</div>'
        )
    return (
        f'<form method="GET" action="" class="sb-form">'
        f'<button type="submit" name="nav" value="{key}" '
        f'class="sb-nav-item sb-nav-item--inactive">'
        f'{icon_html}{label_html}'
        f'</button>'
        f'</form>'
    )


def _render_sidebar(current: str) -> None:
    full_name = st.session_state.get("full_name", "") or "Student"
    dept      = st.session_state.get("profile_department", "Computer Science")
    sem       = st.session_state.get("profile_semester", "Semester 6")
    initial   = full_name[0].upper() if full_name else "S"
    name_disp = full_name[:20] + ("…" if len(full_name) > 20 else "")
    meta_disp = f"{dept} · {sem}"

    nav_html = "".join(
        _nav_item_html(key, label, key == current)
        for key, label in NAV_ITEMS
    )

    profile_active = current == "profile"
    profile_cls = "sb-profile sb-profile--active" if profile_active else "sb-profile"

    if profile_active:
        profile_inner = (
            f'<div class="{profile_cls}">'
            f'<div class="sb-avatar">{initial}</div>'
            f'<div style="min-width:0;flex:1;">'
            f'<div class="sb-profile-name">{name_disp}</div>'
            f'<div class="sb-profile-meta">{meta_disp}</div>'
            f'</div>'
            f'</div>'
        )
    else:
        profile_inner = (
            f'<form method="GET" action="" class="sb-form">'
            f'<button type="submit" name="nav" value="profile" '
            f'style="-webkit-appearance:none;appearance:none;border:none;background:transparent;'
            f'font:inherit;text-align:left;cursor:pointer;width:100%;outline:none;padding:0;">'
            f'<div class="{profile_cls}">'
            f'<div class="sb-avatar">{initial}</div>'
            f'<div style="min-width:0;flex:1;">'
            f'<div class="sb-profile-name">{name_disp}</div>'
            f'<div class="sb-profile-meta">{meta_disp}</div>'
            f'</div>'
            f'</div>'
            f'</button>'
            f'</form>'
        )

    logo_inner, logo_cls = _sidebar_logo_html()

    sidebar_html = f"""
<div class="sb-wrap">
<div class="sb-brand">
<div class="{logo_cls}">
{logo_inner}
</div>
<div>
<div class="sb-brand-name">Studor</div>
<div class="sb-brand-sub">Risk &amp; Performance Predictor</div>
</div>
</div>
<div class="sb-section-label">Navigation</div>
<div class="sb-nav-list">{nav_html}</div>
<hr class="sb-divider">
{profile_inner}
</div>
"""

    with st.sidebar:
        render_html(sidebar_html)


# ---------------------------------------------------------------------------
# Page routing
# ---------------------------------------------------------------------------

def _dispatch(page: str) -> None:
    """Import the page module under pages_/ and call its render(); show a
    friendly placeholder if the page hasn't been implemented yet."""
    module_name = _PAGE_MODULES.get(page, "dashboard")
    try:
        module = importlib.import_module(f"pages_.{module_name}")
    except Exception as exc:  # noqa: BLE001
        st.error(f"Could not load the '{page}' page: {exc}")
        return

    render_fn = getattr(module, "render", None)
    if callable(render_fn):
        render_fn()
    else:
        render_html(
            '<div class="page-h1">Coming soon</div>'
            '<div class="page-sub">This page has not been built yet.</div>'
        )


_render_sidebar(st.session_state.current_page)
_dispatch(st.session_state.current_page)
