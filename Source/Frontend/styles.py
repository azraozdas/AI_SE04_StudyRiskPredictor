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
    padding-top: 0.5rem !important;
    padding-bottom: 0.5rem !important;
    max-width: 100% !important;
    min-height: 0 !important;
}

/* Centre the card vertically inside the viewport */
[data-testid="stMain"] {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}


div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
    background: linear-gradient(180deg, rgba(30,41,59,0.97), rgba(15,23,42,0.97));
    border: 1px solid rgba(148, 163, 184, 0.14);
    border-radius: 20px;
    padding: 22px 34px 24px 34px !important;
    box-shadow: 0 24px 56px rgba(0, 0, 0, 0.50),
                inset 0 1px 0 rgba(255, 255, 255, 0.04);
    max-width: 460px;
    margin: 0 auto !important;
    max-height: calc(100vh - 24px);
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


.login-brand { text-align: center; margin-bottom: 0; }

/* Transparent wrapper — no blue square, no rectangular shadow */
.login-logo-icon {
    width: 72px;
    height: 72px;
    border: none !important;
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 12px auto;
    overflow: visible;
}

/* Fallback SVG (only used if assets/logo.png is missing) */
.login-logo-icon svg {
    width: 56px;
    height: 56px;
    filter: drop-shadow(0 6px 18px rgba(59, 130, 246, 0.35));
}

/* Custom PNG logo — soft glow that follows the logo's shape */
.login-logo-icon img.login-logo-img {
    width: 72px;
    height: 72px;
    object-fit: contain;
    display: block;
    background: transparent !important;
    border: none !important;
    border-radius: 16px !important;
    box-shadow: none !important;
    filter: drop-shadow(0 6px 18px rgba(59, 130, 246, 0.35))
            drop-shadow(0 2px 6px rgba(0, 0, 0, 0.35));
}

.login-brand-name {
    font-size: 21px; font-weight: 800; color: #F8FAFC;
    letter-spacing: -0.02em; line-height: 1.15;
}

.login-brand-subtitle {
    font-size: 12px; font-weight: 500; color: #64748B;
    margin-top: 3px;
}

.login-divider {
    border: none;
    border-top: 1px solid rgba(148,163,184,0.12);
    margin: 14px 0 12px 0;
}


.login-heading {
    font-size: 18px; font-weight: 700; color: #F8FAFC;
    letter-spacing: -0.01em; line-height: 1.2;
}
.login-subheading {
    font-size: 12px; font-weight: 400; color: #64748B;
    margin-top: 3px; margin-bottom: 12px;
}

/* =========================================================
   TEXT INPUTS
   ========================================================= */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
    .stTextInput { margin-bottom: 8px; }

div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
    .stTextInput label {
    font-size: 11px !important;
    font-weight: 600 !important;
    color: #CBD5E1 !important;
    margin-bottom: 3px !important;
    padding: 0 !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
    .stTextInput div[data-baseweb="input"] {
    background: rgba(15, 23, 42, 0.92) !important;
    border: 1px solid rgba(148, 163, 184, 0.16) !important;
    border-radius: 10px !important;
    min-height: 40px;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
    .stTextInput div[data-baseweb="input"]:focus-within {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.18) !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
    .stTextInput input {
    background: transparent !important;
    border: none !important;
    color: #F8FAFC !important;
    font-size: 14px !important;
    padding: 9px 12px 9px 38px !important;
    height: 40px !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
    .stTextInput input::placeholder { color: #475569 !important; }

/* Field icons (data URI, scoped by aria-label) */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
    .stTextInput:has(input[aria-label="Full Name"]) div[data-baseweb="input"] {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' fill='none' stroke='%2364748B' stroke-width='2' viewBox='0 0 24 24'%3E%3Cpath d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='12' cy='7' r='4'/%3E%3C/svg%3E");
    background-repeat: no-repeat; background-position: 11px center;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
    .stTextInput:has(input[aria-label="Email"]) div[data-baseweb="input"] {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' fill='none' stroke='%2364748B' stroke-width='2' viewBox='0 0 24 24'%3E%3Cpath d='M4 4h16v16H4z'/%3E%3Cpath d='m22 6-10 7L2 6'/%3E%3C/svg%3E");
    background-repeat: no-repeat; background-position: 11px center;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
    .stTextInput:has(input[aria-label="Password"]) div[data-baseweb="input"],
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
    .stTextInput:has(input[aria-label="Confirm Password"]) div[data-baseweb="input"] {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' fill='none' stroke='%2364748B' stroke-width='2' viewBox='0 0 24 24'%3E%3Crect x='3' y='11' width='18' height='11' rx='2'/%3E%3Cpath d='M7 11V7a5 5 0 0 1 10 0v4'/%3E%3C/svg%3E");
    background-repeat: no-repeat; background-position: 11px center;
}


.login-meta-row { margin: 0 0 8px 0; }

div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
    .stCheckbox { margin-bottom: 0 !important; }

div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
    .stCheckbox label p {
    font-size: 11px !important;
    color: #94A3B8 !important;
    font-weight: 500 !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
    .stCheckbox label span {
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
    border-radius: 8px; padding: 7px 12px;
    margin-bottom: 8px;
    display: flex; align-items: center; gap: 8px;
}


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
    padding: 10px 0 !important;
    min-height: 42px !important;
    height: 42px !important;
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

div[data-testid="stMarkdownContainer"]:has(#auth-tabs-start)
    + div[data-testid="stHorizontalBlock"] {
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(148, 163, 184, 0.14);
    border-radius: 10px;
    padding: 3px !important;
    gap: 3px !important;
    margin-bottom: 14px;
}

div[data-testid="stMarkdownContainer"]:has(#auth-tabs-start)
    + div[data-testid="stHorizontalBlock"] [data-testid="column"] {
    padding: 0 !important;
}

div[data-testid="stMarkdownContainer"]:has(#auth-tabs-start)
    + div[data-testid="stHorizontalBlock"] button {
    min-height: 34px !important;
    height: 34px !important;
    padding: 6px 12px !important;
    font-size: 13px !important;
    border-radius: 8px !important;
}

div[data-testid="stMarkdownContainer"]:has(#auth-tabs-start)
    + div[data-testid="stHorizontalBlock"] button * {
    font-size: 13px !important;
}
</style>
"""


def inject_login_styles() -> None:
    """Inject the login-page CSS. Idempotent within a single Streamlit run."""
    st.markdown(LOGIN_STYLES, unsafe_allow_html=True)