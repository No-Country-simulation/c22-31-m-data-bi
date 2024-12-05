import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model
from sklearn.metrics import roc_auc_score, classification_report, roc_curve
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
MODEL_PATH = "models/modelo_rna_sintetico_2.h5"

# Test dataset
TEST_PATH = "raw_data/YX_test.csv"

# Page title
st.title("Predictive Modeling")

# Load the machine learning model
st.subheader("Loaded Model")
try:
    model = load_model(MODEL_PATH)
    st.success(f"Model successfully loaded from `{MODEL_PATH}`.")
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()

# Load the test dataset
test_data = pd.read_csv(TEST_PATH)

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

    # use a threshold of 0.5 to convert probabilities to class labels
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
