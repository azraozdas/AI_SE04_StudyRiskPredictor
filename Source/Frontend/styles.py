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
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
    min-height: 0 !important;
}

/* Centre auth card — tuned for 1920×1080 @ 125% Windows scaling (~864px CSS height) */
[data-testid="stMain"] > [data-testid="block-container"],
[data-testid="stMain"] .block-container {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    height: 100vh !important;
    max-height: 100vh !important;
    padding: 2px 0 !important;
    overflow: hidden !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(#studor-auth) {
    background: linear-gradient(180deg, rgba(30,41,59,0.97), rgba(15,23,42,0.97));
    border: 1px solid rgba(148, 163, 184, 0.14);
    border-radius: 20px;
    padding: 8px 24px 10px 24px !important;
    box-shadow: 0 24px 56px rgba(0, 0, 0, 0.50),
                inset 0 1px 0 rgba(255, 255, 255, 0.04);
    max-width: 460px;
    margin: 0 auto !important;
    overflow: visible !important;
    flex-shrink: 0 !important;
    /* ~20% internal compact scale: matches Chrome 80% density at 100% zoom, 125% Windows */
    zoom: 0.82;
}


.login-brand { text-align: center; margin-bottom: 0; }

/* Transparent wrapper — no blue square, no rectangular shadow */
.login-logo-icon {
    width: 44px;
    height: 44px;
    border: none !important;
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 4px auto;
    overflow: visible;
}

/* Fallback SVG (only used if assets/logo.png is missing) */
.login-logo-icon svg {
    width: 44px;
    height: 44px;
    filter: drop-shadow(0 6px 18px rgba(59, 130, 246, 0.35));
}

/* Custom PNG logo — soft glow that follows the logo's shape */
.login-logo-icon img.login-logo-img {
    width: 44px;
    height: 44px;
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
    font-size: 20px; font-weight: 800; color: #F8FAFC;
    letter-spacing: -0.02em; line-height: 1.1;
}

.login-brand-subtitle {
    font-size: 11px; font-weight: 500; color: #64748B;
    margin-top: 1px;
}

.login-divider {
    border: none;
    border-top: 1px solid rgba(148,163,184,0.12);
    margin: 4px 0 4px 0;
}

div[data-testid="column"]:has(#studor-auth) [data-testid="stMarkdownContainer"] {
    margin: 0 !important;
    padding: 0 !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stMarkdownContainer"] p {
    margin: 0 !important;
    padding: 0 !important;
}


.login-heading {
    font-size: 17px; font-weight: 700; color: #F8FAFC;
    letter-spacing: -0.01em; line-height: 1.1;
}
.login-subheading {
    font-size: 11px; font-weight: 400; color: #64748B;
    margin-top: 1px; margin-bottom: 3px;
}

/* =========================================================
   AUTH FORM — Streamlit 1.57+ (stTextInputRootElement, baseui)
   Scoped via #studor-auth + .auth-field markers in login.py
   ========================================================= */
div[data-testid="column"]:has(#studor-auth) {
    color-scheme: dark;
}

/* Compact vertical rhythm — no scroll on 1080p */
div[data-testid="column"]:has(#studor-auth) [data-testid="element-container"],
div[data-testid="column"]:has(#studor-auth) .element-container {
    margin: 0 !important;
    padding: 0 !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stVerticalBlock"],
div[data-testid="column"]:has(#studor-auth) [data-testid="stVerticalBlock"] > div,
div[data-testid="column"]:has(#studor-auth) [data-testid="stVerticalBlockBorderWrapper"] {
    gap: 0 !important;
    row-gap: 0 !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"],
div[data-testid="column"]:has(#studor-auth) [data-testid="stSelectbox"],
div[data-testid="column"]:has(#studor-auth) [data-testid="stCheckbox"] {
    margin: 0 !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stButton"] {
    margin: 2px 0 0 0 !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="element-container"] {
    margin: 0 !important;
    min-height: 0 !important;
}
div[data-testid="column"]:has(#studor-auth) .login-auth-root {
    margin: 0 !important;
    padding: 0 !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stLayoutWrapper"],
div[data-testid="column"]:has(#studor-auth) [data-testid="stAppViewBlockContainer"] {
    gap: 0 !important;
}

/* Labels */
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] label,
div[data-testid="column"]:has(#studor-auth) [data-testid="stSelectbox"] label,
div[data-testid="column"]:has(#studor-auth) [data-testid="stWidgetLabel"],
div[data-testid="column"]:has(#studor-auth) [data-testid="stWidgetLabel"] p,
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] label p,
div[data-testid="column"]:has(#studor-auth) [data-testid="stSelectbox"] label p {
    font-size: 11px !important;
    font-weight: 600 !important;
    color: #BFDBFE !important;
    margin-bottom: 4px !important;
    padding: 0 !important;
    letter-spacing: 0.02em !important;
    line-height: 1.2 !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stWidgetLabel"] {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
    min-height: 0 !important;
}

div[data-testid="column"]:has(#studor-auth) .signup-section-label {
    font-size: 10px !important;
    font-weight: 600 !important;
    color: #BFDBFE !important;
    margin: 1px 0 2px 0 !important;
    line-height: 1.2 !important;
}

/* Text input shells — Streamlit 1.57 Root + legacy baseweb */
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInputRootElement"],
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] div[data-baseweb="input"],
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] div[data-baseweb="base-input"] {
    background-color: #0B1220 !important;
    background-image: linear-gradient(180deg, #111827 0%, #0B1220 100%) !important;
    border-width: 1px !important;
    border-style: solid !important;
    border-color: rgba(96, 165, 250, 0.28) !important;
    border-radius: 10px !important;
    min-height: 34px !important;
    height: 34px !important;
    position: relative !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04) !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
}

div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInputRootElement"]:focus-within,
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.24),
                inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
}

div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] input,
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] input[type="text"],
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] input[type="password"] {
    background: transparent !important;
    background-color: transparent !important;
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
    caret-color: #F8FAFC !important;
    font-size: 13px !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-right: 36px !important;
    padding-left: 0 !important;
    min-height: 34px !important;
    height: 34px !important;
    line-height: 34px !important;
    border: none !important;
    box-shadow: none !important;
}

div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] input::placeholder {
    color: #8AA0BD !important;
    opacity: 1 !important;
}

div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] input:-webkit-autofill,
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] input:-webkit-autofill:focus {
    -webkit-box-shadow: 0 0 0 1000px #0B1220 inset !important;
    -webkit-text-fill-color: #F8FAFC !important;
    caret-color: #F8FAFC !important;
}

/* Selectbox — dark field (shield icon via ::after on security-question widget) */
div[data-testid="column"]:has(#studor-auth) [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #0B1220 !important;
    background-image: linear-gradient(180deg, #111827 0%, #0B1220 100%) !important;
    border: 1px solid rgba(96, 165, 250, 0.28) !important;
    border-radius: 10px !important;
    min-height: 34px !important;
    height: 34px !important;
    position: relative !important;
    padding-left: 36px !important;
    padding-right: 28px !important;
    color: #F8FAFC !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04) !important;
    display: flex !important;
    align-items: center !important;
}
/* Security question — left shield (::before on select trigger; keyed widget class) */
div[data-testid="column"]:has(#studor-auth) .st-key-signup_sec_question [data-testid="stSelectbox"] div[data-baseweb="select"] > div::before,
div[data-testid="column"]:has(#studor-auth) [data-testid="element-container"].st-key-signup_sec_question [data-testid="stSelectbox"] div[data-baseweb="select"] > div::before,
div[data-testid="column"]:has(#studor-auth) .st-key-signup_sec_question div[role="combobox"]::before {
    content: "" !important;
    display: block !important;
    position: absolute !important;
    left: 11px !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    width: 16px !important;
    height: 16px !important;
    background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='none' stroke='%2360A5FA' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' viewBox='0 0 24 24'%3E%3Cpath d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/%3E%3C/svg%3E") center / 16px 16px no-repeat !important;
    pointer-events: none !important;
    z-index: 3 !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.24) !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stSelectbox"] div[data-baseweb="select"] span,
div[data-testid="column"]:has(#studor-auth) [data-testid="stSelectbox"] div[data-baseweb="select"] div[value] {
    color: #F8FAFC !important;
    font-size: 13px !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stSelectbox"] div[data-baseweb="select"] svg {
    fill: #93C5FD !important;
    color: #93C5FD !important;
}

/* Native Streamlit Material icons (icon= parameter) — must stay visible */
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] [data-testid="stIconMaterial"],
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] span[data-testid="stIconMaterial"],
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInputRootElement"] [data-testid="stIconMaterial"] {
    display: inline-flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    color: #60A5FA !important;
    flex-shrink: 0 !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] [data-testid="stIconMaterial"] svg {
    color: #60A5FA !important;
    fill: #60A5FA !important;
    width: 17px !important;
    height: 17px !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInputRootElement"] {
    display: flex !important;
    align-items: center !important;
    gap: 0 !important;
}

/* Max specificity — beat Emotion inline styles */
html body .stApp div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInputRootElement"],
html body .stApp div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] div[data-baseweb="input"] {
    background-color: #0B1220 !important;
    border-color: rgba(96, 165, 250, 0.28) !important;
}
html body .stApp div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] input {
    background-color: transparent !important;
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
}
html body .stApp div[data-testid="column"]:has(#studor-auth) [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #0B1220 !important;
    background-image: linear-gradient(180deg, #111827 0%, #0B1220 100%) !important;
    color: #F8FAFC !important;
}
html body .stApp div[data-testid="column"]:has(#studor-auth) .st-key-signup_sec_question [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    padding-left: 36px !important;
}
html body .stApp div[data-testid="column"]:has(#studor-auth) .st-key-signup_sec_question [data-testid="stSelectbox"] div[data-baseweb="select"] > div::before,
html body .stApp div[data-testid="column"]:has(#studor-auth) [data-testid="element-container"].st-key-signup_sec_question [data-testid="stSelectbox"] div[data-baseweb="select"] > div::before,
html body .stApp div[data-testid="column"]:has(#studor-auth) .st-key-signup_sec_question div[role="combobox"]::before {
    content: "" !important;
    display: block !important;
    position: absolute !important;
    left: 11px !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    width: 16px !important;
    height: 16px !important;
    background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='none' stroke='%2360A5FA' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' viewBox='0 0 24 24'%3E%3Cpath d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/%3E%3C/svg%3E") center / 16px 16px no-repeat !important;
    pointer-events: none !important;
    z-index: 3 !important;
}

.login-meta-row { margin: 0 0 8px 0; }

/* Remember me checkbox */
div[data-testid="column"]:has(#studor-auth) [data-testid="stCheckbox"] {
    margin-bottom: 0 !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stCheckbox"] label p,
div[data-testid="column"]:has(#studor-auth) [data-testid="stCheckbox"] [data-testid="stMarkdownContainer"] p {
    font-size: 11px !important;
    color: #94A3B8 !important;
    font-weight: 500 !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stCheckbox"] [data-baseweb="checkbox"] {
    background: transparent !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stCheckbox"] [data-baseweb="checkbox"] > div:first-child {
    width: 16px !important;
    height: 16px !important;
    min-width: 16px !important;
    background-color: #0B1220 !important;
    border-left-color: rgba(96, 165, 250, 0.4) !important;
    border-right-color: rgba(96, 165, 250, 0.4) !important;
    border-top-color: rgba(96, 165, 250, 0.4) !important;
    border-bottom-color: rgba(96, 165, 250, 0.4) !important;
    border-radius: 4px !important;
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.3) !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stCheckbox"] [aria-checked="true"] > div:first-child {
    background-color: #2563EB !important;
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.28) !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stCheckbox"] [aria-checked="true"] svg {
    fill: #FFFFFF !important;
}
html body .stApp div[data-testid="column"]:has(#studor-auth) [data-testid="stCheckbox"] [data-baseweb="checkbox"] > div:first-child {
    background-color: #0B1220 !important;
}
html body .stApp div[data-testid="column"]:has(#studor-auth) [data-testid="stCheckbox"] [aria-checked="true"] > div:first-child {
    background-color: #2563EB !important;
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
    font-size: 11px; font-weight: 600;
    border-radius: 8px; padding: 5px 10px;
    margin-bottom: 4px;
    display: flex; align-items: center; gap: 6px;
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

/* Password-eye toggle (auth + global) */
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] button {
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    border: none !important;
    min-height: auto !important;
    height: auto !important;
    width: auto !important;
    padding: 0 8px !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] button svg {
    stroke: #64748B !important;
    fill: none !important;
}
div[data-testid="column"]:has(#studor-auth) [data-testid="stTextInput"] button:hover svg {
    stroke: #93C5FD !important;
}

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
    margin-bottom: 6px;
}

div[data-testid="column"]:has(#studor-auth) [data-testid="stHorizontalBlock"]:has(.st-key-tab_signin) {
    margin-bottom: 4px !important;
    padding: 2px !important;
    gap: 4px !important;
}

div[data-testid="stMarkdownContainer"]:has(#auth-tabs-start)
    + div[data-testid="stHorizontalBlock"] [data-testid="column"] {
    padding: 0 !important;
}

div[data-testid="column"]:has(#studor-auth) [data-testid="stHorizontalBlock"] {
    gap: 6px !important;
}

div[data-testid="stMarkdownContainer"]:has(#auth-tabs-start)
    + div[data-testid="stHorizontalBlock"] button,
div[data-testid="column"]:has(#studor-auth) [data-testid="stHorizontalBlock"]:has(.st-key-tab_signin) button,
div[data-testid="column"]:has(#studor-auth) [data-testid="stHorizontalBlock"]:has(.st-key-tab_signin) [data-testid="stButton"] > button {
    min-height: 34px !important;
    height: 34px !important;
    padding: 4px 8px !important;
    font-size: 12px !important;
    border-radius: 8px !important;
}

div[data-testid="stMarkdownContainer"]:has(#auth-tabs-start)
    + div[data-testid="stHorizontalBlock"] button * {
    font-size: 13px !important;
}

/* Auth submit / action buttons — override global 42px (must follow global button rules) */
html body .stApp div[data-testid="column"]:has(#studor-auth) [data-testid="stButton"] > button {
    min-height: 36px !important;
    height: 36px !important;
    padding: 6px 0 !important;
    font-size: 13px !important;
}
html body .stApp div[data-testid="column"]:has(#studor-auth) [data-testid="stHorizontalBlock"]:has(.st-key-tab_signin) [data-testid="stButton"] > button {
    min-height: 34px !important;
    height: 34px !important;
    padding: 4px 8px !important;
    font-size: 12px !important;
}
html body .stApp div[data-testid="column"]:has(#studor-auth) [data-testid="stButton"] > button * {
    font-size: 13px !important;
}
</style>
"""

# Create Account — 1920×1080 @ 125% Windows scaling (~864px CSS viewport, no scroll)
AUTH_CREATE_ACCOUNT_COMPACT = """
<style>
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) {
    padding: 3px 20px 5px 20px !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) .login-logo-icon,
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) .login-logo-icon img.login-logo-img,
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) .login-logo-icon svg {
    width: 40px !important;
    height: 40px !important;
    margin-bottom: 0 !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) .login-brand-name {
    font-size: 17px !important;
    line-height: 1.05 !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) .login-brand-subtitle {
    font-size: 11px !important;
    margin-top: 0 !important;
    line-height: 1.15 !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) .login-divider {
    margin: 2px 0 !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stHorizontalBlock"]:has(.st-key-tab_signin) {
    margin-bottom: 2px !important;
    padding: 2px !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) .login-heading {
    font-size: 15px !important;
    line-height: 1.1 !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) .login-subheading {
    font-size: 11px !important;
    margin-bottom: 0 !important;
    line-height: 1.15 !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stTextInput"] label p,
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stSelectbox"] label p,
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stWidgetLabel"] p {
    font-size: 11px !important;
    margin-bottom: 3px !important;
    line-height: 1.15 !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stTextInput"],
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stSelectbox"] {
    margin-bottom: 6px !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stHorizontalBlock"]:has(.st-key-tab_signin) [data-testid="stButton"] > button {
    min-height: 32px !important;
    height: 32px !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) .st-key-signup_sec_answer {
    margin-bottom: 4px !important;
}
html body .stApp div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) .st-key-signup_submit [data-testid="stButton"] > button {
    min-height: 36px !important;
    height: 36px !important;
    padding: 5px 0 !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stTextInput"],
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stSelectbox"],
div[data-testid="column"]:has(#studor-auth[data-auth-mode="create-account"]) [data-testid="stButton"] {
    min-height: 0 !important;
}
</style>
"""

# Sign In — balanced but fits the same 125% scaled viewport
AUTH_SIGNIN_125_STYLES = """
<style>
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(#studor-auth[data-auth-mode="sign-in"]) {
    padding: 8px 26px 10px 26px !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="sign-in"]) .login-logo-icon,
div[data-testid="column"]:has(#studor-auth[data-auth-mode="sign-in"]) .login-logo-icon img.login-logo-img,
div[data-testid="column"]:has(#studor-auth[data-auth-mode="sign-in"]) .login-logo-icon svg {
    width: 36px !important;
    height: 36px !important;
    margin-bottom: 2px !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="sign-in"]) .login-brand-name {
    font-size: 18px !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="sign-in"]) .login-divider {
    margin: 3px 0 !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="sign-in"]) [data-testid="stHorizontalBlock"]:has(.st-key-tab_signin) {
    margin-bottom: 4px !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="sign-in"]) .login-subheading {
    margin-bottom: 4px !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="sign-in"]) [data-testid="stTextInput"] {
    margin-bottom: 8px !important;
}
div[data-testid="column"]:has(#studor-auth[data-auth-mode="sign-in"]) [data-testid="stCheckbox"] {
    margin-bottom: 2px !important;
}
html body .stApp div[data-testid="column"]:has(#studor-auth[data-auth-mode="sign-in"]) .st-key-login_submit [data-testid="stButton"] > button {
    min-height: 36px !important;
    height: 36px !important;
}
</style>
"""

# Viewport fit helper — card zoom 0.82 is on the column in LOGIN_STYLES
AUTH_VIEWPORT_SHORT = """
<style>
@media (max-height: 920px) {
    [data-testid="stMain"] .block-container {
        padding: 0 !important;
        align-items: center !important;
    }
}
</style>
"""


def inject_login_styles(mode: str = "Sign In") -> None:
    """Inject login CSS sized for 1920×1080 @ 125% Windows display scaling."""
    import re

    extra = (
        AUTH_CREATE_ACCOUNT_COMPACT
        if mode == "Create Account"
        else AUTH_SIGNIN_125_STYLES
    )
    bundle = LOGIN_STYLES + AUTH_VIEWPORT_SHORT + extra
    clean = re.sub(r"\n[ \t]*\n", "\n", bundle)
    st.markdown(clean, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Main application design system
# ---------------------------------------------------------------------------

APP_STYLES = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
/* ── Global font ─────────────────────────────────────────────────────────── */
html, body, [class*="css"], * {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}

/* ── Hide Streamlit chrome ───────────────────────────────────────────────── */
#MainMenu { visibility: hidden; }
header[data-testid="stHeader"] { display: none !important; }
.stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { visibility: hidden; }
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarHeader"],
section[data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    width: 0 !important;
    overflow: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
    font-size: 0 !important;
    line-height: 0 !important;
}

/* Reopen control if the sidebar is collapsed */
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
}

/* ── App canvas ──────────────────────────────────────────────────────────── */
html, body, .stApp, [data-testid="stAppViewContainer"] {
    background: #0F172A !important;
    color: #CBD5E1 !important;
    color-scheme: dark !important;
    --primary-color: #3B82F6 !important;
    --primary-color-rgb: 59, 130, 246 !important;
}

/* ── Block container (balanced viewport fit @ 100% zoom) ─────────────────── */
.block-container {
    padding-top: 0.55rem !important;
    padding-bottom: 0.55rem !important;
    padding-left: 1.35rem !important;
    padding-right: 1.35rem !important;
    max-width: 100% !important;
}

/* Main content vertical rhythm only — sidebar untouched */
[data-testid="stMain"] [data-testid="stVerticalBlock"] {
    gap: 0.5rem !important;
}
[data-testid="stMain"] [data-testid="stHorizontalBlock"] {
    gap: 0.5rem !important;
}
[data-testid="stMain"] .element-container {
    margin-bottom: 0.25rem !important;
}
/* Section titles must sit clearly above their cards (Streamlit widget gap) */
[data-testid="stMain"] .element-container:has(.section-h2) {
    margin-bottom: 10px !important;
}
[data-testid="stMain"] .element-container:has(.page-h1) {
    margin-bottom: 2px !important;
}
[data-testid="stMain"] .element-container:has(.page-sub) {
    margin-bottom: 12px !important;
}
[data-testid="stMain"] [data-testid="column"] > div {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}
[data-testid="stMain"] [data-testid="stSlider"] {
    padding-top: 0.15rem !important;
    padding-bottom: 0.15rem !important;
}
[data-testid="stMain"] [data-testid="stSelectbox"],
[data-testid="stMain"] [data-testid="stTextInput"],
[data-testid="stMain"] [data-testid="stNumberInput"] {
    margin-bottom: 0.15rem !important;
}
[data-testid="stMain"] .stButton {
    margin-bottom: 0.05rem !important;
}

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    width: 21rem !important;
    min-width: 21rem !important;
    max-width: 21rem !important;
    flex-shrink: 0 !important;
    background: #111827 !important;
    border-right: 1px solid #1E293B !important;
    transform: none !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .element-container {
    padding: 0 !important;
    margin: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    text-align: left !important;
}

/* ── Column gaps ─────────────────────────────────────────────────────────── */
[data-testid="column"] {
    padding-left: 6px !important;
    padding-right: 6px !important;
}

/* ── Sidebar nav components ──────────────────────────────────────────────── */
.sb-wrap { display: flex; flex-direction: column; width: 100%; }

.sb-brand {
    display: flex; align-items: center; gap: 13px;
    padding: 22px 20px 18px 20px;
    border-bottom: 1px solid #1E293B;
    margin-bottom: 8px;
}
.sb-logo {
    width: 42px; height: 42px; border-radius: 12px; flex-shrink: 0;
    background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
    box-shadow: 0 4px 14px rgba(59,130,246,0.35);
    display: flex; align-items: center; justify-content: center;
    overflow: hidden;
}
.sb-logo svg { width: 22px; height: 22px; display: block; }
.sb-logo.sb-logo--custom {
    background: transparent;
    box-shadow: none;
}
.sb-logo img.sb-logo-img {
    width: 42px;
    height: 42px;
    object-fit: contain;
    display: block;
    border-radius: 12px;
    filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.35));
}
.sb-brand-name {
    font-size: 17px; font-weight: 800; color: #F8FAFC; letter-spacing: -0.02em;
}
.sb-brand-sub {
    font-size: 10.5px; font-weight: 500; color: #4B5563; margin-top: 2px;
}

.sb-section-label {
    padding: 6px 20px 8px 20px;
    font-size: 10px; font-weight: 700; color: #374151;
    text-transform: uppercase; letter-spacing: 0.14em;
}

.sb-nav-list {
    display: flex; flex-direction: column; align-items: stretch;
    gap: 2px; padding: 0 8px; width: 100%; box-sizing: border-box;
}

.sb-nav-item {
    display: flex; align-items: center; justify-content: flex-start;
    gap: 10px; width: 100%; min-height: 42px;
    padding: 10px 12px 10px 14px;
    border-radius: 10px; border-left: 3px solid transparent;
    font-size: 14px; font-weight: 600; line-height: 1.3; letter-spacing: 0.01em;
    box-sizing: border-box; user-select: none; text-align: left;
    transition: background 0.15s ease, color 0.15s ease, border-left-color 0.15s ease;
    text-decoration: none;
}
.sb-nav-icon {
    width: 18px; height: 18px; min-width: 18px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; color: #64748B;
}
.sb-nav-icon svg {
    width: 16px; height: 16px; display: block;
    stroke: currentColor;
}
.sb-nav-label {
    flex: 1; min-width: 0; text-align: left;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

.sb-nav-item--inactive { color: #94A3B8; background: transparent; cursor: pointer; }
.sb-nav-item--inactive .sb-nav-icon { color: #64748B; }
.sb-nav-item--inactive:hover {
    background: rgba(255,255,255,0.035); color: #CBD5E1;
    border-left-color: #2D3748;
}
.sb-nav-item--inactive:hover .sb-nav-icon { color: #94A3B8; }

.sb-nav-item--active {
    background: linear-gradient(90deg, rgba(59,130,246,0.18) 0%, rgba(59,130,246,0.06) 100%);
    border-left-color: #3B82F6; color: #F1F5F9; font-weight: 700;
    cursor: default; box-shadow: 0 0 0 1px rgba(59,130,246,0.1);
}
.sb-nav-item--active .sb-nav-icon { color: #60A5FA; }

a.sb-nav-item,
a.sb-nav-item:link,
a.sb-nav-item:visited {
    text-decoration: none !important;
    color: inherit;
}
a.sb-nav-item--inactive,
a.sb-nav-item--inactive:link,
a.sb-nav-item--inactive:visited {
    color: #94A3B8 !important;
}

.sb-logout {
    margin: 6px 8px 12px 8px;
}

.sb-divider { margin: 12px 8px 10px; border: none; border-top: 1px solid #1E293B; }

.sb-profile {
    margin: 0 8px 14px; padding: 10px 12px; background: #161F2E;
    border: 1px solid #1E2D40; border-radius: 10px; cursor: pointer;
    transition: background 0.15s ease, border-color 0.15s ease;
    display: flex; align-items: center; gap: 10px; text-decoration: none;
}
.sb-profile:hover { background: #1A2640; border-color: #3B4B63; }
a.sb-profile,
a.sb-profile:link,
a.sb-profile:visited {
    text-decoration: none !important;
    color: inherit;
}
.sb-profile--active {
    border-color: #3B82F6; background: rgba(59,130,246,0.08);
    box-shadow: 0 0 0 1px rgba(59,130,246,0.1); cursor: default;
}
.sb-avatar {
    width: 34px; height: 34px; border-radius: 50%; flex-shrink: 0;
    background: linear-gradient(135deg, #3B82F6 0%, #7C3AED 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 800; color: white;
}
.sb-profile-name { font-size: 13px; font-weight: 700; color: #F8FAFC; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sb-profile-meta { font-size: 11px; font-weight: 500; color: #64748B; }
.sb-profile--active .sb-profile-meta { color: #3B82F6; }

/* ── Cards ───────────────────────────────────────────────────────────────── */
.card {
    background: #1E293B; border: 1px solid #334155;
    border-radius: 14px; padding: 13px 15px;
}
.card.chart-card {
    padding: 12px 14px 10px 14px;
    overflow: visible;
}

/* Scroll panels — viewport-aware, not over-compressed */
.list-panel {
    max-height: clamp(108px, 27vh, 168px);
    overflow-y: auto;
    overflow-x: hidden;
}
.list-panel--tall { max-height: clamp(118px, 31vh, 188px); }
.list-panel--short { max-height: clamp(96px, 23vh, 145px); }
.list-panel--schedule { max-height: clamp(72px, 12vh, 96px); }
.list-panel--rec { max-height: clamp(108px, 30vh, 210px); }
.page-scroll-panel {
    max-height: clamp(200px, calc(100vh - 220px), 420px);
    overflow-y: auto;
    overflow-x: hidden;
}
.courses-scroll-panel {
    max-height: clamp(180px, calc(100vh - 260px), 380px);
    overflow-y: auto;
    overflow-x: hidden;
}
.list-panel::-webkit-scrollbar,
.courses-scroll-panel::-webkit-scrollbar {
    width: 4px;
}
.list-panel::-webkit-scrollbar-thumb,
.courses-scroll-panel::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 2px;
}
.card-accent-high  { border-left: 3px solid #DC2626; }
.card-accent-mid   { border-left: 3px solid #F59E0B; }
.card-accent-low   { border-left: 3px solid #22C55E; }
.card-accent-blue  { border-left: 3px solid #3B82F6; }

/* ── KPI tile ─────────────────────────────────────────────────────────────── */
.kpi-tile {
    background: #1E293B; border: 1px solid #334155; border-radius: 14px;
    padding: 12px 14px;
}
.kpi-label {
    font-size: 10px; font-weight: 700; color: #64748B;
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;
    display: flex; align-items: center; gap: 8px;
}
.kpi-icon {
    width: 28px; height: 28px; border-radius: 8px;
    display: inline-flex; align-items: center; justify-content: center;
}
.kpi-icon svg { width: 14px; height: 14px; display: block; }
.kpi-value { font-size: 34px; font-weight: 800; color: #F8FAFC; line-height: 1.1; }
.kpi-sub   { font-size: 12px; font-weight: 500; color: #64748B; margin-top: 4px; }

/* ── Risk badges ─────────────────────────────────────────────────────────── */
.badge {
    display: inline-block; padding: 3px 10px;
    border-radius: 6px; font-size: 11px; font-weight: 700;
}
.badge-high   { background: #7F1D1D; color: #FCA5A5; }
.badge-medium { background: #78350F; color: #FCD34D; }
.badge-low    { background: #14532D; color: #86EFAC; }
.badge-blue   { background: #1E3A5F; color: #93C5FD; }

/* ── Deadline pill ───────────────────────────────────────────────────────── */
.pill {
    display: inline-block; padding: 3px 8px;
    border-radius: 5px; font-size: 10px; font-weight: 700;
}
.pill-red    { background: #7F1D1D; color: #FCA5A5; }
.pill-amber  { background: #78350F; color: #FCD34D; }
.pill-blue   { background: #1E3A5F; color: #93C5FD; }

/* ── Risk level display ──────────────────────────────────────────────────── */
.risk-display {
    font-size: 46px; font-weight: 900; letter-spacing: -0.02em;
    text-align: center; padding: 14px 0 10px;
}
.risk-display-high   { color: #DC2626; }
.risk-display-medium { color: #F59E0B; }
.risk-display-low    { color: #22C55E; }

/* ── Page headings ───────────────────────────────────────────────────────── */
.page-h1 {
    font-size: 28px; font-weight: 800; color: #F8FAFC;
    letter-spacing: -0.02em; line-height: 1.2; margin: 0 0 4px 0;
}
.page-sub {
    font-size: 14px; font-weight: 400; color: #64748B;
    margin-bottom: 10px; line-height: 1.4;
}

/* ── Section headings ────────────────────────────────────────────────────── */
.section-h2 {
    font-size: 16px; font-weight: 700; color: #F8FAFC;
    margin: 0 0 10px 0;
    padding: 0;
    display: block;
    line-height: 1.35;
}
/* Second section in same column (e.g. Deadlines below chart) */
.section-h2--follow {
    margin-top: 14px !important;
    margin-bottom: 10px !important;
}
.section-spacer {
    display: block;
    height: 8px;
    margin: 0;
    padding: 0;
}

/* ── Health score banner ─────────────────────────────────────────────────── */
.health-banner {
    background: linear-gradient(135deg, #1a2f52 0%, #1E293B 100%);
    border: 1px solid #2D4166; border-radius: 18px; padding: 12px 16px;
    display: flex; align-items: center; gap: 14px; flex-wrap: wrap;
    margin-bottom: 12px;
}
.health-gauge {
    width: 58px; height: 58px; border-radius: 50%; flex-shrink: 0;
    background: conic-gradient(#3B82F6 var(--pct, 76%), #273449 0%);
    display: flex; align-items: center; justify-content: center;
    position: relative;
}
.health-gauge::after {
    content: ''; position: absolute;
    width: 44px; height: 44px; border-radius: 50%; background: #1a2f52;
}
.health-score-num {
    position: relative; z-index: 1;
    font-size: 20px; font-weight: 800; color: #F8FAFC;
}
.health-title {
    font-size: 18px; font-weight: 700; color: #F8FAFC; margin-bottom: 4px; line-height: 1.25;
}
.health-desc { font-size: 13px; color: #64748B; line-height: 1.35; }
.health-stats { display: flex; gap: 16px; flex-wrap: wrap; margin-left: auto; flex-shrink: 0; }
.health-stat-val { font-size: 22px; font-weight: 800; color: #F8FAFC; line-height: 1; }
.health-stat-lbl { font-size: 11px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.06em; }

/* ── st.metric override ──────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 14px !important;
    padding: 11px 13px !important;
}
[data-testid="stMetricLabel"] {
    font-size: 11px !important; font-weight: 700 !important;
    color: #94A3B8 !important; text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
[data-testid="stMetricValue"] {
    font-size: 28px !important; font-weight: 800 !important; color: #F8FAFC !important;
}
[data-testid="stMetricDelta"] { font-size: 12px !important; font-weight: 500 !important; }

/* ── Inputs ──────────────────────────────────────────────────────────────── */
.stTextInput div[data-baseweb="input"],
.stNumberInput div[data-baseweb="input"] {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
}
.stTextInput input, .stNumberInput input, .stTextArea textarea {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    color: #F1F5F9 !important;
    font-size: 14px !important;
}
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15) !important;
    outline: none !important;
}
.stTextInput label, .stNumberInput label, .stTextArea label,
.stSelectbox label, .stSlider label {
    color: #CBD5E1 !important; font-size: 13px !important; font-weight: 600 !important;
}
div[data-baseweb="select"] > div {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    color: #F1F5F9 !important;
}
div[data-baseweb="select"] span { color: #F1F5F9 !important; }
div[data-baseweb="popover"] > div { background: #1E293B !important; border: 1px solid #334155 !important; border-radius: 10px !important; }
li[role="option"] { color: #CBD5E1 !important; }
li[role="option"]:hover { background: #273449 !important; }

/* Date input — match selectbox (dark field) */
[data-testid="stDateInput"] label {
    color: #CBD5E1 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    margin-bottom: 2px !important;
    padding-bottom: 0 !important;
    min-height: 18px !important;
    line-height: 1.25 !important;
}
[data-testid="stDateInput"] div[data-baseweb="input"] {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    min-height: 38px !important;
}
[data-testid="stDateInput"] input {
    background: transparent !important;
    color: #F1F5F9 !important;
    font-size: 14px !important;
}
[data-testid="stDateInput"] div[data-baseweb="input"]:focus-within {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15) !important;
}
[data-testid="stDateInput"] svg { fill: #94A3B8 !important; }
div[data-baseweb="calendar"] {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    color: #F1F5F9 !important;
}
div[data-baseweb="calendar"] button { color: #CBD5E1 !important; }
div[data-baseweb="calendar"] [aria-selected="true"] {
    background: #2563EB !important;
    color: #F8FAFC !important;
}

/* ── Sliders — thin track only (no container/block backgrounds) ─────────── */
[data-testid="stSlider"],
[data-testid="stSlider"] > div,
[data-testid="stSlider"] [data-baseweb="slider"],
[data-testid="stSlider"] [data-baseweb="slider"] > div {
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
}
[data-testid="stSlider"] [data-testid="stSliderThumbValue"],
[data-testid="stSlider"] [data-testid="stSliderThumbValue"] > div {
    background: transparent !important;
    background-color: transparent !important;
    color: #CBD5E1 !important;
}
[data-testid="stSlider"] [data-testid="stSliderTickBar"] {
    background: transparent !important;
    padding: 0 !important;
    min-height: 0 !important;
}
/*
 * Active fill = InnerTrack linear-gradient (theme primaryColor).
 * CSS background-color cannot override inline gradient; use .streamlit/config.toml
 * primaryColor = "#3B82F6". Inactive rail uses theme borderOpaque/backgroundSecondary (#334155).
 */
[data-testid="stSlider"] [data-testid="stSliderTickBar"] > div {
    height: 4px !important;
    min-height: 4px !important;
    max-height: 4px !important;
    border-radius: 4px !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background-color: #2563EB !important;
    border: 2px solid #93C5FD !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.22) !important;
}
[data-testid="stSliderTickBarMin"],
[data-testid="stSliderTickBarMax"] {
    color: #64748B !important;
    background: transparent !important;
}

/* ── Buttons ─────────────────────────────────────────────────────────────── */
.stButton > button {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    color: #CBD5E1 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    transition: background 0.15s ease !important;
}
.stButton > button:hover { background: #273449 !important; color: #F1F5F9 !important; }

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
    box-shadow: 0 6px 20px rgba(37,99,235,0.45) !important;
}
.stButton > button * { color: inherit !important; }

/* ── Tabs ────────────────────────────────────────────────────────────────── */
[data-testid="stTabs"] > div:first-child {
    background: #1E293B; border: 1px solid #334155;
    border-radius: 12px; padding: 4px; gap: 2px;
}
button[data-baseweb="tab"] {
    background: transparent !important; border-radius: 9px !important;
    color: #64748B !important; font-weight: 600 !important; font-size: 13px !important;
    border: none !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: #273449 !important; color: #F1F5F9 !important; font-weight: 700 !important;
}
[data-testid="stTabContent"] { padding-top: 6px !important; }

/* ── Progress bars ───────────────────────────────────────────────────────── */
[data-testid="stProgressBar"] > div { background: #273449 !important; border-radius: 4px !important; }
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #3B82F6, #6366F1) !important; border-radius: 4px !important;
}

/* ── Material icons (global Inter reset breaks expander chevrons → "arrow_down" text) */
[data-testid="stIconMaterial"],
[data-testid="stIconMaterial"] span,
[data-testid="stExpander"] summary [data-testid="stIconMaterial"],
[data-testid="stExpander"] summary span[data-testid="stIconMaterial"] {
    font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
    font-variation-settings: "FILL" 0, "wght" 400, "GRAD" 0, "opsz" 24 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
}

/* ── Expanders ───────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #1E293B !important; border: 1px solid #334155 !important; border-radius: 10px !important;
}
[data-testid="stExpander"] summary {
    color: #CBD5E1 !important;
    font-weight: 600 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}

/* My Courses — add form section title */
.mc-add-label,
.section-label {
    font-size: 15px !important;
    font-weight: 700 !important;
    color: #CBD5E1 !important;
    margin: 0 0 10px 0 !important;
    padding: 0 !important;
}
[data-testid="stMain"] .element-container:has(.mc-add-label) {
    margin-bottom: 0 !important;
}

/* ── Alerts ──────────────────────────────────────────────────────────────── */
[data-testid="stAlert"] { border-radius: 10px !important; border-left-width: 4px !important; }

/* ── Dataframe / Glide data grid (dark theme) ─────────────────────────────── */
[data-testid="stDataFrame"],
[data-testid="stDataFrame"] > div,
[data-testid="stDataFrame"] iframe,
div[data-testid="stDataFrameGlideDataEditor"],
.gdg-wmyidgi,
.dvn-scroller {
    --gdg-bg-cell: #1E293B !important;
    --gdg-bg-cell-medium: #273449 !important;
    --gdg-bg-header: #273449 !important;
    --gdg-bg-header-has-focus: #334155 !important;
    --gdg-bg-header-hovered: #334155 !important;
    --gdg-text-dark: #F8FAFC !important;
    --gdg-text-medium: #94A3B8 !important;
    --gdg-text-light: #64748B !important;
    --gdg-text-bubble: #F8FAFC !important;
    --gdg-border-color: #334155 !important;
    --gdg-horizontal-border-color: #334155 !important;
    --gdg-accent-color: #3B82F6 !important;
    --gdg-accent-fg: #F8FAFC !important;
    --gdg-accent-light: rgba(59, 130, 246, 0.15) !important;
    --gdg-bg-icon-header: #64748B !important;
    --gdg-fg-icon-header: #F8FAFC !important;
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    color: #F8FAFC !important;
}

/* ── Scrollbar ───────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #475569; }

/* ── Plotly charts transparent ───────────────────────────────────────────── */
.main-svg { background: transparent !important; }
.js-plotly-plot .plotly { background: transparent !important; }

/* ── Dividers ────────────────────────────────────────────────────────────── */
hr { border-color: #1E293B !important; margin: 10px 0 !important; }

/* Dataframe in main area */
[data-testid="stMain"] [data-testid="stDataFrame"] {
    min-height: 120px !important;
    background: #1E293B !important;
}
[data-testid="stMain"] [data-testid="stDataFrame"] > div {
    min-height: 120px !important;
    background: #1E293B !important;
}

/* Model Results — predictions HTML table */
.predictions-table-wrap {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    max-height: 220px !important;
    overflow: auto !important;
    width: 100% !important;
}
.predictions-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    line-height: 1.35;
    background: #1E293B !important;
    color: #94A3B8 !important;
}
.predictions-table thead th {
    position: sticky;
    top: 0;
    z-index: 1;
    background: #273449 !important;
    color: #F8FAFC !important;
    font-weight: 700;
    text-align: left;
    padding: 8px 10px;
    border-bottom: 1px solid #334155 !important;
    white-space: nowrap;
}
.predictions-table tbody td {
    background: #1E293B !important;
    color: #94A3B8 !important;
    padding: 6px 10px;
    border-bottom: 1px solid #334155 !important;
    vertical-align: middle;
}
.predictions-table tbody tr:hover td {
    background: #273449 !important;
    color: #CBD5E1 !important;
}
.predictions-table tbody tr:last-child td {
    border-bottom: none !important;
}

/* Legacy / static table fallback */
[data-testid="stTable"] {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}
[data-testid="stTable"] table {
    background: #1E293B !important;
    color: #F8FAFC !important;
    border-collapse: collapse !important;
}
[data-testid="stTable"] thead th {
    background: #273449 !important;
    color: #F8FAFC !important;
    border-bottom: 1px solid #334155 !important;
}
[data-testid="stTable"] tbody td {
    background: #1E293B !important;
    color: #94A3B8 !important;
    border-bottom: 1px solid #334155 !important;
}
[data-testid="stTable"] tbody tr:hover td {
    background: #273449 !important;
}

[data-testid="stDataFrame"] .dvn-scroller,
[data-testid="stDataFrameGlideDataEditor"] .dvn-scroller {
    background: #1E293B !important;
}

/* Plotly — room for labels/legend, no clipping */
[data-testid="stMain"] [data-testid="stPlotlyChart"] {
    min-height: 0 !important;
    overflow: visible !important;
}
[data-testid="stMain"] [data-testid="stPlotlyChart"] > div {
    padding: 0 !important;
    overflow: visible !important;
}
[data-testid="stMain"] .js-plotly-plot .plot-container.plotly {
    min-height: 0 !important;
    overflow: visible !important;
}

/* Dashboard — Risk Distribution chart in matching card shell */
#risk-distribution-chart-card {
    display: block;
    height: 0;
    margin: 0;
    padding: 0;
    border: none;
    overflow: hidden;
}
[data-testid="stMain"] .element-container:has(#risk-distribution-chart-card) {
    margin-bottom: 0 !important;
    padding: 0 !important;
    min-height: 0 !important;
}
[data-testid="stMain"] .element-container:has(#risk-distribution-chart-card) ~ .element-container:has([data-testid="stPlotlyChart"]) {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 14px !important;
    padding: 12px 14px 10px 14px !important;
    overflow: visible !important;
}

/* Study schedule — Week starting + Focus filter alignment */
[data-testid="stSelectbox"] label {
    margin-bottom: 2px !important;
    padding-bottom: 0 !important;
    min-height: 18px !important;
    line-height: 1.25 !important;
}
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    min-height: 38px !important;
    border-radius: 10px !important;
}
[data-testid="stMain"] .element-container:has(#schedule-controls) + .element-container [data-testid="stHorizontalBlock"] {
    align-items: flex-end !important;
}
[data-testid="stMain"] .element-container:has(#schedule-controls) + .element-container [data-testid="column"] {
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-end !important;
}
[data-testid="stMain"] .element-container:has(#schedule-controls) + .element-container [data-testid="stDateInput"],
[data-testid="stMain"] .element-container:has(#schedule-controls) + .element-container [data-testid="stSelectbox"] {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    width: 100% !important;
}

/* Study schedule */
.schedule-day-card {
    margin-bottom: 6px !important;
    min-height: clamp(88px, 14.5vh, 118px);
}
.schedule-day-blocks { overflow: visible; max-height: none; }
.schedule-day-blocks > div:last-child { margin-bottom: 0 !important; }
.schedule-summary { margin-bottom: 10px !important; }

/* Course cards — single list wrapper with reliable external gap (no overlap) */
.courses-list {
    display: flex;
    flex-direction: column;
    gap: 24px;
    width: 100%;
}
.courses-list .course-card-compact {
    margin: 0 !important;
    flex-shrink: 0;
}
.course-card-title {
    font-size: 15px;
    font-weight: 800;
    letter-spacing: -0.01em;
    line-height: 1.25;
}
.course-card-compact .course-stats { margin-top: 8px !important; gap: 20px !important; }
.course-card-compact .course-bars { margin-top: 6px !important; }

/* List row rhythm inside panels */
.panel-row {
    padding: 8px 0;
}

</style>
"""


def inject_app_styles() -> None:
    """Inject the main application design-system CSS.

    Blank lines are stripped before passing to st.markdown because CommonMark
    terminates an HTML block on the first blank line, which would cause the CSS
    to render as visible text instead of being applied as styles.
    """
    import re
    clean = re.sub(r"\n[ \t]*\n", "\n", APP_STYLES)
    st.markdown(clean, unsafe_allow_html=True)