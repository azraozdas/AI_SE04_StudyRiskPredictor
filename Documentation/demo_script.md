# Live Demo Script — Studor

Use this walkthrough for presentations and local smoke tests. Allow **5–8 minutes**.

## Before you start

1. Copy `.env.example` to `.env` and set `DATABASE_URL` (Supabase PostgreSQL).
2. Install dependencies: `pip install -r requirements.txt`
3. Start the app:

```bash
streamlit run Source/Frontend/app.py
```

**Requirements:** Internet access for login, sessions, and saved predictions.

---

## 1. Login (≈1 min)

- Open the app (default `http://localhost:8501`).
- **Register** a new account or **sign in**.
- Confirm you land on the **Dashboard** with the Studor sidebar.

**Talking point:** Authentication uses Supabase PostgreSQL; credentials are not stored in the repository.

---

## 2. Dashboard (≈1 min)

- Review KPI cards and risk distribution chart.
- Explain data comes from the shared training CSV (`Data/student_study_data.csv`), not personal enrollments.

---

## 3. Risk Prediction (≈2 min)

- Sidebar → **Risk Prediction**.
- Enter study hours, attendance, deadline, pass grade, difficulty, workload.
- Click **Predict Risk**.
- Show risk level, confidence, recommendations, and input chart.

**Talking point:** Predictions use `Models/study_risk_model.pkl` and `Models/encoders.pkl` via `Source/model_utils.py`. Test accuracy is **91.11%** on held-out data (see `Outputs/metrics.json`).

---

## 4. Course Analytics (≈1 min)

- Sidebar → **Course Analytics**.
- Show aggregated per-course stats from the training CSV.
- Demo search and risk filter.

**Talking point:** Read-only analytics on the shared dataset — separate from user login data.

---

## 5. Optional extras (if time)

| Page | What to show |
|------|----------------|
| Study Schedule | Rule-based weekly plan from dataset risk levels |
| Recommendations | Tips linked to your latest prediction |
| Model Results | Confusion matrix, feature importance, test predictions |
| Profile | Account info and project team |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Login fails | Check `.env` `DATABASE_URL` and internet |
| Risk page error | Confirm `Models/` and `Outputs/` exist; run `python Source/ml_model.py` |
| Empty Course Analytics | Confirm `Data/student_study_data.csv` exists |
| Chart missing | `pip install plotly` |

---

## Screenshot checklist

PNGs under `Documentation/Screenshots/`:

1. `01_login.png` — login screen
2. `02_overview.png` — dashboard
3. `03_risk_prediction.png` — prediction result
4. `04_dataset_preview.png` — Course Analytics
5. `05_model_outputs.png` — Model Results
