import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------
# MASS UNIT DEFINITIONS
# ---------------------------
mass_units = {
    "Kilogram (kg)": 1,
    "Gram (g)": 0.001,
    "Milligram (mg)": 0.000001,
    "Pound (lb)": 0.45359237,
    "Ounce (oz)": 0.0283495,
    "Ton (metric)": 1000,
    "Microgram (µg)": 1e-9,
    "Stone (st)": 6.35029
}

# ---------------------------
# STREAMLIT PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Mass Converter",
    page_icon="⚖️",
    layout="centered"
)

# ---------------------------
# SIDEBAR SETTINGS
# ---------------------------
st.sidebar.header("⚙️ Settings")

# Theme toggle
theme = st.sidebar.radio("Choose Theme", ["🌞 Light", "🌙 Dark"])
if theme == "🌙 Dark":
    st.markdown(
        """
        <style>
        body {background-color: #0E1117; color: white;}
        .stButton>button {background-color: #262730; color: white; border-radius: 10px;}
        </style>
        """,
        unsafe_allow_html=True
    )

# Precision setting
decimal_places = st.sidebar.slider("Decimal Places", 1, 10, 4)

# ---------------------------
# MAIN TITLE
# ---------------------------
st.title("⚖️ Mass Converter")
st.write("Convert mass between multiple units instantly and view detailed results below.")

# ---------------------------
# INPUT SECTION
# ---------------------------
col1, col2 = st.columns(2)
with col1:
    input_value = st.number_input("Enter value", min_value=0.0, value=1.0, step=0.1)
with col2:
    from_unit = st.selectbox("From Unit", list(mass_units.keys()))

to_unit = st.selectbox("To Unit", list(mass_units.keys()))

# ---------------------------
# CONVERSION LOGIC
# ---------------------------
result = input_value * (mass_units[from_unit] / mass_units[to_unit])
st.success(f"{input_value} {from_unit} = {result:.{decimal_places}f} {to_unit}")

# ---------------------------
# HISTORY MANAGEMENT
# ---------------------------
if "history" not in st.session_state:
    st.session_state["history"] = []

# Save conversion to history
if st.button("Save Conversion"):
    st.session_state["history"].append({
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "From": from_unit,
        "To": to_unit,
        "Input": input_value,
        "Result": round(result, decimal_places)
    })
    st.success("✅ Conversion saved to history!")

# Show history
if st.session_state["history"]:
    st.subheader("📜 Conversion History")
    df_history = pd.DataFrame(st.session_state["history"])
    st.dataframe(df_history, use_container_width=True)

    csv = df_history.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download History (CSV)", csv, "conversion_history.csv", "text/csv")

# ---------------------------
# ENHANCED QUICK TABLE
# ---------------------------
st.divider()
st.subheader("📊 Quick Conversion Table")

converted_values = {
    unit: input_value * (mass_units[from_unit] / mass_units[unit])
    for unit in mass_units
}

df = pd.DataFrame({
    "Unit": converted_values.keys(),
    "Value": [round(v, decimal_places) for v in converted_values.values()]
})

# Search bar
search = st.text_input("🔍 Search unit", "")
if search:
    df = df[df["Unit"].str.contains(search, case=False)]

st.dataframe(df, use_container_width=True)

# Download results
csv_data = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Table (CSV)", csv_data, "mass_conversion_table.csv", "text/csv")

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.caption("Developed with ❤️ by Abdul Saeed | Streamlit Mass Converter v2.0")
