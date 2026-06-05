# Data Dictionary — Student Study Risk Dataset

**Version 1.6** — aligned with `Source/data_generation.py` (300 rows, overlapping profiles, ~12% label noise).

The cleaned dataset (`cleaned_student_data.csv`) contains **8 columns**. The `student_id` column in the raw CSV is dropped during preprocessing and is not used for training.

| Column | Type | Values / Range | Meaning |
|---|---|---|---|
| course | categorical (encoded) | 0–19 | Name of the course being studied (20 courses) |
| study_hours | integer | 0–15 | Weekly hours the student spends studying |
| attendance | integer | 0–100 | Attendance percentage for the course |
| deadline_days | integer | 0–30 | Days remaining until the next assignment deadline |
| pass_grade | integer | 0–100 | Student's current or most recent grade in the course |
| assignment_difficulty | categorical (encoded) | High=0, Low=1, Medium=2 | Difficulty of the current assignment |
| workload_level | categorical (encoded) | High=0, Low=1, Medium=2 | Overall workload level for the course |
| risk_level | categorical (encoded, target) | High=0, Low=1, Medium=2 | Academic risk level — model prediction target |

## Generation Rules (`Source/data_generation.py`)

- **300 rows** — 100 per nominal risk class (High, Medium, Low) before noise.
- **Overlapping profiles** — each class samples from overlapping ranges (e.g. High: 1–4 study hours, 30–65% attendance; Low: 5–9 hours, 75–100% attendance). Classes are not perfectly separable.
- **Probabilistic categoricals** — assignment difficulty and workload are drawn from class-specific weight distributions, not fixed rules.
- **Label noise** — after generation, **~12%** of rows have `risk_level` randomly reassigned to reduce deterministic leakage.
- **Balanced classes** — 100 rows per nominal class before noise; after noise the class counts may differ slightly.

Regenerate the raw CSV with:

```bash
python Source/data_generation.py
python Source/preprocessing.py
```

## Preprocessing (`Source/preprocessing.py`)

1. Drop `student_id`.
2. Fill numeric missing values with column medians; categoricals with mode.
3. Drop duplicate rows.
4. Clip `attendance` and `pass_grade` to 0–100.
5. Label-encode categoricals (`course`, `assignment_difficulty`, `workload_level`, `risk_level`).
6. Save encoders to `Models/encoders.pkl` and cleaned CSV to `Data/cleaned_student_data.csv`.

## Encoder Mapping

Categorical columns use `sklearn.preprocessing.LabelEncoder` (alphabetical order). Fitted encoders are saved to `Models/encoders.pkl`. **Always use `encoders.pkl` for inference** — do not hardcode integer maps.

| Column | Encoded as |
|---|---|
| course | 0–19 (20 courses, alphabetical) |
| assignment_difficulty | High=0, Low=1, Medium=2 |
| workload_level | High=0, Low=1, Medium=2 |
| risk_level (target) | High=0, Low=1, Medium=2 |

## Limitations

- **Fully simulated** — no real student records.
- **Small sample** — 300 rows; metrics have wide confidence intervals on real data.
- **Label noise** — reduces but does not eliminate synthetic bias; patterns still approximate designed profiles.
- **Global dataset** — all 300 rows are shared training/demo data, not per-user histories in the database.
- **Course feature** — low model importance; risk is driven mainly by attendance, deadlines, grades, and study hours (see `Outputs/feature_importance.csv`).
