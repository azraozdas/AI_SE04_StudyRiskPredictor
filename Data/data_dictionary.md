# Data Dictionary

## Project

Studor / AI Smart Study Risk & Performance Predictor

---

## Purpose

This document explains the dataset fields used in the Studor system and identifies which fields are used as machine learning inputs.

The final model predicts academic risk using six academic behavior features. Course names are used for display and course management only.

---

## Dataset Fields

| Field | Type | Description | Used as ML Input |
|---|---|---|---|
| `student_id` | Integer / Identifier | Unique student identifier | No |
| `course` | Text | Course name used for display, course management, dashboard, schedule, and history | No |
| `study_hours` | Numeric | Number of weekly study hours | Yes |
| `attendance` | Numeric | Student attendance percentage | Yes |
| `deadline_days` | Numeric | Number of days remaining until assignment or exam deadline | Yes |
| `pass_grade` | Numeric | Student's previous/pass grade | Yes |
| `assignment_difficulty` | Categorical / Encoded | Difficulty level of the assignment | Yes |
| `workload_level` | Categorical / Encoded | Student workload level | Yes |
| `risk_level` | Categorical / Encoded | Target risk label used for training and evaluation | Target |

---

## Course Field

The `course` field is a text field used for display and course management only.

It is not encoded and not used as a model input.

Students can add any course name, such as:

- Machine Learning
- IT Security
- Web Development
- Database Systems
- Custom course names

These names are stored for personalization, dashboard display, schedule, and prediction history, but they do not affect the machine learning feature vector.

---

## Final Model Input Features

The final model uses the following six input features:

```text
study_hours
attendance
deadline_days
pass_grade
assignment_difficulty
workload_level