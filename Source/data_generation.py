"""
Run only when intentionally regenerating the dataset.
Existing CSV was produced with this same logic.
"""

import os
import random

import pandas as pd
from sklearn.preprocessing import LabelEncoder

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COURSES = [
    "Algorithms",
    "Artificial Intelligence",
    "Cloud Computing",
    "Computer Architecture",
    "Computer Networks",
    "Cybersecurity Fundamentals",
    "Data Science",
    "Database Systems",
    "Discrete Mathematics",
    "Human-Computer Interaction",
    "Information Systems",
    "Introduction to Programming",
    "Linear Algebra",
    "Machine Learning",
    "Mobile App Development",
    "Object-Oriented Programming",
    "Operating Systems",
    "Software Engineering",
    "Statistics",
    "Web Development",
]

random.seed(42)


def _generate_rows(risk_label: str, n: int) -> list:
    rows = []
    for _ in range(n):
        if risk_label == "High":
            row = {
                "course": random.choice(COURSES),
                "study_hours": random.randint(1, 3),
                "attendance": random.randint(30, 58),
                "deadline_days": random.randint(0, 3),
                "pass_grade": random.randint(40, 62),
                "assignment_difficulty": "High",
                "workload_level": "High",
                "risk_level": "High",
            }
        elif risk_label == "Medium":
            row = {
                "course": random.choice(COURSES),
                "study_hours": random.randint(3, 5),
                "attendance": random.randint(55, 80),
                "deadline_days": random.randint(2, 8),
                "pass_grade": random.randint(56, 76),
                "assignment_difficulty": "Medium",
                "workload_level": "Medium",
                "risk_level": "Medium",
            }
        else:  # Low
            row = {
                "course": random.choice(COURSES),
                "study_hours": random.randint(5, 8),
                "attendance": random.randint(78, 100),
                "deadline_days": random.randint(6, 30),
                "pass_grade": random.randint(74, 100),
                "assignment_difficulty": "Low",
                "workload_level": "Low",
                "risk_level": "Low",
            }
        rows.append(row)
    return rows


def generate():
    rows = (
        _generate_rows("High", 70)
        + _generate_rows("Medium", 70)
        + _generate_rows("Low", 70)
    )
    random.shuffle(rows)

    df = pd.DataFrame(rows)
    df.insert(0, "student_id", range(1, len(df) + 1))

    raw_path = os.path.join(ROOT, "Data", "student_study_data.csv")
    df.to_csv(raw_path, index=False)
    print(f"Raw dataset saved to {raw_path}")

    cleaned = df.drop(columns=["student_id"]).copy()
    for col in ["course", "assignment_difficulty", "workload_level", "risk_level"]:
        le = LabelEncoder()
        cleaned[col] = le.fit_transform(cleaned[col])

    cleaned_path = os.path.join(ROOT, "Data", "cleaned_student_data.csv")
    cleaned.to_csv(cleaned_path, index=False)
    print(f"Cleaned dataset saved to {cleaned_path}")


if __name__ == "__main__":
    generate()
