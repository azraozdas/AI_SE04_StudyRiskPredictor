import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("Data/student_study_data.csv")

print("Missing values:")
print(df.isnull().sum())

encoder = LabelEncoder()

df["course"] = encoder.fit_transform(df["course"])
df["assignment_difficulty"] = encoder.fit_transform(df["assignment_difficulty"])
df["risk_level"] = encoder.fit_transform(df["risk_level"])

df.to_csv("Data/cleaned_student_data.csv", index=False)

print("Preprocessing completed successfully.")