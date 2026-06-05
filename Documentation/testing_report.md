# Testing Report — Studor

## Test Environment

- Platform: Windows / macOS (local)
- IDE: Visual Studio Code
- Framework: Streamlit
- Python: 3.10+
- Database: Supabase PostgreSQL (via `.env`)

---

## Functional Testing

### Test 1: Application Launch

| | |
|---|---|
| **Action** | Run `streamlit run Source/Frontend/app.py` |
| **Expected** | Login page opens at localhost:8501 |
| **Result** | Passed |

### Test 2: Registration and Login

| | |
|---|---|
| **Action** | Create account, sign in, sign out |
| **Expected** | User stored in Supabase; session persists with Remember Me |
| **Result** | Passed (requires valid `DATABASE_URL`) |

### Test 3: Navigation

| | |
|---|---|
| **Action** | Visit Dashboard, Course Analytics, Risk Prediction, Study Schedule, Recommendations, Model Results, Profile |
| **Expected** | All sidebar pages load without errors |
| **Result** | Passed |

### Test 4: Risk Prediction

| | |
|---|---|
| **Action** | Submit form with sample inputs |
| **Expected** | Risk level, confidence, recommendations, chart; optional DB save |
| **Result** | Passed |

### Test 5: Course Analytics

| | |
|---|---|
| **Action** | Open Course Analytics; search and filter courses |
| **Expected** | Aggregated stats from `student_study_data.csv` |
| **Result** | Passed |

### Test 6: Model Results

| | |
|---|---|
| **Action** | Open Model Results |
| **Expected** | Confusion matrix, feature importance, predictions table from `Outputs/` |
| **Result** | Passed |

### Test 7: Profile and Team Info

| | |
|---|---|
| **Action** | Open Profile; edit name/department; view team section |
| **Expected** | Session profile updates; team roles displayed |
| **Result** | Passed |

### Test 8: ML Pipeline Reproducibility

| | |
|---|---|
| **Action** | Run `python Source/preprocessing.py` then `python Source/ml_model.py` |
| **Expected** | Regenerates `Models/`, `Outputs/metrics.json`; metrics match evaluation report |
| **Result** | Passed |

---

## Issues Found and Resolved

| Issue | Resolution |
|-------|------------|
| Frontend sent `past_grade` instead of `pass_grade` | Renamed to match model features |
| Encoder mismatch in prediction | Integrated `encoders.pkl` via `model_utils.py` |
| CV evaluated on full dataset (leakage) | CV restricted to training set in `ml_model.py` |
| Dependency version conflicts | Pinned in `requirements.txt` |

---

## Known Gaps (not blocking demo)

- No automated pytest suite (manual testing only)
- Saved predictions written to DB but not listed on Profile page
- Login requires network access to Supabase

---

## Overall Result

The system passes manual functional testing for all implemented pages and the ML training pipeline. Ready for demo with documented limitations on simulated data.
