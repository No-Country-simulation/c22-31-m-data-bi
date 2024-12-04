import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model
from sklearn.metrics import roc_auc_score, classification_report
import os


# Load CSS file for custom styles
def load_css():
    """
    Load custom CSS styles from a file and apply them to the Streamlit app.
    """
    css_path = os.path.join("styles", "styles.css")
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Apply the custom styles
load_css()


# Define a fixed path for the model
MODEL_PATH = "models/modelo_rna_sintetico.h5"

# Page title
st.title("Machine Learning Model Evaluation")

# Load the machine learning model
st.subheader("Loaded Model")
try:
    model = load_model(MODEL_PATH)
    st.success(f"Model successfully loaded from `{MODEL_PATH}`.")
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()

# Section for uploading test data
st.subheader("Upload Test Data")
test_data_file = st.file_uploader(
    "Upload a CSV file with test data", type="csv"
    )

if test_data_file:
    # Read the uploaded test data
    test_data = pd.read_csv(test_data_file)
    st.write("Preview of Test Data:", test_data.head())

    # Assume test data contains features and labels
    try:
        X_test = test_data.iloc[:, :-1].values  # All columns except the last
        y_test = test_data.iloc[:, -1].values   # Last column as labels

        # Model predictions and evaluation
        st.subheader("Model Evaluation")
        y_pred = model.predict(X_test).ravel()
        roc_auc = roc_auc_score(y_test, y_pred)
        classification_rep = classification_report(
            y_test, (y_pred > 0.5).astype(int), output_dict=True
        )

        # Display evaluation results
        st.write(f"**AUC-ROC:** {roc_auc:.4f}")
        st.write("**Classification Report:**")
        st.table(pd.DataFrame(classification_rep).transpose())
    except Exception as e:
        st.error(f"Error during evaluation: {e}")
