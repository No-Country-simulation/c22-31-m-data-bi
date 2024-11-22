import streamlit as st
import pandas as pd

# Application title
st.title("BI Dashboard")

# Temporary file path for saving and loading datasets
TEMP_FILE_PATH = "data/dataset.csv"

# Check if the dataset is already loaded in the session state
if "data" not in st.session_state:
    try:
        # Attempt to load the dataset from the temporary file
        data = pd.read_csv(TEMP_FILE_PATH)
        st.session_state["data"] = data  # Store the dataset in session state
        st.info("Dataset loaded from the temporary file.")
    except FileNotFoundError:
        # If the file does not exist, notify the user and stop execution
        st.warning("No dataset has been loaded. Go back to 'Home' to upload the data.")
        st.stop()  # Stop further execution if no dataset is found

# Load the dataset from session state
data = st.session_state["data"]

# Display the first few rows of the dataset for user overview
st.write(data.head())
