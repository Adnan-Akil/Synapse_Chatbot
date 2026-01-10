import streamlit as st
from config.config import Config

def inject_custom_css():
    """Reads style.css and injects it into the Streamlit app"""
    try:
        with open(Config.CSS_FILE_PATH, "r") as f:
            css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file not found at: {Config.CSS_FILE_PATH}")
