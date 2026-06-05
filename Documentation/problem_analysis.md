# Problem Analysis

## Problem

Students have difficulty identifying which courses, assignments, or deadlines pose the highest academic risk. Without early warning, they may misallocate study time and miss important deadlines.

## Target Users

University or high school students who want to manage study workload and reduce the risk of underperformance.

## Why This Problem Matters

Students often study without knowing which task needs the most attention. An AI-assisted system can surface academic risk earlier and support better planning.

## Proposed Solution

**Studor** analyzes study hours, attendance, deadlines, pass grades, assignment difficulty, and workload level. It predicts whether a student is at **Low**, **Medium**, or **High** academic risk and provides study recommendations through a Streamlit dashboard.

## Inputs

- Study hours (weekly)
- Attendance (%)
- Days until assignment deadline
- Pass grade (current course grade)
- Assignment difficulty (Low / Medium / High)
- Workload level (Low / Medium / High)
- Course name (categorical)

## Outputs

- Risk level prediction (Low / Medium / High)
- Confidence score and class probabilities
- Study recommendations (rule-based tips by risk band)
- Weekly study schedule (heuristic plan from dataset patterns)
- Model evaluation charts (confusion matrix, feature importance)

## Data Note

The current prototype uses a **simulated dataset** (300 rows) for training and demo analytics. Real student data would be required for production deployment.
