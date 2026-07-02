"""My Courses page — add, view, edit, delete, and predict risk for personal courses."""

import os
import sys

import streamlit as st

_FRONTEND = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _FRONTEND not in sys.path:
    sys.path.insert(0, _FRONTEND)

from course_colors import course_color_bg, get_course_color
from utils import ROOT, render_html

_BACKEND = os.path.join(ROOT, "Source", "Backend")
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)

from db import create_course, delete_course, get_user_courses, update_course  # noqa: E402

_LEVELS = ["Low", "Medium", "High"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _navigate(page: str) -> None:
    st.session_state.current_page = page
    st.rerun()


def _next_id(courses: list) -> int:
    return max((c.get("id", 0) for c in courses), default=0) + 1


def _level_color(level: str) -> str:
    return (
        "#DC2626" if level == "High" else
        "#F59E0B" if level == "Medium" else
        "#22C55E"
    )


def _risk_color(level: str) -> str:
    l = str(level).lower()
    if "high"   in l: return "#DC2626"
    if "medium" in l: return "#F59E0B"
    if "low"    in l: return "#22C55E"
    return "#64748B"


def _risk_badge_html(risk_level: str | None) -> str:
    if not risk_level:
        return '<span class="badge" style="background:#1E293B;color:#475569;border:1px solid #334155;">No prediction</span>'
    rc = _risk_color(risk_level)
    return (
        f'<span class="badge" style="background:{rc}22;color:{rc};'
        f'border:1px solid {rc}55;">{risk_level}</span>'
    )


def _load_courses_from_db() -> None:
    """Fetch courses from Supabase and store in session state."""
    user_id = st.session_state.get("user_id")
    if not user_id:
        return
    try:
        st.session_state.user_courses = get_user_courses(user_id)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Course card renderer
# ---------------------------------------------------------------------------

def _course_card(course: dict, idx: int) -> None:
    name    = course.get("name", "Unnamed")
    diff    = course.get("assignment_difficulty") or course.get("difficulty", "Medium")
    wl      = course.get("workload_level") or course.get("workload", "Medium")
    hrs     = course.get("study_hours", 0)
    att     = course.get("attendance", 0)
    dl      = course.get("deadline_days", 0)
    grade   = course.get("pass_grade", 0)
    instr   = course.get("instructor", "")
    notes   = course.get("notes", "")
    risk_lv = course.get("risk_level")
    cid     = course.get("id", idx)
    cc      = get_course_color(name)
    cbg     = course_color_bg(name)
    dc      = _level_color(diff)
    wc      = _level_color(wl)

    instr_line = (
        f'<div style="font-size:11px;color:#94A3B8;margin-top:2px;">👤 {instr}</div>'
        if instr else ""
    )
    notes_line = (
        f'<div style="font-size:11px;color:#64748B;margin-top:4px;font-style:italic;">'
        f'📝 {str(notes)[:90]}{"…" if len(str(notes)) > 90 else ""}</div>'
        if notes else ""
    )

    render_html(f"""
<div class="card" style="border-left:4px solid {cc};padding:14px 16px 10px;
background:linear-gradient(135deg,{cbg} 0%,rgba(15,23,42,0) 60%);">
<div style="display:flex;align-items:flex-start;justify-content:space-between;
gap:8px;flex-wrap:wrap;">
<div style="flex:1;min-width:0;">
<div style="font-size:16px;font-weight:800;color:{cc};
white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{name}</div>
{instr_line}
<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:6px;align-items:center;">
<span class="badge" style="background:{dc}22;color:{dc};border:1px solid {dc}55;">
Difficulty: {diff}</span>
<span class="badge" style="background:{wc}22;color:{wc};border:1px solid {wc}55;">
Workload: {wl}</span>
{_risk_badge_html(risk_lv)}
</div>
<div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:8px;">
<div style="text-align:center;">
<div style="font-size:15px;font-weight:800;color:#F8FAFC;">{hrs}h</div>
<div style="font-size:10px;color:#64748B;text-transform:uppercase;">Study/wk</div>
</div>
<div style="text-align:center;">
<div style="font-size:15px;font-weight:800;color:#F8FAFC;">{att}%</div>
<div style="font-size:10px;color:#64748B;text-transform:uppercase;">Attendance</div>
</div>
<div style="text-align:center;">
<div style="font-size:15px;font-weight:800;color:#F8FAFC;">{dl}d</div>
<div style="font-size:10px;color:#64748B;text-transform:uppercase;">Deadline</div>
</div>
<div style="text-align:center;">
<div style="font-size:15px;font-weight:800;color:#F8FAFC;">{grade}%</div>
<div style="font-size:10px;color:#64748B;text-transform:uppercase;">Grade</div>
</div>
</div>
{notes_line}
</div>
</div>
</div>
""")

    btn1, btn2, btn3 = st.columns([1.2, 1, 1])
    with btn1:
        if st.button(
            "🎯  Predict Risk", key=f"predict_{cid}_{idx}",
            use_container_width=True, type="primary",
        ):
            st.session_state.prefill_course = course.copy()
            _navigate("risk")
    with btn2:
        edit_key   = f"_editing_{cid}"
        edit_label = "✕  Cancel" if st.session_state.get(edit_key) else "✏️  Edit"
        if st.button(edit_label, key=f"edit_toggle_{cid}_{idx}", use_container_width=True):
            st.session_state[edit_key] = not st.session_state.get(edit_key, False)
            st.rerun()
    with btn3:
        if st.button("🗑  Delete", key=f"delete_{cid}_{idx}", use_container_width=True):
            user_id = st.session_state.get("user_id")
            deleted = False
            if user_id and cid:
                try:
                    deleted = delete_course(cid, user_id)
                except Exception:
                    pass
            if deleted or not user_id:
                st.session_state.user_courses = [
                    c for c in st.session_state.user_courses if c.get("id") != cid
                ]
                sched = st.session_state.get("schedule_assignments", {})
                sched.pop(name, None)
                st.session_state.schedule_assignments = sched
            st.rerun()

    # ── Inline edit form ─────────────────────────────────────────────────────
    if st.session_state.get(f"_editing_{cid}"):
        with st.form(key=f"edit_form_{cid}_{idx}"):
            render_html('<div style="font-size:13px;font-weight:700;color:#93C5FD;margin-bottom:8px;">✏️ Edit Course</div>')
            ec1, ec2 = st.columns(2)
            with ec1:
                e_name  = st.text_input("Course Name *", value=name)
                e_diff  = st.selectbox("Difficulty", _LEVELS,
                                       index=_LEVELS.index(diff) if diff in _LEVELS else 1)
                e_wl    = st.selectbox("Workload", _LEVELS,
                                       index=_LEVELS.index(wl) if wl in _LEVELS else 1)
                e_instr = st.text_input("Instructor", value=instr)
            with ec2:
                e_hrs   = st.slider("Study Hours/wk", 0, 15, int(hrs))
                e_att   = st.slider("Attendance (%)", 0, 100, int(att))
                e_dl    = st.slider("Days Until Deadline", 0, 60, min(int(dl), 60))
                e_grade = st.slider("Current Grade (%)", 0, 100, int(grade))
            e_notes = st.text_area("Notes", value=notes, height=60)
            save_col, _ = st.columns([1, 2])
            with save_col:
                saved = st.form_submit_button("💾  Save Changes", type="primary")
            if saved:
                e_name = (e_name or "").strip()
                if not e_name:
                    st.error("Course name cannot be empty.")
                else:
                    user_id = st.session_state.get("user_id")
                    if user_id:
                        try:
                            update_course(
                                course_id=cid,
                                user_id=user_id,
                                name=e_name,
                                difficulty=e_diff,
                                workload=e_wl,
                                study_hours=e_hrs,
                                attendance=e_att,
                                deadline_days=e_dl,
                                pass_grade=e_grade,
                                instructor=e_instr,
                                notes=e_notes.strip(),
                            )
                        except ValueError as ve:
                            st.error(str(ve))
                            st.stop()
                        except Exception:
                            pass
                    for c in st.session_state.user_courses:
                        if c.get("id") == cid:
                            c["name"]                  = e_name
                            c["assignment_difficulty"] = e_diff
                            c["difficulty"]            = e_diff
                            c["workload_level"]        = e_wl
                            c["workload"]              = e_wl
                            c["instructor"]            = e_instr
                            c["study_hours"]           = e_hrs
                            c["attendance"]            = e_att
                            c["deadline_days"]         = e_dl
                            c["pass_grade"]            = e_grade
                            c["notes"]                 = e_notes.strip()
                            break
                    st.session_state[f"_editing_{cid}"] = False
                    st.success(f'"{e_name}" updated.')
                    st.rerun()


# ---------------------------------------------------------------------------
# Add course form
# ---------------------------------------------------------------------------

def _add_course_form() -> None:
    render_html('<div class="section-h2">Add a New Course</div>')

    with st.form("add_course_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name  = st.text_input("Course Name *", placeholder="e.g. Machine Learning, IT Security…")
            diff  = st.selectbox("Assignment Difficulty *", _LEVELS, index=1)
            wl    = st.selectbox("Workload Level *",        _LEVELS, index=1)
            instr = st.text_input("Instructor (optional)", placeholder="e.g. Dr. Smith")
        with col2:
            hrs   = st.slider("Weekly Study Hours *",       0, 15, 4)
            att   = st.slider("Attendance (%) *",           0, 100, 75)
            dl    = st.slider("Days Until Deadline *",      0, 60, 14)
            grade = st.slider("Current / Pass Grade (%) *", 0, 100, 70)
        notes = st.text_area(
            "Notes (optional)",
            placeholder="e.g. Focus on chapters 3–5, exam on Friday…",
            height=68,
        )
        submitted = st.form_submit_button("➕  Add Course", type="primary", use_container_width=True)

    if submitted:
        name = (name or "").strip()
        if not name:
            st.error("Course name is required.")
            return
        existing_lower = [c.get("name", "").lower() for c in st.session_state.user_courses]
        if name.lower() in existing_lower:
            st.warning(f'A course named "{name}" already exists. Use a different name.')
            return

        user_id    = st.session_state.get("user_id")
        new_course = None

        if user_id:
            try:
                course_id = create_course(
                    user_id=user_id,
                    name=name,
                    difficulty=diff,
                    workload=wl,
                    study_hours=hrs,
                    attendance=att,
                    deadline_days=dl,
                    pass_grade=grade,
                    instructor=instr.strip() if instr else "",
                    notes=(notes or "").strip(),
                )
                new_course = {
                    "id":                    course_id,
                    "user_id":               user_id,
                    "name":                  name,
                    "instructor":            instr.strip() if instr else "",
                    "assignment_difficulty": diff,
                    "difficulty":            diff,
                    "workload_level":        wl,
                    "workload":              wl,
                    "study_hours":           hrs,
                    "attendance":            att,
                    "deadline_days":         dl,
                    "pass_grade":            grade,
                    "notes":                 (notes or "").strip(),
                    "risk_level":            None,
                }
            except ValueError as e:
                st.warning(str(e))
                return
            except Exception as exc:
                _msg = str(exc).lower()
                if "enotfound" in _msg or "tenant" in _msg or "nodename" in _msg:
                    st.error("Database is paused. Go to supabase.com/dashboard and restore the project.")
                else:
                    st.error(f"Could not save course to database: {exc}")
                return
        else:
            new_course = {
                "id":                    _next_id(st.session_state.user_courses),
                "name":                  name,
                "instructor":            instr.strip() if instr else "",
                "assignment_difficulty": diff,
                "difficulty":            diff,
                "workload_level":        wl,
                "workload":              wl,
                "study_hours":           hrs,
                "attendance":            att,
                "deadline_days":         dl,
                "pass_grade":            grade,
                "notes":                 (notes or "").strip(),
                "risk_level":            None,
            }

        st.session_state.user_courses.append(new_course)
        st.success(f'✅ "{name}" added successfully!')
        st.rerun()


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render() -> None:
    render_html('<div class="page-h1">My Courses</div>')
    render_html(
        '<div class="page-sub">Add and manage your enrolled courses — '
        'then predict risk directly from each card.</div>'
    )

    if not st.session_state.get("_courses_loaded"):
        _load_courses_from_db()
        st.session_state._courses_loaded = True

    _add_course_form()

    courses = st.session_state.get("user_courses", [])

    render_html(
        f'<div class="section-h2 section-h2--follow">'
        f'Your Courses ({len(courses)})</div>'
    )

    if not courses:
        render_html("""
<div class="card" style="text-align:center;padding:32px 16px;color:#64748B;">
<div style="font-size:32px;margin-bottom:10px;">📂</div>
<div style="font-size:14px;color:#94A3B8;">
No courses added yet. Fill in the form above to add your first course.
</div>
</div>
""")
        return

    for idx, course in enumerate(courses):
        _course_card(course, idx)

    render_html('<div style="height:8px;"></div>')
    if st.button("🎯  Go to Risk Prediction", use_container_width=True, key="my_courses_risk_nav"):
        _navigate("risk")
