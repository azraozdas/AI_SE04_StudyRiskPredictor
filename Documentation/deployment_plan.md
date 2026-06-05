# Deployment Plan

## Local demo (primary)

1. Clone the repository and create a virtual environment.
2. Copy `.env.example` to `.env` and set `DATABASE_URL` to your Supabase PostgreSQL connection string.
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `streamlit run Source/Frontend/app.py`
5. Requires **internet** for login, sessions, and prediction history (hosted Supabase).

## Artifacts

- `Models/study_risk_model.pkl` and `Models/encoders.pkl` are committed so inference works without retraining.
- Retrain only if you change `Data/student_study_data.csv`: run `Source/preprocessing.py` then `Source/ml_model.py`.

## Streamlit Community Cloud (optional)

1. Push the repo to GitHub **without** `.env` (use `.gitignore`).
2. Deploy the app; set `DATABASE_URL` in Streamlit **Secrets**.
3. Entry point: `Source/Frontend/app.py`
4. Python version: match your local 3.10+ environment.

## Security

- Never commit `.env` or rotate credentials if they were ever in Git history.
- `Uploads/` is gitignored; PDFs stay on the server filesystem.

## Demo risks

| Risk | Mitigation |
|------|------------|
| No internet | Demo login and DB writes fail — use offline talking points or a recorded walkthrough |
| Missing plotly | Listed in `requirements.txt` |
| Wrong encodings | Risk page uses `model_utils.predict_for_user()` with `encoders.pkl` |

## Native Streamlit pages

Thin wrappers live under `Source/Frontend/pages/` (evaluator / plan scaffold):

| File | Purpose |
|------|---------|
| `1_Login.py` | Authentication entry |
| `3_My_Courses.py` | Per-user course CRUD |

The main router remains `Source/Frontend/app.py` with custom HTML sidebar navigation. `[client] showSidebarNavigation = false` hides Streamlit’s default multipage sidebar so only one nav appears.

**Not included:** `4_Upload_PDF.py` (deferred).

## Demo

Follow `Documentation/demo_script.md`. Backup PNGs: `Documentation/Screenshots/` (see `README.md` in that folder).

## Out of scope for this demo

- PDF upload and AI analysis (`pdfs` table reserved in schema; no UI page)
