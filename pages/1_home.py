import streamlit as st
import pandas as pd
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

# Description
st.title("Welcome to Riskova!")
st.write("The transaction tracking system that helps you identifying fraudulent activity through data science and machine learning techniques. This model has been built using Kaggle's [Credit Card Transactions Fraud Detection Dataset](https://www.kaggle.com/datasets/kartik2112/fraud-detection?select=fraudTest.csv), that we will use to explain and visualize our approach to detecting fraudulent activity and the benefits it can bring to any organization in the electronic payment space.")

# Path for the temporary file
TEMP_FILE_PATH = "data/dataset.csv"

st.subheader("How to Start")
st.write("1) Upload a CSV file of your company's transaction records to start the analysis.")

# Load Data
uploaded_file = st.file_uploader("Select a CSV file.", type=["csv"])

if uploaded_file is not None:
    # Delete temp file
    if os.path.exists(TEMP_FILE_PATH):
        os.remove(TEMP_FILE_PATH)

    # Clear previous data in session_state
    if "data" in st.session_state:
        del st.session_state["data"]

    # Read and save the new file
    data = pd.read_csv(uploaded_file)
    # Save temporary file
    data.to_csv(TEMP_FILE_PATH, index=False)
    st.session_state["data"] = data  # Guardar en session_state
    st.success("File uploaded successfully. \
               Go to the Data Exploration pages from the sidebar.")
else:
    if "data" not in st.session_state:
        try:
            # Try to load from temporary file
            data = pd.read_csv(TEMP_FILE_PATH)
            st.session_state["data"] = data
            st.info("Dataset loaded from the last session.")
        except FileNotFoundError:
            st.warning("No dataset has been loaded.")

st.write("2) Once your file has been successfully uploaded, navigate the buttons on the side bar to the left to begin exploring your data and receive insights from our data analysis and machine learning model.")
