import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model
from sklearn.metrics import (
    roc_auc_score, classification_report,
    roc_curve, confusion_matrix, ConfusionMatrixDisplay
)
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

    # Calculate confusion matrix
    conf_matrix = confusion_matrix(y_test, y_pred_class)

    # Display evaluation results
    st.write(f"**AUC-ROC:** {roc_auc:.4f}")
    st.write("**Classification Report:**")
    st.table(pd.DataFrame(classification_rep).transpose())

    # Plot ROC Curve
    st.subheader("ROC Curve")
    fpr, tpr, thresholds = roc_curve(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f'AUC = {roc_auc:.4f}', color='tab:blue')
    plt.plot([0, 1], [0, 1], 'k--', label='Random Guess')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc='best')
    st.pyplot(plt)
    plt.close()

    # Plot Confusion Matrix
    st.subheader("Confusion Matrix")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        conf_matrix, annot=True,
        fmt='d', cmap='Blues',
        cbar=False, ax=ax
        )
    ax.set_xlabel("Predicted Labels")
    ax.set_ylabel("True Labels")
    st.pyplot(fig)
    plt.close()

except Exception as e:
    st.error(f"Error during evaluation: {e}")
