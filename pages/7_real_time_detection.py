import streamlit as st
import pandas as pd
import time
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import os
import pickle
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
st.title("Real-Time Fraud Detection")

# Paths
MODEL_PATH = "models/modelo_rna_sintetico_2.h5"
SCALER_PATH = "data/models/scaler.pkl"
SIMULATION_DATA_PATH = "dataset/df_real_detection.csv"


# Load the pre-trained model
def load_model_resource(path):
    return load_model(path)


model = load_model_resource(MODEL_PATH)


# Load the pre-trained scaler
def load_scaler(path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return pickle.load(f)
    else:
        return None


scaler = load_scaler(SCALER_PATH)

# If scaler is not pre-trained, fit it temporarily (not ideal for production)
if scaler is None:
    st.warning(
        "No pre-trained scaler found. Fitting a \
            temporary scaler for this session.")
    scaler = StandardScaler()


# Load the dataset if it exists
data = pd.read_csv(SIMULATION_DATA_PATH)


# Required columns for the model
required_columns = [
    'amt', 'lat', 'long', 'merch_lat',
    'merch_long', 'city_pop', 'distance',
    'time_since_last_transaction'
    ]

# Check if the dataset contains the required columns
if not all(col in data.columns for col in required_columns):
    st.error(
        f"The dataset must contain the following columns:\
              {', '.join(required_columns)}")
    st.stop()

# Sidebar for configuration
st.sidebar.header("Settings")
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 10, 3)

# Transaction monitor
st.header("Transaction Monitor")
transaction_placeholder = st.empty()
alert_placeholder = st.empty()

# Fit the scaler temporarily if it wasn't pre-trained
if not hasattr(scaler, "mean_"):
    scaler.fit(data[required_columns].values)


def preprocess_data(transactions):
    """
    Preprocesses data to extract the required columns and apply
    scaling to match model expectations.
    """
    # Select only the required columns
    X = transactions[required_columns].values

    # Apply scaling using the StandardScaler
    X_scaled = scaler.transform(X)

    # Validate the shape of the processed data
    expected_features = model.input_shape[-1]
    if X_scaled.shape[1] != expected_features:
        st.error(
            f"Input feature mismatch. Model expects \
                  {expected_features} features, but got {X_scaled.shape[1]}.")
        st.stop()

    return X_scaled


if model:
    # Monitor transactions in real-time
    while True:
        # Simulate a batch of transactions being processed in real-time
        batch_size = 10
        transactions_in_transit = data.sample(n=batch_size, replace=True)

        if "transaction_count" not in st.session_state:
            st.session_state["transaction_count"] = 0


        # Increment transaction count in session state
        st.session_state["transaction_count"] += len(transactions_in_transit)

        # Add transaction IDs to the batch
        transactions_in_transit["transaction_id"] = range(
            st.session_state["transaction_count"] - batch_size + 1,
            st.session_state["transaction_count"] + 1
        )

        # Reset index to ensure unique transaction IDs
        transactions_in_transit = transactions_in_transit.reset_index(
            drop=True)

        # Preprocess data to match the model's expected input
        X_scaled = preprocess_data(transactions_in_transit)

        # Ensure the shape matches the model's expected input
        if len(X_scaled.shape) != 2 or \
                X_scaled.shape[1] != model.input_shape[-1]:
            st.error(
                f"Input shape mismatch. Model expects shape \
                    (None, {model.input_shape[-1]}), \
                    but got {X_scaled.shape}.")
            break

        # Make predictions with the model (probabilities)
        try:
            predictions = model.predict(X_scaled)
            transactions_in_transit[
                "is_fraud_pred"] = (predictions > 0.5).astype(int)
        except Exception as e:
            st.error(f"Prediction error: {e}")
            break

        # Display transactions in the monitor
        columns_to_display = list(transactions_in_transit.columns)
        transaction_placeholder.write(
            transactions_in_transit[columns_to_display])

        # Alert if fraudulent transactions are detected
        fraudulent_transactions = transactions_in_transit[
            transactions_in_transit["is_fraud_pred"] == 1]
        if not fraudulent_transactions.empty:
            alert_placeholder.error(
                f"🚨 ALERT: Fraudulent transactions detected:\n"
                f"{fraudulent_transactions[['transaction_id', 'is_fraud_pred']]}")
        else:
            alert_placeholder.success("✅ No fraud detected in this iteration.")

        # Wait before the next iteration
        time.sleep(refresh_rate)
else:
    st.warning("Please load a model to start monitoring.")
