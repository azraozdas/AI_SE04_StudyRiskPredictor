import os
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def preprocess():
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    df = pd.read_csv(os.path.join(ROOT, "Data", "student_study_data.csv"))

    print("Raw dataset loaded successfully.")
    print("Dataset shape:", df.shape)

    print("\nMissing values:")
    print(df.isnull().sum())

    if "student_id" in df.columns:
        df = df.drop("student_id", axis=1)

    numeric_columns = ["study_hours", "attendance", "deadline_days", "pass_grade"]
    for column in numeric_columns:
        df[column] = df[column].fillna(df[column].median())

    # course is kept as a string column for display/context but is NOT encoded
    # for model training — it must not be a model feature.
    categorical_fill = ["course", "assignment_difficulty", "workload_level", "risk_level"]
    for column in categorical_fill:
        df[column] = df[column].fillna(df[column].mode()[0])

    df = df.drop_duplicates()

    df["attendance"] = df["attendance"].clip(0, 100)
    df["pass_grade"] = df["pass_grade"].clip(0, 100)

    # Only encode the columns that are used as model features or as the target.
    # course is intentionally excluded from encoding.
    encode_columns = ["assignment_difficulty", "workload_level", "risk_level"]
    encoders = {}
    for column in encode_columns:
        enc = LabelEncoder()
        df[column] = enc.fit_transform(df[column])
        encoders[column] = enc

    joblib.dump(encoders, os.path.join(ROOT, "Models", "encoders.pkl"))
    df.to_csv(os.path.join(ROOT, "Data", "cleaned_student_data.csv"), index=False)

    print("\nPreprocessing completed successfully.")
    print("Cleaned dataset saved (course column kept as string for display).")
    print("Encoders saved to Models/encoders.pkl (course encoder removed)")


if __name__ == "__main__":
    preprocess()
