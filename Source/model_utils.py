"""
Inference helpers for the Study Risk model.
Pure functions (no Streamlit) so they can be unit-tested directly.
"""

import os
import joblib
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
MODEL_PATH = os.path.join(ROOT, "Models", "study_risk_model.pkl")
ENCODERS_PATH = os.path.join(ROOT, "Models", "encoders.pkl")

_CATEGORICAL = ("assignment_difficulty", "workload_level")


def load_model():
    """Load the trained model and the per-column LabelEncoders.

    Returns (model, encoders). Raises FileNotFoundError with a clear message
    if the artifacts have not been generated yet.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Run: python Source/ml_model.py"
        )
    if not os.path.exists(ENCODERS_PATH):
        raise FileNotFoundError(
            f"Encoders not found at {ENCODERS_PATH}. Run: python Source/preprocessing.py"
        )
    model = joblib.load(MODEL_PATH)
    encoders = joblib.load(ENCODERS_PATH)
    return model, encoders


def _encode(encoders, column, value):
    enc = encoders[column]
    classes = list(enc.classes_)
    if value not in classes:
        raise ValueError(
            f"Unknown {column}: {value!r}. Expected one of {classes}."
        )
    return int(enc.transform([value])[0])


def predict_for_user(model, encoders, *, study_hours, attendance,
                     deadline_days, pass_grade, assignment_difficulty,
                     workload_level):
    """Predict risk for one student. Categorical args are human-readable
    strings (e.g. 'High'); they are encoded here to match training.

    course is NOT a parameter — it is display-only and does not affect
    the prediction. Any course name can be shown in the UI without needing
    to be in the training set.

    Returns: {"risk_level": str, "confidence": float, "probabilities": dict}
    """
    row = {
        "study_hours": float(study_hours),
        "attendance": float(attendance),
        "deadline_days": float(deadline_days),
        "pass_grade": float(pass_grade),
        "assignment_difficulty": _encode(encoders, "assignment_difficulty", assignment_difficulty),
        "workload_level": _encode(encoders, "workload_level", workload_level),
    }

    # Guarantee the column order the model was trained on
    feature_order = list(getattr(model, "feature_names_in_", row.keys()))
    X = pd.DataFrame([[row[c] for c in feature_order]], columns=feature_order)

    pred_int = int(model.predict(X)[0])
    risk_label = encoders["risk_level"].inverse_transform([pred_int])[0]

    proba = model.predict_proba(X)[0]
    class_labels = encoders["risk_level"].inverse_transform(model.classes_)
    probabilities = {lbl: float(p) for lbl, p in zip(class_labels, proba)}

    return {
        "risk_level": risk_label,
        "confidence": float(max(proba)),
        "probabilities": probabilities,
    }