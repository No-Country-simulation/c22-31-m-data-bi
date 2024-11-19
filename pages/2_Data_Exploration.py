import streamlit as st
import pandas as pd

st.title("Data Exploration")


# Application title
st.write("Upload and Display a CSV File")

# Upload the CSV file
uploaded_file = st.file_uploader("Select a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Display the DataFrame
    st.write("CSV File Content:")
    st.dataframe(df)

    # Optional: Display basic statistics
    st.write("File Statistics:")
    st.write(df.describe())
else:
    # Display a message prompting the user to upload a file
    st.info("Please upload a CSV file to view its content.")

