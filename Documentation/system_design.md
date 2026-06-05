# System Design — Studor

## Architecture Overview

Studor follows a modular pipeline from simulated data through ML inference to a Streamlit dashboard with Supabase authentication.

```text
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Data Layer     │────▶│ Preprocessing    │────▶│  ML Training    │
│  student_study  │     │  encoders.pkl    │     │  study_risk_    │
│  _data.csv      │     │  cleaned CSV     │     │  model.pkl      │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                        ┌──────────────────┐              │
                        │  Outputs/        │◀─────────────┘
                        │  metrics, CM, FI │
                        └──────────────────┘
                                                          │
┌─────────────────┐     ┌──────────────────┐     ┌────────▼────────┐
│  Supabase       │◀───▶│  Streamlit App   │────▶│  model_utils    │
│  PostgreSQL     │     │  app.py + pages_ │     │  predict_for_   │
│  users, sessions│     │  login.py        │     │  user()         │
│  predictions    │     └──────────────────┘     └─────────────────┘
└─────────────────┘
```

---

## 1. Dataset Layer

| Component | Location | Role |
|-----------|----------|------|
| Raw CSV | `Data/student_study_data.csv` | 300 simulated student records |
| Generator | `Source/data_generation.py` | Creates overlapping profiles + ~12% label noise |
| Dictionary | `Data/data_dictionary.md` | Column definitions and limitations |

---

## 2. Preprocessing Layer

| Step | Implementation |
|------|----------------|
| Missing values | Median (numeric) / mode (categorical) |
| Validation | Clip attendance and pass_grade to 0–100 |
| Encoding | Per-column `LabelEncoder` → `Models/encoders.pkl` |
| Output | `Data/cleaned_student_data.csv` |

Script: `Source/preprocessing.py`

---

## 3. Machine Learning Layer

| Step | Implementation |
|------|----------------|
| Algorithm | `RandomForestClassifier(random_state=42)` |
| Split | 70% train / 15% validation / 15% test (stratified) |
| Cross-validation | 5-fold on training set only |
| Evaluation | Validation + test accuracy, macro F1, confusion matrix, feature importance |
| Artifacts | `Models/study_risk_model.pkl`, `Outputs/*`, `Outputs/metrics.json` |

Scripts: `Source/ml_model.py`, `Source/model_utils.py`

---

## 4. Model Storage & Inference

| Artifact | Purpose |
|----------|---------|
| `Models/study_risk_model.pkl` | Trained Random Forest |
| `Models/encoders.pkl` | Categorical encoders for train and inference |
| `model_utils.load_model()` | Loads both artifacts |
| `model_utils.predict_for_user()` | Encodes user input, returns risk level + confidence + probabilities |

The Risk Prediction page calls `predict_for_user()`. A rule-based fallback runs only if model files are missing or encoding fails.

---

## 5. Streamlit Frontend

| Component | Location | Role |
|-----------|----------|------|
| Entry point | `Source/Frontend/app.py` | Login gate, sidebar router, page dispatch |
| Auth UI | `Source/Frontend/login.py` | Register, sign in, forgot password |
| Pages | `Source/Frontend/pages_/` | Dashboard, Course Analytics, Risk Prediction, etc. |
| Styling | `Source/Frontend/styles.py` | Dark theme CSS |
| Session | `bootstrap.py`, `utils.py`, `cookie_session.py` | Streamlit session + disk/cookie persistence |

Navigation uses query parameters (`?nav=`, `?logout=`) with a custom HTML sidebar (not Streamlit multipage `pages/`).

---

## 6. Authentication & Database

| Component | Location | Role |
|-----------|----------|------|
| DB helpers | `Source/Backend/db.py` | Supabase PostgreSQL via `DATABASE_URL` |
| Tables | `users`, `sessions`, `predictions` (+ reserved `courses`, `pdfs`) |
| Passwords | bcrypt hashes |
| Sessions | DB tokens + optional 30-day browser cookie (Remember Me) |
| Predictions | `save_prediction()` on successful Risk Prediction |

Login requires a configured `.env` file. Table creation is idempotent (`init_db()` on startup).

---

## 7. Recommendation Generation

Recommendations are **rule-based**, not a separate ML model:

| Source | Logic |
|--------|-------|
| Risk Prediction page | Static tip lists keyed by predicted risk level (High / Medium / Low) |
| Recommendations page | Uses latest session prediction; otherwise shows general tips by risk band |
| Study Schedule page | Weekly hour allocation from dataset course risk levels (heuristic scheduler) |

---

## Technologies

| Layer | Tools |
|-------|-------|
| Language | Python 3.10+ |
| Data | Pandas, NumPy |
| ML | scikit-learn, joblib |
| Visualization | Plotly, matplotlib, seaborn |
| Frontend | Streamlit |
| Database | PostgreSQL (Supabase), psycopg2, bcrypt |
| Config | python-dotenv |

---

## Workflow

Student Input → Dataset Processing → Preprocessing → ML Training → Model Storage → Streamlit Inference → Risk Prediction → Rule-Based Recommendations → Dashboard

See also: `Documentation/workflow_diagram.png`, `Documentation/evaluation_report.md`.
