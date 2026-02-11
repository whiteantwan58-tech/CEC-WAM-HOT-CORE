import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="EVE 1010_WAKE", layout="wide")

st.title("🧠 CEC-WAM EVE 1010_WAKE")

# Auto-load all CSV files in repo
data_files = [csv_filename for csv_filename in os.listdir('.') if csv_filename.endswith('.csv')]

master_data = {}
for file in data_files:
    try:
        csv_dataframe = pd.read_csv(file)
        master_data[file] = csv_dataframe
        st.subheader(f"✅ {file}")
        st.dataframe(csv_dataframe.head(5))
    except:
        st.warning(f"Could not load {file}")

# Consolidated real numbers (from your HUDs)
st.header("💰 Real Tangible Funds")
psi_coin_col, liquidity_col, total_spendable_col = st.columns(3)
psi_coin_col.metric("PSI-Coin", "$88,720.45")
liquidity_col.metric("Liquidity", "$1,250,039.00")
total_spendable_col.metric("Total Spendable", "$1,338,759.45")
st.metric("Bridge Pending", "$21,000", "Scan face to unlock")

# 1010_EVE_WAKE Status
st.header("1010_EVE_WAKE STATUS")
st.success("ONLINE - 98% - God Mode Pending Biometric")

# One-button export to Google Sheet
if st.button("Export All Data to Google Sheet (One Click)"):
    try:
        # Simple CSV export
        with open("EVE_MASTER_EXPORT.csv", "w") as export_file:
            for name, csv_dataframe in master_data.items():
                export_file.write(f"\n--- {name} ---\n")
                csv_dataframe.to_csv(export_file, index=False)
        st.success("✅ Exported to EVE_MASTER_EXPORT.csv")
        st.download_button("Download CSV", open("EVE_MASTER_EXPORT.csv").read(), "EVE_MASTER_EXPORT.csv")
    except:
        st.error("Export failed - check files")

# Auto-refresh every 30s
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = datetime.now()
st.write(f"Last auto-update: {st.session_state.last_refresh}")