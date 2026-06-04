"""
Run only when intentionally regenerating the dataset.
Existing CSV was produced with this same logic.
"""

import os
import random

import pandas as pd

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

DIFFICULTY = ["Low", "Medium", "High"]
WORKLOAD = ["Low", "Medium", "High"]
RISK_LEVELS = ["Low", "Medium", "High"]

N_PER_CLASS = 100
LABEL_NOISE = 0.12

RISK_PROFILES = {
    "High": {
        "hours": (1, 4),
        "att": (30, 65),
        "dead": (0, 5),
        "grade": (40, 68),
        "diff_w": [0.1, 0.3, 0.6],
        "load_w": [0.1, 0.3, 0.6],
    },
    "Medium": {
        "hours": (3, 6),
        "att": (55, 82),
        "dead": (3, 12),
        "grade": (55, 80),
        "diff_w": [0.25, 0.5, 0.25],
        "load_w": [0.25, 0.5, 0.25],
    },
    "Low": {
        "hours": (5, 9),
        "att": (75, 100),
        "dead": (8, 30),
        "grade": (72, 100),
        "diff_w": [0.6, 0.3, 0.1],
        "load_w": [0.6, 0.3, 0.1],
    },
}

random.seed(42)


def _generate_rows(risk_label: str, n: int) -> list:
    p = RISK_PROFILES[risk_label]
    rows = []
    for _ in range(n):
        rows.append({
            "course": random.choice(COURSES),
            "study_hours": random.randint(*p["hours"]),
            "attendance": random.randint(*p["att"]),
            "deadline_days": random.randint(*p["dead"]),
            "pass_grade": random.randint(*p["grade"]),
            "assignment_difficulty": random.choices(DIFFICULTY, weights=p["diff_w"])[0],
            "workload_level": random.choices(WORKLOAD, weights=p["load_w"])[0],
            "risk_level": risk_label,
        })
    return rows


def generate():
    rows = (
        _generate_rows("High", N_PER_CLASS)
        + _generate_rows("Medium", N_PER_CLASS)
        + _generate_rows("Low", N_PER_CLASS)
    )
    random.shuffle(rows)

    for row in rows:
        if random.random() < LABEL_NOISE:
            row["risk_level"] = random.choice(RISK_LEVELS)

    df = pd.DataFrame(rows)
    df.insert(0, "student_id", range(1, len(df) + 1))

    raw_path = os.path.join(ROOT, "Data", "student_study_data.csv")
    df.to_csv(raw_path, index=False)
    print(f"Raw dataset saved to {raw_path} ({len(df)} rows)")


if __name__ == "__main__":
    generate()
