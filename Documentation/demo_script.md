# Live Demo Script

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

- Open the app in the browser (default `http://localhost:8501`).
- **Register** a new account or **sign in** with an existing one.
- Confirm you land on the **Dashboard** with the custom Studor sidebar.

**Talking point:** Authentication uses a hosted Supabase database; credentials are not stored in the repo.

---

## 2. Dashboard (≈1 min)

- Review KPI cards (risk distribution, study hours, attendance).
- Point out dataset-backed overview from `Data/student_study_data.csv`.
- Optional: mention profile link at the bottom of the sidebar.

---

## 3. Risk Prediction (≈2 min)

- Sidebar → **Risk Prediction**.
- Fill in the form (course, study hours, attendance, deadline, grade, difficulty, workload).
- Click **Predict Risk**.
- Show the result panel: risk level, confidence, recommendations, and input chart.

**Talking point:** Predictions use `Models/study_risk_model.pkl` and `Models/encoders.pkl` via `Source/model_utils.py`, with a rule-based fallback if the model is unavailable.

---

## 4. Course Analytics (≈1 min)

- Sidebar → **Course Analytics**.
- Show aggregated per-course stats from the training CSV (not personal enrollments).
- Demo **Search courses** and **Filter by risk**.

**Talking point:** This page is read-only analytics on the shared dataset; it is separate from user login data.

---

## 5. Optional extras (if time)

| Page | What to show |
|------|----------------|
| Study Schedule | Weekly plan from dataset risk levels |
| Recommendations | Study tips by risk band |
| Model Results | Confusion matrix, feature importance |
| Profile | User info and prediction history |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Login fails | Check `.env` `DATABASE_URL` and internet |
| `pip install` error | Ensure `requirements.txt` has no merge conflict markers |
| Risk page chart missing | `pip install plotly` |
| Empty Course Analytics | Confirm `Data/student_study_data.csv` exists |

---

## Screenshot checklist

After a successful run, capture PNGs under `Documentation/Screenshots/`:

1. `01_login.png` — login screen
2. `02_overview.png` — dashboard
3. `03_risk_prediction.png` — prediction result
4. `04_dataset_preview.png` — Course Analytics
5. `05_model_outputs.png` — Model Results
