# Studor – AI Smart Study Risk & Performance Predictor

Studor is an AI-powered academic support application that helps students understand study risk, manage course workload, and receive personalized study recommendations.

The system allows students to add their own courses, submit academic behavior data, and receive a predicted risk level based on machine learning.

---

## Project Purpose

Students often struggle to identify academic risk early enough. Risk can be affected by:

- low attendance
- low study hours
- upcoming deadlines
- low pass grades
- assignment difficulty
- workload pressure

Studor supports students by predicting academic risk and displaying clear study recommendations.

---

## Main Features

| Feature | Description |
|---|---|
| Authentication | Register, login, and logout workflow |
| Dashboard | Overview of student activity and study status |
| My Courses | Students can add and manage custom course names |
| Course Analytics | Displays course-related statistics and insights |
| Risk Prediction | Predicts academic risk using ML model |
| Study Recommendations | Displays recommendation based on prediction result |
| Study Schedule | Updates study planning information after prediction |
| Profile | Shows user information and prediction history |
| Model Results | Displays model-related evaluation outputs |
| Documentation | Includes project analysis, system design, testing, and reports |

---

## Prediction Logic

Studor allows students to add any course name.

Course names are used for personalization, course management, dashboard display, schedule, and prediction history.

The ML model predicts risk based on academic behavior factors only.

The final Random Forest model uses six input features:

```text
study_hours
attendance
deadline_days
pass_grade
assignment_difficulty
workload_level
```

The `course` field is not encoded and is not used as a model input.

There is no custom course fallback model. Both predefined and custom courses use the same Random Forest prediction workflow.

---

## Model Performance

| Metric | Value |
|---|---|
| Validation Accuracy | 91.11% |
| Test Accuracy | 93.33% |

The model performance values are based on the updated final model logic using six academic behavior features.

---

## Technologies Used

- Python
- Streamlit
- Scikit-learn
- Pandas
- NumPy
- Joblib
- Supabase
- Git
- GitHub

---

## Project Structure

```text
AI_SE04_StudyRiskPredictor/
├── Data/
├── Documentation/
├── Logs/
├── Models/
├── Outputs/
├── Reports/
├── Source/
│   ├── Backend/
│   └── Frontend/
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## Documentation

Important documentation files:

```text
Documentation/problem_analysis.md
Documentation/system_design.md
Documentation/testing_report.md
Documentation/evaluation_report.md
Documentation/data_dictionary.md
Documentation/progress_report.md
Documentation/team_contributions.md
Documentation/gantt_chart.md
Documentation/demo_script.md
Documentation/deployment_plan.md
Reports/final_audit_summary.md
Logs/daily_logs.md
```

---

## Current Status

The MVP is functional and supports the final course-management and prediction logic.

Current system status:

- Authentication workflow implemented
- Custom course names supported
- My Courses page implemented
- Course Analytics page implemented
- Prediction history implemented
- Study schedule persistence implemented
- Random Forest prediction workflow functional
- Model uses six academic behavior features
- Documentation updated for final MVP scope

---

## Future Work

Potential future improvements:

- Add broader automated test coverage
- Improve deployment pipeline
- Expand dataset size
- Improve analytics dashboard
- Add more advanced recommendation logic
- Add calendar integration
- Improve UI accessibility and responsiveness

Completed features such as per-user course UI and prediction history are no longer listed as future work.

---

## Team

| Member | Role |
|---|---|
| Dilay Tarhan | Documentation, Testing, Submission Readiness |
| Azra Özdaş | Frontend / Streamlit |
| Eylül Özekinci | Machine Learning |
| Müslüm Selim Akşahin | Data Collection & Preprocessing |

---

## License

This project uses the MIT License.
