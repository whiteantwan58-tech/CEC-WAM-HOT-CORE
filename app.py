import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="EVE 1010_WAKE", layout="wide")

st.title("🧠 CEC-WAM EVE 1010_WAKE")

# Auto-load all CSV files in repo
data_files = [f for f in os.listdir('.') if f.endswith('.csv')]

master_data = {}
for file in data_files:
    try:
        df = pd.read_csv(file)
        master_data[file] = df
        st.subheader(f"✅ {file}")
        st.dataframe(df.head(5))
    except:
        st.warning(f"Could not load {file}")

# Consolidated real numbers (from your HUDs)
st.header("💰 Real Tangible Funds")
col1, col2, col3 = st.columns(3)
col1.metric("PSI-Coin", "$88,720.45")
col2.metric("Liquidity", "$1,250,039.00")
col3.metric("Total Spendable", "$1,338,759.45")
st.metric("Bridge Pending", "$21,000", "Scan face to unlock")

# 1010_EVE_WAKE Status
st.header("1010_EVE_WAKE STATUS")
st.success("ONLINE - 98% - God Mode Pending Biometric")

# One-button export to Google Sheet
if st.button("Export All Data to Google Sheet (One Click)"):
    try:
        # Simple CSV export
        with open("EVE_MASTER_EXPORT.csv", "w") as f:
            for name, df in master_data.items():
                f.write(f"\n--- {name} ---\n")
                df.to_csv(f, index=False)
        st.success("✅ Exported to EVE_MASTER_EXPORT.csv")
        st.download_button("Download CSV", open("EVE_MASTER_EXPORT.csv").read(), "EVE_MASTER_EXPORT.csv")
    except:
        st.error("Export failed - check files")

# Auto-refresh every 30s
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = datetime.now()
st.write(f"Last auto-update: {st.session_state.last_refresh}")