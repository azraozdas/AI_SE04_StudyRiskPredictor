# Evaluation Report

Authoritative metrics are produced by `python Source/ml_model.py` and saved to `Outputs/metrics.json`. The values below match the committed artifacts in `Outputs/` (regenerated with the current dataset and training script).

## 1. Dataset Summary

The model is trained on `Data/cleaned_student_data.csv`.

| Item | Value |
|------|-------|
| Total rows | 300 |
| Features | 7: `course`, `study_hours`, `attendance`, `deadline_days`, `pass_grade`, `assignment_difficulty`, `workload_level` |
| Target | `risk_level` (LabelEncoder — see `Models/encoders.pkl`) |
| Missing values | None (all columns non-null) |
| Label noise | ~12% of rows randomly relabelled during generation (`Source/data_generation.py`, `LABEL_NOISE = 0.12`) |

Column definitions: `Data/data_dictionary.md`.

Data is generated with overlapping feature ranges per risk class, probabilistic difficulty/workload, and injected label noise.

---

## 2. Train / Validation / Test Split

`sklearn.model_selection.train_test_split` with `random_state=42` and stratification.

| Split | Samples | Share |
|-------|---------|-------|
| Train | 210 | 70% |
| Validation | 45 | 15% |
| Test | 45 | 15% |

Model: `RandomForestClassifier(random_state=42)` (default hyperparameters).

The model is fit on the **training set only**. The validation set is used for an intermediate accuracy check. The test set is held out until final evaluation. Cross-validation runs only on the training set.

---

## 3. 5-Fold Cross-Validation

Cross-validation runs **only on the training set** (`X_train`, `y_train`).

| Fold | Accuracy |
|------|----------|
| Fold 1 | 0.9286 |
| Fold 2 | 0.7857 |
| Fold 3 | 0.8810 |
| Fold 4 | 0.8333 |
| Fold 5 | 0.9048 |
| **Mean** | **0.8667** |
| **Std** | **0.0513** |

Validation accuracy (held-out 15%): **0.8889** (88.89%).

Held-out test accuracy: **0.9111** (91.11%).

Test macro F1: **0.91**.

---

## 4. Confusion Matrix (test set)

![Confusion Matrix](../Outputs/confusion_matrix.png)

CSV: `Outputs/confusion_matrix.csv`.

Encoded class IDs follow `Models/encoders.pkl` (`risk_level`: High=0, Low=1, Medium=2).

|  | pred_0 | pred_1 | pred_2 |
|--|--------|--------|--------|
| actual_0 | 14 | 0 | 1 |
| actual_1 | 0 | 14 | 1 |
| actual_2 | 2 | 0 | 13 |

---

## 5. Feature Importance

![Feature Importance](../Outputs/feature_importance.png)

CSV: `Outputs/feature_importance.csv`.

Top features by Gini importance (test-set model):

| Feature | Importance |
|---------|------------|
| attendance | 0.247 |
| deadline_days | 0.224 |
| pass_grade | 0.215 |
| study_hours | 0.182 |
| course | 0.061 |
| workload_level | 0.045 |
| assignment_difficulty | 0.027 |

Risk is driven mainly by attendance, deadlines, grades, and study hours. Course name and difficulty/workload carry less signal after label noise is applied.

---

## 6. Inference API

`Source/model_utils.py` exposes:

- `load_model()` — loads `Models/study_risk_model.pkl` and `Models/encoders.pkl`
- `predict_for_user(...)` — encodes human-readable inputs and returns `risk_level`, `confidence`, and `probabilities`

The Streamlit **Risk Prediction** page (`Source/Frontend/pages_/risk_prediction.py`) calls these helpers and can persist results via `save_prediction()` in `db.py`.

---

## 7. Integration Fix — Feature Naming

During integration testing, predictions failed because the frontend initially sent `past_grade` while the model and dataset use `pass_grade`. The frontend was corrected so inputs match the trained feature schema.

---

## 8. Limitations

- **Simulated data:** No real student records; patterns approximate academic behaviour.
- **Small sample:** 300 rows limits statistical confidence; real deployments would need more data.
- **Label noise:** ~12% random relabelling reduces deterministic leakage but does not replace real-world variability.
- **Default hyperparameters:** Random Forest was not tuned; metrics may improve with search on a larger dataset.

---

## 9. Q&A — “Why isn’t accuracy 100%?”

> An early dataset version used fixed rules on the same features as labels, which produced ~100% cross-validation — a sign of leakage, not a reliable result. We rebuilt the generator with **overlapping value ranges, probabilistic difficulty/workload, and ~12% label noise**, and we evaluate with a **70/15/15 stratified split** plus **5-fold CV on the training set only**. Metrics are now about **87% CV mean** and **91% on the held-out test set**, which is more realistic for this signal. The pipeline (Random Forest, CV, confusion matrix, feature importance) is designed to plug into real student data; the main limitation today is the data source, not the method.

---

## Reproducing Results

```bash
python Source/data_generation.py   # optional — only if regenerating raw CSV
python Source/preprocessing.py
python Source/ml_model.py
```

This regenerates `Models/study_risk_model.pkl`, all files in `Outputs/`, and `Outputs/metrics.json`.
