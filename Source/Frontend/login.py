"""
Authentication page for the AI Smart Study Risk & Performance Predictor.

Public hooks used by app.py:
    - render_login_page()
    - handle_login(email, password)
    - handle_register(full_name, email, password, confirm_password)

Storage: prototype-only JSON at Data/users.json (plain-text passwords, keyed by email).
Logo:    Source/Frontend/assets/logo.png (PNG, square, transparent background recommended).
         If the file is missing, falls back to the inline graduation-cap SVG.
"""

import base64
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import streamlit as st

from utils import render_html
from styles import inject_login_styles


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
USERS_PATH = os.path.join(ROOT, "Data", "users.json")

ASSETS_DIR = Path(__file__).parent / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"

DEFAULT_USERS = {
    "demo@study.ai": {"password": "password123", "full_name": "Demo User"},
    "test@study.ai": {"password": "password123", "full_name": "Test User"},
}

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
    """Return an <img> tag for assets/logo.png; fall back to SVG if missing."""
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


def _normalize_user(record: Any) -> Dict[str, str]:
    if isinstance(record, str):
        return {"password": record, "full_name": ""}
    return {
        "password": record.get("password", ""),
        "full_name": record.get("full_name", ""),
    }


def load_users() -> Dict[str, Dict[str, str]]:
    users = {k.lower(): _normalize_user(v) for k, v in DEFAULT_USERS.items()}
    if os.path.exists(USERS_PATH):
        try:
            with open(USERS_PATH, encoding="utf-8") as f:
                raw = json.load(f)
            for key, rec in raw.items():
                users[str(key).lower()] = _normalize_user(rec)
        except (json.JSONDecodeError, OSError):
            pass
    return users


def save_registered_users(users: Dict[str, Dict[str, str]]) -> None:
    default_keys = {k.lower() for k in DEFAULT_USERS}
    registered = {k: v for k, v in users.items() if k not in default_keys}
    os.makedirs(os.path.dirname(USERS_PATH), exist_ok=True)
    with open(USERS_PATH, "w", encoding="utf-8") as f:
        json.dump(registered, f, indent=2)

def handle_login(email: str, password: str) -> bool:
    mail = (email or "").strip().lower()
    if not mail:
        return False
    users = load_users()
    rec = users.get(mail)
    if rec is None:
        return False
    return rec.get("password", "") == (password or "")


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

    users = load_users()
    if mail in users:
        return False, "This email is already registered. Please sign in instead."

    users[mail] = {"password": pwd, "full_name": name}
    save_registered_users(users)
    return True, None



def _clear_auth_messages() -> None:
    st.session_state.login_error = False
    st.session_state.signup_error = None


def _set_mode(mode: str) -> None:
    st.session_state.auth_mode = mode
    _clear_auth_messages()


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

    render_html('<div class="login-meta-row">')
    m1, m2 = st.columns(2)
    with m1:
        st.checkbox("Remember me", key="remember_me", on_change=_clear_auth_messages)
    with m2:
        render_html('<div class="login-forgot-link">Forgot password?</div>')
    render_html("</div>")

    if st.session_state.login_error:
        render_html(f"""
            <div class="login-error">
                <span>{WARNING_SVG}</span>
                <span>Invalid email or password. Please try again.</span>
            </div>
        """)

    if st.button("Sign In", key="login_submit", type="primary", use_container_width=True):
        if not (email or "").strip():
            st.session_state.login_error = True
            st.rerun()
        elif handle_login(email, password):
            mail = (email or "").strip().lower()
            rec = load_users().get(mail, {})
            st.session_state.logged_in = True
            st.session_state.user_email = mail
            st.session_state.full_name = rec.get("full_name", "")
            st.session_state.student_id = mail  # back-compat for app.py sidebar caption
            st.session_state.login_error = False
            st.rerun()
        else:
            st.session_state.login_error = True
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
            st.session_state.logged_in = True
            st.session_state.user_email = mail
            st.session_state.full_name = (full_name or "").strip()
            st.session_state.student_id = mail  # back-compat for app.py sidebar caption
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
        st.session_state.login_error = False
    if "signup_error" not in st.session_state:
        st.session_state.signup_error = None
    if "remember_me" not in st.session_state:
        st.session_state.remember_me = False

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