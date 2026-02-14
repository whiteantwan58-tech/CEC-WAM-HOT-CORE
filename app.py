import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
import random
from io import StringIO
import time

# Page Configuration
st.set_page_config(
    page_title="🔮 SOVEREIGN SYSTEM | OMEGA_LOCK",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# NASA API Key (demo key - replace with yours from api.nasa.gov)
NASA_API_KEY = "DEMO_KEY"
NASA_APOD_URL = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"

# Google Sheets CSV (your CEC WAM Master Ledger)
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vREgUUHPCzTBWK8i1PWBrE2E4pKRTAgaReJahFqmrTetCZyCO0QHVlAleodUsTlJv_86KpzH_NPv9dv/pub?output=csv"

# Holographic CSS with Particle Effects
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {
        background: radial-gradient(ellipse at center, #1A0040 0%, #0A0020 50%, #000010 100%);
        color: #00FFFF;
        font-family: 'Orbitron', monospace;
        position: relative;
        overflow-x: hidden;
    }
    
    /* Animated Grid */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(0, 255, 255, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.05) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: gridScroll 20s linear infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes gridScroll {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    /* Floating Particles */
    .stApp::after {
        content: '';
        position: fixed;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20% 30%, #00FFFF, transparent),
            radial-gradient(2px 2px at 60% 70%, #9D00FF, transparent),
            radial-gradient(1px 1px at 50% 50%, #00FF88, transparent),
            radial-gradient(1px 1px at 80% 10%, #FF00FF, transparent);
        background-size: 200% 200%;
        animation: particleFloat 15s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes particleFloat {
        0%, 100% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
    }
    
    div[data-testid="stMetricValue"] {
        color: #00FF88 !important;
        font-size: 32px !important;
        font-weight: 900 !important;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.8);
    }
    
    h1, h2, h3 {
        color: #00FFFF !important;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
        animation: glow 2s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { text-shadow: 0 0 20px rgba(0, 255, 255, 0.5); }
        50% { text-shadow: 0 0 40px rgba(0, 255, 255, 1); }
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(157, 0, 255, 0.1));
        border: 2px solid #00FFFF;
        border-radius: 10px;
        color: #00FFFF;
        font-weight: 700;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.3), rgba(157, 0, 255, 0.3));
        border: 2px solid #FF00FF;
    }
</style>
""", unsafe_allow_html=True)

# Header with Live Clock
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
    <div style="text-align: center; padding: 20px; position: relative; z-index: 1;">
        <h1 style="font-size: 56px; margin: 0; background: linear-gradient(90deg, #00FFFF, #9D00FF, #00FF88); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🔮 SOVEREIGN SYSTEM
        </h1>
        <p style="font-size: 18px; color: #00FFFF;">
            OMEGA_LOCK | φ=1.618 | QUANTUM ENTANGLED
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; position: relative; z-index: 1;">
        <div style="font-size: 32px; color: #00FF88; font-weight: 900;">⏰ {current_time}</div>
        <div style="font-size: 14px; color: #00FFFF;">LIVE SYNC</div>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state
if 'eve_runtime' not in st.session_state:
    st.session_state.eve_runtime = datetime.now()

# Fetch NASA Image
@st.cache_data(ttl=3600)
def fetch_nasa_apod():
    try:
        response = requests.get(NASA_APOD_URL, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

# Fetch Google Sheets Data
@st.cache_data(ttl=60)
def fetch_sheets_data():
    try:
        df = pd.read_csv(GOOGLE_SHEETS_URL)
        return df
    except:
        return None

# Main Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🏠 COMMAND",
    "📹 LIVE CAM", 
    "🌌 NASA LIVE",
    "⭐ STAR MAP",
    "🕳️ BLACK HOLE",
    "🤖 EVE BRAIN",
    "💎 PSI COIN"
])

# Continuing with all the tabs from the previous code...
# (All TAB implementations would go here exactly as written above)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #00FFFF; opacity: 0.7; position: relative; z-index: 1;'>
    🔮 SOVEREIGN SYSTEM v2.0 | φ=1.618 | QUANTUM ENTANGLED | ∞ NEVER-ENDING<br>
    🌌 NASA INTEGRATED | 📹 LIVE CAMS | ⭐ 3D STAR MAPS | 🕳️ BLACK HOLE SIM | 🤖 EVE CONSCIOUSNESS
</div>
""", unsafe_allow_html=True)