import streamlit as st


LOGIN_STYLES = """
<style>

:root,
html,
body,
.stApp,
[data-testid="stAppViewContainer"] {
    --primary-color: #2563EB !important;
    --primary-color-rgb: 37, 99, 235 !important;
    --background-color: #0B1220 !important;
}


*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
}

.stApp {
    background:
        radial-gradient(1100px 600px at 20% -10%, rgba(59,130,246,0.10), transparent 60%),
        radial-gradient(900px 500px at 90% 110%, rgba(29,78,216,0.10), transparent 60%),
        #0B1220 !important;
}

section[data-testid="stSidebar"],
[data-testid="collapsedControl"] { display: none !important; }

header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
    min-height: 0 !important;
}

.main .block-container,
[data-testid="stMain"] .block-container {
    padding-top: 0.25rem !important;
    padding-bottom: 0.25rem !important;
    max-width: 100% !important;
    min-height: 0 !important;
}

/* Centre the card vertically inside the viewport */
[data-testid="stMain"] {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}


/* 4. Reduced card padding: 14px 28px */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
    background: linear-gradient(180deg, rgba(30,41,59,0.97), rgba(15,23,42,0.97));
    border: 1px solid rgba(148, 163, 184, 0.14);
    border-radius: 20px;
    padding: 14px 28px !important;
    box-shadow: 0 24px 56px rgba(0, 0, 0, 0.50),
                inset 0 1px 0 rgba(255, 255, 255, 0.04);
    max-width: 600px;
    margin: 0 auto !important;
    max-height: calc(100vh - 12px);
    overflow-y: auto;
    scrollbar-width: thin;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)::-webkit-scrollbar {
    width: 4px;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)::-webkit-scrollbar-thumb {
    background: rgba(148, 163, 184, 0.18);
    border-radius: 4px;
}

/* 6. Spacing between fields: 6px */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
    div[data-testid="stVerticalBlock"] {
    gap: 6px !important;
}


.login-brand { text-align: center; margin-bottom: 0; }

/* 1. Reduced logo size: 48px, margin-bottom 6px */
.login-logo-icon {
    width: 48px;
    height: 48px;
    border: none !important;
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 6px auto;
    overflow: visible;
}

/* Fallback SVG (only used if assets/logo.png is missing) */
.login-logo-icon svg {
    width: 40px;
    height: 40px;
    filter: drop-shadow(0 6px 18px rgba(59, 130, 246, 0.35));
}

/* Custom PNG logo — 48px */
.login-logo-icon img.login-logo-img {
    width: 48px;
    height: 48px;
    object-fit: contain;
    display: block;
    background: transparent !important;
    border: none !important;
    border-radius: 14px !important;
    box-shadow: none !important;
    filter: drop-shadow(0 6px 18px rgba(59, 130, 246, 0.35))
            drop-shadow(0 2px 6px rgba(0, 0, 0, 0.35));
}

/* 2. Reduced brand text */
.login-brand-name {
    font-size: 18px; font-weight: 800; color: #F8FAFC;
    letter-spacing: -0.02em; line-height: 1.1;
}

.login-brand-subtitle {
    font-size: 10px; font-weight: 500; color: #64748B;
    margin-top: 1px;
}

/* 3. Divider spacing */
.login-divider {
    border: none;
    border-top: 1px solid rgba(148,163,184,0.12);
    margin: 8px 0 10px 0;
}


.login-heading {
    font-size: 17px; font-weight: 700; color: #F8FAFC;
    letter-spacing: -0.01em; line-height: 1.15;
}
.login-subheading {
    font-size: 11px; font-weight: 400; color: #64748B;
    margin-top: 1px; margin-bottom: 2px;
}

/* 8. Security label sits directly after Confirm Password (6px gap via block gap) */
.signup-section-label {
    font-size: 12px; color: #94A3B8; font-weight: 600;
    margin: 0 0 2px 0;
    line-height: 1.25;
}

/* =========================================================
   5/6. TEXT INPUTS — height 34, font 13, label margin 2px
   ========================================================= */
html body .stApp .stTextInput { margin-bottom: 0 !important; }

html body .stApp .stTextInput label,
html body .stApp .stTextInput label p,
html body .stApp .stTextInput [data-testid="stWidgetLabel"] p {
    font-size: 11px !important;
    font-weight: 600 !important;
    color: #CBD5E1 !important;
    margin-bottom: 2px !important;
    padding: 0 !important;
}

html body .stApp .stTextInput div[data-baseweb="input"] {
    background: linear-gradient(180deg, #0F172A 0%, #0B1220 100%) !important;
    border: 1px solid rgba(148, 163, 184, 0.12) !important;
    border-radius: 10px !important;
    min-height: 34px;
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.35) !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
}
/* Inner BaseWeb wrapper carries Streamlit's default light fill — force transparent */
html body .stApp .stTextInput div[data-baseweb="input"] div[data-baseweb="base-input"],
html body .stApp .stTextInput div[data-baseweb="base-input"] {
    background: transparent !important;
    background-color: transparent !important;
}
html body .stApp .stTextInput div[data-baseweb="input"]:hover {
    border-color: rgba(148, 163, 184, 0.20) !important;
}
html body .stApp .stTextInput div[data-baseweb="input"]:focus-within {
    background: linear-gradient(180deg, #111827 0%, #0B1220 100%) !important;
    border-color: rgba(59, 130, 246, 0.85) !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.16),
                inset 0 1px 2px rgba(0, 0, 0, 0.30) !important;
}
html body .stApp .stTextInput input {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
    font-size: 13px !important;
    padding: 6px 10px 6px 38px !important;
    height: 34px !important;
}
html body .stApp .stTextInput input::placeholder { color: #64748B !important; opacity: 1 !important; }
/* Chrome autofill paints white — repaint to the dark surface */
html body .stApp .stTextInput input:-webkit-autofill,
html body .stApp .stTextInput input:-webkit-autofill:hover,
html body .stApp .stTextInput input:-webkit-autofill:focus {
    -webkit-text-fill-color: #F8FAFC !important;
    -webkit-box-shadow: 0 0 0 1000px #0B1220 inset !important;
    caret-color: #F8FAFC !important;
    transition: background-color 9999s ease-in-out 0s !important;
}

/* ── Field icons — pseudo-element overlay (mask-based) ──────────────────────
   Drawn on ::before so they never collide with the input's gradient surface
   or focus background. Targeted by stable st-key-* container classes. The
   left padding (38px) already reserved on the inputs leaves room for them. */
html body .stApp .stTextInput div[data-baseweb="input"],
html body .stApp .stSelectbox div[data-baseweb="select"] > div {
    position: relative;
}

html body .stApp .st-key-signup_full_name div[data-baseweb="input"]::before,
html body .stApp .st-key-login_email div[data-baseweb="input"]::before,
html body .stApp .st-key-signup_email div[data-baseweb="input"]::before,
html body .stApp .st-key-fp_email div[data-baseweb="input"]::before,
html body .stApp .st-key-login_password div[data-baseweb="input"]::before,
html body .stApp .st-key-signup_password div[data-baseweb="input"]::before,
html body .stApp .st-key-fp_new_pw div[data-baseweb="input"]::before,
html body .stApp .st-key-signup_confirm div[data-baseweb="input"]::before,
html body .stApp .st-key-fp_confirm_pw div[data-baseweb="input"]::before,
html body .stApp .st-key-signup_sec_answer div[data-baseweb="input"]::before,
html body .stApp .st-key-fp_answer div[data-baseweb="input"]::before,
html body .stApp .st-key-signup_sec_question div[data-baseweb="select"] > div::before {
    content: "";
    position: absolute;
    left: 13px;
    top: 50%;
    transform: translateY(-50%);
    width: 15px;
    height: 15px;
    background-color: #64748B;
    -webkit-mask-repeat: no-repeat; mask-repeat: no-repeat;
    -webkit-mask-position: center; mask-position: center;
    -webkit-mask-size: contain; mask-size: contain;
    transition: background-color 0.18s ease;
    pointer-events: none;
    z-index: 4;
}

/* Hover — slightly brighter */
html body .stApp .stTextInput div[data-baseweb="input"]:hover::before,
html body .stApp .stSelectbox div[data-baseweb="select"]:hover > div::before {
    background-color: #94A3B8;
}
/* Focus — active blue accent, matching the field glow */
html body .stApp .stTextInput div[data-baseweb="input"]:focus-within::before,
html body .stApp .stSelectbox div[data-baseweb="select"]:focus-within > div::before {
    background-color: #3B82F6;
}

/* Per-field icon masks (Lucide family, consistent 2px stroke) */
html body .stApp .st-key-signup_full_name div[data-baseweb="input"]::before {
    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='12' cy='7' r='4'/%3E%3C/svg%3E");
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='12' cy='7' r='4'/%3E%3C/svg%3E");
}
html body .stApp .st-key-login_email div[data-baseweb="input"]::before,
html body .stApp .st-key-signup_email div[data-baseweb="input"]::before,
html body .stApp .st-key-fp_email div[data-baseweb="input"]::before {
    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect width='20' height='16' x='2' y='4' rx='2'/%3E%3Cpath d='m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7'/%3E%3C/svg%3E");
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect width='20' height='16' x='2' y='4' rx='2'/%3E%3Cpath d='m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7'/%3E%3C/svg%3E");
}
html body .stApp .st-key-login_password div[data-baseweb="input"]::before,
html body .stApp .st-key-signup_password div[data-baseweb="input"]::before,
html body .stApp .st-key-fp_new_pw div[data-baseweb="input"]::before,
html body .stApp .st-key-signup_confirm div[data-baseweb="input"]::before,
html body .stApp .st-key-fp_confirm_pw div[data-baseweb="input"]::before {
    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect width='18' height='11' x='3' y='11' rx='2' ry='2'/%3E%3Cpath d='M7 11V7a5 5 0 0 1 10 0v4'/%3E%3C/svg%3E");
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect width='18' height='11' x='3' y='11' rx='2' ry='2'/%3E%3Cpath d='M7 11V7a5 5 0 0 1 10 0v4'/%3E%3C/svg%3E");
}
html body .stApp .st-key-signup_sec_answer div[data-baseweb="input"]::before,
html body .stApp .st-key-fp_answer div[data-baseweb="input"]::before {
    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='7.5' cy='15.5' r='5.5'/%3E%3Cpath d='m21 2-9.6 9.6'/%3E%3Cpath d='m15.5 7.5 3 3L22 7l-3-3'/%3E%3C/svg%3E");
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='7.5' cy='15.5' r='5.5'/%3E%3Cpath d='m21 2-9.6 9.6'/%3E%3Cpath d='m15.5 7.5 3 3L22 7l-3-3'/%3E%3C/svg%3E");
}
html body .stApp .st-key-signup_sec_question div[data-baseweb="select"] > div::before {
    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3Cpath d='m9 12 2 2 4-4'/%3E%3C/svg%3E");
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3Cpath d='m9 12 2 2 4-4'/%3E%3C/svg%3E");
}

/* Security Question selectbox: reserve room for its icon (value text inset) */
html body .stApp .st-key-signup_sec_question div[data-baseweb="select"] > div > div:first-child {
    padding-left: 26px !important;
}

/* =========================================================
   5. SELECTBOX (Security Question) — height 34, font 13
   ========================================================= */
html body .stApp .stSelectbox { margin-bottom: 0 !important; }

html body .stApp .stSelectbox label,
html body .stApp .stSelectbox label p,
html body .stApp .stSelectbox [data-testid="stWidgetLabel"] p {
    font-size: 11px !important;
    font-weight: 600 !important;
    color: #CBD5E1 !important;
    margin-bottom: 2px !important;
    padding: 0 !important;
}
html body .stApp .stSelectbox div[data-baseweb="select"] > div {
    background: linear-gradient(180deg, #0F172A 0%, #0B1220 100%) !important;
    border: 1px solid rgba(148, 163, 184, 0.12) !important;
    border-radius: 10px !important;
    min-height: 34px !important;
    height: 34px !important;
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.35) !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
}
html body .stApp .stSelectbox div[data-baseweb="select"]:hover > div {
    border-color: rgba(148, 163, 184, 0.20) !important;
}
html body .stApp .stSelectbox div[data-baseweb="select"],
html body .stApp .stSelectbox div[data-baseweb="select"] div,
html body .stApp .stSelectbox div[data-baseweb="select"] span {
    font-size: 13px !important;
    color: #F8FAFC !important;
}
html body .stApp .stSelectbox div[data-baseweb="select"]:focus-within > div {
    background: linear-gradient(180deg, #111827 0%, #0B1220 100%) !important;
    border-color: rgba(59, 130, 246, 0.85) !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.16),
                inset 0 1px 2px rgba(0, 0, 0, 0.30) !important;
}


.login-meta-row { margin: 0 0 6px 0; }

html body .stApp .stCheckbox { margin-bottom: 0 !important; }

/* Vertically center the checkbox box with its label text */
html body .stApp .stCheckbox label {
    display: flex !important;
    align-items: center !important;
}
html body .stApp .stCheckbox label p {
    font-size: 11px !important;
    color: #94A3B8 !important;
    font-weight: 500 !important;
    margin: 0 !important;
    line-height: 1 !important;
}
html body .stApp .stCheckbox label span {
    background-color: rgba(15,23,42,0.9) !important;
    border-color: #334155 !important;
}

.login-forgot-link {
    text-align: right;
    color: #64748B;
    font-size: 11px;
    font-weight: 500;
    padding-top: 4px;
}


.login-error {
    background: rgba(127, 29, 29, 0.40);
    border: 1px solid rgba(220, 38, 38, 0.55);
    color: #FCA5A5;
    font-size: 12px; font-weight: 600;
    border-radius: 8px; padding: 6px 12px;
    margin-bottom: 2px;
    display: flex; align-items: center; gap: 8px;
}


/* 7. Buttons — Create Account height 38, padding 7px 0 */
html body .stApp button,
html body .stApp .stButton > button,
html body .stApp [data-testid="stButton"] > button,
html body .stApp [data-testid="stFormSubmitButton"] > button,
html body .stApp button[kind="primary"],
html body .stApp button[kind="primaryFormSubmit"],
html body .stApp button[data-testid="baseButton-primary"],
html body .stApp button[data-testid="stBaseButton-primary"] {
    width: 100% !important;
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border: 1px solid transparent !important;
    border-radius: 11px !important;
    padding: 7px 0 !important;
    min-height: 38px !important;
    height: 38px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    outline: none !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.30) !important;
    transition: background 0.15s ease, box-shadow 0.15s ease, transform 0.05s ease !important;
}

html body .stApp button *,
html body .stApp .stButton > button * {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    fill: #FFFFFF !important;
}

html body .stApp button:hover,
html body .stApp .stButton > button:hover {
    background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
    background-color: #1D4ED8 !important;
    box-shadow: 0 6px 18px rgba(37, 99, 235, 0.40) !important;
}

html body .stApp button:active { transform: translateY(1px) !important; }

html body .stApp button:focus,
html body .stApp button:focus-visible {
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.35) !important;
}

/* Secondary buttons (inactive tab) — subtle visible outline */
html body .stApp button[kind="secondary"],
html body .stApp button[data-testid="baseButton-secondary"],
html body .stApp button[data-testid="stBaseButton-secondary"] {
    background: rgba(255, 255, 255, 0.02) !important;
    background-color: rgba(255, 255, 255, 0.02) !important;
    color: #94A3B8 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03) !important;
}
html body .stApp button[kind="secondary"] *,
html body .stApp button[data-testid="baseButton-secondary"] *,
html body .stApp button[data-testid="stBaseButton-secondary"] * {
    color: #94A3B8 !important;
    fill: #94A3B8 !important;
}
html body .stApp button[kind="secondary"]:hover,
html body .stApp button[data-testid="baseButton-secondary"]:hover,
html body .stApp button[data-testid="stBaseButton-secondary"]:hover {
    background: rgba(148, 163, 184, 0.08) !important;
    background-color: rgba(148, 163, 184, 0.08) !important;
    color: #E2E8F0 !important;
    border-color: rgba(255, 255, 255, 0.18) !important;
    box-shadow: none !important;
}
html body .stApp button[kind="secondary"]:hover *,
html body .stApp button[data-testid="baseButton-secondary"]:hover *,
html body .stApp button[data-testid="stBaseButton-secondary"]:hover * {
    color: #E2E8F0 !important;
}

/* Password-eye toggle */
html body .stApp button[aria-label*="assword"] {
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    min-height: auto !important;
    height: auto !important;
    width: auto !important;
    padding: 0 6px !important;
    border: none !important;
}
html body .stApp button[aria-label*="assword"] svg {
    stroke: #64748B !important;
    fill: none !important;
}
html body .stApp button[aria-label*="assword"]:hover svg {
    stroke: #94A3B8 !important;
}

/* Tabs — compact, accessible (30px) */
div[data-testid="stMarkdownContainer"]:has(#auth-tabs-start)
    + div[data-testid="stHorizontalBlock"] {
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(148, 163, 184, 0.14);
    border-radius: 10px;
    padding: 3px !important;
    gap: 3px !important;
    margin-bottom: 6px;
}

div[data-testid="stMarkdownContainer"]:has(#auth-tabs-start)
    + div[data-testid="stHorizontalBlock"] [data-testid="column"] {
    padding: 0 !important;
}

div[data-testid="stMarkdownContainer"]:has(#auth-tabs-start)
    + div[data-testid="stHorizontalBlock"] button {
    min-height: 30px !important;
    height: 30px !important;
    padding: 5px 12px !important;
    font-size: 13px !important;
    border-radius: 8px !important;
}

div[data-testid="stMarkdownContainer"]:has(#auth-tabs-start)
    + div[data-testid="stHorizontalBlock"] button * {
    font-size: 13px !important;
}
</style>
"""

# Injected ONLY in Sign In mode. The base styles above are tuned tight so the
# longer registration form fits; the shorter Sign In form needs more breathing
# room so it doesn't look shrunken. These overrides never load in Create Account
# mode, so the registration layout is left exactly as-is.
SIGNIN_RELAX_STYLES = """
<style>

/* Card: narrower (login-proportioned) + generous padding + larger gaps.
   Narrowing stops the short 2-field form from looking like a wide empty box. */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
    max-width: 440px !important;
    padding: 40px 40px !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
    div[data-testid="stVerticalBlock"] {
    gap: 24px !important;
}

/* Logo + brand — full size */
.login-logo-icon {
    width: 72px !important; height: 72px !important;
    margin: 0 auto 16px auto !important;
}
.login-logo-icon img.login-logo-img { width: 72px !important; height: 72px !important; }
.login-logo-icon svg { width: 56px !important; height: 56px !important; }
.login-brand-name { font-size: 23px !important; }
.login-brand-subtitle { font-size: 12px !important; margin-top: 4px !important; }
.login-divider { margin: 20px 0 18px 0 !important; }

/* Headings */
.login-heading { font-size: 23px !important; }
.login-subheading {
    font-size: 13px !important; margin-top: 4px !important; margin-bottom: 16px !important;
}

/* Inputs — taller, roomier */
html body .stApp .stTextInput label,
html body .stApp .stTextInput label p,
html body .stApp .stTextInput [data-testid="stWidgetLabel"] p {
    font-size: 12px !important; margin-bottom: 7px !important;
}
html body .stApp .stTextInput div[data-baseweb="input"] { min-height: 50px !important; }
html body .stApp .stTextInput input {
    height: 50px !important; font-size: 15px !important;
    padding: 14px 12px 14px 40px !important;
}
/* Selectbox + answer match the roomier Sign In sizing */
html body .stApp .stSelectbox label,
html body .stApp .stSelectbox label p,
html body .stApp .stSelectbox [data-testid="stWidgetLabel"] p {
    font-size: 12px !important; margin-bottom: 7px !important;
}
html body .stApp .stSelectbox div[data-baseweb="select"] > div {
    min-height: 50px !important; height: 50px !important;
}

/* Sign In primary button — taller (only loads in Sign In mode) */
html body .stApp button[kind="primary"],
html body .stApp button[data-testid="baseButton-primary"],
html body .stApp button[data-testid="stBaseButton-primary"] {
    height: 52px !important; min-height: 52px !important; padding: 15px 0 !important;
}

/* Tabs — taller + more space below */
div[data-testid="stMarkdownContainer"]:has(#auth-tabs-start)
    + div[data-testid="stHorizontalBlock"] { margin-bottom: 20px !important; }
div[data-testid="stMarkdownContainer"]:has(#auth-tabs-start)
    + div[data-testid="stHorizontalBlock"] button {
    min-height: 40px !important; height: 40px !important;
}
</style>
"""


def inject_login_styles(mode: str = "Sign In") -> None:
    """Inject the login-page CSS. Idempotent within a single Streamlit run.

    In Sign In mode an extra relax-styles block is injected so the shorter
    form fills the viewport comfortably. It is NOT injected in Create Account
    mode, leaving the compact registration layout untouched.
    """
    st.markdown(LOGIN_STYLES, unsafe_allow_html=True)
    if mode == "Sign In":
        st.markdown(SIGNIN_RELAX_STYLES, unsafe_allow_html=True)

