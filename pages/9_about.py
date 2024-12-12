import streamlit as st
import os
import base64


# Load CSS file
def load_css():
    """Carga el archivo CSS en la aplicación de Streamlit."""
    css_path = os.path.join("styles", "styles.css")
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def add_logo_to_header():
    """Agrega el logo al encabezado utilizando la clase definida en CSS."""
    logo_path = os.path.join("static", "riskova_logo.png")
    logo_base64 = get_base64_image(logo_path)
    st.markdown(
        f"""
        <style>
        [data-testid="stHeader"]::before {{
            background-image: url('data:image/png;base64,{logo_base64}');
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def get_base64_image(image_path):
    """Convierte una imagen local en un string Base64."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# load css file and add logo
load_css()
add_logo_to_header()


# Application title
st.title("About")

# Project description
with st.container(border=True, height=200):
    st.subheader("Project Description")
    st.write ("""
    The Predictive Fraud Detector (PFD) project aims to create a platform to assist in detecting 
    fraud in electronic payments, utilizing machine learning techniques and data analysis. 
    The dataset used for this project was sourced from Kaggle. https://www.kaggle.com/datasets/kartik2112/fraud-detection
    """)

# Objectives section
with st.container(border=True, height=150):
    st.subheader("General Objective")
    st.write ("""
    Develop a predictive model to detect fraudulent transactions on an electronic payment platform using
    machine learning techniques and behavioral analysis.
    """)

# Specific objetives section
with st.container(border=True, height=500):
    st.subheader("Specific Objetives")
    st.markdown ("""
    **1. Exploratory Data Analysis:** Perform interactive data analysis to uncover insights such as  
     distributions, correlations and outliers.
    \n\n **2. Data Prepocessing:** Prepare the data by cleaning, normalizing, encoding and scaling,
    ensurig readniness for model training.
    \n\n **3. Model Training:** Develop and train predictive models to detect fraudulent transactions,
    leveraging machine learning techniques.
    \n\n **4. Real-Time Fraud Detectio:** Simulate real-time fraud detection with transactional data,
    showcasing system performance.
    \n\n **5. User Interface:** Provide an interactive web-based interface using Streamlit for seamless
     user interaction and data visualization.
    \n\n **6. Report Generation:** Generate downloadable reports with visualizations and key metrics for
    comprehensive analysis summaries.
    """)


# Project Development section
with st.container(border=True, height=850):
    st.markdown(
        """
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        th {
            background-color: #f4f4f4;
            text-align: left;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
    </style>
    <h2>Project Development</h2>
    <h3>Development Phases</h3>
    <table>
        <thead>
            <tr>
                <th>Item</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Home</td>
                <td>Introduction to the credit card fraud problem, its significance, and the areas involved. Navigation to key system sections.</td>
            </tr>
            <tr>
                <td>Data Ingestion & Exploration</td>
                <td>Upload datasets in CSV format or connect to databases. Interactive data exploration: distributions, correlations, and outliers.</td>
            </tr>
            <tr>
                <td>Data Preprocessing</td>
                <td>Data cleaning and transformation: handling missing values, duplicates, and scaling. User-customizable transformations.</td>
            </tr>
            <tr>
                <td>BI Dashboard</td>
                <td>Interactive dashboard for key KPIs like fraud percentage, trends, and geographic analysis. Dynamic charts and visualizations.</td>
            </tr>
            <tr>
                <td>Predictive Modeling</td>
                <td>Model training for fraud prediction. Evaluation metrics such as precision, recall, and F1-score. User testing of hyperparameters.</td>
            </tr>
            <tr>
                <td>Advanced Analysis</td>
                <td>Model interpretation using SHAP. Fraudulent behavior segmentation with clustering techniques.</td>
            </tr>
            <tr>
                <td>Real-Time Detection</td>
                <td>Real-time prediction simulation with uploaded or queried data. Visualization of predictions and associated explanations.</td>
            </tr>
            <tr>
                <td>Reporting & Export</td>
                <td>Generate downloadable reports in PDF or Excel format with key metrics and charts. Includes an executive summary of the analysis.</td>
            </tr>
            <tr>
                <td>Documentation</td>
                <td>Technical details of the project, tools used, and team roles. System usage guide.</td>
            </tr>
        </tbody>
    </table>
    """,
    unsafe_allow_html=True
)


# Authors
with st.container(border=True, height=250):
    st.subheader("About the Authors")
    st.markdown(
        """
    - **Jose Ibarra** - Business Analyst
        :link: [LinkedIn](https://www.linkedin.com/in/jose-ignacio-ibarra-696b03a6)

    - **Gabriela Lopez** - Data Analytics
        :link: [LinkedIn](http://www.linkedin.com/in/-gabriela-lopez")

    - **Silvana Jaramillo** - Machine Learning Engineer
       :link: [LinkedIn]("https://linkedin.com/in/silvana-jaramillo")
    """)