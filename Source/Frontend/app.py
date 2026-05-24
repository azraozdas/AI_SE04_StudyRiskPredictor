import os
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AI Study Risk Predictor",
    page_icon="📘",
    layout="wide"
)

RAW_DATA_PATH = "Data/student_study_data.csv"
CLEANED_DATA_PATH = "Data/cleaned_student_data.csv"
MODEL_PATH = "Models/study_risk_model.pkl"
PREDICTIONS_PATH = "Outputs/predictions.csv"

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #06111F 0%, #0B1730 45%, #102A33 100%);
    color: #E5E7EB;
}

.block-container {
    padding-top: 3.2rem;
    padding-bottom: 3rem;
    max-width: 1180px;
}

section[data-testid="stSidebar"] {
    background: #07111F;
    border-right: 1px solid rgba(148, 163, 184, 0.18);
}

section[data-testid="stSidebar"] * {
    color: #CBD5E1 !important;
}

section[data-testid="stSidebar"] input[type="radio"] {
    accent-color: #2DD4BF !important;
}

section[data-testid="stSidebar"] label[data-baseweb="radio"] {
    background: transparent !important;
}

section[data-testid="stSidebar"] label[data-baseweb="radio"] span {
    color: #E2E8F0 !important;
}

h1, h2, h3 {
    color: #F8FAFC;
    letter-spacing: -0.02em;
}

p, label, span, div {
    color: #CBD5E1;
}

.hero-box {
    background: linear-gradient(135deg, rgba(20, 184, 166, 0.18), rgba(56, 189, 248, 0.10));
    border: 1px solid rgba(94, 234, 212, 0.22);
    border-radius: 24px;
    padding: 34px;
    margin-bottom: 34px;
    box-shadow: 0 18px 42px rgba(0, 0, 0, 0.30);
}

.info-card,
.metric-card {
    background: rgba(15, 23, 42, 0.78);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 18px;
    padding: 22px;
    margin-top: 14px;
    margin-bottom: 22px;
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.22);
}

.metric-label {
    font-size: 14px;
    color: #94A3B8;
    font-weight: 600;
}

.metric-value {
    font-size: 30px;
    color: #F8FAFC;
    font-weight: 800;
    margin-top: 6px;
}

.tag {
    display: inline-block;
    background: rgba(45, 212, 191, 0.12);
    color: #5EEAD4;
    border: 1px solid rgba(45, 212, 191, 0.35);
    border-radius: 999px;
    padding: 6px 12px;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 14px;
}

.workflow-box {
    background: rgba(30, 41, 59, 0.75);
    border: 1px dashed rgba(148, 163, 184, 0.32);
    border-radius: 16px;
    padding: 18px;
    text-align: center;
    font-weight: 700;
    color: #E2E8F0;
}

.risk-high {
    background: rgba(239, 68, 68, 0.16);
    border: 1px solid rgba(248, 113, 113, 0.7);
    color: #FCA5A5;
    border-radius: 18px;
    padding: 24px;
    text-align: center;
    font-size: 26px;
    font-weight: 800;
}

.risk-medium {
    background: rgba(250, 204, 21, 0.14);
    border: 1px solid rgba(250, 204, 21, 0.65);
    color: #FDE68A;
    border-radius: 18px;
    padding: 24px;
    text-align: center;
    font-size: 26px;
    font-weight: 800;
}

.risk-low {
    background: rgba(34, 197, 94, 0.14);
    border: 1px solid rgba(74, 222, 128, 0.65);
    color: #86EFAC;
    border-radius: 18px;
    padding: 24px;
    text-align: center;
    font-size: 26px;
    font-weight: 800;
}

.stSelectbox label,
.stSlider label,
.stNumberInput label {
    color: #E2E8F0 !important;
    font-weight: 600;
}

div[data-baseweb="select"] > div {
    background-color: #111827 !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(148, 163, 184, 0.35) !important;
    border-radius: 12px !important;
}

div[data-baseweb="select"] span {
    color: #F8FAFC !important;
}

input {
    background-color: #111827 !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(148, 163, 184, 0.35) !important;
    border-radius: 12px !important;
}

.stButton > button {
    background: linear-gradient(135deg, #14B8A6, #38BDF8) !important;
    color: #04111F !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 900 !important;
    font-size: 16px !important;
    padding: 0.8rem 1rem !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #2DD4BF, #67E8F9) !important;
    color: #04111F !important;
}

.stButton > button p,
.stButton > button span,
.stButton > button div {
    color: #04111F !important;
    font-weight: 900 !important;
}

.stSlider [data-baseweb="slider"] > div > div > div {
    background: linear-gradient(90deg, #14B8A6, #38BDF8) !important;
}

.stSlider [role="slider"] {
    background-color: #2DD4BF !important;
    border: 2px solid #7DD3FC !important;
    box-shadow: 0 0 10px rgba(45, 212, 191, 0.45) !important;
}

.stSlider span {
    color: #E2E8F0 !important;
}

[data-testid="stDataFrame"] {
    background-color: #0F172A;
    border-radius: 14px;
}

:root {
    --primary-color: #2DD4BF !important;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


def encode_difficulty(value):
    return {"High": 0, "Low": 1, "Medium": 2}[value]


def encode_workload(value):
    return {"High": 0, "Low": 1, "Medium": 2}[value]


def decode_risk(value):
    return {0: "High Risk", 1: "Low Risk", 2: "Medium Risk"}.get(int(value), "Unknown Risk")


def get_recommendation(risk_label):
    if risk_label == "High Risk":
        return "Start studying immediately, prioritize this course, and divide the task into smaller parts."
    elif risk_label == "Medium Risk":
        return "Plan extra study time this week and review the most difficult topics first."
    elif risk_label == "Low Risk":
        return "Maintain your current study routine and keep monitoring upcoming deadlines."
    return "No recommendation available."


def fallback_prediction(study_hours, attendance, deadline_days, pass_grade, difficulty, workload):
    score = 0

    if study_hours < 3:
        score += 2
    elif study_hours < 5:
        score += 1

    if attendance < 60:
        score += 2
    elif attendance < 75:
        score += 1

    if deadline_days <= 2:
        score += 2
    elif deadline_days <= 5:
        score += 1

    if pass_grade < 60:
        score += 2
    elif pass_grade < 75:
        score += 1

    if difficulty == "High":
        score += 2
    elif difficulty == "Medium":
        score += 1

    if workload == "High":
        score += 2
    elif workload == "Medium":
        score += 1

    if score >= 7:
        return "High Risk"
    elif score >= 4:
        return "Medium Risk"
    return "Low Risk"


st.sidebar.title("📘 Study Risk AI")
st.sidebar.caption("Academic AI Prototype")

page = st.sidebar.radio(
    "Navigation",
    [
        "Project Overview",
        "Risk Prediction",
        "Dataset Preview",
        "Model Outputs",
        "Team Info"
    ]
)


if page == "Project Overview":
    st.markdown("""
    <div class="hero-box">
        <span class="tag">Academic AI MVP</span>
        <h1>AI Smart Study Risk & Performance Predictor</h1>
        <p>
            A clean Streamlit dashboard that helps students understand academic risk,
            workload pressure, and study priorities using AI-based prediction logic.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Project Type</div>
            <div class="metric-value">AI MVP</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Frontend</div>
            <div class="metric-value">Streamlit</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Prediction</div>
            <div class="metric-value">Risk Level</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h3>Project Purpose</h3>
        <p>
            This system analyzes study hours, attendance, assignment deadlines,
            workload level, assignment difficulty, and pass grades to estimate
            student academic risk and provide clear study recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h3>System Workflow</h3>
        <div class="workflow-box">
            Student Input → Dataset → Preprocessing → ML Model → Risk Prediction → Recommendation → Dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)


elif page == "Risk Prediction":
    st.title("Academic Risk Prediction")
    st.write("Enter student academic information to predict risk level.")

    model = load_model()
    raw_df = load_csv(RAW_DATA_PATH)

    if raw_df is not None and "course" in raw_df.columns:
        course_options = sorted(raw_df["course"].unique().tolist())
    else:
        course_options = [
            "Introduction to Programming",
            "Database Systems",
            "Machine Learning",
            "Software Engineering"
        ]

    st.markdown("""
    <div class="info-card">
        <h3>Student Input Form</h3>
        <p>Fill in the academic information below to estimate the student's risk level.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        student_id = st.number_input("Student ID", min_value=1, value=1)
        course = st.selectbox("Course", course_options)
        study_hours = st.slider("Weekly Study Hours", 0, 15, 4)
        attendance = st.slider("Attendance (%)", 0, 100, 75)

    with col2:
        deadline_days = st.slider("Days Until Deadline", 0, 30, 5)
        pass_grade = st.slider("Pass Grade", 0, 100, 70)
        assignment_difficulty = st.selectbox("Assignment Difficulty", ["Low", "Medium", "High"])
        workload_level = st.selectbox("Workload Level", ["Low", "Medium", "High"])

    predict_clicked = st.button("Predict Risk", use_container_width=True)

    if predict_clicked:
        difficulty_encoded = encode_difficulty(assignment_difficulty)
        workload_encoded = encode_workload(workload_level)

        if raw_df is not None:
            course_mapping = {
                name: index for index, name in enumerate(sorted(raw_df["course"].unique()))
            }
            course_encoded = course_mapping.get(course, 0)
        else:
            course_encoded = 0

        input_data = pd.DataFrame([{
            "student_id": student_id,
            "course": course_encoded,
            "study_hours": study_hours,
            "attendance": attendance,
            "deadline_days": deadline_days,
            "pass_grade": pass_grade,
            "assignment_difficulty": difficulty_encoded,
            "workload_level": workload_encoded
        }])

        if model is not None:
            prediction = model.predict(input_data)[0]
            risk_label = decode_risk(prediction)
            prediction_source = "Trained Random Forest model"
        else:
            risk_label = fallback_prediction(
                study_hours,
                attendance,
                deadline_days,
                pass_grade,
                assignment_difficulty,
                workload_level
            )
            prediction_source = "Temporary prototype logic"

        st.subheader("Prediction Result")

        if risk_label == "High Risk":
            st.markdown(f'<div class="risk-high">{risk_label}</div>', unsafe_allow_html=True)
        elif risk_label == "Medium Risk":
            st.markdown(f'<div class="risk-medium">{risk_label}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="risk-low">{risk_label}</div>', unsafe_allow_html=True)

        st.caption(f"Prediction source: {prediction_source}")

        st.markdown("""
        <div class="info-card">
            <h3>Study Recommendation</h3>
        </div>
        """, unsafe_allow_html=True)

        st.info(get_recommendation(risk_label))

        chart_data = pd.DataFrame({
            "Factor": ["Study Hours", "Attendance", "Deadline Days", "Pass Grade"],
            "Value": [study_hours, attendance, deadline_days, pass_grade]
        })

        st.subheader("Input Overview")
        st.bar_chart(chart_data.set_index("Factor"))


elif page == "Dataset Preview":
    st.title("Dataset Preview")

    raw_df = load_csv(RAW_DATA_PATH)
    cleaned_df = load_csv(CLEANED_DATA_PATH)

    if raw_df is not None:
        st.markdown("""
        <div class="info-card">
            <h3>Raw Dataset</h3>
            <p>This is the simulated academic dataset used for the prototype.</p>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(raw_df, use_container_width=True)

        col1, col2 = st.columns(2)
        col1.metric("Rows", raw_df.shape[0])
        col2.metric("Columns", raw_df.shape[1])

        if "risk_level" in raw_df.columns:
            st.subheader("Risk Level Distribution")
            st.bar_chart(raw_df["risk_level"].value_counts())
    else:
        st.warning("Raw dataset not found.")

    if cleaned_df is not None:
        st.markdown("""
        <div class="info-card">
            <h3>Cleaned Dataset</h3>
            <p>This dataset is generated after preprocessing and is ready for ML usage.</p>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(cleaned_df, use_container_width=True)
    else:
        st.warning("Cleaned dataset not found.")


elif page == "Model Outputs":
    st.title("Model Outputs")

    predictions_df = load_csv(PREDICTIONS_PATH)

    if predictions_df is not None:
        st.markdown("""
        <div class="info-card">
            <h3>Prediction Results</h3>
            <p>These results were generated by the machine learning model.</p>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(predictions_df, use_container_width=True)

        if "predicted_risk_level" in predictions_df.columns:
            st.subheader("Predicted Risk Distribution")
            decoded = predictions_df["predicted_risk_level"].apply(decode_risk)
            st.bar_chart(decoded.value_counts())
    else:
        st.warning("Predictions file not found. Please run the ML model first.")


elif page == "Team Info":
    st.title("Team and Responsibilities")

    st.markdown("""
    <div class="info-card">
        <h3>Project Team</h3>
        <p><b>Eylül Özekinci</b> – Machine Learning Model</p>
        <p><b>Azra Özdaş</b> – Frontend / Streamlit Dashboard</p>
        <p><b>Müslüm Selim Akşahin</b> – Data Collection & Preprocessing</p>
        <p><b>Dilay Tarhan</b> – Testing & Documentation</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h3>System Flow</h3>
        <div class="workflow-box">
            Student Input → Dataset → Preprocessing → ML Model → Risk Prediction → Recommendation → Dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)