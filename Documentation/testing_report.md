# Testing Report

## Project

Studor / AI Smart Study Risk & Performance Predictor

---

## Purpose

This document summarizes the manual functional testing performed for the final MVP version of Studor.

The testing report has been updated to reflect the current application structure, including authentication, custom course management, Random Forest prediction, study schedule updates, recommendations, and profile prediction history.

---

## Test Environment

- Application: Studor / AI Smart Study Risk & Performance Predictor
- Testing Type: Manual Functional Testing
- Environment: Local development environment
- Tools Used: Browser, VS Code, GitHub
- Tester: Dilay Tarhan

---

## Updated Model Testing Logic

The course name is not used as a model input.

Both normal course names and custom course names use the same Random Forest prediction workflow.

The model predicts risk using six academic behavior features:

```text
study_hours
attendance
deadline_days
pass_grade
assignment_difficulty
workload_level
```

No custom course fallback warning should appear.

---

## Tested Functional Areas

- Register / Login
- Logout
- My Courses page
- Custom course creation
- Normal course creation
- Risk prediction workflow
- Random Forest prediction output
- Confidence display
- Recommendation update after prediction
- Study schedule update after prediction
- Profile prediction history
- Data persistence after logout/login
- Dashboard and navigation consistency

---

## Manual Test Cases

| Test ID | Feature | Test Action | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| T1 | Application Launch | Start the app locally | Application opens without runtime errors | To be verified | Pending |
| T2 | Register | Create a new user account | Account is created successfully | To be verified | Pending |
| T3 | Login | Log in with valid credentials | User reaches the dashboard | To be verified | Pending |
| T4 | Invalid Login | Log in with incorrect credentials | Error message is displayed | To be verified | Pending |
| T5 | My Courses | Open My Courses page | Course management page loads correctly | To be verified | Pending |
| T6 | Add Custom Course | Add course name `IT Security` | Custom course is saved and displayed | To be verified | Pending |
| T7 | Add Normal Course | Add course name `Machine Learning` | Course is saved and displayed | To be verified | Pending |
| T8 | Risk Prediction – Custom Course | Run prediction for `IT Security` | Random Forest prediction is generated | To be verified | Pending |
| T9 | Risk Prediction – Normal Course | Run prediction for `Machine Learning` | Random Forest prediction is generated | To be verified | Pending |
| T10 | Prediction Confidence | Submit prediction form | Risk level and confidence are shown | To be verified | Pending |
| T11 | No Fallback Warning | Use a custom course name | No fallback warning appears | To be verified | Pending |
| T12 | Study Schedule | Run prediction after selecting course | Study schedule updates after prediction | To be verified | Pending |
| T13 | Recommendations | Run prediction | Recommendation updates after prediction | To be verified | Pending |
| T14 | Profile History | Open profile after prediction | Prediction history is displayed | To be verified | Pending |
| T15 | Persistence | Logout and log in again | Saved courses and prediction history remain available | To be verified | Pending |
| T16 | Logout | Click logout | User session ends correctly | To be verified | Pending |

---

## Removed / Outdated Test Items

The following older test assumptions are no longer valid and should not be used:

- Prediction history missing
- Per-user course UI missing
- Custom course fallback warning
- Course encoded as model input
- Course encoded 0–19
- Team Info page as a current navigation test

These items were related to earlier MVP versions and do not reflect the final implemented logic.

---

## Issues / Risks

- Final manual validation should still be completed before submission.
- Test statuses should be updated from `Pending` to `Passed` or `Failed` after the final test run.
- Automated test coverage is still limited.
- Documentation must remain aligned with the current UI and final ML logic.

---

## Conclusion

The testing report has been refreshed to match the final system behavior.

The final MVP supports free-text course names. Course names are stored for personalization and display, while the Random Forest model predicts risk using six academic behavior features.

Final validation should confirm that authentication, custom courses, predictions, recommendations, schedule updates, profile history, and persistence all work correctly.

