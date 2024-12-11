import streamlit as st
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
st.title("About")
