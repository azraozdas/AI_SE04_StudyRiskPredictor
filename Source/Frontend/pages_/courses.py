<<<<<<< HEAD
"""Dataset course stats — aggregated analytics from student_study_data.csv (not user CRUD)."""
=======
"""Courses page — per-user course management (create, view, edit, delete)."""
>>>>>>> 7b5e2eb8716a57dfbd06a107298c4850c204f3e1

import os
import sys

<<<<<<< HEAD
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from course_colors import course_color_bg, get_course_color
from utils import ROOT, render_html

RAW_PATH = os.path.join(ROOT, "Data", "student_study_data.csv")

DIFF_ICONS = {
    "high":   "🔴",
    "medium": "🟡",
    "low":    "🟢",
}


def _load() -> pd.DataFrame | None:
    if os.path.exists(RAW_PATH):
        return pd.read_csv(RAW_PATH)
    return None


def _badge(label: str) -> str:
    l = str(label).lower()
    if "high" in l:
        return f'<span class="badge badge-high">{label}</span>'
    if "medium" in l or "mid" in l:
        return f'<span class="badge badge-medium">{label}</span>'
    return f'<span class="badge badge-low">{label}</span>'


def _progress_bar(pct: float, color: str = "#3B82F6") -> str:
    p = max(0.0, min(100.0, pct))
    return (
        f'<div style="background:#273449;border-radius:4px;height:6px;margin-top:6px;">'
        f'<div style="width:{p:.0f}%;background:{color};height:6px;border-radius:4px;"></div>'
        f'</div>'
    )


def _stat_block(label: str, value: str) -> str:
    return (
        f'<div style="text-align:center;">'
        f'<div style="font-size:18px;font-weight:800;color:#F8FAFC;">{value}</div>'
        f'<div style="font-size:10px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:0.08em;">{label}</div>'
        f'</div>'
    )


def _course_card(name: str, count: int, avg_hrs: float, avg_att: float,
                 top_risk: str, top_diff: str, avg_grade: float) -> str:
    att_color = "#22C55E" if avg_att >= 80 else ("#F59E0B" if avg_att >= 65 else "#DC2626")
    hrs_color = "#22C55E" if avg_hrs >= 6 else ("#F59E0B" if avg_hrs >= 3 else "#DC2626")
    initial = name[0].upper() if name else "C"
    diff_icon = DIFF_ICONS.get(top_diff.lower(), "⚪")
    cc = get_course_color(name)
    cbg = course_color_bg(name)

    return f"""
<div class="card course-card-compact">
<div style="display:flex;align-items:flex-start;gap:12px;">
<div style="width:38px;height:38px;border-radius:12px;background:{cbg};
border:1px solid {cc}40;display:flex;align-items:center;justify-content:center;flex-shrink:0;
font-size:16px;font-weight:800;color:{cc};">{initial}</div>
<div style="flex:1;min-width:0;">
<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px;">
<div class="course-card-title" style="color:{cc};">{name}</div>
{_badge(top_risk)}
</div>
<div style="font-size:11px;color:#64748B;margin-top:2px;">{count} students · Difficulty: {diff_icon} {top_diff}</div>
<div class="course-stats" style="display:flex;gap:16px;margin-top:6px;flex-wrap:wrap;">
{_stat_block("Avg Study", f"{avg_hrs:.1f}h")}
{_stat_block("Attendance", f"{avg_att:.0f}%")}
{_stat_block("Pass Grade", f"{avg_grade:.0f}")}
</div>
<div class="course-bars" style="margin-top:4px;">
<div style="font-size:10px;color:#64748B;margin-bottom:2px;">Study Hours</div>
{_progress_bar(avg_hrs / 15 * 100, hrs_color)}
<div style="font-size:10px;color:#64748B;margin-top:6px;margin-bottom:2px;">Attendance</div>
{_progress_bar(avg_att, att_color)}
</div>
</div>
</div>
</div>
"""


def render() -> None:
    render_html('<div class="page-h1">Dataset Course Stats</div>')
    render_html(
        '<div class="page-sub">Aggregated statistics from the shared training CSV '
        '(<code>Data/student_study_data.csv</code>) — not your personal courses. '
        'Use <strong>My Courses</strong> in the sidebar to add your own subjects.</div>'
    )

    df = _load()
    if df is None or df.empty:
        st.warning("Dataset not found. Place `student_study_data.csv` in the `Data/` folder.")
        return

    if "course" not in df.columns:
        st.warning("No `course` column found in the dataset.")
        return

    # Aggregate per course
    agg: dict = {
        "count": ("course", "size"),
    }
    if "study_hours" in df.columns:
        agg["avg_hrs"] = ("study_hours", "mean")
    if "attendance" in df.columns:
        agg["avg_att"] = ("attendance", "mean")
    if "pass_grade" in df.columns:
        agg["avg_grade"] = ("pass_grade", "mean")

    grouped = df.groupby("course").agg(**agg).reset_index()

    # Top risk per course
    if "risk_level" in df.columns:
        risk_mode = df.groupby("course")["risk_level"].agg(
            lambda x: x.value_counts().idxmax()
        ).reset_index()
        risk_mode.columns = ["course", "top_risk"]
        grouped = grouped.merge(risk_mode, on="course", how="left")
    else:
        grouped["top_risk"] = "Unknown"

    # Top difficulty per course
    if "assignment_difficulty" in df.columns:
        diff_mode = df.groupby("course")["assignment_difficulty"].agg(
            lambda x: x.value_counts().idxmax()
        ).reset_index()
        diff_mode.columns = ["course", "top_diff"]
        grouped = grouped.merge(diff_mode, on="course", how="left")
    else:
        grouped["top_diff"] = "Unknown"

    # Sort high risk first
    risk_order = {"High Risk": 0, "Medium Risk": 1, "Low Risk": 2}
    grouped["_sort"] = grouped["top_risk"].map(risk_order).fillna(3)
    grouped = grouped.sort_values("_sort").drop(columns=["_sort"])

    total_courses = len(grouped)
    high_c = int((grouped["top_risk"].str.lower().str.contains("high", na=False)).sum())
    low_c  = int((grouped["top_risk"].str.lower().str.contains("low", na=False)).sum())

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Courses", total_courses)
    with m2:
        st.metric("High Risk Courses", high_c, delta=f"{high_c/max(total_courses,1)*100:.0f}%")
    with m3:
        st.metric("Low Risk Courses", low_c)

    # Search / filter
    search = st.text_input(
        "Search courses",
        placeholder="Type a course name…",
        key="course_search",
    )
    risk_filter = st.selectbox(
        "Filter by risk",
        ["All", "High Risk", "Medium Risk", "Low Risk"],
        key="course_risk_filter",
    )

    filtered = grouped.copy()
    if search:
        filtered = filtered[filtered["course"].str.contains(search, case=False, na=False)]
    if risk_filter != "All":
        filtered = filtered[filtered["top_risk"] == risk_filter]

    if filtered.empty:
        st.info("No courses match the current filter.")
        return

    cards_html = "".join(
        _course_card(
            name=str(row["course"]),
            count=int(row.get("count", 0)),
            avg_hrs=float(row.get("avg_hrs", 0)),
            avg_att=float(row.get("avg_att", 0)),
            top_risk=str(row.get("top_risk", "Unknown")),
            top_diff=str(row.get("top_diff", "Unknown")),
            avg_grade=float(row.get("avg_grade", 0)),
        )
        for _, row in filtered.iterrows()
    )
    render_html(f'<div class="courses-list">{cards_html}</div>')
=======
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import render_html

_BACKEND = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "Backend",
)
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)

from db import create_course, get_user_courses, update_course, delete_course  # noqa: E402

_DIFFICULTIES = ["Easy", "Medium", "Hard"]
_DIFF_COLOR = {
    "Easy":   ("#22C55E", "rgba(34,197,94,.12)"),
    "Medium": ("#FBBF24", "rgba(251,191,36,.13)"),
    "Hard":   ("#EF4444", "rgba(239,68,68,.12)"),
}


def render():
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please sign in to manage your courses.")
        return

    render_html("""
        <div style="margin-bottom:24px;">
            <div style="font-size:22px;font-weight:800;color:#F8FAFC;letter-spacing:-0.02em;">
                My Courses
            </div>
            <div style="font-size:14px;color:#64748B;margin-top:4px;">
                Track the courses you are enrolled in this semester.
            </div>
        </div>
    """)

    # ── Add course ────────────────────────────────────────────────────────────
    with st.expander("Add a new course", expanded=False):
        with st.form("add_course_form", clear_on_submit=True):
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                new_name = st.text_input("Course Name", placeholder="e.g. Machine Learning")
            with c2:
                new_diff = st.selectbox("Difficulty", _DIFFICULTIES, index=1)
            with c3:
                new_wl = st.number_input("Weekly Hours", min_value=1, max_value=40, value=6)
            if st.form_submit_button("Add Course", type="primary", use_container_width=True):
                name = (new_name or "").strip()
                if not name:
                    st.error("Course name cannot be empty.")
                else:
                    try:
                        create_course(user_id, name, new_diff, int(new_wl))
                        st.success(f'"{name}" added.')
                        st.rerun()
                    except Exception as e:
                        st.error(f"Could not add course: {e}")

    # ── Course list ───────────────────────────────────────────────────────────
    try:
        courses = get_user_courses(user_id)
    except Exception as e:
        st.error(f"Could not load courses: {e}")
        return

    if not courses:
        render_html(
            '<div style="text-align:center;color:#475569;font-size:14px;padding:32px 0;">'
            'No courses yet — add your first course above.</div>'
        )
        return

    render_html(
        f'<div style="color:#64748B;font-size:13px;margin-bottom:12px;">'
        f'{len(courses)} course{"s" if len(courses) != 1 else ""}</div>'
    )

    for course in courses:
        cid, cname, cdiff, cwl, _ = course
        fg, bg = _DIFF_COLOR.get(cdiff or "Medium", ("#94A3B8", "rgba(148,163,184,.1)"))

        col_info, col_edit, col_del = st.columns([6, 1, 1])

        with col_info:
            render_html(
                f'<div style="display:flex;align-items:center;gap:12px;padding:8px 0;">'
                f'<span style="font-weight:700;color:#F1F5F9;font-size:15px;">{cname}</span>'
                f'<span style="padding:2px 10px;border-radius:99px;font-size:12px;'
                f'font-weight:700;color:{fg};background:{bg};">{cdiff or "—"}</span>'
                f'<span style="font-size:12px;color:#64748B;">{cwl or "—"} h/week</span>'
                f'</div>'
            )

        with col_edit:
            if st.button("Edit", key=f"edit_{cid}", use_container_width=True):
                st.session_state[f"_editing_{cid}"] = True

        with col_del:
            if st.button("Delete", key=f"del_{cid}", use_container_width=True):
                try:
                    delete_course(cid, user_id)
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

        if st.session_state.get(f"_editing_{cid}"):
            with st.form(f"edit_form_{cid}"):
                ec1, ec2, ec3 = st.columns([3, 1, 1])
                with ec1:
                    e_name = st.text_input("Name", value=cname, key=f"en_{cid}")
                with ec2:
                    di = _DIFFICULTIES.index(cdiff) if cdiff in _DIFFICULTIES else 1
                    e_diff = st.selectbox("Difficulty", _DIFFICULTIES, index=di, key=f"ed_{cid}")
                with ec3:
                    e_wl = st.number_input(
                        "Hours", min_value=1, max_value=40,
                        value=int(cwl) if cwl else 6, key=f"ew_{cid}"
                    )
                sc1, sc2 = st.columns(2)
                with sc1:
                    save_btn = st.form_submit_button("Save", type="primary", use_container_width=True)
                with sc2:
                    cancel_btn = st.form_submit_button("Cancel", use_container_width=True)

            if save_btn:
                n = (e_name or "").strip()
                if n:
                    try:
                        update_course(cid, user_id, n, e_diff, int(e_wl))
                        st.session_state.pop(f"_editing_{cid}", None)
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
                else:
                    st.error("Name cannot be empty.")

            if cancel_btn:
                st.session_state.pop(f"_editing_{cid}", None)
                st.rerun()

        st.markdown(
            '<hr style="border:none;border-top:1px solid rgba(148,163,184,.08);margin:2px 0;">',
            unsafe_allow_html=True,
        )
>>>>>>> 7b5e2eb8716a57dfbd06a107298c4850c204f3e1
