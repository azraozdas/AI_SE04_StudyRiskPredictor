<<<<<<< HEAD
"""Risk Prediction page — input form + ML model inference via model_utils."""
=======
"""Risk Prediction page — user input form → encoders.pkl → model.pkl → result."""
>>>>>>> 7b5e2eb8716a57dfbd06a107298c4850c204f3e1

import os
import sys

<<<<<<< HEAD
=======
import joblib
>>>>>>> 7b5e2eb8716a57dfbd06a107298c4850c204f3e1
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import ROOT, render_html

<<<<<<< HEAD
RAW_PATH = os.path.join(ROOT, "Data", "student_study_data.csv")

_SOURCE = os.path.join(ROOT, "Source")
_BACKEND = os.path.join(_SOURCE, "Backend")
for _p in (_SOURCE, _BACKEND):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from model_utils import load_model, predict_for_user  # noqa: E402
from db import save_prediction  # noqa: E402

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_DISPLAY_RISK = {
    "High": "High Risk",
    "Medium": "Medium Risk",
    "Low": "Low Risk",
}


def _display_risk(label: str) -> str:
    if label in _DISPLAY_RISK:
        return _DISPLAY_RISK[label]
    if "risk" in label.lower():
        return label
    return f"{label} Risk" if label else "Unknown"


def _fallback(study_hours, attendance, deadline_days, pass_grade, difficulty, workload) -> str:
=======
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
>>>>>>> 7b5e2eb8716a57dfbd06a107298c4850c204f3e1
    score = 0
    score += 2 if study_hours < 3 else (1 if study_hours < 5 else 0)
    score += 2 if attendance < 60 else (1 if attendance < 75 else 0)
    score += 2 if deadline_days <= 2 else (1 if deadline_days <= 5 else 0)
    score += 2 if pass_grade < 60 else (1 if pass_grade < 75 else 0)
    score += 2 if difficulty == "High" else (1 if difficulty == "Medium" else 0)
    score += 2 if workload == "High" else (1 if workload == "Medium" else 0)
<<<<<<< HEAD
    if score >= 7:
        return "High Risk"
    if score >= 4:
        return "Medium Risk"
    return "Low Risk"


@st.cache_resource
def _load_artifacts():
    try:
        return load_model()
    except FileNotFoundError:
        return None, None


@st.cache_data
def _load_raw():
    if os.path.exists(RAW_PATH):
        return pd.read_csv(RAW_PATH)
    return None


def _course_options(encoders, raw_df) -> list[str]:
    if encoders and "course" in encoders:
        return sorted(encoders["course"].classes_.tolist())
    if raw_df is not None and "course" in raw_df.columns:
        return sorted(raw_df["course"].unique().tolist())
    return [
        "Introduction to Programming",
        "Database Systems",
        "Machine Learning",
        "Software Engineering",
    ]


def _risk_pct(label: str, study_hours, attendance, pass_grade) -> int:
    if "high" in label.lower():
        return min(95, max(70, 100 - int(study_hours * 4) - int((attendance - 50) * 0.3)))
    if "medium" in label.lower():
        return min(65, max(35, 50 + int((75 - pass_grade) * 0.3)))
    return min(30, max(5, int((pass_grade - 70) * 0.3) + int(study_hours * 2)))


# ---------------------------------------------------------------------------
# Result panel
# ---------------------------------------------------------------------------

def _result_panel(label: str, source: str, inputs: dict, confidence: float | None = None) -> None:
    css_class = (
        "risk-display-high"   if "high"   in label.lower() else
        "risk-display-medium" if "medium" in label.lower() else
        "risk-display-low"
    )
    border_color = (
        "#DC2626" if "high"   in label.lower() else
        "#F59E0B" if "medium" in label.lower() else
        "#22C55E"
    )
    bg_color = (
        "rgba(220,38,38,0.06)"  if "high"   in label.lower() else
        "rgba(245,158,11,0.06)" if "medium" in label.lower() else
        "rgba(34,197,94,0.06)"
    )

    recommendations = {
        "High Risk": [
            "Start studying immediately — break the material into small daily chunks.",
            "Prioritize attendance; every missed class compounds the deficit.",
            "Schedule a session with your academic advisor this week.",
            "Use the Pomodoro technique: 25 min focus, 5 min break.",
            "Remove all distractions during study time; use focus-mode apps.",
        ],
        "Medium Risk": [
            "Add 1–2 extra study hours this week to stay ahead.",
            "Review the most difficult topics first while energy is high.",
            "Form or join a study group for peer accountability.",
            "Use past exams to identify weak areas.",
            "Monitor your deadline calendar daily.",
        ],
        "Low Risk": [
            "Maintain your current study routine — consistency is key.",
            "Help peers who are struggling; teaching reinforces your own learning.",
            "Use extra time to deepen understanding beyond the curriculum.",
            "Prepare notes and summaries now to ease revision later.",
            "Keep your attendance above 85% to stay in the safe zone.",
        ],
    }

    tips = recommendations.get(label, recommendations["Medium Risk"])
    conf_line = ""
    if confidence is not None:
        conf_line = f'<div style="font-size:12px;color:#64748B;margin-top:4px;">Confidence: {confidence * 100:.0f}%</div>'

    render_html(f"""
<div class="card" style="border:1px solid {border_color};background:{bg_color};text-align:center;">
<div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;">
Prediction Result
</div>
<div class="risk-display {css_class}">{label}</div>
<div style="font-size:12px;color:#64748B;margin-top:4px;">Source: {source}</div>
{conf_line}
</div>
""")

    render_html('<div class="section-h2 section-h2--follow">Study Recommendations</div>')
    tips_html = "".join(
        f"""
<div class="panel-row" style="display:flex;align-items:flex-start;gap:8px;border-bottom:1px solid #273449;">
<span style="color:{border_color};font-size:16px;flex-shrink:0;">›</span>
<span style="font-size:13px;color:#CBD5E1;line-height:1.4;">{tip}</span>
</div>
"""
        for tip in tips
    )
    render_html(f'<div class="card list-panel list-panel--rec">{tips_html}</div>')
    render_html('<div class="section-h2 section-h2--follow">Input Overview</div>')

    import plotly.graph_objects as go

    factors = ["Study Hours", "Attendance (%)", "Days to Deadline", "Pass Grade"]
    values = [
        inputs["study_hours"],
        inputs["attendance"],
        inputs["deadline_days"],
        inputs["pass_grade"],
    ]
    maxes = [15, 100, 30, 100]
    colors = [
        "#22C55E" if v / m >= 0.6 else ("#F59E0B" if v / m >= 0.35 else "#DC2626")
        for v, m in zip(values, maxes)
    ]
    fig = go.Figure(go.Bar(
        x=factors, y=values,
        marker_color=colors,
        text=[str(v) for v in values],
        textposition="outside",
        textfont=dict(color="#F8FAFC", size=13),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        xaxis=dict(tickfont=dict(color="#94A3B8", size=12)),
        margin=dict(t=8, b=28, l=6, r=6),
        height=152,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render() -> None:
    render_html('<div class="page-h1">Risk Prediction</div>')
    render_html('<div class="page-sub">Enter academic information to predict study risk level</div>')

    model, encoders = _load_artifacts()
    raw_df = _load_raw()
    course_options = _course_options(encoders, raw_df)

    default_course = st.session_state.get("selected_course")
    default_idx = (
        course_options.index(default_course)
        if default_course and default_course in course_options
        else 0
    )

    render_html(
        '<div class="section-h2">Student Input Form</div>'
        '<div style="font-size:13px;color:#64748B;margin-bottom:10px;">'
        'Fill in the academic details below to estimate the risk level for this course.'
        '</div>'
    )

    col1, col2 = st.columns(2)

    with col1:
        course = st.selectbox("Course", course_options, index=default_idx)
        study_hours = st.slider("Weekly Study Hours", 0, 15, 4)
        attendance = st.slider("Attendance (%)", 0, 100, 75)

    with col2:
        deadline_days = st.slider("Days Until Deadline", 0, 30, 7)
        pass_grade = st.slider("Current Pass Grade", 0, 100, 70)
        assignment_difficulty = st.selectbox("Assignment Difficulty", ["Low", "Medium", "High"])
        workload_level = st.selectbox("Workload Level", ["Low", "Medium", "High"])

    predict_clicked = st.button("Predict Risk", type="primary", use_container_width=True)

    if predict_clicked:
        risk_raw = None
        confidence = None
        source = "Fallback heuristic"

        if model is not None and encoders is not None:
            try:
                result = predict_for_user(
                    model, encoders,
                    course=course,
                    study_hours=study_hours,
                    attendance=attendance,
                    deadline_days=deadline_days,
                    pass_grade=pass_grade,
                    assignment_difficulty=assignment_difficulty,
                    workload_level=workload_level,
                )
                risk_raw = result["risk_level"]
                confidence = result["confidence"]
                source = "Random Forest (encoders.pkl)"
            except (ValueError, Exception) as exc:
                st.warning(f"Model prediction failed ({exc}). Using fallback logic.")
                risk_raw = None

        if risk_raw is None:
            risk_label = _fallback(
                study_hours, attendance, deadline_days,
                pass_grade, assignment_difficulty, workload_level,
            )
            if model is None or encoders is None:
                source = "Fallback heuristic (model files missing)"
            else:
                source = "Fallback heuristic (model error)"
        else:
            risk_label = _display_risk(risk_raw)
            user_id = st.session_state.get("user_id")
            if user_id:
                try:
                    save_prediction(user_id, risk_raw)
                except Exception as exc:
                    st.warning(f"Could not save prediction to database ({exc}).")

        pct = _risk_pct(risk_label, study_hours, attendance, pass_grade)
        st.session_state.prediction_result = {
            "level": risk_label,
            "pct": pct,
            "course": course,
            "source": source,
            "confidence": confidence,
        }
        st.session_state.selected_course = course

    if st.session_state.get("prediction_result"):
        res = st.session_state.prediction_result
        _result_panel(
            label=res["level"],
            source=res["source"],
            inputs={
                "study_hours": study_hours if predict_clicked else 4,
                "attendance": attendance if predict_clicked else 75,
                "deadline_days": deadline_days if predict_clicked else 7,
                "pass_grade": pass_grade if predict_clicked else 70,
            },
            confidence=res.get("confidence"),
        )
=======
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
>>>>>>> 7b5e2eb8716a57dfbd06a107298c4850c204f3e1
