"""Dashboard page — overview of academic health, KPIs, risk distribution, and deadlines."""

import os
import sys

import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from course_colors import get_course_color
from utils import ROOT, render_html

RAW_PATH = os.path.join(ROOT, "Data", "student_study_data.csv")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_data() -> pd.DataFrame | None:
    if os.path.exists(RAW_PATH):
        return pd.read_csv(RAW_PATH)
    return None


def _risk_class(label: str) -> str:
    label = str(label).lower()
    if "high" in label:
        return "badge badge-high"
    if "medium" in label or "mid" in label:
        return "badge badge-medium"
    return "badge badge-low"


def _deadline_pill(days: int) -> str:
    if days <= 1:
        return '<span class="pill pill-red">Tomorrow</span>'
    if days <= 4:
        return f'<span class="pill pill-amber">{days} days</span>'
    return f'<span class="pill pill-blue">{days} days</span>'


# ---------------------------------------------------------------------------
# Section renderers
# ---------------------------------------------------------------------------

def _health_banner(df: pd.DataFrame) -> None:
    avg_att = df["attendance"].mean() if "attendance" in df.columns else 72
    avg_hrs = df["study_hours"].mean() if "study_hours" in df.columns else 5.2
    total = len(df)

    high_count = 0
    if "risk_level" in df.columns:
        rl = df["risk_level"].astype(str).str.lower()
        high_count = int((rl.str.contains("high")).sum())

    health = min(100, max(0, int(
        avg_att * 0.45 + min(avg_hrs / 10.0, 1.0) * 30 +
        (1 - high_count / max(total, 1)) * 25
    )))
    pct_css = f"{health}%"

    render_html(f"""
<div class="health-banner">
<div class="health-gauge" style="background:conic-gradient(#3B82F6 {pct_css},#273449 0%);">
<span class="health-score-num">{health}</span>
</div>
<div>
<div class="health-title">Academic Health Score</div>
<div class="health-desc">Composite of attendance, study hours &amp; risk distribution</div>
</div>
<div class="health-stats">
<div style="text-align:center;">
<div class="health-stat-val">{total:,}</div>
<div class="health-stat-lbl">Students</div>
</div>
<div style="text-align:center;">
<div class="health-stat-val">{avg_hrs:.1f}h</div>
<div class="health-stat-lbl">Avg Study</div>
</div>
<div style="text-align:center;">
<div class="health-stat-val">{avg_att:.0f}%</div>
<div class="health-stat-lbl">Avg Attend.</div>
</div>
<div style="text-align:center;">
<div class="health-stat-val" style="color:#FCA5A5;">{high_count}</div>
<div class="health-stat-lbl">High Risk</div>
</div>
</div>
</div>
""")


def _kpi_row(df: pd.DataFrame) -> None:
    total = len(df)
    avg_hrs = df["study_hours"].mean() if "study_hours" in df.columns else 0
    avg_att = df["attendance"].mean() if "attendance" in df.columns else 0
    n_courses = df["course"].nunique() if "course" in df.columns else 0

    high_pct = 0.0
    if "risk_level" in df.columns:
        rl = df["risk_level"].astype(str).str.lower()
        high_pct = rl.str.contains("high").sum() / max(total, 1) * 100

    c1, c2, c3, c4 = st.columns(4)

    tiles = [
        (c1, str(total), "Students Analyzed", "↑ dataset size",
         "#3B82F6", """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>"""),
        (c2, f"{high_pct:.1f}%", "High Risk Rate", "of all students",
         "#DC2626", """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m10.29 3.86-8.47 14.67A2 2 0 0 0 3.54 21h16.92a2 2 0 0 0 1.72-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>"""),
        (c3, f"{avg_hrs:.1f}h", "Avg Study Hours", "per week",
         "#22C55E", """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>"""),
        (c4, str(n_courses), "Active Courses", "in dataset",
         "#F59E0B", """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>"""),
    ]

    for col, value, label, sub, color, icon_svg in tiles:
        with col:
            render_html(f"""
<div class="kpi-tile">
<div class="kpi-label">
<span class="kpi-icon" style="background:{color}20;">{icon_svg}</span>
{label}
</div>
<div class="kpi-value">{value}</div>
<div class="kpi-sub">{sub}</div>
</div>
""")


def _risk_chart(df: pd.DataFrame) -> None:
    if "risk_level" not in df.columns:
        return
    try:
        import plotly.graph_objects as go
    except ImportError:
        return

    counts = df["risk_level"].value_counts()
    labels = counts.index.tolist()
    values = counts.values.tolist()

    def _risk_color(label: str) -> str:
        l = str(label).strip().lower()
        if "high" in l:
            return "#DC2626"
        if "medium" in l or "mid" in l:
            return "#F59E0B"
        if "low" in l:
            return "#22C55E"
        return "#64748B"

    def _risk_display(label: str) -> str:
        l = str(label).strip().lower()
        if "high" in l:
            return "High Risk"
        if "medium" in l or "mid" in l:
            return "Medium Risk"
        if "low" in l:
            return "Low Risk"
        return str(label)

    display_labels = [_risk_display(l) for l in labels]
    colors = [_risk_color(l) for l in labels]
    label_colors = colors[:]

    fig = go.Figure(go.Pie(
        labels=display_labels,
        values=values,
        marker=dict(colors=colors, line=dict(color="#0F172A", width=1)),
        hole=0.52,
        textposition="outside",
        textfont=dict(color=label_colors, size=11, family="Inter"),
        outsidetextfont=dict(color=label_colors, size=11, family="Inter"),
        texttemplate="%{label}<br>%{percent:.1%}",
        hovertemplate="%{label}: %{value} students (%{percent})<extra></extra>",
        domain=dict(x=[0.0, 0.68], y=[0.06, 0.94]),
        pull=[0.02] * len(labels),
        automargin=True,
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.0,
            font=dict(color="#94A3B8", size=11, family="Inter"),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
        ),
        margin=dict(t=28, b=28, l=28, r=92),
        height=172,
        autosize=True,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _deadlines_list(df: pd.DataFrame) -> None:
    if "deadline_days" not in df.columns or "course" not in df.columns:
        render_html('<div class="page-sub">No deadline data available.</div>')
        return

    top = (
        df[["course", "deadline_days", "risk_level"]]
        .dropna()
        .sort_values("deadline_days")
        .drop_duplicates("course")
        .head(6)
    )

    rows_html = ""
    for _, row in top.iterrows():
        days = int(row["deadline_days"])
        course = str(row["course"])[:32]
        cc = get_course_color(str(row["course"]))
        risk = str(row.get("risk_level", ""))
        badge_cls = _risk_class(risk)
        pill = _deadline_pill(days)
        rows_html += f"""
<div class="panel-row" style="display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #1E293B;">
<div>
<div style="font-size:13px;font-weight:600;color:{cc};">{course}</div>
<div style="margin-top:3px;">{pill} <span class="{badge_cls}" style="margin-left:4px;">{risk}</span></div>
</div>
<div style="font-size:22px;font-weight:800;color:#94A3B8;">{days}d</div>
</div>
"""

    render_html(f'<div class="card list-panel list-panel--short">{rows_html}</div>')


def _courses_overview(df: pd.DataFrame) -> None:
    if "course" not in df.columns:
        return

    grouped = df.groupby("course").agg(
        count=("course", "size"),
        avg_hrs=("study_hours", "mean") if "study_hours" in df.columns else ("course", "size"),
        avg_att=("attendance", "mean") if "attendance" in df.columns else ("course", "size"),
    ).reset_index()

    if "risk_level" in df.columns:
        risk_mode = df.groupby("course")["risk_level"].agg(
            lambda x: x.value_counts().idxmax()
        ).reset_index()
        risk_mode.columns = ["course", "top_risk"]
        grouped = grouped.merge(risk_mode, on="course", how="left")
    else:
        grouped["top_risk"] = "Unknown"

    rows_html = ""
    for _, row in grouped.iterrows():
        badge_cls = _risk_class(str(row.get("top_risk", "")))
        avg_hrs = row.get("avg_hrs", 0)
        avg_att = row.get("avg_att", 0)
        cc = get_course_color(str(row["course"]))
        rows_html += f"""
<div class="panel-row" style="display:flex;align-items:center;gap:10px;border-bottom:1px solid #1E293B;">
<div style="flex:1;min-width:0;">
<div style="font-size:13px;font-weight:700;color:{cc};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{row['course']}</div>
<div style="font-size:11px;color:#64748B;margin-top:2px;">{int(row['count'])} students · {avg_hrs:.1f}h/wk · {avg_att:.0f}% attend.</div>
</div>
<span class="{badge_cls}">{row.get('top_risk','')}</span>
</div>
"""

    render_html(f'<div class="card list-panel list-panel--tall">{rows_html}</div>')


# ---------------------------------------------------------------------------
# Personalized helpers
# ---------------------------------------------------------------------------

def _welcome_empty_state(full_name: str) -> None:
    """Shown when the student has no courses yet."""
    render_html(f"""
<div class="card" style="text-align:center;padding:36px 24px;">
<div style="font-size:40px;margin-bottom:12px;">📚</div>
<div style="font-size:20px;font-weight:800;color:#F8FAFC;margin-bottom:8px;">
Welcome to Studor, {full_name}!
</div>
<div style="font-size:14px;color:#64748B;max-width:460px;margin:0 auto 20px;">
Your personal dashboard will fill up as you add courses and run risk predictions.
Start by adding your first course below.
</div>
</div>
""")
    col_a, col_b, col_c = st.columns([1, 1.4, 1])
    with col_b:
        if st.button("➕  Add your first course", type="primary", use_container_width=True):
            st.session_state.current_page = "my_courses"
            st.rerun()


def _personal_kpi_row(courses: list, pred: dict | None) -> None:
    """KPI tiles built from the student's own session data."""
    n_courses   = len(courses)
    avg_att     = sum(c.get("attendance", 0) for c in courses) / n_courses if n_courses else 0
    avg_hrs     = sum(c.get("study_hours", 0) for c in courses) / n_courses if n_courses else 0
    nearest_dl  = min((c.get("deadline_days", 999) for c in courses), default=0)
    pred_level  = (pred or {}).get("level", "N/A")

    pred_color  = (
        "#DC2626" if "high"   in pred_level.lower() else
        "#F59E0B" if "medium" in pred_level.lower() else
        "#22C55E" if "low"    in pred_level.lower() else
        "#64748B"
    )

    c1, c2, c3, c4 = st.columns(4)
    tiles = [
        (c1, str(n_courses),       "My Courses",        "added so far",   "#3B82F6"),
        (c2, f"{avg_att:.0f}%",    "Avg Attendance",    "across courses", "#22C55E"),
        (c3, f"{avg_hrs:.1f}h",    "Avg Study Hours",   "per week",       "#F59E0B"),
        (c4, pred_level,           "Last Risk Level",   "latest predict", pred_color),
    ]
    for col, value, label, sub, color in tiles:
        with col:
            render_html(f"""
<div class="kpi-tile">
<div class="kpi-label">{label}</div>
<div class="kpi-value" style="color:{color};">{value}</div>
<div class="kpi-sub">{sub}</div>
</div>
""")


def _personal_courses_list(courses: list) -> None:
    """Compact course rows from session data."""
    if not courses:
        return
    rows_html = ""
    for c in sorted(courses, key=lambda x: x.get("deadline_days", 999)):
        name  = str(c.get("name", ""))[:34]
        diff  = c.get("difficulty", "—")
        wl    = c.get("workload", "—")
        dl    = c.get("deadline_days", "?")
        hrs   = c.get("study_hours", 0)
        att   = c.get("attendance", 0)
        cc    = get_course_color(name)
        diff_color = "#DC2626" if diff == "High" else "#F59E0B" if diff == "Medium" else "#22C55E"
        rows_html += f"""
<div class="panel-row" style="display:flex;align-items:center;gap:10px;border-bottom:1px solid #1E293B;">
<div style="flex:1;min-width:0;">
<div style="font-size:13px;font-weight:700;color:{cc};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{name}</div>
<div style="font-size:11px;color:#64748B;margin-top:2px;">{hrs}h/wk · {att}% attend. · deadline in {dl}d</div>
</div>
<span class="badge" style="background:{diff_color}22;color:{diff_color};border:1px solid {diff_color}55;">{diff}</span>
</div>
"""
    render_html(f'<div class="card list-panel list-panel--tall">{rows_html}</div>')


def _personal_upcoming_deadlines(courses: list) -> None:
    """Deadline list from the student's own courses."""
    sorted_courses = sorted(courses, key=lambda x: x.get("deadline_days", 999))[:6]
    rows_html = ""
    for c in sorted_courses:
        days  = int(c.get("deadline_days", 0))
        name  = str(c.get("name", ""))[:32]
        cc    = get_course_color(name)
        pill  = _deadline_pill(days)
        rows_html += f"""
<div class="panel-row" style="display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #1E293B;">
<div>
<div style="font-size:13px;font-weight:600;color:{cc};">{name}</div>
<div style="margin-top:3px;">{pill}</div>
</div>
<div style="font-size:22px;font-weight:800;color:#94A3B8;">{days}d</div>
</div>
"""
    render_html(f'<div class="card list-panel list-panel--short">{rows_html}</div>')


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render() -> None:
    full_name   = st.session_state.get("full_name", "") or "Student"
    user_courses = st.session_state.get("user_courses", [])

    render_html('<div class="page-h1">Dashboard</div>')

    # ── Personalized view when the student has courses ───────────────────────
    if user_courses:
        render_html(
            f'<div class="page-sub">Your personal academic overview, {full_name}</div>'
        )
        pred = st.session_state.get("prediction_result")
        _personal_kpi_row(user_courses, pred)
        render_html('<div class="section-spacer"></div>')

        left, right = st.columns([1.05, 0.95])
        with left:
            render_html('<div class="section-h2">My Courses</div>')
            _personal_courses_list(user_courses)
        with right:
            render_html('<div class="section-h2">Upcoming Deadlines</div>')
            _personal_upcoming_deadlines(user_courses)
            if pred:
                render_html('<div class="section-h2 section-h2--follow">Last Prediction</div>')
                p_level = pred.get("level", "N/A")
                p_course = pred.get("course", "—")
                lvl_color = (
                    "#DC2626" if "high"   in p_level.lower() else
                    "#F59E0B" if "medium" in p_level.lower() else
                    "#22C55E"
                )
                render_html(f"""
<div class="card" style="border:1px solid {lvl_color}44;background:{lvl_color}0d;text-align:center;padding:16px;">
<div style="font-size:11px;color:#64748B;text-transform:uppercase;letter-spacing:0.1em;">Risk Level</div>
<div style="font-size:28px;font-weight:800;color:{lvl_color};margin:4px 0;">{p_level}</div>
<div style="font-size:12px;color:#64748B;">{p_course}</div>
</div>
""")

    # ── Empty state when no courses exist yet ────────────────────────────────
    else:
        render_html('<div class="page-sub">Your personal space — add courses to get started</div>')
        _welcome_empty_state(full_name)

    # ── Benchmark section (training dataset) — always available ─────────────
    with st.expander("📊  Benchmark / Training Dataset Insights", expanded=False):
        df = _load_data()
        if df is None or df.empty:
            st.info("Dataset not found. Place `student_study_data.csv` in the `Data/` folder.")
        else:
            _health_banner(df)
            _kpi_row(df)
            render_html('<div class="section-spacer"></div>')
            left2, right2 = st.columns([1.05, 0.95])
            with left2:
                render_html('<div class="section-h2">Course Risk Overview (Dataset)</div>')
                _courses_overview(df)
            with right2:
                render_html('<div class="section-h2">Risk Distribution (Dataset)</div>')
                _risk_chart(df)
                render_html('<div class="section-h2 section-h2--follow">Upcoming Deadlines (Dataset)</div>')
                _deadlines_list(df)
