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
    university = st.session_state.get("profile_university", "")
    target_gpa = st.session_state.get("profile_target_gpa", None)

    # ── Profile header card ──────────────────────────────────────────────────
    uni_badge = f'<span class="badge badge-blue">{university}</span>' if university else ""
    gpa_badge = f'<span class="badge badge-blue">GPA goal: {target_gpa}</span>' if target_gpa else ""
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
{uni_badge}
{gpa_badge}
</div>
</div>
</div>
</div>
""")

    # ── Academic stats ───────────────────────────────────────────────────────
    pred          = st.session_state.get("prediction_result")
    pred_level    = pred["level"] if pred else None
    total_courses = len(st.session_state.get("user_courses", []))
    total_preds   = len(st.session_state.get("prediction_history", []))

    c1, c2, c3 = st.columns(3)
    with c1:
        render_html(_stat_card("Total Courses", str(total_courses) if total_courses else "0", "#3B82F6"))
    with c2:
        render_html(_stat_card("Total Predictions", str(total_preds) if total_preds else "0", "#6366F1"))
    with c3:
        if pred_level:
            lvl_color = (
                "#DC2626" if "high"   in pred_level.lower() else
                "#F59E0B" if "medium" in pred_level.lower() else
                "#22C55E"
            )
            render_html(_stat_card("Current Risk Level", pred_level, lvl_color))
        else:
            render_html(_stat_card("Current Risk Level", "No Prediction Yet", "#475569"))

    render_html('<div class="section-h2 section-h2--follow">Edit Profile</div>')

    new_name = st.text_input("Full Name", value=full_name, key="profile_new_name")
    new_university = st.text_input(
        "University / School",
        value=university,
        key="profile_university_input",
        placeholder="e.g. Istanbul University",
    )

    dept_idx = DEPARTMENTS.index(dept) if dept in DEPARTMENTS else 0
    sem_idx  = SEMESTERS.index(sem)    if sem  in SEMESTERS  else 5

    new_dept = st.selectbox("Department", DEPARTMENTS, index=dept_idx, key="profile_dept_sel")
    new_sem  = st.selectbox("Semester",   SEMESTERS,   index=sem_idx,  key="profile_sem_sel")

    gpa_default = str(target_gpa) if target_gpa is not None else ""
    new_gpa_str = st.text_input(
        "Target GPA (optional)",
        value=gpa_default,
        key="profile_gpa_input",
        placeholder="e.g. 3.5",
    )

    col_save, col_reset = st.columns(2)
    with col_save:
        if st.button("Save Changes", type="primary", use_container_width=True):
            if new_name.strip():
                st.session_state.full_name          = new_name.strip()
            st.session_state.profile_department = new_dept
            st.session_state.profile_semester   = new_sem
            st.session_state.profile_university = new_university.strip()
            try:
                st.session_state.profile_target_gpa = float(new_gpa_str) if new_gpa_str.strip() else None
            except ValueError:
                st.session_state.profile_target_gpa = None
            save_auth_session()
            # TODO: persist university + target_gpa to Supabase users table (Selim)
            st.success("Profile updated.")
    with col_reset:
        if st.button("Reset Prediction", use_container_width=True):
            st.session_state.prediction_result = None
            st.session_state.selected_course   = None
            st.info("Prediction data cleared.")

    # ── Prediction History ───────────────────────────────────────────────────
    # TODO (Selim): Load history from db.get_user_predictions(user_id) instead of session_state
    render_html('<div class="section-h2 section-h2--follow">Prediction History</div>')

    history = st.session_state.get("prediction_history", [])
    if not history:
        render_html("""
<div class="card" style="text-align:center;padding:28px 16px;color:#64748B;">
<div style="font-size:28px;margin-bottom:8px;">📊</div>
<div style="font-size:13px;color:#94A3B8;">
No predictions yet this session.
Run a risk prediction on any course to see your history here.
</div>
</div>
""")
    else:
        _risk_color_map = {
            "high":   ("#DC2626", "#FCA5A5"),
            "medium": ("#F59E0B", "#FCD34D"),
            "low":    ("#22C55E", "#86EFAC"),
        }
        rows_html = ""
        for entry in reversed(history):
            c_name  = entry.get("course", "—")
            c_risk  = entry.get("risk_level", "Unknown")
            c_date  = entry.get("created_at", "")
            lkey    = c_risk.lower()
            border, text = next(
                (v for k, v in _risk_color_map.items() if k in lkey),
                ("#64748B", "#94A3B8"),
            )
            cc = get_course_color(c_name)
            rows_html += f"""
<div class="panel-row" style="display:flex;align-items:center;gap:10px;
border-bottom:1px solid #273449;flex-wrap:wrap;">
<div style="flex:1;min-width:120px;">
<div style="font-size:13px;font-weight:700;color:{cc};">{c_name}</div>
{"" if not c_date else f'<div style="font-size:10px;color:#475569;margin-top:1px;">{c_date}</div>'}
</div>
<span class="badge" style="background:{border}22;color:{text};border:1px solid {border}55;">{c_risk}</span>
</div>
"""
        render_html(f'<div class="card list-panel">{rows_html}</div>')

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
