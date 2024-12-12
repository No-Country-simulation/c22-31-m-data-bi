import streamlit as st
import os
import base64
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from fpdf import FPDF
import numpy as np


# Load CSS file
def load_css():
    css_path = os.path.join("styles", "styles.css")
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load styles and text
load_css()


# Application title
st.title("Report")

# path Predictions
PREDICTIONS_PATH = "dataset/predictions_log.csv"

# Load the dataset if it exists
data = pd.read_csv(PREDICTIONS_PATH)


# Function to generate graphics and key metrics
def generate_analysis_report(transactions):
    """
    Generates key metrics and graphs for fraud analysis.
    """
    st.subheader("Data Analysis")

    # Plot Distribution of Transaction Amounts
    fig_amt = px.histogram(
        transactions, x="amt", title="Distribution of Transaction Amounts")
    st.plotly_chart(fig_amt)

    # Key metrics
    total_transactions = len(transactions)
    fraud_transactions = transactions["is_fraud_pred"].sum()
    non_fraud_transactions = total_transactions - fraud_transactions

    st.write(f"**Total Transactions:** {total_transactions}")
    st.write(f"**Fraudulent Transactions:** {fraud_transactions}")
    st.write(f"**Non-Fraudulent Transactions:** {non_fraud_transactions}")

    # PDF file generation
    if st.button("PDF Report"):
        generate_pdf_report(
            transactions, fraud_transactions,
            non_fraud_transactions
            )

    # Export to Excel
    if st.button("Data in Excel"):
        transactions.to_excel("fraud_analysis_report.xlsx", index=False)
        with open("fraud_analysis_report.xlsx", "rb") as excel_file:
            st.download_button(
                label="Download Excel",
                data=excel_file,
                file_name="fraud_analysis_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


# Function to generate PDF report
def generate_pdf_report(transactions, fraud_count, non_fraud_count):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Fraud Analysis Report", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Total Transactions: {len(transactions)}", ln=True)
    pdf.cell(200, 10, txt=f"Fraudulent Transactions: {fraud_count}", ln=True)
    pdf.cell(200, 10, txt=f"Non-Fraudulent Transactions: {non_fraud_count}",
             ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Executive Summary:", ln=True)
    pdf.multi_cell(0, 10,
                   "This report presents a detailed analysis of real-time transactions, "
                   "identifying potential fraud cases and providing key metrics for decision making.")

    pdf_file = "fraud_analysis_report.pdf"
    pdf.output(pdf_file)

    with open(pdf_file, "rb") as f:
        st.download_button(
            label="Download PDF",
            data=f,
            file_name=pdf_file,
            mime="application/pdf"
        )


# Call the analysis function after processing transactions
generate_analysis_report(data)
