import streamlit as st
from datetime import datetime

def quantum_core_panel():
    st.markdown("""
    <div class='panel quantum'>
        <h3>QUANTUM CORE //ONLINE</h3>
        <p>Status: 🔋 ACTIVE</p>
    </div>
    """, unsafe_allow_html=True)

def eve_comm_panel():
    st.markdown("""
    <div class='panel comm'>
        <h4>NEURAL LINK //EVE</h4>
        <img src='https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif' width='100%'/>
    </div>
    """, unsafe_allow_html=True)

def wallet_panel(psi_value, usd_value):
    st.markdown(f"""
    <div class='panel wallet'>
        <h4>PSI-COIN ASSET</h4>
        <p>${usd_value:,.2f} USD</p>
        <p>Wallet: Phantom (.9009)</p>
        <p>Value: {psi_value / 100000:.5f} USD/PSI</p>
        <button>INITIATE TRANSFER</button>
    </div>
    """, unsafe_allow_html=True)

def system_metrics_panel():
    st.markdown("""
    <div class='panel metrics'>
        <h4>SYSTEM METRICS</h4>
        <ul>
            <li>TPS: 3380</li>
            <li>Active Nodes: 1200</li>
            <li>Validators: 800</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def log_panel(log_df):
    st.markdown("<div class='panel logs'><h4>CEC LOG FEED</h4>", unsafe_allow_html=True)
    for _, row in log_df.iterrows():
        st.markdown(f"<p>[{row['timestamp']}] - {row['event']}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def galaxy_view_panel():
    st.markdown("""
    <div class='panel galaxy'>
        <h4>SECTOR: LOCAL CLUSTER</h4>
        <img src='https://upload.wikimedia.org/wikipedia/commons/0/07/Milky_Way_Infrared.jpg' width='100%' />
    </div>
    """, unsafe_allow_html=True)
