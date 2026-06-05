# Deployment Plan — Studor

## Local demo (primary)

1. Clone the repository and create a virtual environment.
2. Copy `.env.example` to `.env` and set `DATABASE_URL` to your Supabase PostgreSQL connection string.
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `streamlit run Source/Frontend/app.py`
5. Requires **internet** for login, sessions, and saved predictions (hosted Supabase).

## Artifacts

- `Models/study_risk_model.pkl`, `Models/encoders.pkl`, and `Outputs/` (including `metrics.json`) are committed so inference works without retraining.
- Retrain if you change the dataset:

```bash
python Source/data_generation.py   # optional
python Source/preprocessing.py
python Source/ml_model.py
```

## Streamlit Community Cloud (optional)

1. Push the repo **without** `.env` (listed in `.gitignore`).
2. Deploy the app; set `DATABASE_URL` in Streamlit **Secrets**.
3. Entry point: `Source/Frontend/app.py`
4. Python version: 3.10+ recommended.

## Security

- Never commit `.env` or database credentials.
- Passwords stored as bcrypt hashes only.

## Demo risks

| Risk | Mitigation |
|------|------------|
| No internet | Login and DB writes fail — use screenshots or recorded walkthrough |
| Missing plotly | Listed in `requirements.txt` |
| Wrong encodings | Risk page uses `model_utils.predict_for_user()` with `encoders.pkl` |
| Metric questions | Refer to `Outputs/metrics.json` and `Documentation/evaluation_report.md` |

## App architecture

Single Streamlit entry point with custom HTML sidebar navigation:

| Component | Location |
|-----------|----------|
| Router | `Source/Frontend/app.py` |
| Auth | `Source/Frontend/login.py` |
| Pages | `Source/Frontend/pages_/` |
| ML inference | `Source/model_utils.py` |
| Database | `Source/Backend/db.py` |

Native Streamlit multipage wrappers under `Source/Frontend/pages/` are **not used**. The live app uses `app.py` + `pages_/` only.

`[client] showSidebarNavigation = false` in `.streamlit/config.toml` hides Streamlit's default multipage sidebar.

## Demo

Follow [demo_script.md](demo_script.md). Backup PNGs: `Documentation/Screenshots/`.

## Out of scope for current MVP

- Per-user course management UI (`courses` table reserved in schema)
- PDF upload and analysis (`pdfs` table reserved; `pdf_utils.py` not wired to UI)
- Display of saved prediction history on Profile (predictions are saved to DB)
