import streamlit as st
from datetime import datetime

# ----------------------- CONFIG -----------------------
st.set_page_config(
    page_title="Mass Converter",
    page_icon="⚖️",
    layout="centered"
)

# ----------------------- THEME TOGGLE -----------------------
st.sidebar.header("⚙️ Settings")
theme = st.sidebar.radio("Choose Theme:", ["Light", "Dark"])
if theme == "Dark":
    st.markdown(
        """
        <style>
        body {background-color: #121212; color: #fafafa;}
        .stButton>button {background-color: #0d6efd; color: white; border-radius: 8px;}
        </style>
        """,
        unsafe_allow_html=True
    )

# ----------------------- UNIT DEFINITIONS -----------------------
mass_units = {
    "Kilogram (kg)": 1,
    "Gram (g)": 0.001,
    "Milligram (mg)": 0.000001,
    "Microgram (µg)": 1e-9,
    "Ton (metric)": 1000,
    "Pound (lb)": 0.45359237,
    "Ounce (oz)": 0.0283495,
    "Stone (st)": 6.35029
}

# ----------------------- TITLE -----------------------
st.title("⚖️ Advanced Mass Converter")
st.caption("Convert between multiple mass units instantly, with live history tracking.")

# ----------------------- INPUT SECTION -----------------------
col1, col2 = st.columns(2)
with col1:
    input_value = st.number_input("Enter Value", min_value=0.0, step=0.1, value=1.0)

# Searchable dropdowns
with col2:
    search = st.text_input("🔍 Search Unit (optional)", "")
    filtered_units = [u for u in mass_units if search.lower() in u.lower()] if search else list(mass_units.keys())
    from_unit = st.selectbox("From Unit", filtered_units)

to_unit = st.selectbox("To Unit", list(mass_units.keys()), index=1)

# ----------------------- CONVERSION LOGIC -----------------------
if "history" not in st.session_state:
    st.session_state.history = []

if st.button("🔁 Convert"):
    result = input_value * (mass_units[from_unit] / mass_units[to_unit])
    st.success(f"{input_value} {from_unit} = {result:.6f} {to_unit}")

    # Save conversion to history
    st.session_state.history.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "from": from_unit,
        "to": to_unit,
        "input": input_value,
        "result": round(result, 6)
    })

# ----------------------- QUICK REFERENCE TABLE -----------------------
st.divider()
st.subheader("📊 Quick Conversion Table")

converted_values = {
    unit: input_value * (mass_units[from_unit] / mass_units[unit])
    for unit in mass_units
}
st.dataframe(converted_values.items(), use_container_width=True)

# ----------------------- HISTORY SECTION -----------------------
st.divider()
st.subheader("🕒 Conversion History")

if st.session_state.history:
    st.table(st.session_state.history)
else:
    st.info("No conversions yet. Perform one to see history here!")

# ----------------------- FOOTER -----------------------
st.markdown("---")
st.caption("Developed with ❤️ by Abdul Saeed | Built using Streamlit ⚡")
