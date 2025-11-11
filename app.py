import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os
import json

# ----------------------- CONFIG -----------------------
st.set_page_config(
    page_title="Mass Converter Pro",
    page_icon="⚖️",
    layout="centered"
)

HISTORY_FILE = "conversion_history.json"
SETTINGS_FILE = "user_settings.json"

# ----------------------- LOAD / SAVE UTILITIES -----------------------
def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ----------------------- PERSISTENT SETTINGS -----------------------
saved_settings = load_json(SETTINGS_FILE)
default_theme = saved_settings.get("theme", "Light")
default_view = saved_settings.get("view_mode", "Compact")

# Sidebar configuration
st.sidebar.header("⚙️ Settings")
theme = st.sidebar.radio("Choose Theme:", ["Light", "Dark"], index=0 if default_theme == "Light" else 1)
view_mode = st.sidebar.selectbox("Table View Mode:", ["Compact", "Detailed"], index=0 if default_view == "Compact" else 1)

# Save updated preferences
save_json(SETTINGS_FILE, {"theme": theme, "view_mode": view_mode})

if theme == "Dark":
    st.markdown(
        """
        <style>
        body {background-color: #121212; color: #fafafa;}
        .stButton>button {background-color: #0d6efd; color: white; border-radius: 8px;}
        .stDataFrame {border-radius: 10px;}
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

# ----------------------- LOAD PERSISTENT HISTORY -----------------------
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        st.session_state.history = json.load(f)
else:
    st.session_state.history = []

# ----------------------- TITLE -----------------------
st.title("⚖️ Mass Converter Pro")
st.caption("Smart, Persistent, and Visual — Built with Streamlit")

# ----------------------- INPUT SECTION -----------------------
col1, col2 = st.columns(2)
with col1:
    input_value = st.number_input("Enter Value", min_value=0.0, step=0.1, value=1.0)

with col2:
    from_unit = st.selectbox("From Unit", list(mass_units.keys()), index=0)

to_unit = st.selectbox("To Unit", list(mass_units.keys()), index=1)

# Reverse units
if st.button("🔄 Reverse Units"):
    from_unit, to_unit = to_unit, from_unit

# ----------------------- AUTO CONVERSION -----------------------
result = input_value * (mass_units[from_unit] / mass_units[to_unit])

st.success(f"✅ {input_value} {from_unit} = {result:.6f} {to_unit}")

# Copy button (visual only)
st.code(f"{result:.6f}", language="text")
st.button("📋 Copy Result", use_container_width=True, key="copy_result")

# ----------------------- SAVE TO HISTORY -----------------------
new_entry = {
    "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "From": from_unit,
    "To": to_unit,
    "Input": input_value,
    "Result": round(result, 6)
}
st.session_state.history.append(new_entry)

# Save persistent history
with open(HISTORY_FILE, "w") as f:
    json.dump(st.session_state.history, f, indent=4)

# ----------------------- QUICK CONVERSION TABLE -----------------------
st.divider()
st.subheader("📊 Quick Conversion Table")

conversion_data = []
for unit, factor in mass_units.items():
    converted_value = input_value * (mass_units[from_unit] / factor)
    conversion_data.append({
        "Unit": unit,
        "Converted Value": round(converted_value, 6),
        "Factor (to 1 kg)": factor if view_mode == "Detailed" else "-"
    })

df = pd.DataFrame(conversion_data)
if view_mode == "Compact":
    df = df[["Unit", "Converted Value"]]

st.dataframe(df, use_container_width=True)

st.download_button(
    "⬇️ Download Table (CSV)",
    df.to_csv(index=False).encode("utf-8"),
    file_name="conversion_table.csv",
    mime="text/csv"
)

# ----------------------- VISUALIZATION -----------------------
st.subheader("📈 Conversion Chart")
chart_df = pd.DataFrame({
    "Unit": [x["Unit"] for x in conversion_data],
    "Value": [x["Converted Value"] for x in conversion_data]
})
st.bar_chart(chart_df.set_index("Unit"))

# ----------------------- HISTORY SECTION -----------------------
st.divider()
st.subheader("🕒 Conversion History (Persistent)")

if st.session_state.history:
    hist_df = pd.DataFrame(st.session_state.history)
    st.dataframe(hist_df, use_container_width=True)

    # Download persistent history as Excel
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        hist_df.to_excel(writer, index=False, sheet_name="History")
    st.download_button(
        label="⬇️ Download History (Excel)",
        data=buffer.getvalue(),
        file_name="conversion_history.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Clear history button
    if st.button("🧹 Clear History"):
        st.session_state.history = []
        os.remove(HISTORY_FILE)
        st.experimental_rerun()
else:
    st.info("No conversions yet. Perform one to see history here!")

# ----------------------- FOOTER -----------------------
st.markdown("---")
st.caption("💾 Persistent Version | Developed by Abdul Saeed | Built using Streamlit ⚡")
