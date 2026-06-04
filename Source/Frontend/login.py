"""
Authentication page for the AI Smart Study Risk & Performance Predictor.

Public hooks used by app.py:
    - render_login_page()
    - handle_login(email, password)      -> bool
    - handle_register(full_name, email, password, confirm_password) -> (bool, str|None)

Storage: hosted PostgreSQL via Supabase (Source/Backend/db.py).
Logo:    Source/Frontend/assets/logo.png — falls back to inline SVG if missing.
"""

import base64
import os
import re
import sys
from pathlib import Path
from typing import Optional, Tuple

import streamlit as st

from utils import render_html
from styles import inject_login_styles

# Allow imports from Source/Backend regardless of working directory
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_BACKEND = os.path.join(_ROOT, "Source", "Backend")
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)

from db import create_user, get_user_by_email, verify_user_password  # noqa: E402

ASSETS_DIR = Path(__file__).parent / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
     fill="none" stroke="white" stroke-width="2"
     stroke-linecap="round" stroke-linejoin="round">
    <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
    <path d="M6 12v5c3 3 9 3 12 0v-5"/>
</svg>
"""

WARNING_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
     fill="none" stroke="#DC2626" stroke-width="2.5"
     stroke-linecap="round" stroke-linejoin="round">
    <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
    <line x1="12" y1="9" x2="12" y2="13"/>
    <line x1="12" y1="17" x2="12.01" y2="17"/>
</svg>
"""


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


def handle_login(email: str, password: str) -> bool:
    mail = (email or "").strip().lower()
    if not mail:
        return False
    try:
        return verify_user_password(mail, password)
    except Exception:
        raise ConnectionError("Unable to reach the database. Please try again later.")


def handle_register(
    full_name: str,
    email: str,
    password: str,
    confirm_password: str,
) -> Tuple[bool, Optional[str]]:
    name = (full_name or "").strip()
    mail = (email or "").strip().lower()
    pwd = password or ""
    conf = confirm_password or ""

    if not name:
        return False, "Full name is required."
    if not mail or not EMAIL_PATTERN.match(mail):
        return False, "Please enter a valid email address."
    if len(pwd) < 6:
        return False, "Password must be at least 6 characters."
    if pwd != conf:
        return False, "Passwords do not match."

    try:
        create_user(email=mail, password=pwd, full_name=name)
        return True, None
    except ValueError:
        return False, "This email is already registered. Please sign in instead."
    except Exception:
        return False, "Unable to reach the database. Please try again later."


def _clear_auth_messages() -> None:
    st.session_state.login_error = None
    st.session_state.signup_error = None


def _set_mode(mode: str) -> None:
    st.session_state.auth_mode = mode
    _clear_auth_messages()


def _set_session_from_user(email: str, full_name: str = "") -> None:
    """Populate session state after a successful login or registration."""
    user_row = get_user_by_email(email)
    st.session_state.logged_in = True
    st.session_state.user_id = user_row[0] if user_row else None
    st.session_state.user_email = email
    st.session_state.full_name = (user_row[3] if user_row else full_name) or ""
    st.session_state.student_id = email  # kept for back-compat with app.py


def _render_tabs(active_mode: str) -> None:
    render_html('<div id="auth-tabs-start"></div>')
    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            "Sign In",
            key="tab_signin",
            type=("primary" if active_mode == "Sign In" else "secondary"),
            use_container_width=True,
        ):
            if active_mode != "Sign In":
                _set_mode("Sign In")
                st.rerun()
    with c2:
        if st.button(
            "Create Account",
            key="tab_register",
            type=("primary" if active_mode == "Create Account" else "secondary"),
            use_container_width=True,
        ):
            if active_mode != "Create Account":
                _set_mode("Create Account")
                st.rerun()


def _render_login_form() -> None:
    render_html("""
        <div class="login-heading">Welcome back</div>
        <div class="login-subheading">Sign in to continue to your dashboard</div>
    """)

    email = st.text_input(
        "Email",
        key="login_email",
        placeholder="name@example.com",
        on_change=_clear_auth_messages,
    )
    password = st.text_input(
        "Password",
        key="login_password",
        type="password",
        placeholder="Enter your password",
        on_change=_clear_auth_messages,
    )

    if st.session_state.login_error:
        render_html(f"""
            <div class="login-error">
                <span>{WARNING_SVG}</span>
                <span>{st.session_state.login_error}</span>
            </div>
        """)

    if st.button("Sign In", key="login_submit", type="primary", use_container_width=True):
        mail = (email or "").strip().lower()
        if not mail:
            st.session_state.login_error = "Please enter your email address."
            st.rerun()
        else:
            try:
                if handle_login(email, password):
                    _set_session_from_user(mail)
                    st.session_state.login_error = None
                    st.rerun()
                else:
                    st.session_state.login_error = "Invalid email or password. Please try again."
                    st.rerun()
            except ConnectionError as e:
                st.session_state.login_error = str(e)
                st.rerun()


def _render_register_form() -> None:
    render_html("""
        <div class="login-heading">Create your account</div>
        <div class="login-subheading">Get started with the study risk predictor</div>
    """)

    full_name = st.text_input(
        "Full Name", key="signup_full_name",
        placeholder="e.g. Azra Özdaş", on_change=_clear_auth_messages,
    )
    email = st.text_input(
        "Email", key="signup_email",
        placeholder="name@example.com", on_change=_clear_auth_messages,
    )
    new_password = st.text_input(
        "Password", key="signup_password", type="password",
        placeholder="At least 6 characters", on_change=_clear_auth_messages,
    )
    confirm_password = st.text_input(
        "Confirm Password", key="signup_confirm", type="password",
        placeholder="Repeat your password", on_change=_clear_auth_messages,
    )

    if st.session_state.signup_error:
        render_html(f"""
            <div class="login-error">
                <span>{WARNING_SVG}</span>
                <span>{st.session_state.signup_error}</span>
            </div>
        """)

    if st.button(
        "Create Account",
        key="signup_submit",
        type="primary",
        use_container_width=True,
    ):
        ok, err = handle_register(full_name, email, new_password, confirm_password)
        if ok:
            mail = (email or "").strip().lower()
            name = (full_name or "").strip()
            _set_session_from_user(mail, full_name=name)
            st.session_state.signup_error = None
            st.rerun()
        else:
            st.session_state.signup_error = err
            st.rerun()


def render_login_page() -> None:
    inject_login_styles()

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "Sign In"
    if "login_error" not in st.session_state:
        st.session_state.login_error = None
    if "signup_error" not in st.session_state:
        st.session_state.signup_error = None

    _, center, _ = st.columns([1, 1.2, 1])

    with center:
        render_html(f"""
            <div class="login-brand">
                <div class="login-logo-icon">{_logo_html()}</div>
                <div class="login-brand-name">AI Smart Study</div>
                <div class="login-brand-subtitle">Risk &amp; Performance Predictor</div>
            </div>
            <hr class="login-divider" />
        """)

        _render_tabs(st.session_state.auth_mode)

        if st.session_state.auth_mode == "Sign In":
            _render_login_form()
        else:
            _render_register_form()
