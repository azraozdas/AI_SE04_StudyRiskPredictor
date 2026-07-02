"""Profile page — user information, academic settings, and sign-out."""

import os
import sys

import streamlit as st

_FRONTEND = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _FRONTEND not in sys.path:
    sys.path.insert(0, _FRONTEND)

from course_colors import get_course_color
from utils import ROOT, render_html, clear_auth_session, save_auth_session

_BACKEND = os.path.join(ROOT, "Source", "Backend")
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)

from db import get_user_profile, update_user_profile, get_user_predictions  # noqa: E402

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


def _load_profile_from_db() -> None:
    """Fetch profile from Supabase and merge into session state."""
    user_id = st.session_state.get("user_id")
    if not user_id:
        return
    try:
        profile = get_user_profile(user_id)
        if profile:
            if profile.get("full_name"):
                st.session_state.full_name = profile["full_name"]
            if profile.get("university"):
                st.session_state.profile_university = profile["university"]
            if profile.get("department"):
                st.session_state.profile_department = profile["department"]
            if profile.get("semester"):
                st.session_state.profile_semester = profile["semester"]
            if profile.get("target_gpa") is not None:
                st.session_state.profile_target_gpa = profile["target_gpa"]
    except Exception:
        pass


def render() -> None:
    render_html('<div class="page-h1">Profile</div>')
    render_html('<div class="page-sub">Manage your academic profile and account settings</div>')

    # Load from DB once per session
    if not st.session_state.get("_profile_loaded"):
        _load_profile_from_db()
        st.session_state._profile_loaded = True

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

    user_id = st.session_state.get("user_id")
    history_count = 0
    if user_id:
        try:
            history = get_user_predictions(user_id, limit=100)
            history_count = len(history)
        except Exception:
            history_count = 1 if pred else 0

    c1, c2, c3 = st.columns(3)
    with c1:
        render_html(_stat_card("Total Courses", str(total_courses), "#3B82F6"))
    with c2:
        render_html(_stat_card("Total Predictions", str(history_count), "#6366F1"))
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

    new_dept    = st.selectbox("Department", DEPARTMENTS, index=dept_idx, key="profile_dept_sel")
    new_sem     = st.selectbox("Semester",   SEMESTERS,   index=sem_idx,  key="profile_sem_sel")

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
            new_name_clean = new_name.strip()
            try:
                new_gpa = float(new_gpa_str) if new_gpa_str.strip() else None
            except ValueError:
                new_gpa = None

            # Persist to Supabase
            if user_id:
                try:
                    update_user_profile(
                        user_id,
                        full_name=new_name_clean or None,
                        university=new_university.strip() or None,
                        department=new_dept,
                        semester=new_sem,
                        target_gpa=new_gpa,
                    )
                except Exception:
                    st.warning("Could not save to database — changes saved to session only.")

            # Always update session state
            if new_name_clean:
                st.session_state.full_name = new_name_clean
            st.session_state.profile_department  = new_dept
            st.session_state.profile_semester    = new_sem
            st.session_state.profile_university  = new_university.strip()
            st.session_state.profile_target_gpa  = new_gpa
            save_auth_session()
            st.success("Profile updated.")

    with col_reset:
        if st.button("Reset Prediction", use_container_width=True):
            st.session_state.prediction_result = None
            st.session_state.selected_course   = None
            st.info("Prediction data cleared.")

    # ── Prediction History (unified: DB with session fallback) ──────────────
    render_html('<div class="section-h2 section-h2--follow">Prediction History</div>')

    history_rows: list[dict] = []
    if user_id:
        try:
            db_hist = get_user_predictions(user_id, limit=100)
            history_rows = [
                {
                    "course":     h.get("course_name") or "—",
                    "risk_level": h.get("risk_level", "Unknown"),
                    "created_at": (
                        h["created_at"].strftime("%d %b %Y %H:%M")
                        if h.get("created_at") else ""
                    ),
                }
                for h in db_hist
            ]
        except Exception:
            pass  # DB offline — fall through to session fallback

    # Fall back to in-session history when DB is unavailable
    if not history_rows:
        sess_hist = st.session_state.get("prediction_history", [])
        history_rows = [
            {
                "course":     e.get("course", "—"),
                "risk_level": e.get("risk_level", "Unknown"),
                "created_at": e.get("created_at", ""),
            }
            for e in reversed(sess_hist)
        ]

    if not history_rows:
        render_html("""
<div class="card" style="text-align:center;padding:28px 16px;color:#64748B;">
<div style="font-size:28px;margin-bottom:8px;">📊</div>
<div style="font-size:13px;color:#94A3B8;">
No predictions yet. Run a risk prediction on any course to see your history here.
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
        for entry in history_rows:
            c_name  = entry["course"]
            c_risk  = entry["risk_level"]
            c_date  = entry["created_at"]
            lkey    = c_risk.lower()
            border, text = next(
                (v for k, v in _risk_color_map.items() if k in lkey),
                ("#64748B", "#94A3B8"),
            )
            cc = get_course_color(c_name)
            date_line = f'<div style="font-size:10px;color:#475569;margin-top:1px;">{c_date}</div>' if c_date else ""
            rows_html += f"""
<div class="panel-row" style="display:flex;align-items:center;gap:10px;
border-bottom:1px solid #273449;flex-wrap:wrap;">
<div style="flex:1;min-width:120px;">
<div style="font-size:13px;font-weight:700;color:{cc};">{c_name}</div>
{date_line}
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
