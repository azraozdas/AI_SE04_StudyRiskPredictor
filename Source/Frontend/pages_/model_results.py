"""Model Results page — ML performance metrics, feature importance, confusion matrix."""

import html as html_lib
import os
import sys

import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import ROOT, render_html

PREDICTIONS_PATH      = os.path.join(ROOT, "Outputs", "predictions.csv")
FEATURE_IMP_PATH      = os.path.join(ROOT, "Outputs", "feature_importance.csv")
CONFUSION_MATRIX_PATH = os.path.join(ROOT, "Outputs", "confusion_matrix.csv")
MODEL_PATH            = os.path.join(ROOT, "Models", "study_risk_model.pkl")


@st.cache_data
def _load(path: str) -> pd.DataFrame | None:
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


def _load_predictions() -> pd.DataFrame | None:
    """Load predictions.csv without cache so table data is always current."""
    if not os.path.isfile(PREDICTIONS_PATH):
        return None
    try:
        df = pd.read_csv(PREDICTIONS_PATH)
    except (pd.errors.EmptyDataError, pd.errors.ParserError, OSError):
        return None
    return df


@st.cache_resource
def _load_model():
    import joblib
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


def _decode_risk(v) -> str:
    return {0: "High Risk", 1: "Low Risk", 2: "Medium Risk"}.get(int(v), str(v))


def _feature_importance_chart(fi_df: pd.DataFrame) -> None:
    try:
        import plotly.graph_objects as go
    except ImportError:
        st.dataframe(fi_df, use_container_width=True)
        return

    fi_sorted = fi_df.sort_values(fi_df.columns[-1], ascending=True).tail(10)
    features  = fi_sorted.iloc[:, 0].tolist()
    values    = fi_sorted.iloc[:, -1].tolist()

    max_v = max(values) if values else 1
    colors = [
        "#3B82F6" if v / max_v >= 0.7 else
        ("#6366F1" if v / max_v >= 0.4 else "#4B5563")
        for v in values
    ]

    fig = go.Figure(go.Bar(
        y=features, x=values,
        orientation="h",
        marker_color=colors,
        text=[f"{v:.3f}" for v in values],
        textposition="outside",
        textfont=dict(color="#94A3B8", size=11),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(tickfont=dict(color="#CBD5E1", size=12)),
        margin=dict(t=8, b=8, l=6, r=52),
        height=148,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


_RISK_CLASS_LABELS = ("High Risk", "Low Risk", "Medium Risk")


def _cm_class_label(name: str) -> str:
    """Map actual_0 / predicted_1 style labels to readable risk names."""
    s = str(name).strip()
    for prefix in ("actual_", "predicted_"):
        if s.startswith(prefix):
            try:
                return _RISK_CLASS_LABELS[int(s.split("_")[-1])]
            except (ValueError, IndexError):
                pass
    return s


def _parse_confusion_matrix(cm_df: pd.DataFrame) -> tuple[list[str], list[str], list[list]]:
    df = cm_df.copy()
    first_col = df.columns[0]
    if (
        str(first_col).startswith("Unnamed")
        or df.iloc[:, 0].astype(str).str.contains("actual", case=False, na=False).any()
    ):
        df = df.set_index(first_col)
    z = df.values.tolist()
    x_labels = [_cm_class_label(c) for c in df.columns]
    y_labels = [_cm_class_label(i) for i in df.index]
    return x_labels, y_labels, z


def _confusion_heatmap(cm_df: pd.DataFrame) -> None:
    try:
        import plotly.graph_objects as go
    except ImportError:
        st.dataframe(cm_df, use_container_width=True)
        return

    x_labels, y_labels, z = _parse_confusion_matrix(cm_df)

    fig = go.Figure(go.Heatmap(
        z=z,
        x=x_labels,
        y=y_labels,
        colorscale=[[0, "#1E293B"], [0.5, "#2563EB"], [1.0, "#93C5FD"]],
        text=[[str(v) for v in row] for row in z],
        texttemplate="%{text}",
        textfont=dict(size=16, color="#F8FAFC"),
        showscale=False,
        xgap=2,
        ygap=2,
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            tickfont=dict(color="#CBD5E1", size=11),
            title=dict(text="Predicted", font=dict(color="#64748B", size=11)),
            side="bottom",
            tickangle=0,
        ),
        yaxis=dict(
            tickfont=dict(color="#CBD5E1", size=11),
            title=dict(text="Actual", font=dict(color="#64748B", size=11)),
            autorange="reversed",
        ),
        margin=dict(t=12, b=48, l=72, r=16),
        height=165,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _predictions_table(display_df: pd.DataFrame) -> None:
    """Render predictions as HTML table (Glide st.dataframe fails under custom dark CSS)."""
    if display_df.empty:
        render_html(
            '<div class="card" style="padding:12px 14px;">'
            '<div style="font-size:13px;color:#64748B;">predictions.csv is empty.</div></div>'
        )
        return

    cols = list(display_df.columns)
    head = "".join(
        f'<th scope="col">{html_lib.escape(str(c))}</th>' for c in cols
    )
    rows = []
    for _, row in display_df.iterrows():
        cells = "".join(
            f"<td>{html_lib.escape(str(row[c]))}</td>" for c in cols
        )
        rows.append(f"<tr>{cells}</tr>")
    body = "".join(rows)

    render_html(f"""
<div class="predictions-table-wrap">
<table class="predictions-table">
<thead><tr>{head}</tr></thead>
<tbody>{body}</tbody>
</table>
</div>
""")


def _distribution_chart(preds: pd.DataFrame, col_name: str) -> None:
    try:
        import plotly.graph_objects as go
    except ImportError:
        return

    if col_name not in preds.columns:
        return

    decoded = preds[col_name].apply(_decode_risk)
    counts  = decoded.value_counts()
    labels  = counts.index.tolist()
    values  = counts.values.tolist()

    COLORS = {"High Risk": "#DC2626", "Medium Risk": "#F59E0B", "Low Risk": "#22C55E"}
    colors = [COLORS.get(l, "#3B82F6") for l in labels]

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=colors,
        text=values,
        textposition="outside",
        textfont=dict(color="#94A3B8", size=13),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickfont=dict(color="#CBD5E1", size=13)),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(t=10, b=32, l=6, r=10),
        height=152,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render() -> None:
    render_html('<div class="page-h1">Model Results</div>')
    render_html('<div class="page-sub">Random Forest classifier — training outputs and performance metrics</div>')

    preds_df = _load_predictions()
    fi_df    = _load(FEATURE_IMP_PATH)
    cm_df    = _load(CONFUSION_MATRIX_PATH)
    model    = _load_model()

    # ── Model presence banner ────────────────────────────────────────────────
    if model is not None:
        try:
            n_estimators = model.n_estimators
            model_info = f"Random Forest · {n_estimators} trees"
        except AttributeError:
            model_info = "Trained model loaded"
        render_html(f"""
<div class="card card-accent-blue" style="margin-bottom:10px;padding:10px 14px;display:flex;align-items:center;gap:10px;">
<span style="font-size:20px;">✅</span>
<div>
<div style="font-size:13px;font-weight:700;color:#F8FAFC;">{model_info}</div>
<div style="font-size:12px;color:#64748B;">study_risk_model.pkl loaded successfully</div>
</div>
</div>
""")
    else:
        render_html("""
<div class="card" style="margin-bottom:10px;padding:10px 14px;border-left:3px solid #F59E0B;display:flex;align-items:center;gap:10px;">
<span style="font-size:20px;">⚠️</span>
<div style="font-size:13px;color:#FCD34D;">
Model not found. Run <code style="background:#0F172A;padding:2px 6px;border-radius:4px;">python Source/ml_model.py</code> to train.
</div>
</div>
""")

    # ── KPI metrics ──────────────────────────────────────────────────────────
    if preds_df is not None:
        total = len(preds_df)
        pred_col = "predicted_risk_level" if "predicted_risk_level" in preds_df.columns else None
        actual_col = "risk_level" if "risk_level" in preds_df.columns else None

        accuracy = None
        if pred_col and actual_col:
            correct = (preds_df[pred_col] == preds_df[actual_col]).sum()
            accuracy = correct / max(total, 1) * 100

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Predictions", f"{total:,}")
        with m2:
            st.metric("Accuracy", f"{accuracy:.1f}%" if accuracy is not None else "N/A")
        with m3:
            if pred_col:
                decoded = preds_df[pred_col].apply(_decode_risk)
                high_n = int((decoded == "High Risk").sum())
                st.metric("High Risk (predicted)", high_n)
            else:
                st.metric("High Risk", "N/A")
        with m4:
            if pred_col:
                low_n = int((decoded == "Low Risk").sum())
                st.metric("Low Risk (predicted)", low_n)
            else:
                st.metric("Low Risk", "N/A")

        render_html('<div class="section-spacer"></div>')

    # ── Two-column layout ─────────────────────────────────────────────────────
    left, right = st.columns(2)

    with left:
        render_html('<div class="section-h2">Feature Importance</div>')
        if fi_df is not None and not fi_df.empty:
            _feature_importance_chart(fi_df)
        else:
            render_html('<div class="card"><div style="font-size:13px;color:#64748B;">feature_importance.csv not found.</div></div>')

    with right:
        render_html('<div class="section-h2">Confusion Matrix</div>')
        if cm_df is not None and not cm_df.empty:
            _confusion_heatmap(cm_df)
        else:
            render_html('<div class="card"><div style="font-size:13px;color:#64748B;">confusion_matrix.csv not found.</div></div>')

    # ── Distribution + table (side by side to fit viewport) ───────────────────
    render_html('<div class="section-spacer"></div>')
    if preds_df is None:
        render_html("""
<div class="card">
<div style="font-size:13px;color:#64748B;">
predictions.csv not found. Run <code style="background:#0F172A;padding:2px 6px;border-radius:4px;">python Source/ml_model.py</code> to generate outputs.
</div>
</div>
""")
    elif preds_df.empty:
        render_html("""
<div class="card">
<div style="font-size:13px;color:#64748B;">predictions.csv is empty. Run <code style="background:#0F172A;padding:2px 6px;border-radius:4px;">python Source/ml_model.py</code> to regenerate outputs.</div>
</div>
""")
    else:
        display_df = preds_df.copy()
        for col in ("predicted_risk_level", "actual_risk_level", "risk_level"):
            if col in display_df.columns:
                display_df[col] = display_df[col].apply(_decode_risk)

        has_dist = "predicted_risk_level" in preds_df.columns
        if has_dist:
            dist_col, table_col = st.columns([0.95, 1.05])
            with dist_col:
                render_html('<div class="section-h2">Predicted Risk Distribution</div>')
                _distribution_chart(preds_df, "predicted_risk_level")
            with table_col:
                render_html('<div class="section-h2">Predictions Table</div>')
                _predictions_table(display_df)
        else:
            render_html('<div class="section-h2 section-h2--follow">Predictions Table</div>')
            _predictions_table(display_df)
