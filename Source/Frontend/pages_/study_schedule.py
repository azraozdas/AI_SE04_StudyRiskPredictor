"""Study Schedule page — personalized planner built from the student's own courses and predictions."""

import os
import sys
from datetime import date, timedelta

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from course_colors import course_color_bg, get_course_color
from utils import ROOT, render_html

_BACKEND = os.path.join(ROOT, "Source", "Backend")
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)

from db import upsert_study_schedule, get_user_schedule  # noqa: E402

# Hours recommended per risk level (AI decision)
RISK_HOURS: dict[str, float] = {
    "High Risk":   5.0,
    "Medium Risk": 3.0,
    "Low Risk":    1.5,
}

RISK_COLOR: dict[str, str] = {
    "High Risk":   "#DC2626",
    "Medium Risk": "#F59E0B",
    "Low Risk":    "#22C55E",
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DAYS_OPTIONS = ["(Not assigned)"] + DAYS

# Map day names to a study_date offset from today's Monday (ISO weekday 1-7)
_DAY_TO_ISO = {d: i + 1 for i, d in enumerate(DAYS)}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _navigate(page: str) -> None:
    st.session_state.current_page = page
    st.rerun()


def _slug(name: str) -> str:
    """Convert course name to a safe session_state key segment."""
    return name.lower().replace(" ", "_").replace("-", "_")[:40]


def _date_for_day(day_name: str) -> date:
    """Return the date of the given weekday in the CURRENT week (Mon-Sun).

    Uses timedelta so it correctly crosses month boundaries
    (e.g. Wednesday when today is 30 June → 2 July, not ValueError).
    """
    today = date.today()
    target_iso = _DAY_TO_ISO.get(day_name, 1)   # Mon=1 … Sun=7
    diff = target_iso - today.isoweekday()       # may be negative (past days this week)
    return today + timedelta(days=diff)


def _load_schedule_from_db() -> None:
    """Restore schedule_assignments from DB for the current user.

    Converts stored study_schedules rows back into the
    {course_name: {suggested_hours, assigned_day}} dict used by the UI.
    Only called once per session (guarded by _schedule_loaded flag).
    """
    user_id = st.session_state.get("user_id")
    if not user_id:
        return
    try:
        rows = get_user_schedule(user_id)
        if not rows:
            return
        assignments: dict[str, dict] = {}
        for row in rows:
            cname = row.get("course_name") or ""
            if not cname:
                continue
            # Map study_date back to a day name (best effort)
            sd = row.get("study_date")
            day_name = None
            if sd:
                # date objects have isoweekday() 1-7; list is 0-indexed
                try:
                    day_name = DAYS[sd.isoweekday() - 1]
                except Exception:
                    day_name = None
            hrs = row.get("duration_minutes", 60) / 60
            assignments[cname] = {
                "suggested_hours": hrs,
                "assigned_day": day_name,
            }
        if assignments:
            st.session_state.schedule_assignments = assignments
    except Exception:
        pass  # DB offline — fall back to session state silently


# ---------------------------------------------------------------------------
# State 1 — No courses
# ---------------------------------------------------------------------------

def _render_no_courses() -> None:
    render_html("""
<div class="card" style="text-align:center;padding:48px 24px;">
<div style="font-size:44px;margin-bottom:14px;">📅</div>
<div style="font-size:20px;font-weight:800;color:#F8FAFC;margin-bottom:10px;">
No Courses Yet
</div>
<div style="font-size:14px;color:#64748B;max-width:440px;margin:0 auto 24px;line-height:1.7;">
Add your enrolled courses first. Once you have courses and predictions, Studor
will generate a personalized weekly study plan for you.
</div>
</div>
""")
    col_a, col_b, col_c = st.columns([1, 1.4, 1])
    with col_b:
        if st.button("📚  Go to My Courses", type="primary", use_container_width=True, key="sched_empty_btn"):
            _navigate("my_courses")


# ---------------------------------------------------------------------------
# State 2 — Has courses, no predictions yet
# ---------------------------------------------------------------------------

def _render_no_predictions(courses: list) -> None:
    render_html("""
<div class="card" style="padding:20px;border-left:3px solid #F59E0B;
background:rgba(245,158,11,0.06);margin-bottom:12px;">
<div style="font-size:13px;font-weight:700;color:#FCD34D;margin-bottom:4px;">
⚡ Predictions needed
</div>
<div style="font-size:13px;color:#94A3B8;line-height:1.5;">
Your courses are added. Run a risk prediction for each course so Studor can
recommend how many hours per week you should study.
</div>
</div>
""")

    render_html('<div class="section-h2">Your Courses — Awaiting Prediction</div>')

    for c in sorted(courses, key=lambda x: x.get("deadline_days", 999)):
        name = str(c.get("name", ""))
        dl   = c.get("deadline_days", "?")
        hrs  = c.get("study_hours", 0)
        att  = c.get("attendance", 0)
        cc   = get_course_color(name)
        cbg  = course_color_bg(name)
        cid  = c.get("id", 0)

        render_html(f"""
<div class="card" style="border-left:3px solid {cc};
background:linear-gradient(135deg,{cbg} 0%,rgba(15,23,42,0) 60%);
padding:12px 16px;margin-bottom:6px;">
<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;">
<div>
<div style="font-size:14px;font-weight:700;color:{cc};">{name}</div>
<div style="font-size:11px;color:#64748B;margin-top:2px;">
{hrs}h/wk · {att}% attendance · deadline in {dl}d
</div>
</div>
<span class="badge" style="background:#1E293B;color:#64748B;border:1px solid #334155;">
No prediction
</span>
</div>
</div>
""")
        btn_col, _ = st.columns([1, 3])
        with btn_col:
            if st.button(
                "🎯  Predict Risk",
                key=f"sched_predict_{cid}_{_slug(name)}",
                use_container_width=True,
                type="primary",
            ):
                st.session_state.prefill_course = c.copy()
                _navigate("risk")


# ---------------------------------------------------------------------------
# State 3 — Full schedule builder
# ---------------------------------------------------------------------------

def _render_schedule_builder(predicted_courses: list) -> None:
    sched = st.session_state.setdefault("schedule_assignments", {})

    total_hours = sum(
        RISK_HOURS.get(c.get("risk_level", ""), 2.0) for c in predicted_courses
    )
    high_n   = sum(1 for c in predicted_courses if "high"   in str(c.get("risk_level","")).lower())
    medium_n = sum(1 for c in predicted_courses if "medium" in str(c.get("risk_level","")).lower())
    low_n    = sum(1 for c in predicted_courses if "low"    in str(c.get("risk_level","")).lower())

    render_html(f"""
<div class="card card-accent-blue" style="display:flex;gap:20px;flex-wrap:wrap;
align-items:center;padding:16px 20px;margin-bottom:12px;">
<div>
<div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;
letter-spacing:0.1em;margin-bottom:2px;">This Week</div>
<div style="font-size:30px;font-weight:800;color:#F8FAFC;line-height:1.1;">{total_hours:.1f}h</div>
<div style="font-size:11px;color:#64748B;">recommended total</div>
</div>
<div style="display:flex;gap:20px;flex-wrap:wrap;">
<div style="text-align:center;">
<div style="font-size:22px;font-weight:800;color:#FCA5A5;">{high_n}</div>
<div style="font-size:10px;font-weight:700;color:#64748B;text-transform:uppercase;">High Risk</div>
</div>
<div style="text-align:center;">
<div style="font-size:22px;font-weight:800;color:#FCD34D;">{medium_n}</div>
<div style="font-size:10px;font-weight:700;color:#64748B;text-transform:uppercase;">Medium</div>
</div>
<div style="text-align:center;">
<div style="font-size:22px;font-weight:800;color:#86EFAC;">{low_n}</div>
<div style="font-size:10px;font-weight:700;color:#64748B;text-transform:uppercase;">Low Risk</div>
</div>
</div>
<div style="flex:1;min-width:220px;font-size:12px;color:#64748B;line-height:1.6;
border-left:1px solid #273449;padding-left:16px;">
🤖 <strong style="color:#93C5FD;">AI recommends</strong> how many hours to study.<br>
📅 <strong style="color:#93C5FD;">You choose</strong> which day each course falls on.
</div>
</div>
""")

    # ── Course-day assignment table ──────────────────────────────────────────
    render_html('<div class="section-h2">Assign Study Days</div>')

    sorted_courses = sorted(
        predicted_courses,
        key=lambda c: (
            0 if "high"   in str(c.get("risk_level","")).lower() else
            1 if "medium" in str(c.get("risk_level","")).lower() else 2,
            c.get("deadline_days", 999),
        ),
    )

    # Collect assignments from selectboxes during this render
    live_assignments: dict[str, dict] = {}

    for c in sorted_courses:
        name     = str(c.get("name", ""))
        risk_lv  = c.get("risk_level", "")
        hours    = RISK_HOURS.get(risk_lv, 2.0)
        rc       = RISK_COLOR.get(risk_lv, "#64748B")
        cc       = get_course_color(name)
        key      = f"sched_day_{_slug(name)}"

        # Default from saved assignments
        saved_day = sched.get(name, {}).get("assigned_day") or "(Not assigned)"
        default_idx = DAYS_OPTIONS.index(saved_day) if saved_day in DAYS_OPTIONS else 0

        col_name, col_risk, col_hours, col_day = st.columns([2.2, 1.2, 0.9, 1.9])
        with col_name:
            render_html(
                f'<div style="font-size:13px;font-weight:700;color:{cc};'
                f'padding-top:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">'
                f'{name}</div>'
            )
        with col_risk:
            render_html(
                f'<div style="padding-top:6px;">'
                f'<span class="badge" style="background:{rc}22;color:{rc};'
                f'border:1px solid {rc}55;">{risk_lv}</span></div>'
            )
        with col_hours:
            render_html(
                f'<div style="font-size:15px;font-weight:800;color:#F8FAFC;'
                f'padding-top:4px;text-align:center;">{hours:.1f}h</div>'
            )
        with col_day:
            selected = st.selectbox(
                "Day",
                DAYS_OPTIONS,
                index=default_idx,
                key=key,
                label_visibility="collapsed",
            )

        assigned = selected if selected != "(Not assigned)" else None
        live_assignments[name] = {"suggested_hours": hours, "assigned_day": assigned}

    # Save button
    render_html('<div style="margin-top:8px;"></div>')
    save_col, _ = st.columns([1, 3])
    with save_col:
        if st.button("💾  Save My Schedule", type="primary", use_container_width=True, key="sched_save_btn"):
            st.session_state.schedule_assignments = live_assignments
            sched = live_assignments

            # ── Persist to database ────────────────────────────────────
            user_id = st.session_state.get("user_id")
            if user_id:
                try:
                    entries = []
                    for cname, data in live_assignments.items():
                        assigned_day = data.get("assigned_day")
                        if not assigned_day:
                            continue  # skip unassigned courses
                        study_dt = _date_for_day(assigned_day)
                        hours = data.get("suggested_hours", 1.0)
                        entries.append({
                            "course_name":      cname,
                            "study_date":       study_dt.isoformat(),
                            "duration_minutes": int(hours * 60),
                            "priority":         "High" if hours >= 5 else (
                                                "Medium" if hours >= 3 else "Low"),
                            "topic":            "",
                            "completed":        False,
                            "notes":            "",
                        })
                    saved_n = upsert_study_schedule(user_id, entries)
                    if entries:
                        st.success(f"✅ Schedule saved! ({saved_n} entries persisted to database)")
                    else:
                        st.success("✅ Schedule saved (no days assigned yet).")
                except Exception as exc:
                    st.success("✅ Schedule saved to session!")
                    st.warning(f"Could not persist to database: {exc}")
            else:
                st.success("✅ Schedule saved!")

    # ── Weekly planner ───────────────────────────────────────────────────────
    render_html('<div class="section-h2 section-h2--follow">Weekly Planner</div>')

    # Build day → list of (name, hours) from current selectbox values
    weekly: dict[str, list[dict]] = {d: [] for d in DAYS}
    for name, data in live_assignments.items():
        day = data.get("assigned_day")
        if day and day in weekly:
            weekly[day].append({"name": name, "hours": data["suggested_hours"]})

    day_cols = st.columns(7)
    for col, day in zip(day_cols, DAYS):
        with col:
            blocks = weekly[day]
            if not blocks:
                render_html(f"""
<div class="card schedule-day-card" style="min-height:90px;">
<div style="font-size:10px;font-weight:700;color:#94A3B8;text-transform:uppercase;
letter-spacing:0.1em;margin-bottom:6px;">{day}</div>
<div style="font-size:11px;color:#475569;font-style:italic;">Rest day</div>
</div>
""")
            else:
                blocks_html = ""
                for b in blocks:
                    cc  = get_course_color(b["name"])
                    cbg = course_color_bg(b["name"])
                    blocks_html += f"""
<div style="background:{cbg};border-left:3px solid {cc};border-radius:5px;
padding:6px 8px;margin-bottom:5px;">
<div style="font-size:10px;font-weight:700;color:{cc};line-height:1.3;
white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{b['name']}</div>
<div style="font-size:11px;font-weight:600;color:#F8FAFC;margin-top:2px;">{b['hours']:.1f} hours</div>
</div>
"""
                render_html(f"""
<div class="card schedule-day-card" style="min-height:90px;">
<div style="font-size:10px;font-weight:700;color:#94A3B8;text-transform:uppercase;
letter-spacing:0.1em;margin-bottom:6px;">{day}</div>
{blocks_html}
</div>
""")

    # ── Study tips ───────────────────────────────────────────────────────────
    render_html("""
<div class="card" style="margin-top:10px;">
<div style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;
letter-spacing:0.1em;margin-bottom:4px;">Study Science Tips</div>
<div style="font-size:12px;color:#94A3B8;line-height:1.6;">
High-risk courses benefit from studying earlier in the week while cognitive energy is highest.
Avoid scheduling more than 3 hours of a single course in one day — use spaced sessions.
Rest days are intentional: sleep consolidates memory and improves recall.
</div>
</div>
""")

    # ── CTAs ─────────────────────────────────────────────────────────────────
    render_html('<div style="margin-top:10px;"></div>')
    cta1, cta2 = st.columns(2)
    with cta1:
        if st.button("🏠  View Dashboard", use_container_width=True, key="sched_dash_btn"):
            _navigate("dashboard")
    with cta2:
        if st.button("💡  Recommendations", use_container_width=True, key="sched_rec_btn"):
            _navigate("recommendations")


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render() -> None:
    render_html('<div class="page-h1">Study Schedule</div>')
    render_html(
        '<div class="page-sub">AI recommends weekly study hours · '
        'You choose the days · Your courses only</div>'
    )

    # Load saved schedule from DB once per session
    if not st.session_state.get("_schedule_loaded"):
        _load_schedule_from_db()
        st.session_state._schedule_loaded = True

    user_courses = st.session_state.get("user_courses", [])

    if not user_courses:
        _render_no_courses()
        return

    predicted = [c for c in user_courses if c.get("risk_level")]
    unpredicted = [c for c in user_courses if not c.get("risk_level")]

    if not predicted:
        _render_no_predictions(user_courses)
        return

    # Show partial-state banner if some courses still lack predictions
    if unpredicted:
        render_html(f"""
<div class="card" style="padding:12px 16px;border-left:3px solid #3B82F6;
background:rgba(59,130,246,0.06);margin-bottom:10px;">
<div style="font-size:12px;color:#93C5FD;">
ℹ️ {len(unpredicted)} course{"s" if len(unpredicted) != 1 else ""} still
{"have" if len(unpredicted) != 1 else "has"} no prediction.
Go to <strong>Risk Prediction</strong> to complete your schedule.
</div>
</div>
""")

    _render_schedule_builder(predicted)
