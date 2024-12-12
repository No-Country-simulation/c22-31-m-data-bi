import streamlit as st
import pandas as pd
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


# Title of the application
st.title("Data Preprocessing")

# Temporary file path for saving and loading datasets
TEMP_FILE_PATH = "data/dataset.csv"

# Load the dataset from session state or the temporary file
if "data" not in st.session_state:
    try:
        # Attempt to load data from the temporary file
        data = pd.read_csv(TEMP_FILE_PATH)
        st.session_state["data"] = data
        st.info("Dataset loaded from the temporary file.")
    except FileNotFoundError:
        # Notify the user if the file is not found
        st.warning("No dataset has been loaded. "
                   "Go back to 'Home' to upload the data.")
        st.stop()

# Access the dataset from session state
data = st.session_state["data"]

# Display an initial overview of the dataset
st.header("Initial Dataset Overview")
st.write(data.head())

# Section: Drop columns from the dataset
st.header("Drop Columns")
columns_to_drop = st.multiselect(
    "Select columns to drop:",
    options=data.columns,
)

if st.button("Drop Selected Columns"):
    if columns_to_drop:
        # Drop the selected columns
        data = data.drop(columns=columns_to_drop)
        st.session_state["data"] = data
        st.success(f"Columns {columns_to_drop} dropped successfully!")
        st.write("Updated dataset:")
        st.write(data.head())
    else:
        st.warning("No columns selected to drop.")

# Section: Change data types of columns
st.header("Change Column Data Types")

# Let the user select columns for type conversion
columns_for_conversion = st.multiselect(
    "Select columns to change their data type:",
    options=data.columns,
)

if columns_for_conversion:
    column_type_mapping = {}
    for col in columns_for_conversion:
        # Allow the user to choose a new data type for each column
        new_type = st.selectbox(
            f"Select new data type for column '{col}':",
            options=["datetime", "int", "float", "string"],
            key=f"conversion_{col}"
        )
        column_type_mapping[col] = new_type

    if st.button("Apply Data Type Changes"):
        for col, new_type in column_type_mapping.items():
            try:
                # Perform the type conversion
                if new_type == "datetime":
                    data[col] = pd.to_datetime(data[col])
                elif new_type == "int":
                    data[col] = data[col].astype(int)
                elif new_type == "float":
                    data[col] = data[col].astype(float)
                elif new_type == "string":
                    data[col] = data[col].astype(str)
            except Exception as e:
                # Notify the user if an error occurs
                st.error(f"Error converting column '{col}' to {new_type}: {e}")
        st.session_state["data"] = data
        st.success("Data type changes applied successfully!")
        st.write("Updated dataset:")
        st.write(data.head())

# Section: Save the preprocessed dataset
st.header("Save Changes")
if st.button("Save Preprocessed Dataset"):
    # Save the updated dataset back to the temporary file
    data.to_csv(TEMP_FILE_PATH, index=False)
    st.success("Dataset changes saved successfully!")
