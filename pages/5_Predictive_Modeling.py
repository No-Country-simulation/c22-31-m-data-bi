import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from tensorflow.keras import models, layers

# Título de la página
st.title("Predictive Modeling")
st.write("Training models to predict fraud.")

def train_val_test_split(df, rstate=42, shuffle=True, stratify=None):
    strat = df[stratify] if stratify else None
    train_set, test_set = train_test_split(
        df, test_size=0.4, random_state=rstate, shuffle=shuffle, stratify=strat)
    strat = test_set[stratify] if stratify else None
    val_set, test_set = train_test_split(
        test_set, test_size=0.5, random_state=rstate, shuffle=shuffle, stratify=strat)
    return train_set, val_set, test_set

def remove_labels(df, label_name):
    X = df.drop(label_name, axis=1)
    y = df[label_name].copy()
    return X, y

# Cargar el dataset
TEMP_FILE_PATH = "data/dataset.csv"

if "data" not in st.session_state:
    try:
        data = pd.read_csv(TEMP_FILE_PATH)
        st.session_state["data"] = data
        st.info("Dataset loaded from the temporary file.")
    except FileNotFoundError:
        st.warning("No dataset has been loaded. Upload a dataset to proceed.")
        st.stop()

data = st.session_state["data"]
st.write("### Data Overview")
st.write(data.head())

# Representación gráfica
if not data.empty:
    x_col = st.selectbox("Select X-axis column:", data.columns)
    y_col = st.selectbox("Select Y-axis column:", data.columns)

    if x_col and y_col:
        fig, ax = plt.subplots(figsize=(10, 6))
        try:
            ax.scatter(data[x_col][data['Class'] == 0], data[y_col][data['Class'] == 0], c="g", label="Legit")
            ax.scatter(data[x_col][data['Class'] == 1], data[y_col][data['Class'] == 1], c="r", label="Fraud")
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.legend()
            st.pyplot(fig)
        except KeyError:
            st.error("Invalid column selection.")

# Selecting columns and splitting the dataset
st.sidebar.header("Feature Selection")
feature_columns = st.sidebar.multiselect("Select feature columns:", data.columns)
target_column = st.sidebar.selectbox("Select target column:", data.columns)

if feature_columns and target_column:
    X = data[feature_columns]
    y = data[target_column]

    train_set, val_set, test_set = train_val_test_split(data, stratify=target_column)
    X_train, y_train = remove_labels(train_set, target_column)
    X_val, y_val = remove_labels(val_set, target_column)
    X_test, y_test = remove_labels(test_set, target_column)

    st.write("### Dataset Split")
    st.write(f"Train Set: {len(train_set)} rows")
    st.write(f"Validation Set: {len(val_set)} rows")
    st.write(f"Test Set: {len(test_set)} rows")

    # Model selection
    st.sidebar.header("Model Selection")
    model_type = st.sidebar.selectbox("Select model:", ["Neural Network"])
    if model_type == "Neural Network":
        model = models.Sequential([
            layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
            layers.Dense(64, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        st.write("### Model Summary")
        model.summary(print_fn=lambda x: st.text(x))

        # Train the model
        if st.button("Train Model"):
            st.write("Training model...")
            # report, cm, fpr, tpr = train_model(model, X_train, X_test, y_train, y_test)
            # st.write("### Classification Report")
            # st.json(report)

