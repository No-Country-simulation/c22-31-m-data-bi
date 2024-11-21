import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Data Exploration")


@st.cache_data
def load_data(filename, delimiter):
    """
    - filename is the file to load from
    - delimiter is the column separator
    Returns:
    - pd.DataFrame: the loaded DataFrame
    """
    return pd.read_csv(filename, delimiter=delimiter)

# Load Dataset
data = load_data('data/raw_data/fraudTest.csv', ',')

# Mostrar el dataset
st.header("Overview of the dataset")
st.write(data.head())

# Dataset information.
st.header("Dataset information.")
st.write(f"Rows: {data.shape[0]}  |  Columns: {data.shape[1]}")
st.write(data.describe(include="all"))
st.write("Data types:")
st.write(data.dtypes)

# Duplicates and nan counts
st.write("Duplicate Rows")
st.write(data.duplicated().sum())

st.write("Null Values")
st.write(data.isna().sum())

# Create the pie chart
fraud_counts = data['is_fraud'].value_counts()
labels = fraud_counts.index
sizes = fraud_counts.values
fig, ax = plt.subplots(figsize=(10, 8))
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'salmon'])
ax.axis('equal')  # Asegura que el gráfico sea circular
plt.title('Proportion of Fraudulent vs Legitimate Transactions')
st.pyplot(fig)

# Transaction amount vs fraud
st.header("Fraud vs Non-Fraud Amount Distribution")
fig, ax = plt.subplots(figsize=(10, 8))
ax=sns.boxplot(y='amt',data=data,x='is_fraud', hue='is_fraud')
ax.set_ylabel('Transaction Amount (USD)')
ax.set_xlabel('Type')
plt.legend(title='Type', labels=['Fraud', 'Not Fraud'])
st.pyplot(fig)

#Gender vs Fraud
st.header("Correlation matrix")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(data[['amt', 'city_pop', 'unix_time', 'lat', 'long', 'merch_lat', 'merch_long']].corr(), annot=True, cmap='coolwarm')
st.pyplot(fig)