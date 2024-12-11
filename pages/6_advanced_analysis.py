import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import shap
import os
import base64


# Load CSS file
def load_css():
    css_path = os.path.join("styles", "styles.css")
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load styles and text
load_css()


# Application title
st.title("Advanced Analysis")

# Fixed paths
MODEL_PATH = "models/modelo_rna_sintetico_2.h5"
TEST_PATH = "dataset/YX_test.csv"


# Load the model
if "model" not in st.session_state:
    try:
        st.session_state["model"] = load_model(MODEL_PATH)
        st.success(f"Model successfully loaded from {MODEL_PATH}.")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

model = st.session_state["model"]

# Load test data
if "test_data" not in st.session_state:
    try:
        st.session_state["test_data"] = pd.read_csv(TEST_PATH)
        st.success(f"Test data loaded from {TEST_PATH}.")
    except FileNotFoundError:
        st.error(f"Test dataset not found at {TEST_PATH}.")
        st.stop()

test_data = st.session_state["test_data"]

# Separate features (X) and labels (y)
X_test = test_data.drop(columns=["is_fraud"])
y_test = test_data["is_fraud"]

# Show the loaded data
if st.checkbox("Show test data"):
    st.dataframe(test_data)


# SHAP Analysis
st.header("Model Interpretation with SHAP")

# Create SHAP explainer for the Keras model
if "explainer" not in st.session_state:
    try:
        st.session_state["explainer"] = shap.Explainer(model, X_test)
        st.session_state["shap_values"] = st.session_state["explainer"](X_test)
    except Exception as e:
        st.error(f"Error creating SHAP explainer: {e}")
        st.stop()

explainer = st.session_state["explainer"]
shap_values = st.session_state["shap_values"]

# SHAP Summary Plot
st.subheader("SHAP Summary Plot")
if "summary_plot" not in st.session_state:
    try:
        plt.figure()  # Create a new figure
        shap.summary_plot(shap_values, X_test, show=False)
        st.session_state["summary_plot"] = plt.gcf()
    except Exception as e:
        st.error(f"Error generating SHAP summary plot: {e}")

# Display the stored summary plot
st.pyplot(st.session_state["summary_plot"])


# SHAP Dependence Plot
st.subheader("SHAP Dependence Plot")
try:
    # Feature selection for dependence plot
    feature_name = st.selectbox(
        "Select a feature for dependence plot:", X_test.columns)
    if "dependence_plot" not in st.session_state or \
            st.session_state.get("selected_feature") != feature_name:

        st.session_state["selected_feature"] = feature_name
        feature_index = X_test.columns.get_loc(feature_name)
        plt.figure()
        shap.dependence_plot(
            feature_index, shap_values.values, X_test, show=False)
        st.session_state["dependence_plot"] = plt.gcf()
    st.pyplot(st.session_state["dependence_plot"])
except Exception as e:
    st.error(f"Error generating SHAP dependence plot: {e}")


# SHAP Force Plot
st.subheader("SHAP Force Plot")
try:
    sample_index = st.number_input(
        "Select sample index for Force Plot:",
        min_value=0, max_value=len(X_test) - 1, value=0)
    if "force_plot" not in st.session_state or \
            st.session_state.get("selected_sample") != sample_index:
        st.session_state["selected_sample"] = sample_index
        sample_data = X_test.iloc[sample_index].values
        base_value = model.predict(np.expand_dims(sample_data, axis=0)).mean()

        # Generate force plot and store in session state
        plt.figure()
        shap.force_plot(
            base_value,
            shap_values[sample_index].values,
            sample_data,
            feature_names=X_test.columns.tolist(),
            matplotlib=True,
        )
        st.session_state["force_plot"] = plt.gcf()
    st.pyplot(st.session_state["force_plot"])
except Exception as e:
    st.error(f"Error generating SHAP force plot: {e}")
