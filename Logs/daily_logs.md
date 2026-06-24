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

### 01.06.2026

**Azra Özdaş – Frontend Stabilization & README Update**

Completed:

* Fixed the urgent prediction input issue in `Source/Frontend/app.py`.
* Removed `student_id` from the model input data to prevent feature mismatch errors.
* Renamed `past_grade` to `pass_grade` to match the model’s expected feature name.
* Ran the Streamlit application and tested the **Predict Risk** workflow.
* Verified that the prediction process works with the trained model loaded.
* Captured screenshots of all 5 application pages.
* Saved screenshots under `Documentation/Screenshots/`.
* Added the screenshots to the README documentation.
* Updated README model metrics with real evaluation results.
* Corrected the output folder reference from `Results/` to `Outputs/`.
* Removed the broken `workflow_diagram.png` image link from README.

Next Steps:

* Perform final repository review.
* Confirm all documentation and screenshots are committed.

**Azra Özdaş – Frontend / Auth UI / Repository Cleanup**

Completed:

- Fixed the urgent prediction input issue in `Source/Frontend/app.py` by removing `student_id` from the model input payload and aligning the feature name with the model's expected `pass_grade`.
- Verified the **Predict Risk** workflow end-to-end with the trained Random Forest model loaded.
- Updated `README.md` with real evaluation metrics, corrected the `Results/` reference to `Outputs/`, and removed the broken `workflow_diagram.png` image link.
- Added the authentication UI as the new app entry point:
  - `Source/Frontend/login.py` — Sign In / Create Account flow with JSON-backed user storage and validation.
  - `Source/Frontend/styles.py` — shared dark login theme.
  - `Source/Frontend/utils.py` — `render_html` helper.
  - `Source/Frontend/assets/logo.png` — application logo (lowercase filename to match the loader path).
- Refactored `Source/Frontend/app.py` to require login before rendering the dashboard and to expose a Sign Out button in the sidebar.
- Cleaned up `.gitignore` by removing the `Models/*.pkl` and `Outputs/*.csv` rules so that the trained model and ML artifacts ship with the repository (clean-clone reproducibility for v1.0).
- Committed `Outputs/confusion_matrix.csv` and `Outputs/feature_importance.csv` as v1.0 evaluation artifacts.

Next Steps:

- Capture five real screenshots of the running app (login, project overview, risk prediction, dataset preview, model outputs) and save them under `Documentation/Screenshots/`.
- Replace the screenshot placeholder in `README.md` with the captured images.
- Participate in tonight's clean-machine rehearsal and tag `v1.0`.
- Plan the migration from the sidebar-radio layout to Streamlit's native `pages/` structure for the 2 June scaffold work.

### 01.06.2026

**Dilay Tarhan – Testing & Documentation**

Completed:
- Reviewed repository documentation consistency.
- Corrected `progress_report.md` prediction bug description.
- Updated documentation to reflect frontend correction using `pass_grade` to match the trained model.
- Synced documentation updates with repository progress tracking.
- Prepared Teams project status update.

Next Steps:
- Continue final documentation review.
- Support final repository consistency checks.
- Assist final submission preparation.

### 02.06.2026

**Eylül Özekinci – ML Honest Evaluation**

Completed:

- Fixed CV leakage in `Source/ml_model.py`: `cross_val_score` now uses `X_train, y_train` instead of full `X, y`.
- Added matplotlib/seaborn plots saved before `joblib.dump`: `Outputs/confusion_matrix.png` and `Outputs/feature_importance.png`.
- Re-ran pipeline on 210-row dataset — 5-Fold CV mean **1.0000** (std 0.0), test accuracy **0.9762**.
- Rewrote `Documentation/evaluation_report.md`: dataset summary, train/test split, CV table, embedded PNGs, bug-fix note ("frontend was corrected to use `pass_grade`"), and Limitations (leakage, dataset size, no noise).
- Committed under `ml: honest evaluation — fix CV split, add chart PNGs, document leakage`.

Next Steps:

- Investigate why CV reports 1.0 — likely small N + highly separable features; try a held-out validation slice.
- Surface the new PNGs in the Streamlit dashboard.

**Azra Özdaş – Frontend Development & Documentation**

**Completed:**

* Refactored frontend file paths using portable path handling.
* Added encoder (`encoders.pkl`) integration with fallback support.
* Replaced hardcoded encoding/decoding logic with encoder-based functions.
* Updated Risk Prediction and Model Outputs pages to use saved encoders.
* Improved frontend-model consistency and portability.
* Reworked README structure and setup instructions.
* Added demo account information and updated repository structure.
* Updated model performance metrics and documentation references.
* Added screenshots section placeholders to README.

**Next Steps:**

* Capture application screenshots.
* Add screenshots to `Documentation/Screenshots/`.
* Perform final UI review and testing.


### 04.06.2026 

**Müslüm Selim Akşahin – Backend & Data**

Completed:
- Expanded dataset from 210 to 300 rows (100 per class) via `Source/data_generation.py`; regenerated `Data/student_study_data.csv` and `Data/cleaned_student_data.csv`.
- Re-ran `Source/preprocessing.py` to rebuild `Models/encoders.pkl` from the new 300-row data.
- Re-ran `Source/ml_model.py` — retrained RandomForest; test accuracy 1.00, 5-Fold CV mean 1.00; updated `Outputs/` artifacts.
- Added course CRUD to `Source/Backend/db.py`: `create_course`, `get_user_courses`, `update_course`, `delete_course` — all scoped to the owning user.
- Created `Source/Backend/pdf_utils.py`: `extract_text`, `extract_metadata`, `save_upload` using `pypdf`; added `pypdf` to `requirements.txt`.
- Updated `Data/data_dictionary.md` to v1.5: corrected row count to 300, added Encoder Mapping section, expanded Limitations.
- Created `Documentation/performance_check.md`: model metrics, feature importances, DB latency measurements, key optimisations, known limitations.
- Fixed encoder integration gap: `Source/Frontend/pages_/risk_prediction.py` now loads `encoders.pkl` via `joblib` and calls `encoders[col].transform()` instead of hardcoded integer maps; prediction results saved to `predictions` table.
- Implemented `Source/Frontend/pages_/courses.py` with full create / read / edit / delete UI backed by Supabase.
- Fixed Supabase connectivity for IPv4-only networks: switched `DATABASE_URL` to Supabase Supavisor pooler (`aws-0-eu-west-1.pooler.supabase.com:6543`).

Next Steps:
- Implement remaining stub pages: `model_results.py`, `profile.py`, `recommendations.py`, `study_schedule.py`.
- Capture screenshots for README.
- Final documentation review before submission.

### 04.06.2026

**Azra Özdaş – Frontend / Auth UI & App Router**

Completed:
- Redesigned the Create Account page so the full registration form fits on a 1920×1080 screen at 100% browser zoom without scrolling.
- Kept a single-column unified card layout; compacted logo, spacing, input/selectbox heights (34px), tabs (30px), and button height (38px).
- Moved the Security Question hint into the selectbox label in `login.py`, removing extra vertical space.
- Added Sign-In-only relaxed styles (`SIGNIN_RELAX_STYLES`) via `inject_login_styles(mode)` so Sign In stays balanced while Create Account stays compact; fixed the related `TypeError` on app launch.
- Renamed the application to **Studor** across login branding, page title, sidebar, and dashboard hero.
- Redesigned auth tabs (Sign In / Create Account) to match the dark premium theme — inactive dark navy, active blue gradient, unified segmented control.
- Fixed input field styling: dark gradient backgrounds, readable labels/placeholders, focus glow; re-scoped CSS for Streamlit 1.57 (`stColumn` selector change).
- Restored contextual field icons (mail, lock, shield, key) using `::before` pseudo-elements with `mask-image`.
- Fixed "Remember me for 30 days" checkbox alignment with flexbox vertical centering in `styles.py`.
- Refactored `app.py` to a router-based structure with `pages_/` dispatch, disk session persistence (`save_auth_session` / `restore_auth_session`), and defensive `inject_app_styles` import.
- Verified app boots at `localhost:8501`, `plotly` and `pages_/dashboard.py` import cleanly, and dashboard is reachable after login.

Next Steps:
- Implement `inject_app_styles()` for sidebar and dashboard dark theme.
- Build out remaining `pages_/` modules (courses, profile, risk prediction, etc.).
- Final UI review and testing.

**Eylül Özekinci – ML Inference API & Honest Metrics**

Completed:
- Added `Source/model_utils.py` with `load_model()` (loads `study_risk_model.pkl` + `encoders.pkl`) and `predict_for_user()` (encodes human-readable inputs, returns risk level, confidence, and per-class probabilities).
- Reworked `Source/data_generation.py` to remove deterministic leakage: 300 rows, overlapping feature ranges per class, probabilistic difficulty/workload, and ~12% label noise.
- Updated `Source/ml_model.py` to a 70/15/15 train/validation/test split (stratified) and added a held-out validation accuracy check alongside 5-Fold CV.
- Regenerated dataset, encoders, model, and Outputs; new metrics: CV mean 86.67% (±0.05), validation 88.89%, test 91.11%, macro F1 0.91.
- Rewrote `Documentation/evaluation_report.md` with the new split, metrics, confusion matrix, feature importance, and a 30-second Q&A answer for the earlier 100% CV.
- Updated the README Model Performance table to the realistic metrics.

Next Steps:
- Surface model outputs (confusion matrix / feature importance PNGs) in the Model Results page.

### 05.06.2026

**Azra Özdaş – Frontend Buildout & Presentation Polish**
Completed:
- Refactored `app.py` into a query-param router (`?nav=`, `?logout=`) with a custom HTML sidebar (icon nav, brand block, profile shortcut, logout) and a login gate that dispatches to the `pages_/` modules.
- Built/polished the dark-theme login UI in `login.py`: Sign In / Create Account tabs, security-question selector, "Remember me for 30 days", a 3-step forgot-password flow, inline error/success banners, and Material field icons.
- Implemented `styles.py` `inject_app_styles()` for the sidebar and dashboard dark theme, plus the compact/relaxed login styles (`inject_login_styles(mode)`).
- Built out the `pages_/` modules:
  - **Dashboard** — KPI cards, risk distribution, deadlines from training CSV.
  - **Course Analytics** — aggregated per-course stats with search and risk filter.
  - **Risk Prediction** — model form, confidence, recommendations, Plotly input chart.
  - **Study Schedule** — weekly plan from dataset risk levels and deadlines.
  - **Recommendations** — tips linked to latest prediction plus general study tips.
  - **Model Results** — confusion matrix, feature importance, predictions table.
  - **Profile** — account settings and project team section.
- Added `course_colors.py` for consistent per-course color coding across schedule and recommendations.
- Made all frontend paths portable via `os.path` and added defensive imports/fallbacks (missing model files, empty dataset).
- Renamed the app to **Studor** across login branding, page title, sidebar, and dashboard.
- Verified the app boots and the full login → navigation → prediction flow works on `localhost`; captured page screenshots under `Documentation/Screenshots/`.
- Clarified page subtitles so Dashboard and Course Analytics clearly use the shared training CSV (not user-specific data).
- Removed stale “My Courses” reference from Course Analytics.
- Updated Study Schedule and Recommendations wording to rule-based/heuristic (not a separate ML model).
- Updated Profile stat label to “Predictions (session)” and Model Results subtitle to reference `Outputs/metrics.json` and `Documentation/evaluation_report.md`.
Next Steps:
- Final demo rehearsal before progress presentation.
- Confirm all screenshots match the live app.


**Müslüm Selim Akşahin – Data Dictionary & Backend Cleanup**
Completed:
•⁠  ⁠Updated ⁠ Data/data_dictionary.md ⁠ (v1.6): overlapping class profiles, ~12% label noise, preprocessing steps, and corrected limitations.
•⁠  ⁠Supported dataset regeneration via ⁠ Source/data_generation.py ⁠ and ⁠ Source/preprocessing.py ⁠.
•⁠  ⁠Cleaned ⁠ Source/Backend/db.py ⁠: removed duplicate course CRUD functions; marked remaining course helpers as reserved for future UI.
•⁠  ⁠Marked ⁠ Source/Backend/pdf_utils.py ⁠ as deferred (no upload UI in current MVP).
•⁠  ⁠Verified ⁠ Data/student_study_data.csv ⁠ and ⁠ Data/cleaned_student_data.csv ⁠ remain aligned with preprocessing and model training.
Next Steps:
•⁠  ⁠Support final data-related questions during presentation.
•⁠  ⁠Document future scope for per-user courses and PDF upload if asked in Q&A.

**Eylül Özekinci – ML Pipeline Alignment & Evaluation**
Completed:
- Finalized `Source/ml_model.py` with **70/15/15 stratified split** (210 train / 45 validation / 45 test) and 5-fold CV on the training set only.
- Regenerated dataset, encoders, model, and all `Outputs/` artifacts after label-noise data generation.
- Added `Outputs/metrics.json` as the single authoritative metrics file for the project.
- Confirmed final metrics: CV mean **86.67%** (±0.0513), validation **88.89%**, test **91.11%**, macro F1 **0.91**.
- Updated `Documentation/evaluation_report.md` so confusion matrix, feature importance, and split methodology match committed artifacts.
- Rewrote `Documentation/performance_check.md` to remove outdated 100% accuracy and 80/20 split claims.
- Verified `Source/model_utils.py` inference remains aligned with `Models/encoders.pkl` and the retrained model.
Next Steps:
- Support demo Q&A on simulated data limitations and evaluation methodology.
- Assist with final model-results walkthrough during presentation.

**Dilay Tarhan – Documentation, Testing & Submission Readiness**
Completed:
- Updated `README.md`: Studor branding, daily logs link, dashboard feature table, and model performance table aligned with `Outputs/metrics.json`.
- Expanded `Documentation/system_design.md` with dataset, preprocessing, ML, inference, Streamlit, auth, and recommendation layers.
- Updated `Documentation/problem_analysis.md`, `progress_report.md`, and `team_contributions.md` for final MVP scope.
- Refreshed `Documentation/testing_report.md` with current page names and auth/ML pipeline tests.
- Updated `Documentation/demo_script.md` and `Documentation/deployment_plan.md`; removed references to removed or deferred features.
- Added `Documentation/gantt_chart.md` with six-week milestone timeline.
- Completed `Reports/final_audit_summary.md` (replaced placeholder).
- Reviewed documentation consistency across README, logs, evaluation report, and frontend page names.
- Prepared Teams progress summary for submission/presentation readiness.
Next Steps:
- Final documentation consistency check before presentation.
- Support team during demo rehearsal and instructor Q&A.
---

### 06.06.2026

**Azra Özdaş – Frontend Resilience: DB Timeout & One-Time Init**
Completed:
- Diagnosed app freeze / very slow page loads as a blocking database connection: `Source/Frontend/app.py` ran `init_db()` and a Remember-Me lookup on every load/navigation, with no connection timeout, so an unreachable Supabase host blocked for tens of seconds per attempt.
- Added a 5-second `connect_timeout` to `psycopg2.connect()` in `Source/Backend/db.py` so the app fails fast and reaches the login screen instead of hanging.
- Guarded `ensure_database()` in `Source/Frontend/bootstrap.py` with a module-level `_DB_INIT_DONE` flag so `init_db()` runs only once per Streamlit server process instead of on every page reload/navigation.
- Guarded the Remember-Me cookie lookup with a `_REMEMBER_ME_DB_LOOKUP_DONE` flag so `get_session_user()` is queried at most once per process when a cookie exists.
- Kept all existing login, session, logout, and saved-prediction behavior unchanged; no Supabase credentials, schema, `.env`, or database settings were modified.

Next Steps:
- Optional: surface a non-blocking warning banner in the UI when the database is unreachable.
- Confirm normal startup timing once the Supabase project is back online.

### 24.06.2026

**Azra Özdaş – Frontend Personalization & Auth UI**

Completed:
- Extended session defaults in `Source/Frontend/bootstrap.py` and `utils.py` for `profile_university`, `profile_target_gpa`, `user_courses`, and `prefill_course`.
- Updated sign-up form in `Source/Frontend/login.py`: two-column layout (Account Information | Academic Profile), optional Target GPA, security question/answer side by side; unified auth shell so Sign In and Create Account share the same card width, header spacing, and tab button styling.
- Updated `Source/Frontend/pages_/profile.py` to display and edit university and target GPA.
- Reworked `Source/Frontend/pages_/dashboard.py`: welcome empty state for new users; personalized KPIs, course list, deadlines, and last prediction when `user_courses` exists; training CSV stats moved to collapsible “Benchmark / Training Dataset Insights”.
- Added `Source/Frontend/pages_/my_courses.py`: add/delete courses in `st.session_state`, duplicate-name check, “Predict Risk” navigates with `prefill_course` (TODO: Supabase persistence — Selim).
- Wired `my_courses` into `Source/Frontend/app.py` navigation and routing.
- Updated `Source/Frontend/pages_/risk_prediction.py` to prefer user courses in the dropdown and pre-fill sliders from course cards.

Next Steps:
- Selim: extend Supabase `users` / `courses` tables and replace session-only course/profile storage.
- Restore or update `DATABASE_URL` in `.env` (current pooler user returns `tenant/user not found`).
- PDF upload feature remains deferred to a future phase.