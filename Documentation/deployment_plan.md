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

## App architecture

The live dashboard is a **single Streamlit entry point** with custom HTML sidebar navigation:

- **Router:** `Source/Frontend/app.py`
- **Feature pages:** `Source/Frontend/pages_/` (dashboard, Course Analytics, risk prediction, etc.)
- **Login:** `Source/Frontend/login.py` (rendered by `app.py` before the main shell)

Native Streamlit multipage wrappers under `Source/Frontend/pages/` are **optional/deferred** (evaluator scaffold only). They are not required to run the demo.

| Planned wrapper | Status |
|-----------------|--------|
| `1_Login.py` | Deferred — login handled in `login.py` + `app.py` |
| `3_My_Courses.py` | Deferred — not in current sidebar |
| `4_Upload_PDF.py` | Deferred — PDF upload UI not included |

`[client] showSidebarNavigation = false` hides Streamlit’s default multipage sidebar so only the custom nav appears.

## Demo

Follow [demo_script.md](demo_script.md). Backup PNGs: `Documentation/Screenshots/`.

## Out of scope for this demo

- Per-user course CRUD (My Courses page removed from current build)
- PDF upload and AI analysis (`pdfs` table reserved in schema; `pypdf` kept for future `pdf_utils.py`)
