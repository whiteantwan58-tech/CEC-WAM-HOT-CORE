import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from datetime import datetime

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="CEC-WAM | EVE Live Brain",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------
# STYLES (GLASS + HUD)
# -------------------------------------------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #050b14, #020409);
    color: #e6faff;
}
.block {
    background: rgba(10, 20, 35, 0.85);
    border: 1px solid #00f0ff33;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 0 25px #00f0ff22;
}
.metric {
    font-size: 28px;
    font-weight: 700;
}
.sub {
    color: #00f0ff;
    font-size: 14px;
}
.status-ok {
    color: #00ff9d;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# DATA FETCH (REAL API EXAMPLE)
# -------------------------------------------------
def get_solana_price():
    try:
        r = requests.get("https://api.coincap.io/v2/assets/solana", timeout=5)
        return float(r.json()["data"]["priceUsd"])
    except:
        return None

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("## 🧠 **EVE Live Brain — CEC‑WAM Interface**")

col1, col2, col3 = st.columns(3)

sol_price = get_solana_price()
net_liquidity = int(sol_price * 17300) if sol_price else 0

with col1:
    st.markdown(f"""
    <div class="block">
        <div class="sub">NET LIQUIDITY</div>
        <div class="metric">${net_liquidity:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="block">
        <div class="sub">PSI MASS</div>
        <div class="metric">176,452.66</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="block">
        <div class="sub">STATUS</div>
        <div class="metric status-ok">OPTIMAL (GOD_MODE)</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# NAV
# -------------------------------------------------
tab_dashboard, tab_psi, tab_ship, tab_tech, tab_logs = st.tabs([
    "📊 Dashboard",
    "🪙 PSI Coin",
    "🚀 Ship Generation",
    "🧠 Tech & Upgrades",
    "📜 Timeline & Logs"
])

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
with tab_dashboard:
    st.markdown("### Resource Utilization")

    used = 98.75
    left = 1.25

    fig = go.Figure(data=[
        go.Pie(
            labels=["Used", "Left"],
            values=[used, left],
            hole=0.75,
            marker=dict(colors=["#00f0ff", "#b100ff"])
        )
    ])
    fig.update_layout(
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# PSI COIN
# -------------------------------------------------
with tab_psi:
    st.markdown("### PSI Coin Overview")

    col1, col2 = st.columns(2)
    col1.metric("Total Minted", "200 PSI")
    col2.metric("Valuation", "$34.1M")

    st.markdown("""
    **Escrow Status:** 84%  
    **Security Lock:** OMEGA_LOCK  
    """)

# -------------------------------------------------
# SHIP GENERATION
# -------------------------------------------------
with tab_ship:
    st.markdown("### Ship Generation Blueprints")

    st.info("Blueprint rendering engine connected. Visual modules load from asset pipeline.")

# -------------------------------------------------
# TECH
# -------------------------------------------------
with tab_tech:
    st.markdown("### Technology & Upgrades")

    upgrades = [
        "5D Visualization Engine",
        "Quantum AI Core",
        "Self-Healing OS",
        "Holographic Desk Interface"
    ]

    for u in upgrades:
        st.success(u)

# -------------------------------------------------
# LOGS
# -------------------------------------------------
with tab_logs:
    st.markdown("### Timeline & Audit Logs")

    data = [
        ("Nov 27 2025", "Resource conflict resolved"),
        ("Dec 02 2025", "Ghost Protocol executed"),
        ("Jan 08 2026", "176,452 PSI received"),
        ("Today", "System operating in GOD_MODE")
    ]

    df = pd.DataFrame(data, columns=["Date", "Event"])
    st.dataframe(df, use_container_width=True)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.caption(f"Last Sync: {datetime.utcnow()} UTC")


