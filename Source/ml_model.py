import os
import pandas as pd
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.makedirs(os.path.join(ROOT, "Outputs"), exist_ok=True)
os.makedirs(os.path.join(ROOT, "Models"), exist_ok=True)


df = pd.read_csv(os.path.join(ROOT, "Data", "cleaned_student_data.csv"))

print("Dataset loaded successfully")
print(df.head())
print(df.info())


X = df.drop("risk_level", axis=1)
y = df["risk_level"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)


model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)


cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
print("\n5-Fold Cross Validation Scores:", cv_scores)
print("CV Mean Accuracy:", cv_scores.mean())
print("CV Std Deviation:", cv_scores.std())


predictions = model.predict(X_test)


accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:", accuracy)
print("Classification Report:")
print(classification_report(y_test, predictions, zero_division=0))


cm = confusion_matrix(y_test, predictions)
cm_df = pd.DataFrame(
    cm,
    index=[f"actual_{c}" for c in sorted(y.unique())],
    columns=[f"predicted_{c}" for c in sorted(y.unique())],
)
print("\nConfusion Matrix:")
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
results["actual_risk_level"] = y_test
results["predicted_risk_level"] = predictions
results.to_csv(os.path.join(ROOT, "Outputs", "predictions.csv"), index=False)


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
plt.title("Confusion Matrix — Random Forest")
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
    palette="viridis",
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
