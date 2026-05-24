import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. Load cleaned dataset
df = pd.read_csv("Data/cleaned_student_data.csv")

print("Dataset loaded successfully")
print(df.head())
print(df.info())

# 2. Separate features and target
X = df.drop("risk_level", axis=1)
y = df["risk_level"]

# 3. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# 4. Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 5. Make predictions
predictions = model.predict(X_test)

# 6. Evaluate model
accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)
print("Classification Report:")
print(classification_report(y_test, predictions, zero_division=0))

# 7. Save predictions
results = X_test.copy()
results["actual_risk_level"] = y_test
results["predicted_risk_level"] = predictions
results.to_csv("Outputs/predictions.csv", index=False)

# 8. Save trained model
joblib.dump(model, "Models/study_risk_model.pkl")

print("Predictions saved to Outputs/predictions.csv")
print("Model saved to Models/study_risk_model.pkl")