# Performance Check — Studor Risk Predictor

**Date:** 04.06.2026  
**Dataset:** 300 rows · 3 balanced classes · synthetic

---

## Model Performance

| Metric | Value |
|---|---|
| Test Accuracy | **1.00** (300-row dataset) |
| 5-Fold CV Mean Accuracy | **1.00** |
| 5-Fold CV Std Dev | **0.00** |
| Macro Avg F1 | **1.00** |
| Train / Test Split | 80 % / 20 % (240 train · 60 test) |
| Algorithm | Random Forest (default hyperparameters, `random_state=42`) |

> **Why is CV = 1.0?** The dataset is fully synthetic and deterministic — risk_level is a direct function of the input features with no noise. A simple decision tree would also achieve perfect separation. These metrics **do not generalise** to real student data. See `Data/data_dictionary.md § Limitations`.

---

## Top Feature Importances (Gini, 300-row retrain)

| Feature | Importance |
|---|---|
| workload_level | 0.298 |
| assignment_difficulty | 0.260 |
| pass_grade | 0.160 |
| attendance | 0.159 |
| deadline_days | 0.071 |
| study_hours | 0.052 |
| course | 0.000 |

Course ID carries no signal — the risk simulation rules do not vary by course.

---

## Application Response Times (localhost, measured 04.06.2026)

| Operation | Approx. time |
|---|---|
| Cold app start (first load) | ~3–5 s (Supabase `init_db` + model load) |
| Subsequent page navigation | < 100 ms (model cached via `@st.cache_resource`) |
| Login / Register (DB round-trip) | ~300–600 ms (Supabase pooler, EU West 1) |
| Risk prediction (model.predict) | < 10 ms |
| Dashboard load (CSV read + Plotly) | ~200–400 ms (CSV cached via `@st.cache_data`) |

**Key optimisation applied:** `init_db()` wrapped in `@st.cache_resource` so it runs once per server process instead of on every Streamlit rerun (previously added ~400 ms per interaction).

---

## Database (Supabase PostgreSQL)

| Parameter | Value |
|---|---|
| Host | `aws-0-eu-west-1.pooler.supabase.com` (IPv4 pooler) |
| Port | 6543 (transaction mode) |
| Connection mode | Supavisor pooler — compatible with IPv4-only networks |
| Tables | users, sessions, courses, pdfs, predictions, password_reset_tokens |
| Average query latency | ~80–150 ms (EU West 1, from Istanbul / Frankfurt) |

---

## Known Limitations

1. **Synthetic data** — metrics are not real-world indicators of model quality.
2. **No hyperparameter tuning** — default RandomForest parameters used throughout.
3. **Single-node deployment** — Streamlit Cloud or a single server; no horizontal scaling.
4. **No caching for DB reads** — user-specific DB queries (e.g. `get_user_courses`) run on every page load.
5. **Cookie-based Remember Me** — relies on `streamlit-cookies-controller`; may not persist across incognito sessions or strict browser privacy modes.
