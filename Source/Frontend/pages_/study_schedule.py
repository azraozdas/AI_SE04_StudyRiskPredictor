"""Study Schedule page — AI-generated weekly study plan."""

import os
import sys

import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from course_colors import course_color_bg, get_course_color
from utils import ROOT, render_html

RAW_PATH = os.path.join(ROOT, "Data", "student_study_data.csv")

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Hours allocated per risk level
RISK_HOURS = {"High Risk": 4, "Medium Risk": 2.5, "Low Risk": 1.5}

RISK_COLOR = {
    "High Risk":   "#DC2626",
    "Medium Risk": "#F59E0B",
    "Low Risk":    "#22C55E",
}

RISK_BG = {
    "High Risk":   "rgba(220,38,38,0.08)",
    "Medium Risk": "rgba(245,158,11,0.08)",
    "Low Risk":    "rgba(34,197,94,0.08)",
}


def _load() -> pd.DataFrame | None:
    if os.path.exists(RAW_PATH):
        return pd.read_csv(RAW_PATH)
    return None


def _build_schedule(courses: list[dict]) -> dict[str, list[dict]]:
    """Distribute course study blocks across the week."""
    schedule: dict[str, list[dict]] = {d: [] for d in DAYS}
    day_idx = 0
    for c in courses:
        hrs = RISK_HOURS.get(c["risk"], 2.0)
        # Spread large blocks across two days
        if hrs >= 3:
            schedule[DAYS[day_idx % 7]].append({**c, "hours": hrs / 2, "label": "Part 1"})
            day_idx += 1
            schedule[DAYS[day_idx % 7]].append({**c, "hours": hrs / 2, "label": "Part 2"})
        else:
            schedule[DAYS[day_idx % 7]].append({**c, "hours": hrs, "label": ""})
        day_idx += 1
    return schedule


def _day_card(day: str, blocks: list[dict]) -> str:
    if not blocks:
        body = (
            '<div style="font-size:12px;color:#475569;padding:2px 0;">'
            'Rest day — recovery is part of learning.'
            '</div>'
        )
    else:
        rows = ""
        for b in blocks:
            cc     = get_course_color(b["course"])
            cbg    = course_color_bg(b["course"])
            label  = f" · {b['label']}" if b["label"] else ""
            rows += f"""
<div style="background:{cbg};border-left:3px solid {cc};border-radius:5px;
padding:5px 8px;margin-bottom:4px;">
<div style="font-size:11px;font-weight:700;color:{cc};line-height:1.35;">{b['course']}{label}</div>
<div style="font-size:10px;color:#64748B;margin-top:2px;line-height:1.25;">{b['hours']:.1f}h · {b['risk']}</div>
</div>
"""
        body = f'<div class="schedule-day-blocks">{rows}</div>'

    return f"""
<div class="card schedule-day-card">
<div style="font-size:12px;font-weight:700;color:#64748B;text-transform:uppercase;
letter-spacing:0.1em;margin-bottom:4px;">{day}</div>
{body}
</div>
"""


def render() -> None:
    render_html('<div class="page-h1">Study Schedule</div>')
    render_html('<div class="page-sub">AI-generated weekly plan based on course risk levels and deadlines</div>')

    df = _load()
    if df is None or df.empty:
        st.warning("Dataset not found. Place `student_study_data.csv` in the `Data/` folder.")
        return

    # Build course list from dataset
    courses_raw: list[dict] = []
    if "course" in df.columns:
        agg: dict = {}
        if "risk_level" in df.columns:
            risk_mode = df.groupby("course")["risk_level"].agg(
                lambda x: x.value_counts().idxmax()
            )
        else:
            risk_mode = pd.Series(dtype=str)

        if "deadline_days" in df.columns:
            deadline_avg = df.groupby("course")["deadline_days"].mean()
        else:
            deadline_avg = pd.Series(dtype=float)

        for course_name in sorted(df["course"].unique()):
            risk = risk_mode.get(course_name, "Medium Risk")
            days = int(deadline_avg.get(course_name, 7))
            courses_raw.append({"course": course_name, "risk": risk, "deadline": days})

    # Sort by deadline urgency then risk severity
    risk_order = {"High Risk": 0, "Medium Risk": 1, "Low Risk": 2}
    courses_raw.sort(key=lambda c: (risk_order.get(c["risk"], 1), c["deadline"]))

    # Controls (anchor for scoped alignment / date-input styling)
    render_html('<span id="schedule-controls" aria-hidden="true"></span>')
    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        week_start = st.date_input("Week starting", key="schedule_week")
    with col_ctrl2:
        focus = st.selectbox(
            "Focus filter",
            ["All courses", "High Risk only", "Medium & High Risk"],
            key="schedule_focus",
        )

    if focus == "High Risk only":
        courses_filtered = [c for c in courses_raw if c["risk"] == "High Risk"]
    elif focus == "Medium & High Risk":
        courses_filtered = [c for c in courses_raw if c["risk"] in ("High Risk", "Medium Risk")]
    else:
        courses_filtered = courses_raw

    if not courses_filtered:
        st.info("No courses match the selected filter.")
        return

    schedule = _build_schedule(courses_filtered)

    # Summary banner
    total_hrs = sum(
        RISK_HOURS.get(c["risk"], 2.0)
        for c in courses_filtered
    )
    high_n  = sum(1 for c in courses_filtered if c["risk"] == "High Risk")
    mid_n   = sum(1 for c in courses_filtered if c["risk"] == "Medium Risk")
    low_n   = sum(1 for c in courses_filtered if c["risk"] == "Low Risk")

    render_html(f"""
<div class="card card-accent-blue schedule-summary" style="display:flex;gap:10px;flex-wrap:nowrap;align-items:center;">
<div>
<div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:0.1em;">This Week</div>
<div style="font-size:28px;font-weight:800;color:#F8FAFC;line-height:1.1;">{total_hrs:.0f}h</div>
<div style="font-size:12px;color:#64748B;">total study time</div>
</div>
<div style="display:flex;gap:20px;flex-wrap:wrap;">
<div style="text-align:center;">
<div style="font-size:20px;font-weight:800;color:#FCA5A5;">{high_n}</div>
<div style="font-size:10px;font-weight:700;color:#64748B;text-transform:uppercase;">High Risk</div>
</div>
<div style="text-align:center;">
<div style="font-size:20px;font-weight:800;color:#FCD34D;">{mid_n}</div>
<div style="font-size:10px;font-weight:700;color:#64748B;text-transform:uppercase;">Medium Risk</div>
</div>
<div style="text-align:center;">
<div style="font-size:20px;font-weight:800;color:#86EFAC;">{low_n}</div>
<div style="font-size:10px;font-weight:700;color:#64748B;text-transform:uppercase;">Low Risk</div>
</div>
</div>
</div>
""")

    # Calendar grid — single row (7 days) to fit laptop viewport
    day_cols = st.columns(7)
    for col, day in zip(day_cols, DAYS):
        with col:
            render_html(_day_card(day, schedule[day]))

    render_html("""
<div class="card" style="margin-top:8px;">
<div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:3px;">Study Tips</div>
<div style="font-size:13px;color:#94A3B8;line-height:1.4;">
High-risk sessions are placed earlier in the week when cognitive energy is highest.
Rest days are intentional — sleep consolidates memory and improves recall.
Adjust session length based on your personal focus capacity.
</div>
</div>
""")
