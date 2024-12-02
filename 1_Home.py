import streamlit as st
import pandas as pd
import os

def load_styles():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_styles()


st.title("Welcome to Fraud Detection System")
st.write("Description of the project...")

# Path for the temporary file
TEMP_FILE_PATH = "data/dataset.csv"

st.write("Upload a CSV file to start the analysis.")

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

