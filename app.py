
import streamlit as st
import pandas as pd
import os
from modules.panel_components import *

# Setup page
st.set_page_config(layout="wide", page_title="CEC-WAM Interface", page_icon="🪐")

# Inject Glassmorphism CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load logs
@st.cache_data
def load_logs():
    df = pd.read_csv("CEC_LOG.csv")
    return df.tail(50)

# Run EVE logic
def run_eve_sync():
    import eve_sync
    return eve_sync.run_eve_cycle()

# Layout Grid
st.markdown("## 🧠 CEC-WAM Quantum Core Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    quantum_core_panel()
    eve_comm_panel()

with col2:
    wallet_panel(psi_value=87321, usd_value=8500.00)
    system_metrics_panel()

with col3:
    log_panel(load_logs())
    galaxy_view_panel()
