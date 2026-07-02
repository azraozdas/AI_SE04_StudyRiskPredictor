"""Dashboard page — personal homepage with three progressive states."""

import os
import sys

import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from course_colors import get_course_color
from utils import ROOT, render_html

RAW_PATH = os.path.join(ROOT, "Data", "student_study_data.csv")


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _navigate(page: str) -> None:
    st.session_state.current_page = page
    st.rerun()


def _risk_color(level: str) -> str:
    l = str(level).lower()
    if "high" in l:
        return "#DC2626"
    if "medium" in l or "mid" in l:
        return "#F59E0B"
    if "low" in l:
        return "#22C55E"
    return "#64748B"


def _deadline_pill(days: int) -> str:
    if days <= 1:
        return '<span class="pill pill-red">Tomorrow</span>'
    if days <= 4:
        return f'<span class="pill pill-amber">{days}d</span>'
    return f'<span class="pill pill-blue">{days}d</span>'


# ---------------------------------------------------------------------------
# State 1 — Empty (no courses, no predictions)
# ---------------------------------------------------------------------------

def _render_empty_state(full_name: str) -> None:
    render_html(f"""
<div class="card" style="text-align:center;padding:48px 24px 40px;margin-bottom:12px;">
<div style="font-size:52px;margin-bottom:16px;">🎓</div>
<div style="font-size:24px;font-weight:800;color:#F8FAFC;margin-bottom:10px;">
Welcome to Studor, {full_name}!
</div>
<div style="font-size:14px;color:#64748B;max-width:540px;margin:0 auto 28px;line-height:1.7;">
Studor predicts your academic risk using a trained AI model, helps you track your
courses, and builds a personalized weekly study schedule — all in one place.
</div>
<div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:8px;">
<div style="background:#1E293B;border:1px solid #273449;border-radius:10px;
padding:16px 20px;min-width:150px;text-align:center;">
<div style="font-size:24px;margin-bottom:6px;">📚</div>
<div style="font-size:11px;font-weight:700;color:#3B82F6;text-transform:uppercase;
letter-spacing:0.05em;">Step 1</div>
<div style="font-size:13px;color:#94A3B8;margin-top:2px;">Add Your Courses</div>
</div>
<div style="font-size:20px;color:#334155;align-self:center;">→</div>
<div style="background:#1E293B;border:1px solid #273449;border-radius:10px;
padding:16px 20px;min-width:150px;text-align:center;">
<div style="font-size:24px;margin-bottom:6px;">🎯</div>
<div style="font-size:11px;font-weight:700;color:#3B82F6;text-transform:uppercase;
letter-spacing:0.05em;">Step 2</div>
<div style="font-size:13px;color:#94A3B8;margin-top:2px;">Predict Risk Level</div>
</div>
<div style="font-size:20px;color:#334155;align-self:center;">→</div>
<div style="background:#1E293B;border:1px solid #273449;border-radius:10px;
padding:16px 20px;min-width:150px;text-align:center;">
<div style="font-size:24px;margin-bottom:6px;">📅</div>
<div style="font-size:11px;font-weight:700;color:#3B82F6;text-transform:uppercase;
letter-spacing:0.05em;">Step 3</div>
<div style="font-size:13px;color:#94A3B8;margin-top:2px;">Build Your Schedule</div>
</div>
</div>
</div>
""")

    col_a, col_b, col_c = st.columns([1, 1.4, 1])
    with col_b:
        if st.button("➕  Add Your First Course", type="primary", use_container_width=True, key="empty_add_btn"):
            _navigate("my_courses")


# ---------------------------------------------------------------------------
# State 2 — Has courses, no predictions yet
# ---------------------------------------------------------------------------

def _render_has_courses(full_name: str, courses: list) -> None:
    n       = len(courses)
    avg_att = sum(c.get("attendance", 0) for c in courses) / n if n else 0
    avg_hrs = sum(c.get("study_hours", 0) for c in courses) / n if n else 0
    nearest = min((c.get("deadline_days", 999) for c in courses), default=999)

    render_html(
        f'<div class="page-sub">Hi {full_name} — you have {n} course{"s" if n != 1 else ""} '
        f'added. Run a risk prediction to unlock your full dashboard.</div>'
    )

    near_val   = f"{nearest}d" if nearest < 999 else "—"
    near_color = "#DC2626" if nearest <= 3 else ("#F59E0B" if nearest <= 7 else "#94A3B8")
    preds_done = len(st.session_state.get("prediction_history", []))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_html(f"""
<div class="kpi-tile">
<div class="kpi-label">My Courses</div>
<div class="kpi-value" style="color:#3B82F6;">{n}</div>
<div class="kpi-sub">added so far</div>
</div>
""")
    with c2:
        render_html(f"""
<div class="kpi-tile">
<div class="kpi-label">Avg Attendance</div>
<div class="kpi-value" style="color:#22C55E;">{avg_att:.0f}%</div>
<div class="kpi-sub">across your courses</div>
</div>
""")
    with c3:
        render_html(f"""
<div class="kpi-tile">
<div class="kpi-label">Nearest Deadline</div>
<div class="kpi-value" style="color:{near_color};">{near_val}</div>
<div class="kpi-sub">days remaining</div>
</div>
""")
    with c4:
        render_html(f"""
<div class="kpi-tile">
<div class="kpi-label">Predictions Run</div>
<div class="kpi-value" style="color:#6366F1;">{preds_done}</div>
<div class="kpi-sub">this session</div>
</div>
""")

    left, right = st.columns([1.1, 0.9])

    with left:
        render_html('<div class="section-h2 section-h2--follow">My Courses</div>')
        rows_html = ""
        for c in sorted(courses, key=lambda x: x.get("deadline_days", 999)):
            name    = str(c.get("name", ""))[:34]
            dl      = c.get("deadline_days", "?")
            hrs     = c.get("study_hours", 0)
            att     = c.get("attendance", 0)
            diff    = c.get("assignment_difficulty", "—")
            risk_lv = c.get("risk_level")
            cc      = get_course_color(name)
            dc      = "#DC2626" if diff == "High" else "#F59E0B" if diff == "Medium" else "#22C55E"
            if risk_lv:
                rc = _risk_color(risk_lv)
                badge_html = f'<span class="badge" style="background:{rc}22;color:{rc};border:1px solid {rc}55;">{risk_lv}</span>'
            else:
                badge_html = f'<span class="badge" style="background:{dc}22;color:{dc};border:1px solid {dc}55;">{diff}</span>'
            rows_html += f"""
<div class="panel-row" style="display:flex;align-items:center;gap:10px;border-bottom:1px solid #1E293B;">
<div style="flex:1;min-width:0;">
<div style="font-size:13px;font-weight:700;color:{cc};
white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{name}</div>
<div style="font-size:11px;color:#64748B;margin-top:2px;">
{hrs}h/wk · {att}% attendance · deadline in {dl}d
</div>
</div>
{badge_html}
</div>
"""
        render_html(f'<div class="card list-panel list-panel--tall">{rows_html}</div>')

    with right:
        render_html('<div class="section-h2 section-h2--follow">Upcoming Deadlines</div>')
        dl_rows = ""
        for c in sorted(courses, key=lambda x: x.get("deadline_days", 999))[:5]:
            days = int(c.get("deadline_days", 0))
            name = str(c.get("name", ""))[:28]
            cc   = get_course_color(name)
            pill = _deadline_pill(days)
            dl_rows += f"""
<div class="panel-row" style="display:flex;align-items:center;
justify-content:space-between;border-bottom:1px solid #1E293B;">
<div>
<div style="font-size:12px;font-weight:600;color:{cc};">{name}</div>
<div style="margin-top:3px;">{pill}</div>
</div>
<div style="font-size:20px;font-weight:800;color:#94A3B8;">{days}d</div>
</div>
"""
        render_html(f'<div class="card list-panel list-panel--short">{dl_rows}</div>')

        sched_ready = bool(st.session_state.get("schedule_assignments"))
        if sched_ready:
            next_icon, next_msg = "📅", "Your weekly study plan is ready — check your Study Schedule."
        else:
            next_icon, next_msg = "🎯", "Run a risk prediction to unlock your personalized study schedule."
        render_html(f"""
<div class="card" style="margin-top:10px;padding:14px 16px;
border-left:3px solid #3B82F6;background:rgba(59,130,246,0.06);">
<div style="font-size:12px;font-weight:700;color:#93C5FD;margin-bottom:4px;">
⚡ Next Step
</div>
<div style="font-size:13px;color:#94A3B8;line-height:1.5;">{next_icon} {next_msg}</div>
</div>
""")

    render_html('<div class="section-h2 section-h2--follow">Quick Actions</div>')
    qa1, qa2, qa3 = st.columns(3)
    with qa1:
        if st.button("🎯  Predict Risk", type="primary", use_container_width=True, key="state2_risk_btn"):
            _navigate("risk")
    with qa2:
        if st.button("📚  Manage Courses", use_container_width=True, key="state2_courses_btn"):
            _navigate("my_courses")
    with qa3:
        if st.button("📅  Study Schedule", use_container_width=True, key="state2_sched_btn"):
            _navigate("schedule")


# ---------------------------------------------------------------------------
# State 3 — Full personalized dashboard (courses + predictions)
# ---------------------------------------------------------------------------

def _render_full_dashboard(full_name: str, courses: list, pred: dict) -> None:
    render_html(f'<div class="page-sub">Your personal academic overview, {full_name}</div>')

    n            = len(courses)
    high_n       = sum(1 for c in courses if "high"   in str(c.get("risk_level","")).lower())
    medium_n     = sum(1 for c in courses if "medium" in str(c.get("risk_level","")).lower())
    low_n        = sum(1 for c in courses if "low"    in str(c.get("risk_level","")).lower())
    avg_att      = sum(c.get("attendance", 0) for c in courses) / n if n else 0
    nearest      = min((c.get("deadline_days", 999) for c in courses), default=999)
    near_val     = f"{nearest}d" if nearest < 999 else "—"
    near_color   = "#DC2626" if nearest <= 3 else ("#F59E0B" if nearest <= 7 else "#F8FAFC")

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    for col, value, label, sub, color in [
        (c1, str(n),         "My Courses",       "enrolled",         "#3B82F6"),
        (c2, str(high_n),    "High Risk",         "need attention",   "#DC2626"),
        (c3, f"{avg_att:.0f}%", "Avg Attendance", "across courses",   "#22C55E"),
        (c4, near_val,       "Nearest Deadline",  "days remaining",   near_color),
    ]:
        with col:
            render_html(f"""
<div class="kpi-tile">
<div class="kpi-label">{label}</div>
<div class="kpi-value" style="color:{color};">{value}</div>
<div class="kpi-sub">{sub}</div>
</div>
""")

    render_html('<div class="section-spacer"></div>')
    left, right = st.columns([1.1, 0.9])

    with left:
        render_html('<div class="section-h2">My Courses</div>')
        rows_html = ""
        for c in sorted(courses, key=lambda x: x.get("deadline_days", 999)):
            name    = str(c.get("name", ""))[:34]
            dl      = c.get("deadline_days", "?")
            hrs     = c.get("study_hours", 0)
            att     = c.get("attendance", 0)
            risk_lv = c.get("risk_level")
            cc      = get_course_color(name)
            risk_html = ""
            if risk_lv:
                rc = _risk_color(risk_lv)
                risk_html = (
                    f'<span class="badge" style="background:{rc}22;color:{rc};'
                    f'border:1px solid {rc}55;flex-shrink:0;">{risk_lv}</span>'
                )
            rows_html += f"""
<div class="panel-row" style="display:flex;align-items:center;gap:10px;border-bottom:1px solid #1E293B;">
<div style="flex:1;min-width:0;">
<div style="font-size:13px;font-weight:700;color:{cc};
white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{name}</div>
<div style="font-size:11px;color:#64748B;margin-top:2px;">
{hrs}h/wk · {att}% attendance · {dl}d left
</div>
</div>
{risk_html}
</div>
"""
        render_html(f'<div class="card list-panel list-panel--tall">{rows_html}</div>')

    with right:
        render_html('<div class="section-h2">Upcoming Deadlines</div>')
        dl_rows = ""
        for c in sorted(courses, key=lambda x: x.get("deadline_days", 999))[:4]:
            days = int(c.get("deadline_days", 0))
            name = str(c.get("name", ""))[:26]
            cc   = get_course_color(name)
            pill = _deadline_pill(days)
            dl_rows += f"""
<div class="panel-row" style="display:flex;align-items:center;
justify-content:space-between;border-bottom:1px solid #1E293B;">
<div>
<div style="font-size:12px;font-weight:600;color:{cc};">{name}</div>
<div style="margin-top:2px;">{pill}</div>
</div>
<div style="font-size:20px;font-weight:800;color:#94A3B8;">{days}d</div>
</div>
"""
        render_html(f'<div class="card list-panel list-panel--short">{dl_rows}</div>')

        # Last prediction card
        if pred:
            p_level  = pred.get("level", "N/A")
            p_course = pred.get("course", "—")
            p_conf   = pred.get("confidence")
            lvl_color = _risk_color(p_level)
            conf_line = ""
            if p_conf is not None:
                conf_line = f'<div style="font-size:11px;color:#64748B;margin-top:2px;">Confidence: {p_conf*100:.0f}%</div>'
            render_html(f"""
<div class="section-h2 section-h2--follow">Last Prediction</div>
<div class="card" style="border:1px solid {lvl_color}44;
background:{lvl_color}0d;text-align:center;padding:16px;">
<div style="font-size:11px;color:#64748B;text-transform:uppercase;
letter-spacing:0.08em;margin-bottom:4px;">Risk Level</div>
<div style="font-size:26px;font-weight:800;color:{lvl_color};margin:4px 0;">{p_level}</div>
<div style="font-size:12px;color:#64748B;">{p_course}</div>
{conf_line}
</div>
""")

        render_html('<div class="section-h2 section-h2--follow">Quick Actions</div>')
        if st.button("🎯  New Prediction", type="primary", use_container_width=True, key="dash_risk_btn"):
            _navigate("risk")
        if st.button("📅  Study Schedule", use_container_width=True, key="dash_sched_btn"):
            _navigate("schedule")
        if st.button("💡  Recommendations", use_container_width=True, key="dash_rec_btn"):
            _navigate("recommendations")

    # Risk summary row (only when predictions exist)
    if high_n + medium_n + low_n > 0:
        render_html('<div class="section-h2 section-h2--follow">Risk Overview</div>')
        r1, r2, r3 = st.columns(3)
        for col, count, label, color in [
            (r1, high_n,   "High Risk",   "#DC2626"),
            (r2, medium_n, "Medium Risk", "#F59E0B"),
            (r3, low_n,    "Low Risk",    "#22C55E"),
        ]:
            with col:
                render_html(f"""
<div class="kpi-tile" style="text-align:center;">
<div class="kpi-value" style="color:{color};font-size:28px;">{count}</div>
<div class="kpi-sub">{label}</div>
</div>
""")


# ---------------------------------------------------------------------------
# Benchmark expander (always available, collapsed by default)
# ---------------------------------------------------------------------------

def _render_benchmark_expander() -> None:
    with st.expander("📊  Dataset Insights — Training Data Benchmark", expanded=False):
        render_html("""
<div style="font-size:12px;color:#64748B;margin-bottom:10px;padding:8px 10px;
background:rgba(59,130,246,0.06);border-radius:6px;border:1px solid rgba(59,130,246,0.2);">
ℹ️ This section shows statistics from the <strong style="color:#93C5FD;">300-student
training dataset</strong> used to train the ML model — not your personal data.
</div>
""")
        if not os.path.exists(RAW_PATH):
            st.info("Dataset not found. Place `student_study_data.csv` in the `Data/` folder.")
            return
        df = pd.read_csv(RAW_PATH)
        if df.empty:
            return

        total     = len(df)
        avg_att   = df["attendance"].mean()  if "attendance"  in df.columns else 0
        avg_hrs   = df["study_hours"].mean() if "study_hours" in df.columns else 0
        n_courses = df["course"].nunique()   if "course"      in df.columns else 0
        high_c    = 0
        if "risk_level" in df.columns:
            high_c = int(df["risk_level"].astype(str).str.lower().str.contains("high").sum())

        b1, b2, b3, b4 = st.columns(4)
        for col, val, lbl in [
            (b1, str(total),        "Total Students"),
            (b2, f"{avg_hrs:.1f}h", "Avg Study/wk"),
            (b3, f"{avg_att:.0f}%", "Avg Attendance"),
            (b4, str(high_c),       "High Risk Count"),
        ]:
            with col:
                render_html(f"""
<div class="kpi-tile" style="text-align:center;">
<div class="kpi-value" style="font-size:18px;">{val}</div>
<div class="kpi-sub">{lbl}</div>
</div>
""")

        if "risk_level" in df.columns:
            try:
                import plotly.graph_objects as go
                counts = df["risk_level"].value_counts()
                color_map = {"High": "#DC2626", "Medium": "#F59E0B", "Low": "#22C55E"}
                c_list = [color_map.get(l.split()[0] if " " in l else l, "#64748B")
                          for l in counts.index]
                fig = go.Figure(go.Bar(
                    x=counts.index.tolist(),
                    y=counts.values.tolist(),
                    marker_color=c_list,
                    text=counts.values.tolist(),
                    textposition="outside",
                    textfont=dict(color="#94A3B8", size=12),
                ))
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(tickfont=dict(color="#94A3B8", size=12)),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    margin=dict(t=10, b=10, l=6, r=6),
                    height=140,
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            except ImportError:
                pass


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render() -> None:
    render_html('<div class="page-h1">Dashboard</div>')

    full_name    = st.session_state.get("full_name", "") or "Student"
    user_courses = st.session_state.get("user_courses", [])
    pred         = st.session_state.get("prediction_result")

    has_courses    = len(user_courses) > 0
    has_prediction = pred is not None

    if not has_courses:
        _render_empty_state(full_name)
    elif not has_prediction:
        _render_has_courses(full_name, user_courses)
    else:
        _render_full_dashboard(full_name, user_courses, pred)

    _render_benchmark_expander()
