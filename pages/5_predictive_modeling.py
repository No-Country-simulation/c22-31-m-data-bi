import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model
from sklearn.metrics import roc_auc_score, classification_report, roc_curve
import os
import base64


# Load CSS file for custom styles
def load_css():
    """
    Load custom CSS styles from a file and apply them to the Streamlit app.
    """
    css_path = os.path.join("styles", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Apply the custom styles
load_css()

# Define fixed paths
MODEL_PATH = "models/modelo_rna_sintetico_2.h5"
TEST_PATH = "dataset/YX_test.csv"

# Page title
st.title("Predictive Modeling")

# Ensure model is loaded into session state
if "model" not in st.session_state:
    try:
        st.session_state["model"] = load_model(MODEL_PATH)
        st.success(f"Model successfully loaded from `{MODEL_PATH}`.")
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        st.stop()

model = st.session_state["model"]

# Ensure test data is loaded into session state
if "test_data" not in st.session_state:
    try:
        st.session_state["test_data"] = pd.read_csv(TEST_PATH)
    except FileNotFoundError:
        st.error(f"Test dataset not found at `{TEST_PATH}`.")
        st.stop()

test_data = st.session_state["test_data"]

# Display test dataset
if st.checkbox('Show test dataset'):
    st.subheader('Test dataset')
    st.write(test_data)

# Separate features and labels
X_test = test_data.iloc[:, :-1].values  # All columns except the last
y_test = test_data.iloc[:, -1].values   # Last column as labels

# Model evaluation
try:
    st.subheader("Model Evaluation")
    # Get predictions from the model
    y_pred = model.predict(X_test).ravel()

    # Use a threshold of 0.5 to convert probabilities to class labels
    y_pred_class = (y_pred > 0.5).astype(int)

    # Calculate AUC-ROC for binary or multi-class classification
    if len(set(y_test)) == 2:  # Binary classification
        roc_auc = roc_auc_score(y_test, y_pred)
    else:  # Multi-class classification
        roc_auc = roc_auc_score(y_test, y_pred, multi_class="ovr")

    # Generate classification report
    classification_rep = classification_report(
        y_test, y_pred_class, output_dict=True
    )

    # Display evaluation results
    st.write(f"**AUC-ROC:** {roc_auc:.4f}")
    st.write("**Classification Report:**")
    st.table(pd.DataFrame(classification_rep).transpose())

    # Plot AUC-ROC curve
    st.subheader("ROC Curve")
    fpr, tpr, thresholds = roc_curve(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f'AUC = {roc_auc:.4f}', color='blue')
    plt.plot([0, 1], [0, 1], 'k--', label='Random Guess')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc='best')
    st.pyplot(plt)  # Display the plot in Streamlit
    plt.close()

except Exception as e:
    st.error(f"Error during evaluation: {e}")
