"""Recommendations page — study tips connected to the student's own predictions."""

import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from course_colors import get_course_color
from utils import render_html

# ---------------------------------------------------------------------------
# Recommendation content
# ---------------------------------------------------------------------------

TIPS: dict[str, list[dict]] = {
    "High Risk": [
        {
            "icon": "🚨",
            "title": "Emergency Study Sprint",
            "body": "Dedicate at least 5 hours per week to this course. Use active recall — close the book and write down everything you remember.",
        },
        {
            "icon": "💬",
            "title": "Talk to Your Instructor",
            "body": "Reach out now. Instructors often provide extra guidance or extend deadlines for students who engage proactively.",
        },
        {
            "icon": "🗂️",
            "title": "Chunk the Curriculum",
            "body": "Break the remaining material into daily micro-goals. Completing small tasks daily is more effective than one marathon session.",
        },
        {
            "icon": "📵",
            "title": "Eliminate Distractions",
            "body": "Use Forest, Focus@Will, or similar tools. Even 90 minutes of deep, distraction-free work can equal 4 hours of fragmented studying.",
        },
        {
            "icon": "😴",
            "title": "Sleep — Do Not Cut It",
            "body": "Memory consolidation happens during sleep. Cutting sleep to study more is counterproductive beyond the first night.",
        },
    ],
    "Medium Risk": [
        {
            "icon": "⏱️",
            "title": "Add One Focused Hour",
            "body": "You are close to safe territory. Adding just one extra focused hour per day can shift you from medium to low risk within a week.",
        },
        {
            "icon": "🃏",
            "title": "Spaced Repetition",
            "body": "Use Anki or similar flashcard tools. Spaced repetition is the most evidence-backed method for long-term retention.",
        },
        {
            "icon": "👥",
            "title": "Study Groups",
            "body": "Teaching peers is one of the most effective ways to identify gaps in your own understanding.",
        },
        {
            "icon": "📋",
            "title": "Past Exam Analysis",
            "body": "Analyse previous exams to identify question patterns. Most courses test the same core concepts repeatedly.",
        },
        {
            "icon": "📆",
            "title": "Weekly Review Sessions",
            "body": "Reserve 90 minutes every Sunday to review the week's material. This prevents knowledge decay over the weekend.",
        },
    ],
    "Low Risk": [
        {
            "icon": "✅",
            "title": "Maintain Consistency",
            "body": "You are on track. Do not let a low-risk status encourage complacency — maintain your current study rhythm.",
        },
        {
            "icon": "🔬",
            "title": "Go Deeper",
            "body": "Use your extra bandwidth to explore topics beyond the syllabus. Depth of understanding pays off in exams.",
        },
        {
            "icon": "📅",
            "title": "Prepare Early",
            "body": "Begin exam preparation 3–4 weeks early instead of the usual 1 week. This reduces stress and improves performance.",
        },
        {
            "icon": "🤝",
            "title": "Support Peers",
            "body": "Helping struggling peers reinforces your own knowledge and builds the collective academic environment.",
        },
        {
            "icon": "📊",
            "title": "Track Attendance Actively",
            "body": "Staying above 85% attendance is the single most reliable predictor of academic success across all institutions.",
        },
    ],
}

GENERAL_TIPS = [
    ("📖", "Active Recall",      "Don't re-read — close the material and test yourself. This produces 2–3× better retention than passive review."),
    ("🧩", "Interleaving",       "Alternate between different subjects in the same session. This strengthens the ability to distinguish concepts."),
    ("🏃", "Physical Exercise",  "30 minutes of moderate exercise before studying increases BDNF — a protein that promotes neuron growth and learning."),
    ("🍅", "Pomodoro Technique", "25 minutes focus, 5 minutes break, repeat. After 4 cycles take a 20-minute break. Prevents mental fatigue."),
    ("📝", "Feynman Technique",  "Explain a concept simply as if teaching a child. Where you stumble reveals what you have not truly understood."),
    ("🌙", "Sleep Hygiene",      "Aim for 7–8 hours. REM sleep is when the brain consolidates and cross-links new memories with existing knowledge."),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _navigate(page: str) -> None:
    st.session_state.current_page = page
    st.rerun()


def _risk_color(level: str) -> str:
    l = str(level).lower()
    if "high"   in l: return "#DC2626"
    if "medium" in l: return "#F59E0B"
    if "low"    in l: return "#22C55E"
    return "#64748B"


def _normalize_risk(level: str) -> str:
    """Map 'High Risk' / 'High' / 'high' all to the TIPS key."""
    l = str(level).lower()
    if "high"   in l: return "High Risk"
    if "medium" in l: return "Medium Risk"
    if "low"    in l: return "Low Risk"
    return "Medium Risk"


def _tips_panel(tips: list[dict], color: str) -> str:
    rows = "".join(f"""
<div class="panel-row" style="display:flex;align-items:flex-start;gap:10px;
border-bottom:1px solid #273449;border-left:3px solid {color};padding-left:8px;">
<div style="font-size:18px;flex-shrink:0;">{t["icon"]}</div>
<div>
<div style="font-size:14px;font-weight:700;color:#F1F5F9;margin-bottom:2px;">{t["title"]}</div>
<div style="font-size:13px;color:#94A3B8;line-height:1.45;">{t["body"]}</div>
</div>
</div>
""" for t in tips)
    return f'<div class="card list-panel list-panel--rec">{rows}</div>'


# ---------------------------------------------------------------------------
# Render sections
# ---------------------------------------------------------------------------

def _render_empty_state() -> None:
    render_html("""
<div class="card" style="text-align:center;padding:48px 24px;margin-bottom:12px;">
<div style="font-size:44px;margin-bottom:14px;">💡</div>
<div style="font-size:20px;font-weight:800;color:#F8FAFC;margin-bottom:10px;">
No Predictions Yet
</div>
<div style="font-size:14px;color:#64748B;max-width:440px;margin:0 auto 24px;line-height:1.7;">
Run a risk prediction for at least one course to receive personalized
study recommendations tailored to your academic situation.
</div>
</div>
""")
    col_a, col_b, col_c = st.columns([1, 1.4, 1])
    with col_b:
        if st.button("🎯  Run Risk Prediction", type="primary", use_container_width=True, key="rec_empty_btn"):
            _navigate("risk")

    # Still show general tips below empty state
    render_html('<div class="section-h2 section-h2--follow">Universal Study Science</div>')
    render_html('<div class="page-sub">Evidence-based techniques that help all students regardless of risk level</div>')
    _render_general_tips()


def _render_single_prediction(result: dict) -> None:
    level   = result.get("level", "Medium Risk")
    course  = result.get("course", "")
    conf    = result.get("confidence")
    color   = _risk_color(level)
    key     = _normalize_risk(level)

    conf_line = f'Confidence: {conf*100:.0f}%' if conf is not None else ""
    render_html(f"""
<div class="card card-accent-blue" style="margin-bottom:10px;">
<div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;
letter-spacing:0.1em;margin-bottom:6px;">Based on your latest prediction</div>
<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
<span style="font-size:15px;font-weight:700;color:{get_course_color(course)};">{course}</span>
<span class="badge" style="background:{color}22;color:{color};border:1px solid {color}55;">{level}</span>
{"" if not conf_line else f'<span style="font-size:12px;color:#64748B;">{conf_line}</span>'}
</div>
</div>
""")
    render_html(f'<div class="section-h2" style="color:{color};">{level} — Action Plan</div>')
    render_html(_tips_panel(TIPS.get(key, TIPS["Medium Risk"]), color))


def _render_multi_course(history: list) -> None:
    """Show per-course recommendations when multiple predictions exist."""
    # Deduplicate: keep latest prediction per course
    seen: dict[str, dict] = {}
    for entry in reversed(history):
        c = entry.get("course", "")
        if c and c not in seen:
            seen[c] = entry

    # Sort by risk severity
    risk_order = {"High Risk": 0, "Medium Risk": 1, "Low Risk": 2}
    sorted_entries = sorted(
        seen.values(),
        key=lambda e: risk_order.get(_normalize_risk(e.get("risk_level", "")), 3),
    )

    for entry in sorted_entries:
        course  = entry.get("course", "")
        level   = entry.get("risk_level", "")
        key     = _normalize_risk(level)
        color   = _risk_color(level)
        cc      = get_course_color(course)
        date    = entry.get("created_at", "")

        render_html(f"""
<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:14px 0 6px;">
<span style="font-size:15px;font-weight:700;color:{cc};">{course}</span>
<span class="badge" style="background:{color}22;color:{color};border:1px solid {color}55;">{level}</span>
{"" if not date else f'<span style="font-size:11px;color:#475569;">{date}</span>'}
</div>
""")
        render_html(_tips_panel(TIPS.get(key, TIPS["Medium Risk"])[:3], color))


def _render_general_tips() -> None:
    rows = "".join(f"""
<div class="panel-row" style="display:flex;align-items:flex-start;gap:10px;border-bottom:1px solid #273449;">
<div style="font-size:18px;flex-shrink:0;">{icon}</div>
<div>
<div style="font-size:13px;font-weight:700;color:#F1F5F9;">{title}</div>
<div style="font-size:12px;color:#64748B;margin-top:2px;line-height:1.45;">{body}</div>
</div>
</div>
""" for icon, title, body in GENERAL_TIPS)
    render_html(f'<div class="card list-panel list-panel--rec">{rows}</div>')


def _render_cta_buttons() -> None:
    render_html('<div class="section-h2 section-h2--follow">What\'s Next?</div>')
    cta1, cta2, cta3 = st.columns(3)
    with cta1:
        if st.button("📅  View Schedule", use_container_width=True, key="rec_cta_sched"):
            _navigate("schedule")
    with cta2:
        if st.button("🎯  New Prediction", use_container_width=True, key="rec_cta_risk"):
            _navigate("risk")
    with cta3:
        if st.button("🏠  Dashboard", use_container_width=True, key="rec_cta_dash"):
            _navigate("dashboard")


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render() -> None:
    render_html('<div class="page-h1">Recommendations</div>')
    render_html(
        '<div class="page-sub">Personalized study strategies based on your risk predictions</div>'
    )

    result  = st.session_state.get("prediction_result")
    history = st.session_state.get("prediction_history", [])

    if not result and not history:
        _render_empty_state()
        return

    # Multiple courses with predictions → per-course view
    if len(history) > 1:
        render_html('<div class="section-h2">Per-Course Action Plans</div>')
        render_html(
            '<div class="page-sub">Courses sorted by risk level — highest risk first.</div>'
        )
        _render_multi_course(history)
    elif result:
        _render_single_prediction(result)
    elif len(history) == 1:
        # prediction_result was cleared (e.g. Profile reset) but history still has the entry
        entry = history[0]
        _render_single_prediction({
            "level":      entry.get("risk_level", ""),
            "course":     entry.get("course", ""),
            "confidence": None,
        })

    render_html('<div class="section-h2 section-h2--follow">Universal Study Science</div>')
    render_html('<div class="page-sub">Evidence-based techniques that benefit every student</div>')
    _render_general_tips()

    _render_cta_buttons()
