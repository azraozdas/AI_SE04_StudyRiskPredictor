"""Risk Prediction page — user input form → encoders.pkl → model.pkl → result."""

import os
import sys

import joblib
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import ROOT, render_html

_BACKEND = os.path.join(ROOT, "Source", "Backend")
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)
from db import save_prediction  # noqa: E402

MODEL_PATH    = os.path.join(ROOT, "Models", "study_risk_model.pkl")
ENCODERS_PATH = os.path.join(ROOT, "Models", "encoders.pkl")
RAW_PATH      = os.path.join(ROOT, "Data", "student_study_data.csv")


# ── Cached loaders ────────────────────────────────────────────────────────────

@st.cache_resource
def _load_model():
    return joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None


@st.cache_resource
def _load_encoders():
    return joblib.load(ENCODERS_PATH) if os.path.exists(ENCODERS_PATH) else None


@st.cache_data
def _load_courses():
    if os.path.exists(RAW_PATH):
        df = pd.read_csv(RAW_PATH)
        if "course" in df.columns:
            return sorted(df["course"].unique().tolist())
    return ["Introduction to Programming", "Database Systems",
            "Machine Learning", "Software Engineering"]


# ── Encoding helpers — uses encoders.pkl, no hardcoded maps ──────────────────

def _enc(encoders, key, value, fallback):
    if encoders and key in encoders:
        try:
            return int(encoders[key].transform([value])[0])
        except Exception:
            pass
    return fallback.get(value, 0)


def _decode_risk(pred, encoders):
    if encoders and "risk_level" in encoders:
        try:
            return str(encoders["risk_level"].inverse_transform([pred])[0])
        except Exception:
            pass
    return {0: "High", 1: "Low", 2: "Medium"}.get(pred, "Unknown")


def _rule_based(study_hours, attendance, deadline_days, pass_grade, difficulty, workload):
    score = 0
    score += 2 if study_hours < 3 else (1 if study_hours < 5 else 0)
    score += 2 if attendance < 60 else (1 if attendance < 75 else 0)
    score += 2 if deadline_days <= 2 else (1 if deadline_days <= 5 else 0)
    score += 2 if pass_grade < 60 else (1 if pass_grade < 75 else 0)
    score += 2 if difficulty == "High" else (1 if difficulty == "Medium" else 0)
    score += 2 if workload == "High" else (1 if workload == "Medium" else 0)
    return "High" if score >= 7 else ("Medium" if score >= 4 else "Low")


_RECS = {
    "High":   "Start studying immediately. Break the material into daily chunks, "
              "attend all remaining sessions, and reach out to your instructor today.",
    "Medium": "Plan two extra study sessions this week. Review the most difficult "
              "topics first and keep an eye on upcoming deadlines.",
    "Low":    "You're on track. Maintain your routine, review once before the deadline, "
              "and help a peer if you can.",
}

_COLOR = {
    "High":   ("#EF4444", "rgba(239,68,68,.15)",  "rgba(239,68,68,.4)"),
    "Medium": ("#FBBF24", "rgba(251,191,36,.13)", "rgba(251,191,36,.4)"),
    "Low":    ("#22C55E", "rgba(34,197,94,.12)",  "rgba(34,197,94,.4)"),
}


# ── Page renderer ─────────────────────────────────────────────────────────────

def render():
    model    = _load_model()
    encoders = _load_encoders()
    courses  = _load_courses()

    render_html("""
        <div style="margin-bottom:24px;">
            <div style="font-size:22px;font-weight:800;color:#F8FAFC;letter-spacing:-0.02em;">
                Risk Prediction
            </div>
            <div style="font-size:14px;color:#64748B;margin-top:4px;">
                Enter your academic data to get an AI-powered risk assessment.
            </div>
        </div>
    """)

    if model is None:
        st.warning("Model file not found — rule-based fallback will be used.")
    if encoders is None:
        st.warning("Encoders file not found — fallback category maps will be used.")

    with st.form("risk_form"):
        col1, col2 = st.columns(2)

        with col1:
            course      = st.selectbox("Course", courses)
            study_hours = st.slider("Weekly Study Hours", 0, 15, 4)
            attendance  = st.slider("Attendance (%)", 0, 100, 75)
            deadline    = st.slider("Days Until Deadline", 0, 30, 7)

        with col2:
            pass_grade  = st.slider("Current Grade", 0, 100, 70)
            difficulty  = st.selectbox("Assignment Difficulty", ["Low", "Medium", "High"])
            workload    = st.selectbox("Workload Level",        ["Low", "Medium", "High"])

        submitted = st.form_submit_button(
            "Predict Risk Level", use_container_width=True, type="primary"
        )

    if not submitted:
        return

    # ── Inference ─────────────────────────────────────────────────────────────
    _DIFF_FB = {"High": 0, "Low": 1, "Medium": 2}
    _WL_FB   = {"High": 0, "Low": 1, "Medium": 2}

    if model is not None and encoders is not None:
        X = pd.DataFrame([{
            "course":                _enc(encoders, "course", course, {}),
            "study_hours":           study_hours,
            "attendance":            attendance,
            "deadline_days":         deadline,
            "pass_grade":            pass_grade,
            "assignment_difficulty": _enc(encoders, "assignment_difficulty", difficulty, _DIFF_FB),
            "workload_level":        _enc(encoders, "workload_level", workload, _WL_FB),
        }])
        try:
            risk   = _decode_risk(int(model.predict(X)[0]), encoders)
            source = "Random Forest · encoders.pkl"
        except Exception as e:
            st.warning(f"Model error ({e}). Using fallback.")
            risk   = _rule_based(study_hours, attendance, deadline, pass_grade, difficulty, workload)
            source = "Rule-based fallback"
    else:
        risk   = _rule_based(study_hours, attendance, deadline, pass_grade, difficulty, workload)
        source = "Rule-based fallback (model/encoders missing)"

    # ── Result card ───────────────────────────────────────────────────────────
    fg, bg, border = _COLOR.get(risk, ("#94A3B8", "rgba(148,163,184,.1)", "rgba(148,163,184,.3)"))

    render_html(f"""
        <div style="margin-top:28px;border-radius:18px;padding:28px 32px;
                    background:{bg};border:1px solid {border};text-align:center;">
            <div style="font-size:13px;color:#64748B;font-weight:600;text-transform:uppercase;
                        letter-spacing:.08em;margin-bottom:10px;">Predicted Risk Level</div>
            <div style="font-size:42px;font-weight:900;color:{fg};letter-spacing:-0.02em;">
                {risk} Risk
            </div>
            <div style="font-size:12px;color:#475569;margin-top:8px;">via {source}</div>
        </div>
        <div style="margin-top:18px;border-radius:14px;padding:20px 24px;
                    background:rgba(15,23,42,.6);border:1px solid rgba(148,163,184,.15);">
            <div style="font-size:13px;font-weight:700;color:#CBD5E1;margin-bottom:6px;">
                Recommendation
            </div>
            <div style="font-size:14px;color:#94A3B8;line-height:1.65;">
                {_RECS.get(risk, "No recommendation available.")}
            </div>
        </div>
    """)

    with st.expander("Input Overview", expanded=False):
        st.bar_chart(pd.DataFrame({
            "Factor": ["Study Hours", "Attendance", "Days to Deadline", "Grade"],
            "Value":  [study_hours, attendance, deadline, pass_grade],
        }).set_index("Factor"))

    # Save to DB (non-critical)
    uid = st.session_state.get("user_id")
    if uid:
        try:
            save_prediction(uid, f"{risk} Risk")
        except Exception:
            pass
