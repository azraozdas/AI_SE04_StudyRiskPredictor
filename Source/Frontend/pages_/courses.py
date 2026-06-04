"""Courses page — per-user course management (create, view, edit, delete)."""

import os
import sys

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
