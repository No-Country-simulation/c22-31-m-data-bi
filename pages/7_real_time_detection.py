import streamlit as st
import pandas as pd
import time
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import os
import pickle
import os


# Load CSS file
def load_css():
    css_path = os.path.join("styles", "styles.css")
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load styles and text
load_css()



# Application title
st.title("Real-Time Fraud Detection")

# Paths
MODEL_PATH = "models/modelo_rna_sintetico.h5"
SCALER_PATH = "data/models/scaler.pkl"
TEMP_FILE_PATH = "data/dataset.csv"

# Load the pre-trained model
@st.cache_resource
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
    st.warning("No pre-trained scaler found. Fitting a temporary scaler for this session.")
    scaler = StandardScaler()

# Ensure the dataset is loaded into the session state
if "data" not in st.session_state:
    try:
        # Load the dataset if it exists
        data = pd.read_csv(TEMP_FILE_PATH)
        st.session_state["data"] = data
        # Initialize transaction counter if not present
        if "transaction_count" not in st.session_state:
            st.session_state["transaction_count"] = 0
        st.info("Dataset loaded from the temporary file.")
    except FileNotFoundError:
        st.warning("No dataset loaded. Please upload a file.")
        st.stop()
else:
    # Ensure the transaction counter is initialized
    if "transaction_count" not in st.session_state:
        st.session_state["transaction_count"] = 0

# Load data from session state
data = st.session_state["data"]

# Required columns for the model
required_columns = ['amt', 'lat', 'long', 'merch_lat', 'merch_long', 'city_pop']

# Check if the dataset contains the required columns
if not all(col in data.columns for col in required_columns):
    st.error(f"The dataset must contain the following columns: {', '.join(required_columns)}")
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
    Preprocesses data to extract the required columns and apply scaling to match model expectations.
    """
    # Select only the required columns
    X = transactions[required_columns].values
    
    # Apply scaling using the StandardScaler
    X_scaled = scaler.transform(X)

    # Validate the shape of the processed data
    expected_features = model.input_shape[-1]
    if X_scaled.shape[1] != expected_features:
        st.error(f"Input feature mismatch. Model expects {expected_features} features, but got {X_scaled.shape[1]}.")
        st.stop()
    
    return X_scaled

if model:
    # Monitor transactions in real-time
    while True:
        # Simulate a batch of transactions being processed in real-time
        batch_size = 10
        transactions_in_transit = data.sample(n=batch_size, replace=True)
        
        # Increment transaction count in session state
        st.session_state["transaction_count"] += len(transactions_in_transit)
        
        # Add transaction IDs to the batch
        transactions_in_transit["transaction_id"] = range(
            st.session_state["transaction_count"] - batch_size + 1,
            st.session_state["transaction_count"] + 1
        )

        # Reset index to ensure unique transaction IDs
        transactions_in_transit = transactions_in_transit.reset_index(drop=True)

        # Preprocess data to match the model's expected input
        X_scaled = preprocess_data(transactions_in_transit)

        # Ensure the shape matches the model's expected input
        if len(X_scaled.shape) != 2 or X_scaled.shape[1] != model.input_shape[-1]:
            st.error(f"Input shape mismatch. Model expects shape (None, {model.input_shape[-1]}), but got {X_scaled.shape}.")
            break

        # Make predictions with the model (probabilities)
        try:
            predictions = model.predict(X_scaled)
            transactions_in_transit["is_fraud_pred"] = (predictions > 0.5).astype(int)  # Convert to binary class
        except Exception as e:
            st.error(f"Prediction error: {e}")
            break
        
        # Display transactions in the monitor
        columns_to_display = list(transactions_in_transit.columns)
        transaction_placeholder.write(transactions_in_transit[columns_to_display])
        
        # Alert if fraudulent transactions are detected
        fraudulent_transactions = transactions_in_transit[transactions_in_transit["is_fraud_pred"] == 1]
        if not fraudulent_transactions.empty:
            alert_placeholder.error(f"🚨 ALERT: Fraudulent transactions detected:\n"
                                    f"{fraudulent_transactions[['transaction_id', 'is_fraud_pred']]}")
        else:
            alert_placeholder.success("✅ No fraud detected in this iteration.")
        
        # Wait before the next iteration
        time.sleep(refresh_rate)
else:
    st.warning("Please load a model to start monitoring.")
