"""
Train and evaluate the Study Risk Random Forest classifier.

Split policy (documented in Documentation/evaluation_report.md):
  70% train | 15% validation | 15% test — stratified, random_state=42
  5-fold CV runs on the training set only.
  Final model is fit on the training set and evaluated on held-out val/test.
"""

import json
import os

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import cross_val_score, train_test_split

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.makedirs(os.path.join(ROOT, "Outputs"), exist_ok=True)
os.makedirs(os.path.join(ROOT, "Models"), exist_ok=True)


df = pd.read_csv(os.path.join(ROOT, "Data", "cleaned_student_data.csv"))

print("Dataset loaded successfully")
print(f"Shape: {df.shape}")
print(df.head())
print(df.info())

X = df.drop("risk_level", axis=1)
y = df["risk_level"]

# 70% train, 30% temporary (validation + test)
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)
# Split temporary 50/50 → 15% validation, 15% test
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
)

print(f"\nSplit sizes — train: {len(X_train)}, val: {len(X_val)}, test: {len(X_test)}")

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
val_predictions = model.predict(X_val)
val_accuracy = accuracy_score(y_val, val_predictions)

test_predictions = model.predict(X_test)
test_accuracy = accuracy_score(y_test, test_predictions)
test_macro_f1 = f1_score(y_test, test_predictions, average="macro")

print("\n5-Fold Cross Validation Scores:", cv_scores)
print("CV Mean Accuracy:", cv_scores.mean())
print("CV Std Deviation:", cv_scores.std())
print(f"\nValidation Accuracy: {val_accuracy:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Test Macro F1: {test_macro_f1:.4f}")
print("\nClassification Report (test set):")
print(classification_report(y_test, test_predictions, zero_division=0))

cm = confusion_matrix(y_test, test_predictions)
class_ids = sorted(y.unique())
cm_df = pd.DataFrame(
    cm,
    index=[f"actual_{c}" for c in class_ids],
    columns=[f"predicted_{c}" for c in class_ids],
)
print("\nConfusion Matrix (test set):")
print(cm_df)
cm_df.to_csv(os.path.join(ROOT, "Outputs", "confusion_matrix.csv"))

importances = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_,
}).sort_values("importance", ascending=False)

print("\nFeature Importance:")
print(importances.to_string(index=False))
importances.to_csv(os.path.join(ROOT, "Outputs", "feature_importance.csv"), index=False)

results = X_test.copy()
results["actual_risk_level"] = y_test.values
results["predicted_risk_level"] = test_predictions
results.to_csv(os.path.join(ROOT, "Outputs", "predictions.csv"), index=False)

metrics = {
    "dataset_rows": int(len(df)),
    "train_samples": int(len(X_train)),
    "validation_samples": int(len(X_val)),
    "test_samples": int(len(X_test)),
    "cv_fold_scores": [float(s) for s in cv_scores],
    "cv_mean_accuracy": float(cv_scores.mean()),
    "cv_std_accuracy": float(cv_scores.std()),
    "validation_accuracy": float(val_accuracy),
    "test_accuracy": float(test_accuracy),
    "test_macro_f1": float(test_macro_f1),
    "feature_importance_ranking": importances[["feature", "importance"]].to_dict(orient="records"),
}
metrics_path = os.path.join(ROOT, "Outputs", "metrics.json")
with open(metrics_path, "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)
print(f"\nMetrics saved to {metrics_path}")

cm_fig_path = os.path.join(ROOT, "Outputs", "confusion_matrix.png")
plt.figure(figsize=(6, 5))
sns.heatmap(
    cm_df,
    annot=True,
    fmt="d",
    cmap="Blues",
    cbar=True,
    linewidths=0.5,
    linecolor="white",
)
plt.title("Confusion Matrix — Random Forest (test set)")
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.tight_layout()
plt.savefig(cm_fig_path, dpi=150)
plt.close()

fi_fig_path = os.path.join(ROOT, "Outputs", "feature_importance.png")
plt.figure(figsize=(7, 5))
sns.barplot(
    data=importances,
    x="importance",
    y="feature",
    hue="feature",
    palette="viridis",
    legend=False,
)
plt.title("Feature Importance — Random Forest")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.tight_layout()
plt.savefig(fi_fig_path, dpi=150)
plt.close()

joblib.dump(model, os.path.join(ROOT, "Models", "study_risk_model.pkl"))

print("\nPredictions saved to Outputs/predictions.csv")
print("Confusion matrix saved to Outputs/confusion_matrix.csv")
print("Feature importance saved to Outputs/feature_importance.csv")
print("Confusion matrix plot saved to Outputs/confusion_matrix.png")
print("Feature importance plot saved to Outputs/feature_importance.png")
print("Model saved to Models/study_risk_model.pkl")
