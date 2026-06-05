# Data Dictionary — Student Study Risk Dataset
**Version 1.5** — updated 04.06.2026: expanded to 300 rows (100 per class), retrained model.

The cleaned dataset (`cleaned_student_data.csv`) contains 8 columns. The `student_id` column present in the raw dataset is dropped during preprocessing and is not included here.

| Column | Type | Values / Range | Meaning |
|---|---|---|---|
| course | categorical (encoded) | 0–19 | Name of the course being studied |
| study_hours | integer | 0–15 | Weekly hours the student spends studying |
| attendance | integer | 0–100 | Attendance percentage for the course |
| deadline_days | integer | 0–30 | Days remaining until the next assignment deadline |
| pass_grade | integer | 0–100 | Student's current or most recent grade in the course |
| assignment_difficulty | categorical (encoded) | 0=High, 1=Low, 2=Medium | Difficulty level of the current assignment |
| workload_level | categorical (encoded) | 0=High, 1=Low, 2=Medium | Overall workload level for the course |
| risk_level | categorical (encoded, target) | 0=High, 1=Low, 2=Medium | Predicted academic risk level — this is what the model predicts |

## Simulation Rules

Risk levels were assigned based on a combination of academic performance and workload indicators. A student was labelled **High Risk** when they had low study hours (1–3 h/week), low attendance (30–58%), a deadline within 0–3 days, a low pass grade (40–62), and High assignment difficulty together with High workload. **Medium Risk** was assigned for moderate values across all indicators: 3–5 study hours, 55–80% attendance, 2–8 days to deadline, a pass grade of 56–76, and Medium difficulty and workload. **Low Risk** was assigned when a student showed strong engagement: 5–8 study hours, 78–100% attendance, at least 6 days until the deadline, a pass grade of 74–100, and Low difficulty and workload. The dataset was constructed with balanced class sizes (100 rows per class, 300 total) to avoid bias toward any single risk category during model training.

## Encoder Mapping

Categorical columns are encoded with `sklearn.preprocessing.LabelEncoder` (alphabetical order). The fitted encoders are serialised to `Models/encoders.pkl` via `joblib`. **Always use `encoders.pkl` for inference** — do not rely on hardcoded integer maps, as re-running `preprocessing.py` may produce a different ordering if new category values are added.

| Column | Encoded as |
|---|---|
| course | 0–19 (20 courses, alphabetical) |
| assignment_difficulty | High=0, Low=1, Medium=2 |
| workload_level | High=0, Low=1, Medium=2 |
| risk_level (target) | High=0, Low=1, Medium=2 |

## Limitations

- Dataset is fully simulated. No real student records.
- Target leakage by construction. risk_level is a deterministic function of the same six features the model trains on.
- Small sample. 300 rows / no noise / balanced classes inflate apparent performance.
- Multi-user story not supported by per-user data store — all 300 rows represent the global dataset, not individual student histories.
