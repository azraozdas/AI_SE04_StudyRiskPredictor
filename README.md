# AI Smart Study Risk & Performance Predictor

## Project Overview

AI Smart Study Risk & Performance Predictor is a prototype system designed to help students identify potential academic risks before they become serious problems. The system analyzes factors such as study hours, attendance, deadlines, grades, assignment difficulty, and workload level to predict whether a student has a Low, Medium, or High academic risk level.

The project combines data preprocessing, machine learning, and an interactive Streamlit dashboard to provide risk predictions and study recommendations.

---

## Team Members

| Team Member          | Role                            |
| -------------------- | ------------------------------- |
| Eylül Özekinci       | Machine Learning Model          |
| Azra Özdaş           | Frontend / Streamlit Dashboard  |
| Müslüm Selim Akşahin | Data Collection & Preprocessing |
| Dilay Tarhan         | Testing & Documentation         |

---

## System Workflow

![Workflow Diagram](Documentation/workflow_diagram.png)

Student Input → Dataset → Preprocessing → Machine Learning Model → Risk Prediction → Study Recommendation → Dashboard

---

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit
* Joblib
* PostgreSQL (Supabase — hosted, shared database)
* GitHub
* Microsoft Teams

---

## Repository Structure

```text
Data/
├── student_study_data.csv
├── cleaned_student_data.csv
└── data_dictionary.md

Source/
├── preprocessing.py
├── ml_model.py
├── data_generation.py
├── Backend/
│   └── db.py
└── Frontend/
    ├── app.py
    ├── login.py
    ├── styles.py
    ├── utils.py
    └── assets/
        └── logo.png

Models/
├── study_risk_model.pkl
└── encoders.pkl

Outputs/
├── predictions.csv
├── confusion_matrix.csv
├── confusion_matrix.png
├── feature_importance.csv
└── feature_importance.png

Documentation/
├── workflow_diagram.png
├── system_design.md
├── problem_analysis.md
├── progress_report.md
├── testing_report.md
├── evaluation_report.md
├── team_contributions.md
└── Screenshots/

Logs/
└── daily_logs.md

Reports/
└── final_audit_summary.md
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd AI_SE04_StudyRiskPredictor
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## First-Run Setup

The trained model (`Models/study_risk_model.pkl`), the encoders (`Models/encoders.pkl`), and the ML output files in `Outputs/` are **already included** in this repository so the app runs out of the box.

The `.env` file is also included and pre-configured with the shared Supabase database — no additional database setup is required.

You only need to re-run the steps below if you change the dataset and want to retrain.

### Step 1 — Data Preprocessing

```bash
python Source/preprocessing.py
```

### Step 2 — Train the Machine Learning Model

```bash
python Source/ml_model.py
```

### Step 3 — Launch the Dashboard

```bash
streamlit run Source/Frontend/app.py
```

Register a new account on the login screen. All users share the same hosted Supabase database.

---

## Dashboard Features

* Login and registration (Supabase PostgreSQL)
* Academic risk prediction
* Study recommendations
* Dataset preview
* Model output visualization
* Team information page
* Interactive user interface

---

## Model Performance

**Random Forest Classifier — 210-row simulated dataset**

| Metric | Value |
| --- | --- |
| Test Accuracy | 97.62% |
| 5-Fold CV Mean Accuracy | 100.00% |
| 5-Fold CV Std Deviation | 0.0000 |
| Macro Avg F1 Score | 0.98 |

> Note: The dataset is simulated using the rules described in `Data/data_dictionary.md`, so accuracy is unrealistically high.
> Cross-validation runs only on the training set to avoid leakage.
> See `Documentation/evaluation_report.md` for the full discussion of limitations.

---

## Screenshots

<!-- Replace with real captures saved under Documentation/Screenshots/ -->

![Login](Documentation/Screenshots/01_login.png)
![Project Overview](Documentation/Screenshots/02_overview.png)
![Risk Prediction](Documentation/Screenshots/03_risk_prediction.png)
![Dataset Preview](Documentation/Screenshots/04_dataset_preview.png)
![Model Outputs](Documentation/Screenshots/05_model_outputs.png)

---

## Future Improvements

* Larger and real-world academic datasets
* More advanced machine learning models
* Personalized AI recommendations (OpenAI / Gemini API)
* PDF and document analysis
* Real-time notifications and reminders
* Cloud deployment support

---

## License

This project is released under the MIT License. See the `LICENSE` file for details.