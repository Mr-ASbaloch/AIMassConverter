# app.py — Streamlit Mass Converter

import streamlit as st
from streamlit_mass_converter import *  # import all logic from main converter file

# Just run the imported Streamlit app
def main():
    st.title("Mass Converter — Streamlit App")
    st.write("This is the main entry point. All logic is in `streamlit_mass_converter.py`.")
    st.write("Run this file using: `streamlit run app.py`")

    # Optionally just call the logic (since the file already runs Streamlit on import)
    st.write("Below loads the converter interface.")
    import streamlit_mass_converter  # ensure it runs fully

if __name__ == "__main__":
    main()


# requirements.txt — dependencies for Mass Converter
# ---------------------------------------------------
# streamlit web framework
streamlit>=1.40.0

# core dependencies\pandas>=2.2.0
numpy>=1.26.0

# optional for better CSV handling
openpyxl>=3.1.2
