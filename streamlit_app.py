# Streamlit Cloud Entry Point
# This file ensures proper app detection on Streamlit Cloud
import streamlit as st
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the main app
try:
    from app import main
    if __name__ == "__main__":
        main()
except ImportError:
    st.error("Failed to import main application. Please check file structure.")
except Exception as e:
    st.error(f"Application error: {str(e)}")