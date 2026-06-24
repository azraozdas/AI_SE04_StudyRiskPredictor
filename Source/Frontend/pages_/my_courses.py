"""My Courses page — add, view, delete, and predict risk for personal courses."""

import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from course_colors import get_course_color
from utils import render_html

_LEVELS = ["Low", "Medium", "High"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _next_id(courses: list) -> int:
    return max((c.get("id", 0) for c in courses), default=0) + 1


def _level_color(level: str) -> str:
    return (
        "#DC2626" if level == "High" else
        "#F59E0B" if level == "Medium" else
        "#22C55E"
    )


def _course_card(course: dict, idx: int) -> None:
    """Render one course card with Predict Risk and Delete buttons."""
    name   = course.get("name", "Unnamed")
    diff   = course.get("difficulty", "Medium")
    wl     = course.get("workload", "Medium")
    hrs    = course.get("study_hours", 0)
    att    = course.get("attendance", 0)
    dl     = course.get("deadline_days", 0)
    grade  = course.get("pass_grade", 0)
    instr  = course.get("instructor", "")
    notes  = course.get("notes", "")
    cid    = course.get("id", idx)
    cc     = get_course_color(name)
    dc     = _level_color(diff)
    wc     = _level_color(wl)

    instr_line = f'<div style="font-size:11px;color:#94A3B8;margin-top:2px;">👤 {instr}</div>' if instr else ""
    notes_line = f'<div style="font-size:11px;color:#64748B;margin-top:4px;font-style:italic;">📝 {notes[:80]}</div>' if notes else ""

    render_html(f"""
<div class="card" style="border-left:3px solid {cc};padding:14px 16px 10px;">
<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px;flex-wrap:wrap;">
<div style="flex:1;min-width:0;">
<div style="font-size:15px;font-weight:800;color:{cc};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{name}</div>
{instr_line}
<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:6px;">
<span class="badge" style="background:{dc}22;color:{dc};border:1px solid {dc}55;">Difficulty: {diff}</span>
<span class="badge" style="background:{wc}22;color:{wc};border:1px solid {wc}55;">Workload: {wl}</span>
</div>
<div style="font-size:11px;color:#64748B;margin-top:6px;">
{hrs}h/wk &nbsp;·&nbsp; {att}% attendance &nbsp;·&nbsp; Deadline in {dl} days &nbsp;·&nbsp; Grade: {grade}%
</div>
{notes_line}
</div>
</div>
</div>
""")

    btn_col1, btn_col2, _ = st.columns([1, 1, 2])
    with btn_col1:
        if st.button("🎯  Predict Risk", key=f"predict_{cid}_{idx}", use_container_width=True, type="primary"):
            st.session_state.prefill_course = course.copy()
            st.session_state.current_page = "risk"
            st.rerun()
    with btn_col2:
        if st.button("🗑  Delete", key=f"delete_{cid}_{idx}", use_container_width=True):
            st.session_state.user_courses = [
                c for c in st.session_state.user_courses if c.get("id") != cid
            ]
            st.rerun()


# ---------------------------------------------------------------------------
# Add course form
# ---------------------------------------------------------------------------

def _add_course_form() -> None:
    render_html('<div class="section-h2">Add a New Course</div>')

    with st.form("add_course_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Course Name *", placeholder="e.g. Machine Learning")
            difficulty = st.selectbox("Difficulty Level *", _LEVELS, index=1)
            workload   = st.selectbox("Workload Level *",   _LEVELS, index=1)
            instructor = st.text_input("Instructor (optional)", placeholder="e.g. Dr. Smith")

        with col2:
            study_hours   = st.slider("Weekly Study Hours *", 0, 15, 4)
            attendance    = st.slider("Attendance (%) *", 0, 100, 75)
            deadline_days = st.slider("Days Until Deadline *", 0, 60, 14)
            pass_grade    = st.slider("Current / Pass Grade (%) *", 0, 100, 70)

        notes = st.text_area("Notes (optional)", placeholder="Any extra info about this course...", height=68)

        submitted = st.form_submit_button("➕  Add Course", type="primary", use_container_width=True)

    if submitted:
        name = (name or "").strip()
        if not name:
            st.error("Course name is required.")
            return

        existing_names = [c.get("name", "").lower() for c in st.session_state.user_courses]
        if name.lower() in existing_names:
            st.warning(f'You already have a course named "{name}". Choose a different name.')
            return

        new_course = {
            "id":            _next_id(st.session_state.user_courses),
            "name":          name,
            "instructor":    instructor.strip() if instructor else "",
            "difficulty":    difficulty,
            "workload":      workload,
            "study_hours":   study_hours,
            "attendance":    attendance,
            "deadline_days": deadline_days,
            "pass_grade":    pass_grade,
            "notes":         (notes or "").strip(),
        }
        st.session_state.user_courses.append(new_course)
        # TODO: replace with db.create_course(st.session_state.user_id, ...) — Selim
        st.success(f'"{name}" added successfully!')
        st.rerun()


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render() -> None:
    render_html('<div class="page-h1">My Courses</div>')
    render_html('<div class="page-sub">Add and manage your enrolled courses, then predict risk from here</div>')

    # TODO: load courses from Supabase on first render — Selim
    # if st.session_state.get("user_id") and not st.session_state.get("_courses_loaded"):
    #     from db import get_user_courses
    #     st.session_state.user_courses = [dict(zip(...), row) for row in get_user_courses(user_id)]
    #     st.session_state._courses_loaded = True

    _add_course_form()

    courses = st.session_state.get("user_courses", [])

    render_html(f'<div class="section-h2 section-h2--follow">Your Courses ({len(courses)})</div>')

    if not courses:
        render_html("""
<div class="card" style="text-align:center;padding:28px 16px;color:#64748B;">
<div style="font-size:28px;margin-bottom:8px;">📂</div>
<div style="font-size:14px;">No courses added yet. Use the form above to add your first course.</div>
</div>
""")
        return

    for idx, course in enumerate(courses):
        _course_card(course, idx)
