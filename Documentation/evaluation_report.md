# Evaluation Report

## Project

Studor / AI Smart Study Risk & Performance Predictor

---

## Evaluation Purpose

This report summarizes the current machine learning model evaluation results and explains the updated prediction logic used in the final MVP.

The model is designed to predict student academic risk based on academic behavior features rather than the course name itself.

---

## Updated Model Logic

The course name is no longer used as an ML feature. It is kept only for display, course management, dashboard, schedule, and history.

The Random Forest predicts risk using academic behavior features:

- attendance
- study_hours
- deadline_days
- pass_grade
- assignment_difficulty
- workload_level

This means students can add any course name, including custom course names such as `IT Security`, and the prediction still uses the same trained Random Forest model.

There is no custom course fallback model. All predictions are handled by the Random Forest using the six academic behavior features.

---

## Model Input Features

The final model uses 6 input features:

| Feature | Description |
|---|---|
| `study_hours` | Number of weekly study hours |
| `attendance` | Student attendance percentage |
| `deadline_days` | Number of days remaining until deadline |
| `pass_grade` | Student's previous/pass grade |
| `assignment_difficulty` | Encoded assignment difficulty level |
| `workload_level` | Encoded workload level |

The `course` field is not used as a model input.

---

## Model Performance

| Metric | Value |
|---|---|
| Validation Accuracy | 91.11% |
| Test Accuracy | 93.33% |

The updated performance values reflect the final model setup using six academic behavior features.

---

## Feature Importance

The course feature was removed from the model input and should not appear in the feature importance table.

The model evaluates risk based on the following features only:

| Feature |
|---|
| attendance |
| study_hours |
| deadline_days |
| pass_grade |
| assignment_difficulty |
| workload_level |

Feature importance outputs should be interpreted only for these six academic behavior features.

---

## Evaluation Notes

- The model no longer depends on predefined course IDs.
- Custom course names are supported because course names are stored for personalization and display only.
- The same Random Forest prediction workflow is used for all courses.
- The prediction result includes risk level and confidence output.
- Course information remains useful for dashboard, schedule, history, and course management features.

---

## Conclusion

The final model setup is more flexible and realistic because it allows students to create any course name while keeping the ML prediction based on measurable academic behavior.

The system now separates personalization data from machine learning input data:
- `course` is used for display and user experience.
- Six academic behavior features are used for prediction.