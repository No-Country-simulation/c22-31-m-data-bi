import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Constants
TEMP_FILE_PATH = "data/dataset.csv"

# Title
st.title("Data Exploration")


def load_data():
    """
    Load the dataset into the application, ensuring persistence using
    Streamlit's session_state.
    Returns:
        pd.DataFrame: Loaded dataset.
    """
    if "data" not in st.session_state:
        try:
            data = pd.read_csv(TEMP_FILE_PATH)
            st.session_state["data"] = data
            st.info("Dataset loaded from the temporary file.")
        except FileNotFoundError:
            st.warning("No dataset has been loaded. \
                       Go back to 'Home' to upload.")
            st.stop()
    return st.session_state["data"]


def show_overview(data):
    """
    Display an overview of the dataset including head, shape,
    descriptive statistics, data types, duplicate rows, and null values.
    Args:
        data (pd.DataFrame): The dataset to analyze.
    """
    st.subheader("Overview of the Dataset")
    st.write(data.head())
    st.write(f"Rows: {data.shape[0]} | Columns: {data.shape[1]}")
    st.write(data.describe(include="all"))
    st.subheader("Data Types")
    st.write(data.dtypes)
    st.subheader("Duplicate Rows")
    st.write(data.duplicated().sum())
    st.subheader("Null Values")
    st.write(data.isna().sum())


def analyze_target_column(data):
    """
    Allow the user to select a target column and display its analysis.
    Supports both categorical (pie chart) and numerical (histogram)
    visualizations.
    Args:
        data (pd.DataFrame): The dataset to analyze.
    """
    st.subheader("Select Target Column for Analysis")
    if "target_column" not in st.session_state:
        default_target = 'is_fraud' if 'is_fraud' in data.columns \
            else data.columns[0]
        st.session_state["target_column"] = default_target
    target_column = st.selectbox(
        "Choose a column:",
        data.columns,
        index=list(data.columns).index(st.session_state["target_column"])
    )
    if target_column != st.session_state["target_column"]:
        st.session_state["target_column"] = target_column
    if data[target_column].dtype == 'object' or \
            data[target_column].nunique() <= 10:
        value_counts = data[target_column].value_counts()
        labels = value_counts.index
        sizes = value_counts.values
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.pie(
            sizes, labels=labels, autopct='%1.1f%%', startangle=90,
            colors=['skyblue', 'salmon']
        )
        ax.axis('equal')
        plt.title(f'Proportion of {target_column}')
        st.pyplot(fig)
    else:
        fig, ax = plt.subplots()
        sns.histplot(
            data[target_column], kde=True, bins=20, ax=ax, color="skyblue"
        )
        ax.set_title(f'Distribution of {target_column}')
        st.pyplot(fig)


def show_correlation_matrix(data):
    """
    Display a correlation matrix heatmap for numerical columns in the dataset.
    Args:
        data (pd.DataFrame): The dataset to analyze.
    """
    st.subheader("Correlation Matrix")
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    if "selected_columns" not in st.session_state:
        st.session_state["selected_columns"] = numeric_columns.tolist()
    selected_columns = st.multiselect(
        "Select columns for the correlation matrix:",
        options=numeric_columns,
        default=st.session_state["selected_columns"]
    )
    if selected_columns != st.session_state["selected_columns"]:
        st.session_state["selected_columns"] = selected_columns
    if len(selected_columns) > 1:
        correlation_matrix = data[selected_columns].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(
            correlation_matrix, annot=True, cmap='coolwarm', ax=ax
        )
        ax.set_title("Correlation Matrix")
        st.pyplot(fig)
    else:
        st.warning("Select at least two columns for the correlation matrix.")


def show_transaction_vs_fraud(data):
    """
    Display a boxplot comparing fraud vs. non-fraud transaction amounts.
    Allow dynamic selection of categorical and numerical columns.
    Args:
        data (pd.DataFrame): The dataset to analyze.
    """
    st.header("Fraud vs Non-Fraud Amount Distribution")
    categorical_columns = data.select_dtypes(
        include=['object', 'category', 'bool', 'int']
    ).columns.tolist()
    numerical_columns = data.select_dtypes(
        include=['float64', 'int64']
    ).columns.tolist()

    # Initialize session state if not already done
    if "selected_x_column" not in st.session_state:
        st.session_state["selected_x_column"] = (
            'is_fraud' if 'is_fraud' in categorical_columns
            else categorical_columns[0]
        )
    if "selected_y_column" not in st.session_state:
        st.session_state["selected_y_column"] = (
            'amt' if 'amt' in numerical_columns else numerical_columns[0]
        )

    # Use session state for default values in widgets without redefining them
    selected_x_column = st.selectbox(
        "Select X-axis column (categorical):",
        options=categorical_columns,
        key="selected_x_column"  # Value managed directly by session state
    )
    selected_y_column = st.selectbox(
        "Select Y-axis column (numerical):",
        options=numerical_columns,
        key="selected_y_column"  # Value managed directly by session state
    )

    # Create the boxplot if valid columns are selected
    if selected_x_column and selected_y_column:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.boxplot(
            x=selected_x_column,
            y=selected_y_column,
            data=data,
            hue=selected_x_column,
            ax=ax
        )
        ax.set_ylabel(f"{selected_y_column} (Transaction Amount)")
        ax.set_xlabel(selected_x_column.capitalize())
        plt.legend(title=selected_x_column.capitalize())
        st.pyplot(fig)
    else:
        st.warning("Select both a categorical \
            column for X and numerical for Y.")


# Main Flow
data = load_data()
show_overview(data)
analyze_target_column(data)
show_correlation_matrix(data)
show_transaction_vs_fraud(data)