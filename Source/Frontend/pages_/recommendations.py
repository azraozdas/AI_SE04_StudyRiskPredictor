"""Recommendations page — AI study tips based on risk patterns."""

import os
import sys

import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from course_colors import get_course_color
from utils import ROOT, render_html

RAW_PATH = os.path.join(ROOT, "Data", "student_study_data.csv")

# ---------------------------------------------------------------------------
# Recommendation content
# ---------------------------------------------------------------------------

TIPS: dict[str, list[dict]] = {
    "High Risk": [
        {
            "title": "Emergency Study Sprint",
            "body": "Dedicate at least 4 hours per day to the high-risk course. Use active recall — close the book and write down everything you remember.",
            "icon": "🚨",
        },
        {
            "title": "Talk to Your Instructor",
            "body": "Reach out now. Instructors often provide extra guidance or extend deadlines for students who engage proactively.",
            "icon": "💬",
        },
        {
            "title": "Chunk the Curriculum",
            "body": "Break the remaining material into daily micro-goals. Completing small tasks daily is more effective than one marathon session.",
            "icon": "🗂️",
        },
        {
            "title": "Eliminate Distractions",
            "body": "Use Forest, Focus@Will, or similar tools. Even 90 minutes of deep, distraction-free work can equal 4 hours of fragmented studying.",
            "icon": "📵",
        },
        {
            "title": "Sleep — Do Not Cut It",
            "body": "Memory consolidation happens during sleep. Cutting sleep to study more is counterproductive beyond the first night.",
            "icon": "😴",
        },
    ],
    "Medium Risk": [
        {
            "title": "Add One Focused Hour",
            "body": "You are close to safe territory. Adding just one extra focused hour per day can shift you from medium to low risk within a week.",
            "icon": "⏱️",
        },
        {
            "title": "Spaced Repetition",
            "body": "Use Anki or similar flashcard tools. Spaced repetition is the most evidence-backed method for long-term retention.",
            "icon": "🃏",
        },
        {
            "title": "Study Groups",
            "body": "Teaching peers is one of the most effective ways to identify gaps in your own understanding. Join or start a study group.",
            "icon": "👥",
        },
        {
            "title": "Past Exam Analysis",
            "body": "Analyse previous exams to identify question patterns. Most courses test the same core concepts repeatedly.",
            "icon": "📋",
        },
        {
            "title": "Weekly Review Sessions",
            "body": "Reserve 90 minutes every Sunday to review the week's material. This prevents knowledge decay over the weekend.",
            "icon": "📆",
        },
    ],
    "Low Risk": [
        {
            "title": "Maintain Consistency",
            "body": "You are on track. Do not let a low-risk status encourage complacency — maintain your current study rhythm.",
            "icon": "✅",
        },
        {
            "title": "Go Deeper",
            "body": "Use your extra bandwidth to explore topics beyond the syllabus. Depth of understanding pays off significantly in exams.",
            "icon": "🔬",
        },
        {
            "title": "Prepare Early",
            "body": "Begin exam preparation 3–4 weeks early instead of the usual 1 week. This reduces stress and improves performance.",
            "icon": "📅",
        },
        {
            "title": "Support Peers",
            "body": "Helping struggling peers reinforces your own knowledge and improves the collective academic environment.",
            "icon": "🤝",
        },
        {
            "title": "Track Attendance Actively",
            "body": "Staying above 85% attendance is the single most reliable predictor of academic success across all institutions.",
            "icon": "📊",
        },
    ],
}

GENERAL_TIPS = [
    ("📖", "Active Recall", "Don't re-read — close the material and test yourself. This produces 2–3× better retention than passive review."),
    ("🧩", "Interleaving", "Alternate between different subjects within the same study session. This strengthens the ability to distinguish concepts."),
    ("🏃", "Physical Exercise", "30 minutes of moderate exercise before studying increases BDNF — a protein that promotes neuron growth and learning."),
    ("🍅", "Pomodoro Technique", "25 minutes focus, 5 minutes break, repeat. After 4 cycles take a 20-minute break. Prevents mental fatigue."),
    ("📝", "The Feynman Technique", "Explain a concept in simple terms as if teaching a child. Where you stumble reveals what you have not truly understood."),
    ("🌙", "Sleep Hygiene", "Aim for 7–8 hours. REM sleep is when the brain consolidates and cross-links new memories with existing knowledge."),
]


def _tips_panel_html(tips: list, color: str) -> str:
    rows = "".join(
        f"""
<div class="panel-row" style="display:flex;align-items:flex-start;gap:8px;border-bottom:1px solid #273449;border-left:3px solid {color};padding-left:8px;">
<div style="font-size:18px;flex-shrink:0;">{t["icon"]}</div>
<div>
<div style="font-size:14px;font-weight:700;color:#F1F5F9;margin-bottom:2px;">{t["title"]}</div>
<div style="font-size:13px;color:#94A3B8;line-height:1.4;">{t["body"]}</div>
</div>
</div>
"""
        for t in tips
    )
    return f'<div class="card list-panel list-panel--rec">{rows}</div>'


def _tip_card(icon: str, title: str, body: str, color: str) -> str:
    return _tips_panel_html([{"icon": icon, "title": title, "body": body}], color)


def _general_tip(icon: str, title: str, body: str) -> str:
    return f"""
<div class="card" style="margin-bottom:10px;display:flex;align-items:flex-start;gap:10px;">
<div style="font-size:18px;flex-shrink:0;">{icon}</div>
<div>
<div style="font-size:13px;font-weight:700;color:#F1F5F9;">{title}</div>
<div style="font-size:12px;color:#64748B;margin-top:2px;line-height:1.5;">{body}</div>
</div>
</div>
"""


def render() -> None:
    render_html('<div class="page-h1">Recommendations</div>')
    render_html('<div class="page-sub">Personalised study strategies based on your risk profile</div>')

    # Check if there is a recent prediction result
    result = st.session_state.get("prediction_result")

    if result:
        level  = result.get("level", "Medium Risk")
        course = result.get("course", "")
        color  = (
            "#DC2626" if "high"   in level.lower() else
            "#F59E0B" if "medium" in level.lower() else
            "#22C55E"
        )
        badge_cls = (
            "badge badge-high"   if "high"   in level.lower() else
            "badge badge-medium" if "medium" in level.lower() else
            "badge badge-low"
        )
        render_html(f"""
<div class="card card-accent-blue" style="margin-bottom:10px;">
<div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;">
Based on your latest prediction
</div>
<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
<span style="font-size:15px;font-weight:700;color:{get_course_color(course)};">{course}</span>
<span class="{badge_cls}">{level}</span>
</div>
</div>
""")
        render_html(f'<div class="section-h2" style="color:{color};">{level} — Action Plan</div>')
        render_html(_tips_panel_html(TIPS.get(level, TIPS["Medium Risk"]), color))
    else:
        # Show all three categories collapsed
        df = None
        if os.path.exists(RAW_PATH):
            df = pd.read_csv(RAW_PATH)

        # Build overall risk distribution hint
        if df is not None and "risk_level" in df.columns:
            dist = df["risk_level"].value_counts(normalize=True) * 100
            high_pct = dist.get("High Risk", 0)
            dominant = "High Risk" if high_pct > 40 else ("Medium Risk" if high_pct > 20 else "Low Risk")
        else:
            dominant = "Medium Risk"

        color_dom = (
            "#DC2626" if "high"   in dominant.lower() else
            "#F59E0B" if "medium" in dominant.lower() else
            "#22C55E"
        )

        render_html(f"""
<div class="card" style="margin-bottom:10px;">
<div style="font-size:13px;color:#64748B;">
Run a <strong style="color:#93C5FD;">Risk Prediction</strong> first to get personalised recommendations.
Showing general tips for <span style="color:{color_dom};font-weight:700;">{dominant}</span> based on dataset patterns.
</div>
</div>
""")

        tab_high, tab_mid, tab_low = st.tabs(["🔴 High Risk", "🟡 Medium Risk", "🟢 Low Risk"])
        with tab_high:
            render_html(_tips_panel_html(TIPS["High Risk"], "#DC2626"))
        with tab_mid:
            render_html(_tips_panel_html(TIPS["Medium Risk"], "#F59E0B"))
        with tab_low:
            render_html(_tips_panel_html(TIPS["Low Risk"], "#22C55E"))

    render_html('<div class="section-h2 section-h2--follow">Universal Study Science</div>')
    render_html('<div class="page-sub">Evidence-based techniques that benefit students at every risk level</div>')
    general_rows = "".join(
        f"""
<div class="panel-row" style="display:flex;align-items:flex-start;gap:8px;border-bottom:1px solid #273449;">
<div style="font-size:18px;flex-shrink:0;">{icon}</div>
<div>
<div style="font-size:13px;font-weight:700;color:#F1F5F9;">{title}</div>
<div style="font-size:12px;color:#64748B;margin-top:2px;line-height:1.4;">{body}</div>
</div>
</div>
"""
        for icon, title, body in GENERAL_TIPS
    )
    render_html(f'<div class="card list-panel list-panel--rec">{general_rows}</div>')
