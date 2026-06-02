# Evaluation Report

## 1. Dataset Summary

The model is trained on `Data/cleaned_student_data.csv`.

| Item | Value |
|------|-------|
| Total rows | 210 |
| Features | 7: `course`, `study_hours`, `attendance`, `deadline_days`, `pass_grade`, `assignment_difficulty`, `workload_level` |
| Target | `risk_level` (0 = low, 1 = medium, 2 = high) |
| Missing values | None (all columns non-null) |

Column definitions: `Data/data_dictionary.md`.

---

## 2. Train / Test Split

`sklearn.model_selection.train_test_split` with `test_size=0.2`, `random_state=42`.

| Split | Samples |
|-------|---------|
| Train | 168 (80%) |
| Test | 42 (20%) |

Model: `RandomForestClassifier(random_state=42)`.

---

## 3. 5-Fold Cross-Validation

Cross-validation runs **only on the training set** (`X_train`, `y_train`) so the held-out test set does not leak into the CV estimate.

| Fold | Accuracy |
|------|----------|
| Fold 1 | 1.0000 |
| Fold 2 | 1.0000 |
| Fold 3 | 1.0000 |
| Fold 4 | 1.0000 |
| Fold 5 | 1.0000 |
| **Mean** | **1.0000** |
| **Std** | **0.0000** |

Held-out test accuracy: **0.9762** (97.62%).

---

## 4. Confusion Matrix

![Confusion Matrix](../Outputs/confusion_matrix.png)

CSV: `Outputs/confusion_matrix.csv`.

|  | pred_0 | pred_1 | pred_2 |
|--|--------|--------|--------|
| actual_0 | 11 | 0 | 0 |
| actual_1 | 0 | 16 | 1 |
| actual_2 | 0 | 0 | 14 |

---

## 5. Feature Importance

![Feature Importance](../Outputs/feature_importance.png)

CSV: `Outputs/feature_importance.csv`.

Top features by importance: `workload_level` (0.27), `assignment_difficulty` (0.25), `attendance` (0.23), `pass_grade` (0.15).

---

## 6. Bug Fix — Feature Naming

During integration testing, predictions failed because the frontend sent `past_grade` while the model and dataset use `pass_grade`. **The frontend was corrected to use `pass_grade`** so inputs match the trained feature schema.

---

## 7. Limitations

- **Leakage:** An earlier version ran `cross_val_score` on full `X, y` instead of `X_train, y_train`, which could inflate CV by mixing test data into folds. The script now CVs only on the train split; other leakage paths (e.g. target-derived features) were not formally audited.
- **Dataset size:** 210 rows limits how stable accuracy and CV estimates are.
- **No noise:** Data are fully observed integers with no missing values or measurement noise; real-world student data would likely perform worse than these metrics suggest.