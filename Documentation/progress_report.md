# Progress Report

**Project:** Studor — AI Smart Study Risk & Performance Predictor  
**Status:** MVP complete — documentation and metrics aligned (05.06.2026)

---

## Completed Tasks

### Documentation
- Problem analysis
- Workflow diagram (`Documentation/workflow_diagram.png`)
- System design (architecture aligned with implementation)
- Gantt chart timeline (`Documentation/gantt_chart.md`)
- Testing report
- Evaluation report + `Outputs/metrics.json`
- Daily logs (`Logs/daily_logs.md`)
- Demo script and deployment plan
- Team contributions

### Data & Machine Learning
- 300-row simulated dataset with overlapping profiles and ~12% label noise
- Preprocessing pipeline with portable paths and `encoders.pkl`
- Random Forest classifier with 70/15/15 stratified split
- 5-fold CV on training set; validation and test evaluation
- Inference API (`Source/model_utils.py`)
- Regenerated model artifacts in `Models/` and `Outputs/`

### Frontend (Studor)
- Login / registration (Supabase)
- Dashboard, Course Analytics, Risk Prediction, Study Schedule, Recommendations, Model Results, Profile
- Custom dark-theme UI with query-param router
- Screenshots in `Documentation/Screenshots/`

### Backend
- Supabase PostgreSQL: users, sessions, predictions
- bcrypt authentication and security-question password reset
- Saved predictions on successful inference

### Repository
- `.gitignore`, MIT `LICENSE`, `requirements.txt`
- Consistent naming: `AI_SE04_StudyRiskPredictor`

---

## Current Status

| Area | Status |
|------|--------|
| Frontend | Operational |
| ML inference | Operational |
| Database auth | Operational (requires `.env`) |
| Documentation | Aligned with implementation |
| Metrics | Single source: `Outputs/metrics.json` |

---

## Remaining / Future Work (out of current MVP)

- Display saved prediction history from database on Profile
- Per-user course management UI (schema reserved in `db.py`)
- Automated unit tests for `model_utils.py`
- Streamlit Cloud deployment

---

## Overall Progress

Core development, ML pipeline, dashboard, authentication, and documentation are complete. The project is ready for progress presentation and demo with honest discussion of simulated data limitations.
