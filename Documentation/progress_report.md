# Progress Report

**Project:** Studor — AI Smart Study Risk & Performance Predictor  
**Status:** Final MVP implemented — documentation and model logic aligned (05.06.2026)

---

## Completed Tasks

### Documentation

- Problem analysis completed and updated for final MVP scope.
- Workflow diagram finalized and uploaded (`Documentation/workflow_diagram.png`).
- System design documented and aligned with the current implementation.
- Gantt chart timeline added (`Documentation/gantt_chart.md`).
- Testing report refreshed with current page names, authentication flow, and ML pipeline tests.
- Evaluation report updated with final model logic and current performance metrics.
- Data dictionary updated to reflect the final six-feature model input.
- Daily logs maintained (`Logs/daily_logs.md`).
- Demo script and deployment plan updated.
- Team contributions updated for final MVP scope.
- Final audit summary completed in `Reports/final_audit_summary.md`.

### Data & Machine Learning

- Simulated academic dataset created.
- Data preprocessing pipeline implemented.
- Encoders generated for categorical academic behavior fields.
- Random Forest classifier trained using a 70/15/15 stratified train/validation/test split.
- 5-fold cross-validation completed on the training set.
- Validation and test evaluation completed.
- Model artifacts regenerated in `Models/`.
- Output metrics regenerated in `Outputs/`.
- Inference API implemented in `Source/model_utils.py`.

### Final Model Logic

- The final system supports free-text course names.
- Course names are stored for personalization, display, course management, dashboard, study schedule, and prediction history.
- The `course` field is no longer encoded and is not used as a machine learning input.
- The previous custom course fallback approach is no longer used.
- Both normal and custom course names use the same Random Forest prediction workflow.

The Random Forest model predicts academic risk using six academic behavior features:

```text
study_hours
attendance
deadline_days
pass_grade
assignment_difficulty
workload_level
```

### Frontend (Studor)

- Login and registration implemented.
- Dashboard implemented.
- My Courses page implemented.
- Course Analytics page implemented.
- Risk Prediction page implemented.
- Study Schedule page implemented with persistence.
- Recommendations page implemented and updated after prediction.
- Model Results page implemented.
- Profile page implemented with prediction history.
- Custom dark-theme UI implemented.
- Query-parameter navigation/router implemented.
- Screenshots added in `Documentation/Screenshots/`.

### Backend

- Supabase PostgreSQL integration implemented.
- User authentication flow implemented.
- Session handling implemented.
- Predictions saved after successful inference.
- Prediction history stored for user profile display.

### Repository

- `.gitignore` configured.
- MIT `LICENSE` added.
- `requirements.txt` updated with working dependency versions.
- Repository structure reviewed.
- Consistent naming maintained: `AI_SE04_StudyRiskPredictor`.
- GitHub repository synchronized.

---

## Current Status

| Area | Status |
|------|--------|
| Frontend | Operational |
| Authentication | Operational with environment configuration |
| My Courses | Implemented |
| Custom course names | Supported |
| ML inference | Operational |
| Prediction workflow | Operational |
| Study Schedule persistence | Implemented |
| Recommendations update | Implemented |
| Profile prediction history | Implemented |
| Documentation | Aligned with final MVP logic |
| Metrics | Updated and aligned with final model output |

---

## Model Performance

| Metric | Value |
|---|---|
| Validation Accuracy | 91.11% |
| Test Accuracy | 93.33% |

The model performance reflects the final Random Forest setup using six academic behavior features.

---

## Remaining / Future Work

The following items are outside the current MVP scope or remain as future improvements:

- Add broader automated unit tests for `model_utils.py`.
- Add automated authentication and CRUD tests.
- Improve deployment pipeline.
- Prepare Streamlit Cloud or alternative deployment.
- Expand dataset size beyond simulated data.
- Improve analytics dashboard.
- Add more advanced recommendation logic.
- Add calendar integration.
- Improve accessibility and responsiveness.

Completed features such as My Courses, prediction history, and study schedule persistence are no longer listed as future work.

---

## Overall Progress

The project is in the final MVP completion stage.

Core development, machine learning pipeline, dashboard, authentication, My Courses, prediction history, study schedule persistence, recommendations, and documentation are implemented.

The current MVP reflects the final model logic: course names are used for personalization and display, while academic risk prediction is based on six academic behavior features.

The project is ready for progress presentation and demo, with honest discussion of simulated data limitations and remaining future improvements.
