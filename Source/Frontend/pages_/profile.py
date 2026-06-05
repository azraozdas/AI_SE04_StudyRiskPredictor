"""Profile page — user information, academic settings, and sign-out."""

import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from course_colors import get_course_color
from utils import ROOT, render_html, clear_auth_session, save_auth_session

DEPARTMENTS = [
    "Computer Science",
    "Software Engineering",
    "Information Technology",
    "Electrical Engineering",
    "Mathematics",
    "Physics",
    "Business Administration",
    "Other",
]

SEMESTERS = [f"Semester {i}" for i in range(1, 9)]


def _avatar_html(initial: str, size: int = 64) -> str:
    return (
        f'<div style="width:{size}px;height:{size}px;border-radius:50%;flex-shrink:0;'
        f'background:linear-gradient(135deg,#3B82F6 0%,#7C3AED 100%);'
        f'display:flex;align-items:center;justify-content:center;'
        f'font-size:{size // 2}px;font-weight:800;color:white;">{initial}</div>'
    )


def _stat_card(label: str, value: str, color: str = "#3B82F6") -> str:
    return (
        f'<div class="kpi-tile" style="text-align:center;">'
        f'<div class="kpi-value" style="color:{color};font-size:26px;">{value}</div>'
        f'<div class="kpi-sub">{label}</div>'
        f'</div>'
    )


def render() -> None:
    render_html('<div class="page-h1">Profile</div>')
    render_html('<div class="page-sub">Manage your academic profile and account settings</div>')

    # Retrieve session values
    full_name  = st.session_state.get("full_name", "") or "Student"
    email      = st.session_state.get("user_email", "")
    initial    = full_name[0].upper() if full_name else "S"
    dept       = st.session_state.get("profile_department", DEPARTMENTS[0])
    sem        = st.session_state.get("profile_semester", SEMESTERS[5])

    # ── Profile header card ──────────────────────────────────────────────────
    render_html(f"""
<div class="card" style="margin-bottom:10px;">
<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
{_avatar_html(initial, 72)}
<div style="flex:1;min-width:0;">
<div style="font-size:22px;font-weight:800;color:#F8FAFC;">{full_name}</div>
<div style="font-size:13px;color:#64748B;margin-top:3px;">{email}</div>
<div style="margin-top:8px;display:flex;gap:8px;flex-wrap:wrap;">
<span class="badge badge-blue">{dept}</span>
<span class="badge badge-blue">{sem}</span>
</div>
</div>
</div>
</div>
""")

    # ── Academic stats ───────────────────────────────────────────────────────
    pred = st.session_state.get("prediction_result")
    pred_level = pred["level"] if pred else "N/A"
    pred_course = pred["course"] if pred else "—"

    c1, c2, c3 = st.columns(3)
    with c1:
        render_html(_stat_card("Last Risk Level", pred_level,
                               "#DC2626" if "high" in pred_level.lower() else
                               "#F59E0B" if "medium" in pred_level.lower() else
                               "#22C55E" if "low" in pred_level.lower() else "#64748B"))
    with c2:
        course_val = pred_course[:16] if pred_course != "—" else "—"
        course_color = get_course_color(pred_course) if pred_course != "—" else "#64748B"
        render_html(_stat_card("Last Course Assessed", course_val, course_color))
    with c3:
        preds_run = 1 if pred else 0
        render_html(_stat_card("Predictions Run", str(preds_run), "#6366F1"))

    render_html('<div class="section-h2 section-h2--follow">Edit Profile</div>')

    new_name = st.text_input("Full Name", value=full_name, key="profile_new_name")

    dept_idx = DEPARTMENTS.index(dept) if dept in DEPARTMENTS else 0
    sem_idx  = SEMESTERS.index(sem)    if sem  in SEMESTERS  else 5

    new_dept = st.selectbox("Department", DEPARTMENTS, index=dept_idx, key="profile_dept_sel")
    new_sem  = st.selectbox("Semester",   SEMESTERS,   index=sem_idx,  key="profile_sem_sel")

    col_save, col_reset = st.columns(2)
    with col_save:
        if st.button("Save Changes", type="primary", use_container_width=True):
            if new_name.strip():
                st.session_state.full_name          = new_name.strip()
            st.session_state.profile_department = new_dept
            st.session_state.profile_semester   = new_sem
            save_auth_session()
            st.success("Profile updated.")
    with col_reset:
        if st.button("Reset Prediction", use_container_width=True):
            st.session_state.prediction_result = None
            st.session_state.selected_course   = None
            st.info("Prediction data cleared.")

    # ── Account section ──────────────────────────────────────────────────────
    render_html('<div class="section-h2 section-h2--follow">Account</div>')

    render_html(f"""
<div class="card" style="margin-bottom:10px;">
<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;">
<div>
<div style="font-size:14px;font-weight:700;color:#F1F5F9;">Signed in as</div>
<div style="font-size:12px;color:#64748B;margin-top:2px;">{email}</div>
</div>
</div>
</div>
""")

    if st.button("Sign Out", use_container_width=False):
        clear_auth_session()
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # ── Team info ────────────────────────────────────────────────────────────
    render_html('<div class="section-h2 section-h2--follow">Project Team</div>')
    render_html("""
<div class="card list-panel list-panel--short">
<div style="display:flex;flex-direction:column;gap:4px;">
<div style="display:flex;align-items:center;gap:12px;">
<div style="width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#3B82F6,#7C3AED);
display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;color:white;flex-shrink:0;">E</div>
<div>
<div style="font-size:13px;font-weight:700;color:#F1F5F9;">Eylül Özekinci</div>
<div style="font-size:11px;color:#64748B;">Machine Learning Model</div>
</div>
</div>
<div style="display:flex;align-items:center;gap:12px;">
<div style="width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#3B82F6,#7C3AED);
display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;color:white;flex-shrink:0;">A</div>
<div>
<div style="font-size:13px;font-weight:700;color:#F1F5F9;">Azra Özdaş</div>
<div style="font-size:11px;color:#3B82F6;">Frontend · Streamlit Dashboard</div>
</div>
</div>
<div style="display:flex;align-items:center;gap:12px;">
<div style="width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#3B82F6,#7C3AED);
display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:white;flex-shrink:0;">M</div>
<div>
<div style="font-size:13px;font-weight:700;color:#F1F5F9;">Müslüm Selim Akşahin</div>
<div style="font-size:11px;color:#64748B;">Data Collection &amp; Preprocessing</div>
</div>
</div>
<div style="display:flex;align-items:center;gap:12px;">
<div style="width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#3B82F6,#7C3AED);
display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:white;flex-shrink:0;">D</div>
<div>
<div style="font-size:13px;font-weight:700;color:#F1F5F9;">Dilay Tarhan</div>
<div style="font-size:11px;color:#64748B;">Testing &amp; Documentation</div>
</div>
</div>
</div>
</div>
""")
