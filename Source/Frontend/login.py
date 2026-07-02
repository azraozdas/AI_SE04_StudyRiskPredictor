"""
Authentication page for the AI Smart Study Risk & Performance Predictor.

Public hook used by app.py:
    render_login_page()

Storage  : hosted PostgreSQL via Supabase (Source/Backend/db.py)
Sessions : 30-day browser cookie via cookie_session.py  (Remember Me)
Recovery : in-app security-question flow — no email required
Logo     : Source/Frontend/assets/logo.png — falls back to inline SVG
"""

import base64
import os
import re
import sys
from pathlib import Path
import streamlit as st

from utils import render_html
from styles import inject_login_styles

# ── Backend path setup ────────────────────────────────────────────────────────
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_BACKEND = os.path.join(_ROOT, "Source", "Backend")
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)

from db import (  # noqa: E402
    create_user,
    get_user_by_email,
    verify_user_password,
    create_session,
    get_security_question,
    verify_security_answer,
    reset_password_direct,
)

# ── Constants ─────────────────────────────────────────────────────────────────
ASSETS_DIR = Path(__file__).parent / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

DEPARTMENTS = [
    "Computer Science",
    "Software Engineering",
    "Information Technology",
    "Electrical Engineering",
    "Mathematics",
    "Physics",
    "Business Administration",
    "Other",
]

SEMESTERS = [f"Semester {i}" for i in range(1, 9)]

SECURITY_QUESTIONS = [
    "What was the name of your first pet?",
    "What was the name of your first teacher?",
    "What is your mother's maiden name?",
    "What city were you born in?",
    "What was the name of your childhood best friend?",
    "What was the make of your first car?",
    "What is the name of the street you grew up on?",
]

LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
     fill="none" stroke="white" stroke-width="2"
     stroke-linecap="round" stroke-linejoin="round">
  <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
  <path d="M6 12v5c3 3 9 3 12 0v-5"/>
</svg>"""

WARNING_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
     fill="none" stroke="#DC2626" stroke-width="2.5"
     stroke-linecap="round" stroke-linejoin="round">
  <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
  <line x1="12" y1="9" x2="12" y2="13"/>
  <line x1="12" y1="17" x2="12.01" y2="17"/>
</svg>"""

SUCCESS_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
     fill="none" stroke="#16a34a" stroke-width="2.5"
     stroke-linecap="round" stroke-linejoin="round">
  <polyline points="20 6 9 17 4 12"/>
</svg>"""


# ── Helpers ───────────────────────────────────────────────────────────────────

def _logo_html() -> str:
    try:
        if LOGO_PATH.exists():
            b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
            return (
                f'<img src="data:image/png;base64,{b64}" '
                f'alt="AI Smart Study logo" class="login-logo-img" />'
            )
    except OSError:
        pass
    return LOGO_SVG


def _error_html(msg: str) -> str:
    return f'<div class="login-error"><span>{WARNING_SVG}</span><span>{msg}</span></div>'


def _success_html(msg: str) -> str:
    return (
        f'<div class="login-error" style="border-color:rgba(34,197,94,.5);'
        f'background:rgba(34,197,94,.08);color:#86efac;">'
        f'<span>{SUCCESS_SVG}</span><span>{msg}</span></div>'
    )


# Material Symbols (rounded) — rendered inside fields by Streamlit 1.57+
_ICON_USER = ":material/person:"
_ICON_MAIL = ":material/mail:"
_ICON_LOCK = ":material/lock:"
_ICON_KEY = ":material/key:"
_ICON_SHIELD = ":material/shield:"

def _auth_mode_slug() -> str:
    return (st.session_state.get("auth_mode") or "Sign In").replace(" ", "-").lower()


def _auth_text_input(label: str, key: str, icon: str, **kwargs) -> str:
    """Text/password input with a built-in Material icon (Streamlit native)."""
    kwargs.setdefault("on_change", _clear_auth)
    return st.text_input(label, key=key, icon=icon, **kwargs)


def _auth_selectbox(label: str, options, key: str, **kwargs):
    """Selectbox; shield icon via CSS ::before on .st-key-{key}."""
    return st.selectbox(label, options, key=key, **kwargs)


def _clear_auth() -> None:
    st.session_state.login_error = None
    st.session_state.signup_error = None


# Shared auth shell — same width, header spacing, and tabs for both modes
_AUTH_LAYOUT_CSS = """
<style>
html body .stApp [data-testid="stMain"] > [data-testid="block-container"]:has(#studor-auth),
html body .stApp [data-testid="stMain"] .block-container:has(#studor-auth) {
    align-items: flex-start !important;
    justify-content: center !important;
    padding-top: 8px !important;
    padding-bottom: 12px !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(#studor-auth) {
    max-width: min(880px, 96vw) !important;
    width: 100% !important;
    padding: 8px 20px 12px 20px !important;
    margin-top: 0 !important;
    zoom: 0.9 !important;
}

div[data-testid="column"]:has(#studor-auth) .login-brand {
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.1 !important;
}

div[data-testid="column"]:has(#studor-auth) .login-logo-icon,
div[data-testid="column"]:has(#studor-auth) .login-logo-icon img.login-logo-img,
div[data-testid="column"]:has(#studor-auth) .login-logo-icon svg {
    width: 32px !important;
    height: 32px !important;
    margin: 0 auto 4px auto !important;
}

div[data-testid="column"]:has(#studor-auth) .login-brand-name {
    font-size: 16px !important;
    margin: 0 !important;
    line-height: 1.1 !important;
}

div[data-testid="column"]:has(#studor-auth) .login-brand-subtitle {
    font-size: 11px !important;
    margin-top: 2px !important;
    line-height: 1.15 !important;
}

div[data-testid="column"]:has(#studor-auth) .login-divider {
    margin: 8px 0 0 0 !important;
}

div[data-testid="column"]:has(#studor-auth) .login-auth-tabs-spacer {
    display: block;
    height: 14px;
    margin: 0;
    padding: 0;
}

div[data-testid="column"]:has(#studor-auth) [data-testid="stHorizontalBlock"]:has(.st-key-tab_signin) {
    margin: 0 0 8px 0 !important;
    padding: 3px !important;
    gap: 6px !important;
}

html body .stApp div[data-testid="column"]:has(#studor-auth) [data-testid="stHorizontalBlock"]:has(.st-key-tab_signin) [data-testid="stButton"] > button {
    min-height: 32px !important;
    height: 32px !important;
    padding: 4px 8px !important;
    font-size: 12px !important;
}

div[data-testid="column"]:has(#studor-auth) .login-heading--auth {
    margin: 2px 0 2px 0 !important;
    font-size: 14px !important;
    line-height: 1.15 !important;
    text-align: center !important;
}

div[data-testid="column"]:has(#studor-auth) .login-subheading--auth {
    margin: 0 0 10px 0 !important;
    font-size: 11px !important;
    line-height: 1.2 !important;
    text-align: center !important;
}

div[data-testid="column"]:has(#studor-auth) .auth-form-panel {
    width: 100% !important;
}

div[data-testid="column"]:has(#studor-auth[data-auth-mode="sign-in"]) [data-testid="stTextInput"],
div[data-testid="column"]:has(#studor-auth[data-auth-mode="sign-in"]) [data-testid="stCheckbox"],
div[data-testid="column"]:has(#studor-auth[data-auth-mode="sign-in"]) [data-testid="stButton"] {
    width: 100% !important;
}

div[data-testid="column"]:has(#studor-auth[data-auth-mode="sign-in"]) [data-testid="stTextInput"] {
    margin-bottom: 8px !important;
}

div[data-testid="column"]:has(#studor-auth[data-auth-mode="sign-in"]) [data-testid="stHorizontalBlock"]:has(.st-key-remember_me) {
    margin: 2px 0 8px 0 !important;
}
</style>
"""

# Create Account field density — keeps the two-column form compact
_REGISTER_COMPACT_CSS = """
<style>
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) .login-heading--register {
    margin: 2px 0 0 0 !important;
    font-size: 13px !important;
    line-height: 1.1 !important;
    text-align: center !important;
}

div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) .signup-section-label {
    margin: 0 0 0 !important;
    font-size: 9px !important;
    letter-spacing: 0.06em !important;
    line-height: 1.1 !important;
}

div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="element-container"] {
    margin: 0 !important;
    padding: 0 !important;
    min-height: 0 !important;
}

div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stVerticalBlock"],
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stVerticalBlock"] > div,
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stVerticalBlockBorderWrapper"] {
    gap: 0 !important;
}

div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stHorizontalBlock"] {
    gap: 0.35rem !important;
}

div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stTextInput"],
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stSelectbox"] {
    margin-bottom: 0 !important;
}

div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stTextInput"] label p,
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stSelectbox"] label p,
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stWidgetLabel"] p {
    margin-bottom: 0 !important;
    font-size: 10px !important;
    line-height: 1.05 !important;
}

div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stWidgetLabel"] {
    margin-bottom: 0 !important;
    min-height: 0 !important;
}

div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stTextInputRootElement"],
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stTextInput"] div[data-baseweb="input"] {
    min-height: 26px !important;
}

html body .stApp div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stTextInputRootElement"],
html body .stApp div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stTextInput"] div[data-baseweb="input"] {
    min-height: 26px !important;
}

div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stTextInput"] input {
    min-height: 26px !important;
    padding: 2px 6px 2px 2px !important;
    font-size: 11px !important;
    line-height: 1.1 !important;
}

html body .stApp div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stTextInput"] input {
    min-height: 26px !important;
    padding: 2px 6px 2px 2px !important;
    font-size: 11px !important;
}

div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    min-height: 26px !important;
    height: 26px !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

html body .stApp div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    min-height: 26px !important;
    height: 26px !important;
}

div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) .st-key-signup_sec_question [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    padding-left: 26px !important;
}

div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) .login-error {
    margin: 2px 0 !important;
    padding: 3px 8px !important;
    font-size: 10px !important;
}

div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) .st-key-signup_submit {
    margin-top: 4px !important;
    margin-bottom: 4px !important;
}

html body .stApp div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) .st-key-signup_submit [data-testid="stButton"] > button {
    min-height: 30px !important;
    height: 30px !important;
    padding: 3px 0 !important;
    font-size: 12px !important;
}
</style>
"""


def _inject_auth_layout_styles() -> None:
    st.markdown(_AUTH_LAYOUT_CSS, unsafe_allow_html=True)


def _inject_register_compact_styles() -> None:
    st.markdown(_REGISTER_COMPACT_CSS, unsafe_allow_html=True)


def _render_auth_brand_html() -> None:
    """Render Studor logo/title block — shared by Sign In and Create Account."""
    mode_slug = _auth_mode_slug()
    render_html(f"""
<div id="studor-auth" class="login-auth-root" data-auth-mode="{mode_slug}">
<div class="login-brand">
<div class="login-logo-icon">{_logo_html()}</div>
<div class="login-brand-name">Studor</div>
<div class="login-brand-subtitle">Risk &amp; Performance Predictor</div>
</div>
<hr class="login-divider" />
</div>
""")


def _set_mode(mode: str) -> None:
    st.session_state.auth_mode = mode
    _clear_auth()
    # Clear forgot-password state when switching tabs
    for k in ("forgot_step", "forgot_email", "forgot_question", "forgot_error", "reset_success"):
        st.session_state.pop(k, None)


def _set_session_from_user(email: str, full_name: str = "", remember: bool = False) -> None:
    """Populate session state and optionally create a persistent Remember Me cookie."""
    from db import get_user_profile, get_user_courses  # noqa: E402

    user_row = get_user_by_email(email)
    user_id = user_row[0] if user_row else None

    st.session_state.logged_in   = True
    st.session_state.user_id     = user_id
    st.session_state.user_email  = email
    st.session_state.full_name   = (user_row[3] if user_row else full_name) or ""
    st.session_state.student_id  = email  # back-compat

    # Load persisted profile fields from DB
    if user_id:
        try:
            profile = get_user_profile(user_id)
            if profile:
                st.session_state.full_name           = profile.get("full_name") or st.session_state.full_name
                st.session_state.profile_university  = profile.get("university") or ""
                st.session_state.profile_department  = profile.get("department") or "Computer Science"
                st.session_state.profile_semester    = profile.get("semester")   or "Semester 6"
                st.session_state.profile_target_gpa  = profile.get("target_gpa")
        except Exception:
            pass

        # Load courses into session state
        try:
            st.session_state.user_courses   = get_user_courses(user_id)
            st.session_state._courses_loaded = True
        except Exception:
            pass

        # Restore most-recent risk level on each course from prediction history
        try:
            from db import get_user_predictions  # noqa: E402
            preds = get_user_predictions(user_id, limit=50)
            risk_map = {p["course_name"]: p["risk_level"] for p in reversed(preds) if p.get("course_name")}
            for c in st.session_state.user_courses:
                if c.get("name") in risk_map:
                    c["risk_level"] = risk_map[c["name"]]
        except Exception:
            pass

    if remember and user_row:
        try:
            token = create_session(user_row[0])
            st.session_state._pending_session_cookie = token
        except Exception:
            pass


# ── Tab navigation ────────────────────────────────────────────────────────────

def _render_tabs(active_mode: str) -> None:
    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            "Sign In",
            key="tab_signin",
            type="primary" if active_mode == "Sign In" else "secondary",
            use_container_width=True,
        ):
            if active_mode != "Sign In":
                _set_mode("Sign In")
                st.rerun()
    with c2:
        if st.button(
            "Create Account",
            key="tab_register",
            type="primary" if active_mode == "Create Account" else "secondary",
            use_container_width=True,
        ):
            if active_mode != "Create Account":
                _set_mode("Create Account")
                st.rerun()


# ── Forgot-password 3-step flow ───────────────────────────────────────────────

def _reset_forgot() -> None:
    for k in ("forgot_step", "forgot_email", "forgot_question", "forgot_error", "reset_success"):
        st.session_state.pop(k, None)


def _render_forgot_password() -> None:
    step = st.session_state.get("forgot_step", "email")

    if st.button("← Back to Sign In", key="back_to_login", use_container_width=False):
        _reset_forgot()
        st.rerun()

    if step == "email":
        render_html("""
            <div class="login-heading">Forgot Password</div>
            <div class="login-subheading">Enter your email to verify your identity</div>
        """)

        email_input = _auth_text_input(
            "Registered Email", key="fp_email", icon=_ICON_MAIL,
            placeholder="name@example.com",
        )

        if st.session_state.get("forgot_error"):
            render_html(_error_html(st.session_state.forgot_error))

        if st.button("Continue →", key="fp_continue", type="primary", use_container_width=True):
            mail = (email_input or "").strip().lower()
            if not mail:
                st.session_state.forgot_error = "Please enter your email address."
                st.rerun()
            try:
                question = get_security_question(mail)
                if question:
                    st.session_state.forgot_email = mail
                    st.session_state.forgot_question = question
                    st.session_state.forgot_step = "question"
                    st.session_state.forgot_error = None
                else:
                    # Always show same message — don't reveal whether email exists
                    st.session_state.forgot_error = (
                        "No security question found for this account. "
                        "Please register a new account."
                    )
            except Exception:
                st.session_state.forgot_error = "Database unavailable. Please try again later."
            st.rerun()

    elif step == "question":
        render_html('<div class="login-heading">Security Question</div>')
        question = st.session_state.get("forgot_question", "")
        render_html(f'<div class="login-subheading" style="font-style:italic;">{question}</div>')

        answer_input = _auth_text_input(
            "Your Answer", key="fp_answer", icon=_ICON_KEY,
            placeholder="Answer is not case-sensitive",
        )

        if st.session_state.get("forgot_error"):
            render_html(_error_html(st.session_state.forgot_error))

        if st.button("Verify Answer", key="fp_verify", type="primary", use_container_width=True):
            if not (answer_input or "").strip():
                st.session_state.forgot_error = "Please enter your answer."
                st.rerun()
            try:
                mail = st.session_state.get("forgot_email", "")
                if verify_security_answer(mail, answer_input):
                    st.session_state.forgot_step = "reset"
                    st.session_state.forgot_error = None
                else:
                    st.session_state.forgot_error = "Incorrect answer. Please try again."
            except Exception:
                st.session_state.forgot_error = "Database unavailable. Please try again later."
            st.rerun()

    elif step == "reset":
        render_html("""
            <div class="login-heading">Choose a New Password</div>
            <div class="login-subheading">Your identity has been verified ✓</div>
        """)

        new_pw = _auth_text_input(
            "New Password", key="fp_new_pw", icon=_ICON_LOCK, type="password",
            placeholder="At least 6 characters",
        )
        confirm_pw = _auth_text_input(
            "Confirm Password", key="fp_confirm_pw", icon=_ICON_LOCK, type="password",
            placeholder="Repeat your password",
        )

        if st.session_state.get("forgot_error"):
            render_html(_error_html(st.session_state.forgot_error))

        if st.button("Reset Password", key="fp_reset", type="primary", use_container_width=True):
            if len(new_pw or "") < 6:
                st.session_state.forgot_error = "Password must be at least 6 characters."
                st.rerun()
            elif new_pw != confirm_pw:
                st.session_state.forgot_error = "Passwords do not match."
                st.rerun()
            try:
                mail = st.session_state.get("forgot_email", "")
                if reset_password_direct(mail, new_pw):
                    _reset_forgot()
                    st.session_state.reset_success = True
                else:
                    st.session_state.forgot_error = "Reset failed. Please try again."
            except Exception:
                st.session_state.forgot_error = "Database unavailable. Please try again later."
            st.rerun()


# ── Sign-in form ──────────────────────────────────────────────────────────────

def _render_login_form() -> None:
    # Show forgot-password flow when active
    if st.session_state.get("forgot_step"):
        _render_forgot_password()
        return

    render_html("""
<div class="login-heading login-heading--auth">Welcome back</div>
<div class="login-subheading login-subheading--auth">Sign in to continue to your dashboard</div>
""")

    # Success banner after password reset
    if st.session_state.pop("reset_success", False):
        render_html(_success_html("Password reset successfully! Please sign in."))

    email = _auth_text_input(
        "Email", key="login_email", icon=_ICON_MAIL,
        placeholder="name@example.com",
    )
    password = _auth_text_input(
        "Password", key="login_password", icon=_ICON_LOCK, type="password",
        placeholder="Enter your password",
    )

    col_l, col_r = st.columns(2)
    with col_l:
        remember_me = st.checkbox("Remember me for 30 days", key="remember_me")
    with col_r:
        if st.button("Forgot password?", key="forgot_btn",
                     use_container_width=True, type="secondary"):
            st.session_state.forgot_step = "email"
            st.session_state.forgot_error = None
            st.rerun()

    if st.session_state.login_error:
        render_html(_error_html(st.session_state.login_error))

    if st.button("Sign In", key="login_submit", type="primary", use_container_width=True):
        mail = (email or "").strip().lower()
        if not mail:
            st.session_state.login_error = "Please enter your email address."
            st.rerun()
        try:
            if verify_user_password(mail, password or ""):
                _set_session_from_user(mail, remember=remember_me)
                st.session_state.login_error = None
                st.rerun()
            else:
                st.session_state.login_error = "Invalid email or password. Please try again."
                st.rerun()
        except Exception as _e:
            _msg = str(_e).lower()
            if "enotfound" in _msg or "tenant" in _msg or "not found" in _msg or "nodename" in _msg:
                st.session_state.login_error = (
                    "Database is paused. Please go to supabase.com/dashboard and click 'Restore project', then try again."
                )
            else:
                st.session_state.login_error = "Database unavailable. Please try again later."
            st.rerun()


# ── Registration form ─────────────────────────────────────────────────────────

def _render_register_form() -> None:
    render_html('<div class="login-heading login-heading--auth login-heading--register">Create your account</div>')

    col_account, col_academic = st.columns(2, gap="small")

    with col_account:
        render_html('<div class="signup-section-label">Account Information</div>')
        full_name = _auth_text_input(
            "Full Name", key="signup_full_name", icon=_ICON_USER,
            placeholder="e.g. Azra Özdaş",
        )
        email = _auth_text_input(
            "Email", key="signup_email", icon=_ICON_MAIL,
            placeholder="name@example.com",
        )
        new_password = _auth_text_input(
            "Password", key="signup_password", icon=_ICON_LOCK, type="password",
            placeholder="At least 6 characters",
        )
        confirm_password = _auth_text_input(
            "Confirm Password", key="signup_confirm", icon=_ICON_LOCK, type="password",
            placeholder="Repeat your password",
        )

    with col_academic:
        render_html('<div class="signup-section-label">Academic Profile</div>')
        university = _auth_text_input(
            "University / School", key="signup_university", icon=_ICON_USER,
            placeholder="e.g. Istanbul University",
        )
        signup_dept = _auth_selectbox(
            "Department / Program", DEPARTMENTS, key="signup_department",
        )
        signup_sem = _auth_selectbox(
            "Semester", SEMESTERS, key="signup_semester",
        )
        target_gpa_str = _auth_text_input(
            "Target GPA (optional)", key="signup_target_gpa", icon=_ICON_KEY,
            placeholder="e.g. 3.5",
        )

    col_sec_q, col_sec_a = st.columns(2, gap="small")
    with col_sec_q:
        render_html('<div class="signup-section-label">Security</div>')
        security_question = _auth_selectbox(
            "Security question", SECURITY_QUESTIONS,
            key="signup_sec_question",
        )
    with col_sec_a:
        render_html('<div class="signup-section-label" style="visibility:hidden;">&nbsp;</div>')
        security_answer = _auth_text_input(
            "Your Answer", key="signup_sec_answer", icon=_ICON_KEY,
            placeholder="Not case-sensitive",
        )

    if st.session_state.signup_error:
        render_html(_error_html(st.session_state.signup_error))

    if st.button("Create Account", key="signup_submit", type="primary", use_container_width=True):
        name = (full_name or "").strip()
        mail = (email or "").strip().lower()
        pwd = new_password or ""
        conf = confirm_password or ""
        answer = (security_answer or "").strip()

        if not name:
            st.session_state.signup_error = "Full name is required."
        elif not mail or not EMAIL_PATTERN.match(mail):
            st.session_state.signup_error = "Please enter a valid email address."
        elif len(pwd) < 6:
            st.session_state.signup_error = "Password must be at least 6 characters."
        elif pwd != conf:
            st.session_state.signup_error = "Passwords do not match."
        elif not answer or len(answer) < 2:
            st.session_state.signup_error = "Please provide an answer for your security question."
        else:
            try:
                try:
                    gpa_val = float(target_gpa_str) if (target_gpa_str or "").strip() else None
                except ValueError:
                    gpa_val = None

                create_user(
                    email=mail,
                    password=pwd,
                    full_name=name,
                    security_question=security_question,
                    security_answer=answer,
                    university=(university or "").strip() or None,
                    department=signup_dept,
                    semester=signup_sem,
                    target_gpa=gpa_val,
                )
                _set_session_from_user(mail, full_name=name)
                st.session_state.profile_university  = (university or "").strip()
                st.session_state.profile_department  = signup_dept
                st.session_state.profile_semester    = signup_sem
                st.session_state.profile_target_gpa = gpa_val
                st.session_state.user_courses = []
                st.session_state.signup_error = None
                st.rerun()
            except ValueError:
                st.session_state.signup_error = (
                    "This email is already registered. Please sign in instead."
                )
            except Exception as _e:
                _msg = str(_e).lower()
                if "enotfound" in _msg or "tenant" in _msg or "not found" in _msg or "nodename" in _msg:
                    st.session_state.signup_error = (
                        "Database is paused. Please go to supabase.com/dashboard and click 'Restore project', then try again."
                    )
                else:
                    st.session_state.signup_error = (
                        "Database unavailable. Please try again later."
                    )
        st.rerun()


# ── Entry point ───────────────────────────────────────────────────────────────

def render_login_page() -> None:
    st.session_state.setdefault("auth_mode", "Sign In")
    st.session_state.setdefault("login_error", None)
    st.session_state.setdefault("signup_error", None)

    is_register = st.session_state.auth_mode == "Create Account"

    inject_login_styles(st.session_state.auth_mode)
    _inject_auth_layout_styles()
    if is_register:
        _inject_register_compact_styles()

    _, center, _ = st.columns([0.25, 3.5, 0.25])

    with center:
        _render_auth_brand_html()
        render_html('<div class="login-auth-tabs-spacer" aria-hidden="true"></div>')
        _render_tabs(st.session_state.auth_mode)

        if st.session_state.auth_mode == "Sign In":
            _render_login_form()
        else:
            _render_register_form()

    # Re-inject after widgets so auth CSS wins over Streamlit 1.57 theme rules
    inject_login_styles(st.session_state.auth_mode)
    _inject_auth_layout_styles()
    if is_register:
        _inject_register_compact_styles()
