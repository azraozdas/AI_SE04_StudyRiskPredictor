## Daily Logs

### 23.05.2026

**Müslüm Selim Akşahin – Data Collection & Preprocessing**

Completed:
- Created the simulated academic dataset.
- Added features such as study hours, attendance, deadline days, past grade, assignment difficulty, workload level, and risk level.
- Created and tested the preprocessing script.
- Checked missing values.
- Encoded categorical variables.
- Generated the cleaned dataset for machine learning.

Next Steps:
- Support the ML model development with the cleaned dataset.

**Dilay Tarhan – Testing & Documentation**

Completed:
- Created the `Documentation` folder in the repository.
- Added `problem_analysis.md`.
- Designed and improved the workflow diagram using Figma AI.
- Exported and uploaded `workflow_diagram.png`.
- Created `workflow_diagram.md` for GitHub documentation.
- Synced VS Code project with GitHub using Git.

Next Steps:
- Prepare System Design document.
- Prepare Testing Report.
- Prepare Progress Report.





**Eylül Özekinci – ML Model & Predictions**

Completed:
- Loaded the cleaned student dataset.
- Checked dataset structure and columns.
- Split the dataset into training and testing data.
- Trained a Random Forest classification model.
- Generated student risk level predictions.
- Evaluated the model with accuracy and classification report.
- Achieved 0.75 accuracy on the test set.
- Saved predictions to Outputs/predictions.csv.
- Saved trained model to Models/study_risk_model.pkl.

Note:
- The dataset currently has only 20 rows, so the model accuracy may change with more data.

Next Steps:
- Support Streamlit dashboard integration using the saved model file.
 (Update README and ML outputs)

Updated contributor identity

### 24.05.2026

**Azra Özdaş – Frontend**

Completed:
- Improved the dashboard UI design concept for the Streamlit frontend.
- Created a simpler and more realistic academic dashboard layout.
- Updated project terminology and corrected “past grade” to “pass grade”.
- Updated documentation and daily progress logs.
- Synced local project changes with GitHub.
- Resolved Git pull/push synchronization issues.
- Fixed contributor identity and Git configuration problems in the repository.

Next Steps:
- Start implementing the Streamlit dashboard interface.
- Connect the trained ML model to the frontend.
- Add prediction result cards and dataset preview sections.

### 24.05.2026

**Dilay Tarhan – Testing & Documentation**

Completed:
- Created `testing_report.md`.
- Updated project documentation structure in the repository.
- Synced local documentation changes with GitHub using Git.
- Reviewed repository documentation consistency.
- Planned the Gantt chart structure for project timeline documentation.
- Prepared Teams project progress updates.

Next Steps:
- Design and finalize the Gantt chart.
- Add Gantt chart documentation to the repository.
- Update daily logs.
- Prepare System Design document.

### 25.05.2026

**Dilay Tarhan – Testing & Documentation**

Completed:
- Designed and finalized the project Gantt chart using Figma.
- Added project milestones and 6-week timeline structure.
- Exported and uploaded `gantt_chart.png`.
- Created `gantt_chart.md` for GitHub documentation.
- Updated repository documentation files.
- Prepared final daily log updates.
- Synced documentation updates with GitHub.

Next Steps:
- Complete System Design document.
- Finalize Progress Report.
- Perform final documentation review.
- Prepare repository for final submission.

### 30.05.2026

**Dilay Tarhan – Bug Fixing & Repository Cleanup**

Completed:

- Recreated and configured the local project environment.
- Installed project dependencies and resolved Streamlit setup issues.
- Identified and fixed the prediction feature mismatch bug in the frontend.
- Tested and verified application functionality on localhost.
- Updated `requirements.txt` for stable project setup.
- Created and organized the `Reports` folder.
- Updated Progress Report, Evaluation Report, and Team Contributions files.
- Removed unnecessary `Outputs` folder from the repository.
- Cleaned repository structure and synced updates with GitHub.

Next Steps:
- Perform final system validation testing.
- Review repository documentation for final submission.
- Support final MVP testing and project review.

### 31.05.2026

**Dilay Tarhan – Testing & Documentation**

### 26.05.2026

**Dilay Tarhan – Testing & Documentation**

Completed:
- Updated `requirements.txt` with working dependency versions.
- Added `.gitignore` to exclude virtual environment, cache files, environment files, and generated files.
- Added MIT `LICENSE` file.
- Created `Reports/` folder.
- Added `final_audit_summary.md` placeholder for the final audit review.
- Updated `progress_report.md` after repository maintenance changes.
- Synced repository maintenance updates with GitHub.

Next Steps:
- Complete final audit summary.
- Perform final documentation consistency review.
- Support final system validation and submission preparation.


**Müslüm Selim Akşahin – Data Collection & Preprocessing**

Completed:
- Expanded `student_study_data.csv` from 20 to 210 rows with balanced class distribution (~70 rows per risk level: High / Medium / Low).
- Fixed column name inconsistency: `past_grade` corrected to `pass_grade` throughout the preprocessing script.
- Dropped `student_id` from cleaned output; raw dataset retains it for future backend use.
- Moved `drop_duplicates()` to run after `fillna()` for correct deduplication on complete rows.
- Replaced shared `LabelEncoder` instance with a per-column encoder dictionary; serialized to `Models/encoders.pkl` via joblib so downstream code no longer needs hardcoded category mappings.
- Made all file paths resolve relative to script location using `os.path`, eliminating working directory dependency.
- Added `.streamlit/config.toml` to suppress the usage-statistics prompt on first launch.
- Regenerated `Data/cleaned_student_data.csv` and `Models/encoders.pkl` from updated dataset.

Next Steps:
- Eylül retrain with the 210-row dataset and update evaluation metrics.

### — Azra Özdaş

- Investigated and fixed the prediction issue in the Streamlit application.
- Identified a feature mismatch between training and prediction data.
- Removed student_id from the prediction input payload.
- Resolved the prediction error and verified successful model predictions.
- Tested the updated application to ensure stable functionality.

Next Step:
- Continue frontend improvements and support final integration testing.



### — Eylül Özekinci

- Updated ml_model.py with portable file paths using os.path.
- Added automatic creation of Models and Outputs folders.
- Implemented 5-Fold Cross Validation for model evaluation.
- Added confusion matrix generation and feature importance analysis.
- Exported evaluation results to the Outputs folder.
- Retrained the model using the updated 210-row dataset and regenerated model outputs.

Next Step:
- Support API integration and connect model predictions to the Streamlit dashboard.