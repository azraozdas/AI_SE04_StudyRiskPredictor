"""AI Smart Study: Risk & Performance Predictor — main entry point."""

import base64
import os
import sys

# Ensure imports from this directory resolve (pages_, utils, styles, login)
_HERE = os.path.dirname(os.path.abspath(__file__))
_LOGO_PATH = os.path.join(_HERE, "assets", "logo.png")
_SIDEBAR_LOGO_SVG = """
<svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
<path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
<path d="M6 12v5c3 3 9 3 12 0v-5"/>
</svg>
"""
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import streamlit as st
from streamlit import config as st_config

# Slider active track uses theme primaryColor (inline gradient — not overridable via background-color CSS)
st_config.set_option("theme.primaryColor", "#3B82F6")

from bootstrap import ensure_database, handle_logout_query, handle_nav_query, init_session_state
from utils import render_html, restore_auth_session, save_auth_session

st.set_page_config(
    page_title="Studor",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------

init_session_state()

# Restore login after GET nav reload (full page load can reset Streamlit session)
restore_auth_session()
ensure_database()

# ---------------------------------------------------------------------------
# Handle GET-form navigation (before login gate — nav param preserved on reload)
# ---------------------------------------------------------------------------

_VALID_PAGES = {
    "dashboard", "my_courses", "courses", "risk", "schedule",
    "recommendations", "model", "profile",
}

handle_logout_query()
handle_nav_query(_VALID_PAGES)

# ---------------------------------------------------------------------------
# Login gate
# ---------------------------------------------------------------------------

if not st.session_state.logged_in:
    from login import render_login_page
    render_login_page()
    st.stop()

# Persist auth so sidebar navigation / reloads keep the session
save_auth_session()

# ---------------------------------------------------------------------------
# Inject design-system styles
# ---------------------------------------------------------------------------

from styles import inject_app_styles
inject_app_styles()

# ---------------------------------------------------------------------------
# SVG icon definitions (Lucide-style, currentColor)
# ---------------------------------------------------------------------------

_ICON = {
    "dashboard": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>""",
    "my_courses": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/></svg>""",
    "courses":   """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>""",
    "schedule":  """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>""",
    "risk":      """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>""",
    "recommendations": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12v2h8v-2a7 7 0 0 0-4-12z"/></svg>""",
    "model":     """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>""",
    "logout":    """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>""",
}

NAV_ITEMS = [
    ("dashboard",       "Dashboard"),
    ("my_courses",      "My Courses"),
    ("courses",         "Dataset Course Stats"),
    ("schedule",        "Study Schedule"),
    ("risk",            "Risk Prediction"),
    ("recommendations", "Recommendations"),
    ("model",           "Model Results"),
]

# ---------------------------------------------------------------------------
# Sidebar builder (HTML nav + icons — left-aligned, anchor links)
# ---------------------------------------------------------------------------

def _nav_item_html(key: str, label: str, active: bool) -> str:
    icon_svg = _ICON.get(key, "")
    icon_html = f'<span class="sb-nav-icon">{icon_svg}</span>'
    label_html = f'<span class="sb-nav-label">{label}</span>'
    if active:
        return (
            f'<div class="sb-nav-item sb-nav-item--active">'
            f'{icon_html}{label_html}</div>'
        )
    return (
        f'<a href="?nav={key}" target="_self" class="sb-nav-item sb-nav-item--inactive">'
        f'{icon_html}{label_html}</a>'
    )


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


def _render_sidebar(current: str) -> None:
    full_name = st.session_state.get("full_name", "") or "Student"
    dept      = st.session_state.get("profile_department", "Computer Science")
    sem       = st.session_state.get("profile_semester", "Semester 6")
    initial   = full_name[0].upper() if full_name else "S"
    name_disp = full_name[:20] + ("…" if len(full_name) > 20 else "")
    meta_disp = f"{dept} · {sem}"

    logo_inner, logo_cls = _sidebar_logo_html()
    brand_html = f"""
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
</div>
"""

    nav_html = "".join(
        _nav_item_html(key, label, key == current)
        for key, label in NAV_ITEMS
    )
    logout_html = (
        f'<a href="?logout=1" target="_self" class="sb-nav-item sb-nav-item--inactive sb-logout">'
        f'<span class="sb-nav-icon">{_ICON["logout"]}</span>'
        f'<span class="sb-nav-label">Logout</span></a>'
    )

    with st.sidebar:
        render_html(brand_html)
        render_html(f'<div class="sb-nav-list">{nav_html}</div>')
        render_html('<hr class="sb-divider">')

        profile_inner = f"""
<div class="sb-avatar">{initial}</div>
<div style="min-width:0;flex:1;">
<div class="sb-profile-name">{name_disp}</div>
<div class="sb-profile-meta">{meta_disp}</div>
</div>
"""
        if current == "profile":
            render_html(
                f'<div class="sb-profile sb-profile--active">{profile_inner}</div>'
            )
        else:
            render_html(
                f'<a href="?nav=profile" target="_self" class="sb-profile" '
                f'title="View profile">{profile_inner}</a>'
            )

        render_html(logout_html)


# ---------------------------------------------------------------------------
# Page routing
# ---------------------------------------------------------------------------

_render_sidebar(st.session_state.current_page)

current = st.session_state.current_page

if current == "dashboard":
    from pages_ import dashboard
    dashboard.render()

elif current == "my_courses":
    from pages_ import my_courses
    my_courses.render()

elif current == "courses":
    from pages_ import courses
    courses.render()

elif current == "risk":
    from pages_ import risk_prediction
    risk_prediction.render()

elif current == "schedule":
    from pages_ import study_schedule
    study_schedule.render()

elif current == "recommendations":
    from pages_ import recommendations
    recommendations.render()

elif current == "model":
    from pages_ import model_results
    model_results.render()

elif current == "profile":
    from pages_ import profile
    profile.render()

else:
    from pages_ import dashboard
    dashboard.render()
