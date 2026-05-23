import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("Data/student_study_data.csv")

print("Raw dataset loaded successfully.")
print("Dataset shape:", df.shape)

print("\nMissing values:")
print(df.isnull().sum())

df = df.drop_duplicates()

numeric_columns = [
    "study_hours",
    "attendance",
    "deadline_days",
    "past_grade"
]

for column in numeric_columns:
    df[column] = df[column].fillna(df[column].median())

categorical_columns = [
    "course",
    "assignment_difficulty",
    "workload_level",
    "risk_level"
]

for column in categorical_columns:
    df[column] = df[column].fillna(df[column].mode()[0])

df["attendance"] = df["attendance"].clip(0, 100)
df["past_grade"] = df["past_grade"].clip(0, 100)

encoder = LabelEncoder()

for column in categorical_columns:
    df[column] = encoder.fit_transform(df[column])

df.to_csv("Data/cleaned_student_data.csv", index=False)

print("\nPreprocessing completed successfully.")
print("Cleaned dataset saved.")