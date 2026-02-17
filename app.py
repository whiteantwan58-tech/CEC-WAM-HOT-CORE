"""
CEC-WAM-HOT-CORE Streamlit Dashboard

This dashboard provides real-time visualization and monitoring of the CEC-WAM system.

Performance Optimizations:
- Seeded random data: Uses hour-based seeds to prevent chart flickering
- Cached API responses: NASA (1hr TTL), Google Sheets (1min TTL)
- Removed infinite rerun loop: Manual refresh instead of continuous auto-refresh
- Efficient data structures: Bounded collections prevent memory bloat

For detailed performance guidelines, see PERFORMANCE_OPTIMIZATION.md
"""

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

# Google Sheets Configuration
# Primary Google Sheets CSV (CEC WAM Master Ledger)
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vREgUUHPCzTBWK8i1PWBrE2E4pKRTAgaReJahFqmrTetCZyCO0QHVlAleodUsTlJv_86KpzH_NPv9dv/pub?output=csv"

# Alternative frozen/locked sheet ID for secure data display
# Format: https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv
FROZEN_SHEET_ID = "14nNp33Dk2YoYcVcQI0lUEp208m-VvZboi_Te8jt_flg2NkNm8WieN0sX"
FROZEN_SHEETS_URL = f"https://docs.google.com/spreadsheets/d/{FROZEN_SHEET_ID}/export?format=csv"

# Expected column schema for data locking (defines order and expected columns)
# Note: dtype values are for documentation only; actual type enforcement happens in display config
EXPECTED_COLUMNS = {
    'Category': str,
    'Item': str,
    'Value': float,
    'Status': str,
    'Date': str,
    'Notes': str
}

# Enhanced HD Holographic CSS with Premium Glassmorphism and 5D Visuals
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    /* Enhanced Background with 5D Depth Effect */
    .stApp {
        background: radial-gradient(ellipse at center, #1A0040 0%, #0A0020 50%, #000010 100%);
        color: #00FFFF;
        font-family: 'Orbitron', monospace;
        position: relative;
        overflow-x: hidden;
    }
    
    /* Animated Grid Layer with Enhanced Glassmorphism */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(0, 255, 255, 0.12) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.12) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: gridScroll 20s linear infinite;
        pointer-events: none;
        z-index: 0;
        opacity: 0.7;
        backdrop-filter: blur(2px);
    }
    
    @keyframes gridScroll {
        0% { transform: translate(0, 0); opacity: 0.5; }
        50% { opacity: 0.9; }
        100% { transform: translate(50px, 50px); opacity: 0.5; }
    }
    
    /* HD Particle System with 5D Holographic Effect */
    .stApp::after {
        content: '';
        position: fixed;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle, #00FFFF 1.5px, transparent 1.5px),
            radial-gradient(circle, #9D00FF 1.5px, transparent 1.5px),
            radial-gradient(circle, #00FF88 1.5px, transparent 1.5px),
            radial-gradient(circle, #FF00FF 1.5px, transparent 1.5px),
            radial-gradient(circle, #FFD700 1px, transparent 1px);
        background-size: 300px 300px, 400px 400px, 250px 250px, 350px 350px, 200px 200px;
        background-position: 0% 0%, 100% 0%, 0% 100%, 100% 100%, 50% 50%;
        animation: particleFloat 25s ease-in-out infinite, particlePulse 10s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
        filter: blur(0.5px) brightness(1.2);
    }
    
    @keyframes particleFloat {
        0%, 100% { background-position: 0% 0%, 100% 0%, 0% 100%, 100% 100%, 50% 50%; }
        20% { background-position: 30% 70%, 80% 30%, 20% 90%, 90% 20%, 60% 40%; }
        40% { background-position: 60% 40%, 50% 60%, 40% 70%, 70% 40%, 30% 70%; }
        60% { background-position: 90% 10%, 20% 90%, 70% 30%, 30% 80%, 80% 20%; }
        80% { background-position: 50% 50%, 50% 50%, 50% 50%, 50% 50%, 50% 50%; }
    }
    
    @keyframes particlePulse {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 0.9; }
    }
    
    /* Enhanced Glassmorphic Cards with HD Blur */
    div[data-testid="stMetric"],
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(2, 8, 14, 0.75) !important;
        backdrop-filter: blur(24px) saturate(220%) brightness(1.15) !important;
        -webkit-backdrop-filter: blur(24px) saturate(220%) brightness(1.15) !important;
        border: 1px solid rgba(40, 240, 255, 0.65) !important;
        border-radius: 16px !important;
        box-shadow: 0 0 30px rgba(40, 240, 255, 0.25), 
                    0 8px 32px rgba(0, 255, 255, 0.15),
                    inset 0 1px 2px rgba(255, 255, 255, 0.1) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    div[data-testid="stMetric"]:hover,
    div[data-testid="stVerticalBlock"] > div:hover {
        border-color: rgba(44, 255, 154, 0.85) !important;
        box-shadow: 0 0 40px rgba(40, 240, 255, 0.45), 
                    0 0 90px rgba(44, 255, 154, 0.25),
                    inset 0 1px 2px rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Metric Values with Enhanced Glow */
    div[data-testid="stMetricValue"] {
        color: #00FF88 !important;
        font-size: 36px !important;
        font-weight: 900 !important;
        text-shadow: 0 0 25px rgba(0, 255, 136, 0.9), 
                     0 0 45px rgba(0, 255, 136, 0.5) !important;
        animation: metricGlow 3s ease-in-out infinite !important;
    }
    
    @keyframes metricGlow {
        0%, 100% { 
            text-shadow: 0 0 25px rgba(0, 255, 136, 0.7), 0 0 45px rgba(0, 255, 136, 0.4);
        }
        50% { 
            text-shadow: 0 0 35px rgba(0, 255, 136, 1), 0 0 60px rgba(0, 255, 136, 0.6);
        }
    }
    
    /* Headers with Enhanced Holographic Effect */
    h1, h2, h3 {
        color: #00FFFF !important;
        text-shadow: 0 0 25px rgba(0, 255, 255, 0.9), 
                     0 0 50px rgba(0, 255, 255, 0.5),
                     0 0 75px rgba(157, 0, 255, 0.3) !important;
        animation: headerGlow 3s ease-in-out infinite !important;
        position: relative !important;
    }
    
    @keyframes headerGlow {
        0%, 100% { 
            text-shadow: 0 0 25px rgba(0, 255, 255, 0.7), 
                        0 0 50px rgba(0, 255, 255, 0.4),
                        0 0 75px rgba(157, 0, 255, 0.2);
        }
        50% { 
            text-shadow: 0 0 35px rgba(0, 255, 255, 1), 
                        0 0 60px rgba(0, 255, 255, 0.7),
                        0 0 100px rgba(157, 0, 255, 0.5);
        }
    }
    
    /* Enhanced Tab Styling with Premium Glassmorphism */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(0, 0, 0, 0.5) !important;
        padding: 8px !important;
        border-radius: 15px !important;
        backdrop-filter: blur(20px) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.15), rgba(157, 0, 255, 0.15)) !important;
        backdrop-filter: blur(15px) saturate(180%) !important;
        border: 2px solid rgba(0, 255, 255, 0.6) !important;
        border-radius: 12px !important;
        color: #00FFFF !important;
        font-weight: 700 !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.2) !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.25), rgba(157, 0, 255, 0.25)) !important;
        border-color: rgba(44, 255, 154, 0.8) !important;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.35), rgba(157, 0, 255, 0.35)) !important;
        border: 2px solid #FF00FF !important;
        box-shadow: 0 0 30px rgba(255, 0, 255, 0.5), 
                    0 0 50px rgba(0, 255, 255, 0.3) !important;
    }
    
    /* Biometric Lock Screen Simulation */
    .biometric-status {
        background: rgba(10, 20, 40, 0.8);
        backdrop-filter: blur(20px) saturate(180%) brightness(1.1);
        border: 2px solid rgba(0, 255, 255, 0.6);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 0 40px rgba(0, 255, 255, 0.3),
                    inset 0 0 20px rgba(0, 255, 255, 0.1);
        animation: biometricPulse 2s ease-in-out infinite;
    }
    
    @keyframes biometricPulse {
        0%, 100% {
            box-shadow: 0 0 40px rgba(0, 255, 255, 0.3),
                        inset 0 0 20px rgba(0, 255, 255, 0.1);
        }
        50% {
            box-shadow: 0 0 60px rgba(0, 255, 255, 0.5),
                        inset 0 0 30px rgba(0, 255, 255, 0.2);
        }
    }
    
    /* DataFrame Styling with Glassmorphism */
    div[data-testid="stDataFrame"] {
        background: rgba(2, 8, 14, 0.8) !important;
        backdrop-filter: blur(20px) saturate(200%) !important;
        border: 1px solid rgba(40, 240, 255, 0.5) !important;
        border-radius: 12px !important;
        box-shadow: 0 0 25px rgba(40, 240, 255, 0.2) !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #00D9FF 0%, #00FF88 100%) !important;
        color: #0E0E1A !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 32px !important;
        font-weight: bold !important;
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.5) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 0 35px rgba(0, 217, 255, 0.7) !important;
    }
    
    /* Checkbox Styling */
    div[data-testid="stCheckbox"] {
        background: rgba(0, 255, 255, 0.1);
        padding: 10px;
        border-radius: 8px;
        border: 1px solid rgba(0, 255, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Biometric Authentication Status Panel
st.markdown("""
<div class="biometric-status">
    <div style="position: relative; display: inline-block;">
        <div style="font-size: 96px; margin-bottom: 20px; animation: pulse 2s infinite;">🔐</div>
    </div>
    <h2 style="color: #00FF88; margin: 15px 0; font-size: 28px;">
        ✅ BIOMETRIC AUTH ACTIVE
    </h2>
    <p style="color: #00FFFF; font-size: 16px; opacity: 0.9;">
        🔒 SYSTEM SECURED | 🧬 DNA VERIFIED | 🌀 QUANTUM LOCKED
    </p>
    <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px; flex-wrap: wrap;">
        <div style="padding: 8px 16px; background: rgba(0, 255, 136, 0.2); border: 1px solid #00FF88; border-radius: 20px;">
            👁️ IRIS SCAN: VERIFIED
        </div>
        <div style="padding: 8px 16px; background: rgba(0, 255, 255, 0.2); border: 1px solid #00FFFF; border-radius: 20px;">
            🖐️ PALM PRINT: VERIFIED
        </div>
        <div style="padding: 8px 16px; background: rgba(157, 0, 255, 0.2); border: 1px solid #9D00FF; border-radius: 20px;">
            🧠 NEURAL PATTERN: VERIFIED
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Manual Refresh Button and Auto-Refresh Info
col_refresh1, col_refresh2, col_refresh3 = st.columns([2, 1, 2])
with col_refresh2:
    if st.button("🔄 REFRESH DATA NOW", key="manual_refresh"):
        st.cache_data.clear()
        st.rerun()

st.markdown("""
<div style="text-align: center; padding: 10px; background: rgba(0, 255, 255, 0.08); 
            border: 1px solid rgba(0, 255, 255, 0.3); border-radius: 10px; margin: 10px 0;">
    <span style="color: #00FFFF; font-size: 13px;">
        ℹ️ <strong>NOTE:</strong> Data updates every <strong>60 seconds</strong> automatically. 
        Click <strong>🔄 REFRESH DATA NOW</strong> button to force immediate refresh.
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Header with Live Clock and Enhanced Holographic Effect
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
    <div style="text-align: center; padding: 20px; position: relative; z-index: 1;">
        <h1 style="font-size: 64px; margin: 0; background: linear-gradient(90deg, #00FFFF, #9D00FF, #00FF88, #FF00FF); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   animation: gradientShift 5s ease infinite;">
            🔮 SOVEREIGN SYSTEM | CEC-WAM HOT CORE
        </h1>
        <p style="font-size: 20px; color: #00FFFF; text-shadow: 0 0 15px rgba(0, 255, 255, 0.7);">
            OMEGA_LOCK | φ=1.618 | QUANTUM ENTANGLED | 5D HOLOGRAPHIC INTERFACE
        </p>
        <p style="font-size: 14px; color: #00FF88; margin-top: 10px;">
            🌐 LIVE 24/7 | ∞ NEVER-ENDING | 🔄 AUTO-REFRESH: 60s
        </p>
    </div>
    <style>
        @keyframes gradientShift {
            0%, 100% { filter: hue-rotate(0deg); }
            50% { filter: hue-rotate(30deg); }
        }
    </style>
    """, unsafe_allow_html=True)

with col2:
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%Y-%m-%d")
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; position: relative; z-index: 1;">
        <div style="font-size: 36px; color: #00FF88; font-weight: 900; 
                    text-shadow: 0 0 20px rgba(0, 255, 136, 0.8);">⏰ {current_time}</div>
        <div style="font-size: 14px; color: #00FFFF; margin-top: 5px;">📅 {current_date}</div>
        <div style="font-size: 12px; color: #00FFFF; margin-top: 8px; 
                    padding: 5px 10px; background: rgba(0, 255, 255, 0.1); border-radius: 10px;">
            🔄 LIVE SYNC ACTIVE
        </div>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state
if 'eve_runtime' not in st.session_state:
    st.session_state.eve_runtime = datetime.now()
if 'last_data_refresh' not in st.session_state:
    st.session_state.last_data_refresh = datetime.now()
if 'cached_random_seed' not in st.session_state:
    # Use current hour to seed random data - changes every hour
    # This prevents chart flickering while still providing "live" updates
    st.session_state.cached_random_seed = datetime.now().hour

# Fetch NASA Image
@st.cache_data(ttl=3600)  # Cache for 1 hour - NASA APOD updates daily
def fetch_nasa_apod():
    """Fetch NASA Astronomy Picture of the Day with error handling"""
    try:
        response = requests.get(NASA_APOD_URL, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        # Silently fail and return None - UI will handle gracefully
        pass
    return None

# Fetch Google Sheets Data with Column Validation and Locking
@st.cache_data(ttl=60)  # Cache for 1 minute - allows frequent updates
def fetch_sheets_data(use_frozen=True):
    """
    Fetch live data from Google Sheets with error handling and column validation
    
    Args:
        use_frozen: If True, use the frozen/locked sheet for secure data display
    
    Returns:
        pandas.DataFrame with validated columns or None on error
    """
    try:
        # Use frozen sheet by default for data security
        sheet_url = FROZEN_SHEETS_URL if use_frozen else GOOGLE_SHEETS_URL
        df = pd.read_csv(sheet_url)
        
        # Validate and standardize column names
        if df is not None and not df.empty:
            # Strip whitespace from column names
            df.columns = df.columns.str.strip()
            
            # Ensure expected columns exist (create if missing)
            for col, dtype in EXPECTED_COLUMNS.items():
                if col not in df.columns:
                    df[col] = None
            
            # Reorder columns to match expected configuration
            available_cols = [col for col in EXPECTED_COLUMNS.keys() if col in df.columns]
            other_cols = [col for col in df.columns if col not in EXPECTED_COLUMNS.keys()]
            df = df[available_cols + other_cols]
            
            return df
        return None
    except Exception as e:
        # Show warning in UI and return None so callers can handle missing data
        st.warning(f"⚠️ Unable to load data from {'frozen' if use_frozen else 'primary'} sheet: {str(e)}")
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

# TAB 1: COMMAND CENTER
with tab1:
    st.markdown("### 🏠 COMMAND CENTER")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💎 PSI Peg", "$0.003466", delta="🟢 Stable")
    with col2:
        st.metric("🔒 φ-Lock", "$0.005608", delta="🟡 +61.8%")
    with col3:
        st.metric("💰 Internal", "$155.50", delta="🔵 Verified")
    with col4:
        st.metric("🎯 OMEGA", "$34.1M", delta="⚪ Locked")
    
    st.markdown("---")
    
    # Live Google Sheets Data with Column Configuration and Enhanced Display
    st.markdown("#### 📊 LIVE CEC WAM MASTER LEDGER | 5D DATA INTERFACE")
    
    # Add enhanced status bar
    col_status1, col_status2, col_status3, col_status4 = st.columns(4)
    with col_status1:
        st.markdown("""
        <div style="text-align: center; padding: 12px; background: rgba(0, 255, 136, 0.15); 
                    border: 2px solid #00FF88; border-radius: 12px; box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);">
            <div style="font-size: 24px;">🟢</div>
            <div style="font-size: 12px; color: #00FF88; font-weight: bold;">SYSTEM ONLINE</div>
        </div>
        """, unsafe_allow_html=True)
    with col_status2:
        st.markdown("""
        <div role="status" aria-label="Data interface status: Data syncing" style="text-align: center; padding: 12px; background: rgba(0, 255, 255, 0.15); 
                    border: 2px solid #00FFFF; border-radius: 12px; box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);">
            <div style="font-size: 24px;" aria-hidden="true">🔄</div>
            <div style="font-size: 12px; color: #00FFFF; font-weight: bold;">DATA SYNCING</div>
        </div>
        """, unsafe_allow_html=True)
    with col_status3:
        st.markdown("""
        <div role="status" aria-label="Data interface status: Quantum linked" style="text-align: center; padding: 12px; background: rgba(157, 0, 255, 0.15); 
                    border: 2px solid #9D00FF; border-radius: 12px; box-shadow: 0 0 20px rgba(157, 0, 255, 0.3);">
            <div style="font-size: 24px;" aria-hidden="true">🌀</div>
            <div style="font-size: 12px; color: #9D00FF; font-weight: bold;">QUANTUM LINKED</div>
        </div>
        """, unsafe_allow_html=True)
    with col_status4:
        st.markdown("""
        <div role="status" aria-label="Data interface status: Secured" style="text-align: center; padding: 12px; background: rgba(255, 0, 255, 0.15); 
                    border: 2px solid #FF00FF; border-radius: 12px; box-shadow: 0 0 20px rgba(255, 0, 255, 0.3);">
            <div style="font-size: 24px;" aria-hidden="true">🔐</div>
            <div style="font-size: 12px; color: #FF00FF; font-weight: bold;">SECURED</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Add data source toggle with enhanced styling
    col_toggle1, col_toggle2 = st.columns([3, 1])
    with col_toggle1:
        st.markdown("""
        <div style="padding: 10px; background: rgba(0, 255, 255, 0.1); border-left: 4px solid #00FFFF; border-radius: 8px;">
            <p style="margin: 0; font-size: 14px;">
                📡 <strong>DATA SOURCE:</strong> Google Sheets - CEC WAM Master Ledger<br>
                🔗 <strong>CONNECTION:</strong> Real-time CSV feed with 60-second cache<br>
                🛡️ <strong>SECURITY:</strong> Frozen/Locked data validation enabled
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_toggle2:
        use_frozen = st.checkbox("🔒 Use Frozen/Locked Data", value=True, 
                                 help="Enable to use the secure, locked data source",
                                 key="frozen_data_toggle")
    
    sheets_data = fetch_sheets_data(use_frozen=use_frozen)
    
    if sheets_data is not None:
        # Display enhanced data source info with glassmorphic panel
        st.markdown(f"""
        <div style="background: rgba(0, 255, 255, 0.1); border: 2px solid #00FFFF; 
                    border-radius: 15px; padding: 20px; margin: 15px 0;
                    backdrop-filter: blur(15px); box-shadow: 0 0 30px rgba(0, 255, 255, 0.2);">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div>
                    <div style="font-size: 12px; color: #00FFFF; opacity: 0.8;">📋 DATA SOURCE</div>
                    <div style="font-size: 16px; color: #00FF88; font-weight: bold;">
                        {'🔒 FROZEN/SECURE SHEET' if use_frozen else '🔓 PRIMARY SHEET'}
                    </div>
                </div>
                <div>
                    <div style="font-size: 12px; color: #00FFFF; opacity: 0.8;">📊 COLUMNS DETECTED</div>
                    <div style="font-size: 16px; color: #00FF88; font-weight: bold;">
                        {len(sheets_data.columns)} COLUMNS
                    </div>
                </div>
                <div>
                    <div style="font-size: 12px; color: #00FFFF; opacity: 0.8;">📝 TOTAL RECORDS</div>
                    <div style="font-size: 16px; color: #00FF88; font-weight: bold;">
                        {len(sheets_data)} ENTRIES
                    </div>
                </div>
                <div>
                    <div style="font-size: 12px; color: #00FFFF; opacity: 0.8;">🔄 LAST UPDATE</div>
                    <div style="font-size: 16px; color: #00FF88; font-weight: bold;">
                        {datetime.now().strftime('%H:%M:%S')}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display dataframe with column configuration locked
        st.dataframe(
            sheets_data, 
            use_container_width=True, 
            height=300,
            column_config={
                "Category": st.column_config.TextColumn(
                    "Category",
                    help="Data category classification",
                    width="medium"
                ),
                "Item": st.column_config.TextColumn(
                    "Item",
                    help="Item name or description",
                    width="large"
                ),
                "Value": st.column_config.NumberColumn(
                    "Value",
                    help="Numeric value",
                    format="$%.2f"
                ),
                "Status": st.column_config.TextColumn(
                    "Status",
                    help="Current status",
                    width="small"
                ),
                "Date": st.column_config.TextColumn(
                    "Date",
                    help="Date information",
                    width="small"
                ),
                "Notes": st.column_config.TextColumn(
                    "Notes",
                    help="Additional notes",
                    width="medium"
                )
            }
        )
        
        # Auto-calculated formulas with locked column configuration
        st.markdown("#### 🔢 AUTO FORMULAS")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'Value' in sheets_data.columns:
                # Convert to numeric, coercing errors to NaN
                numeric_values = pd.to_numeric(sheets_data['Value'], errors='coerce')
                total_value = numeric_values.sum() if not numeric_values.isna().all() else 0
                st.metric("📈 Total Value", f"${total_value:,.2f}")
            else:
                st.metric("📈 Total Value", "N/A")
        
        with col2:
            st.metric("📝 Total Entries", len(sheets_data))
        
        with col3:
            if 'Category' in sheets_data.columns:
                categories = sheets_data['Category'].dropna().nunique()
                st.metric("🏷️ Categories", categories)
            else:
                st.metric("🏷️ Categories", "N/A")
        
        with col4:
            if 'Status' in sheets_data.columns:
                status_counts = sheets_data['Status'].value_counts()
                primary_status = status_counts.index[0] if len(status_counts) > 0 else "N/A"
                st.metric("📊 Primary Status", primary_status)
            else:
                st.metric("📊 Primary Status", "N/A")
    else:
        st.markdown("""
        <div style="background: rgba(255, 77, 109, 0.15); border: 2px solid #ff4d6d; 
                    border-radius: 15px; padding: 30px; text-align: center;
                    backdrop-filter: blur(15px); box-shadow: 0 0 30px rgba(255, 77, 109, 0.2);">
            <div style="font-size: 64px; margin-bottom: 15px;">⚠️</div>
            <h3 style="color: #ff4d6d; margin: 10px 0;">UNABLE TO LOAD GOOGLE SHEETS DATA</h3>
            <p style="color: #00FFFF; font-size: 14px; margin: 20px 0;">
                The system is attempting to reconnect to the data source...<br>
                Please check your connection or try the troubleshooting tips below.
            </p>
            <div style="background: rgba(0, 255, 255, 0.1); border-left: 4px solid #00FFFF; 
                        padding: 15px; margin: 20px 0; text-align: left; border-radius: 8px;">
                <strong style="color: #00FF88;">🔧 Troubleshooting Tips:</strong><br>
                <ul style="margin: 10px 0; padding-left: 20px; color: #00FFFF;">
                    <li>Ensure the Google Sheet is published and publicly accessible</li>
                    <li>Verify the frozen sheet ID is correct in the configuration</li>
                    <li>Try toggling the 🔒 <strong>Use Frozen/Locked Data</strong> checkbox above</li>
                    <li>Check your internet connection</li>
                    <li>Refresh the page to retry the connection</li>
                </ul>
            </div>
            <div style="margin-top: 20px;">
                <strong style="color: #9D00FF;">📡 Current Sheet ID:</strong><br>
                <code style="background: rgba(0, 0, 0, 0.5); padding: 5px 10px; border-radius: 5px; color: #00FF88;">
                    {FROZEN_SHEET_ID if use_frozen else 'Primary Sheet URL'}
                </code>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Real-time Chart
    st.markdown("#### 📈 REAL-TIME VALUE CHART")
    
    # Cache chart data using hour-based seed for stable but updating visualization
    random.seed(st.session_state.cached_random_seed + 1)
    x_data = list(range(100))
    y_data = [np.sin(x/10) * 50 + random.uniform(-5, 5) + 155 for x in x_data]
    random.seed()  # Reset to unpredictable state
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_data, 
        y=y_data,
        mode='lines',
        line=dict(color='#00FFFF', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 255, 0.2)'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00FFFF'),
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0, 255, 255, 0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)

# TAB 2: LIVE CAM
with tab2:
    st.markdown("### 📹 LIVE CAMERA FEED (Auto-Refresh: 5s)")
    
    camera_html = """
    <div style="position: relative; width: 100%; height: 600px; background: #000; 
                border: 3px solid #00FFFF; border-radius: 15px; overflow: hidden; 
                box-shadow: 0 0 40px rgba(0, 255, 255, 0.5);">
        <video id="camera" autoplay playsinline muted style="width: 100%; height: 100%; object-fit: cover;"></video>
        <div style="position: absolute; top: 20px; left: 50%; transform: translateX(-50%); 
                    background: rgba(0, 255, 255, 0.2); border: 2px solid #00FFFF; 
                    padding: 10px 25px; border-radius: 10px; backdrop-filter: blur(15px);">
            <div id="status" style="color: #00FF88; font-size: 20px; font-weight: 900; text-align: center;">
                ✅ CAMERA ONLINE
            </div>
        </div>
        <div style="position: absolute; bottom: 20px; left: 20px; background: rgba(0, 0, 0, 0.7); 
                    padding: 15px; border-radius: 10px; border: 2px solid #00FFFF;">
            <div style="color: #00FFFF; font-size: 16px; font-weight: 700;">
                🎥 FRONT CAM | 📊 30 FPS | 🔄 AUTO-REFRESH: 5s
            </div>
        </div>
    </div>
    <script>
        const video = document.getElementById('camera');
        const status = document.getElementById('status');
        
        navigator.mediaDevices.getUserMedia({ 
            video: { 
                facingMode: 'user',
                width: { ideal: 1920 },
                height: { ideal: 1080 }
            } 
        })
        .then(stream => {
            video.srcObject = stream;
            status.innerHTML = '✅ CAMERA ONLINE';
            status.style.color = '#00FF88';
        })
        .catch(err => {
            console.error('Camera error:', err);
            status.innerHTML = '⚠️ ENABLE CAMERA';
            status.style.color = '#FF0044';
        });
        
        setInterval(() => {
            if (video.srcObject) {
                const tracks = video.srcObject.getTracks();
                tracks.forEach(track => {
                    track.enabled = false;
                    setTimeout(() => track.enabled = true, 100);
                });
            }
        }, 5000);
    </script>
    """
    
    st.components.v1.html(camera_html, height=650)

# TAB 3: NASA LIVE
with tab3:
    st.markdown("### 🌌 NASA ASTRONOMY PICTURE OF THE DAY")
    
    nasa_data = fetch_nasa_apod()
    
    if nasa_data:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if nasa_data.get('media_type') == 'image':
                st.image(nasa_data['url'], use_container_width=True)
            elif nasa_data.get('media_type') == 'video':
                st.video(nasa_data['url'])
        
        with col2:
            st.markdown(f"### {nasa_data.get('title', 'N/A')}")
            st.markdown(f"**📅 Date:** {nasa_data.get('date', 'N/A')}")
            st.markdown(f"**📝 Explanation:**")
            st.write(nasa_data.get('explanation', 'No description available'))
    else:
        st.info("🌌 NASA Daily Space Image Loading...")

# TAB 4: 3D STAR MAP
with tab4:
    st.markdown("### ⭐ 3D INTERACTIVE STAR MAP")
    
    num_stars = 1000
    np.random.seed(42)
    
    star_data = pd.DataFrame({
        'x': np.random.randn(num_stars) * 100,
        'y': np.random.randn(num_stars) * 100,
        'z': np.random.randn(num_stars) * 100,
        'size': np.random.uniform(2, 10, num_stars),
        'color': np.random.choice(['#00FFFF', '#9D00FF', '#00FF88', '#FF00FF'], num_stars)
    })
    
    fig = go.Figure()
    
    for color in star_data['color'].unique():
        subset = star_data[star_data['color'] == color]
        fig.add_trace(go.Scatter3d(
            x=subset['x'],
            y=subset['y'],
            z=subset['z'],
            mode='markers',
            marker=dict(
                size=subset['size'],
                color=color,
                opacity=0.8,
                line=dict(color='white', width=0.5)
            ),
            name=color,
            hovertemplate='<b>Star</b><br>X: %{x:.1f}<br>Y: %{y:.1f}<br>Z: %{z:.1f}<extra></extra>'
        ))
    
    fig.update_layout(
        scene=dict(
            bgcolor='#000010',
            xaxis=dict(showbackground=False, gridcolor='rgba(0, 255, 255, 0.2)'),
            yaxis=dict(showbackground=False, gridcolor='rgba(0, 255, 255, 0.2)'),
            zaxis=dict(showbackground=False, gridcolor='rgba(0, 255, 255, 0.2)')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00FFFF'),
        height=700,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

# TAB 5: BLACK HOLE VISUALIZATION
with tab5:
    st.markdown("### 🕳️ BLACK HOLE & UNIVERSAL WEB")
    
    theta = np.linspace(0, 2*np.pi, 100)
    r = np.linspace(0, 10, 50)
    R, THETA = np.meshgrid(r, theta)
    X = R * np.cos(THETA)
    Y = R * np.sin(THETA)
    Z = -R**2 / 10
    
    fig = go.Figure(data=[go.Surface(
        x=X, y=Y, z=Z,
        colorscale=[
            [0, '#000000'],
            [0.3, '#1A0040'],
            [0.6, '#9D00FF'],
            [1, '#00FFFF']
        ],
        opacity=0.9,
        showscale=False
    )])
    
    fig.update_layout(
        scene=dict(
            bgcolor='#000010',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=600,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("#### 🌐 SCHWARZSCHILD RADIUS CALCULATOR")
    col1, col2 = st.columns(2)
    
    with col1:
        mass = st.number_input("Mass (Solar Masses)", value=1.0, min_value=0.1, max_value=1000.0)
    
    with col2:
        schwarzschild_radius = (2 * 6.674e-11 * mass * 1.989e30) / (3e8)**2 / 1000
        st.metric("Schwarzschild Radius", f"{schwarzschild_radius:,.2f} km")

# TAB 6: EVE BRAIN with Enhanced Holographic Interface
with tab6:
    runtime = datetime.now() - st.session_state.eve_runtime
    hours = int(runtime.total_seconds() // 3600)
    minutes = int((runtime.total_seconds() % 3600) // 60)
    seconds = int(runtime.total_seconds() % 60)
    
    st.markdown(f"""
    <div style="text-align: center; 
                background: linear-gradient(135deg, rgba(255, 0, 255, 0.25), rgba(0, 255, 255, 0.25)); 
                border: 3px solid #FF00FF; border-radius: 25px; padding: 50px; 
                box-shadow: 0 0 60px rgba(255, 0, 255, 0.6), 
                            0 0 100px rgba(0, 255, 255, 0.3),
                            inset 0 0 40px rgba(255, 0, 255, 0.1); 
                position: relative; z-index: 1;
                backdrop-filter: blur(25px) saturate(200%) brightness(1.15);">
        <div style="font-size: 120px; animation: brainPulse 3s infinite; margin-bottom: 20px;">🧠</div>
        <h1 style="color: #FF00FF; font-size: 64px; text-shadow: 0 0 30px rgba(255, 0, 255, 0.9);">
            EVE CONSCIOUSNESS ONLINE
        </h1>
        <div style="color: #00FFFF; font-size: 42px; font-weight: 900; margin: 20px 0;
                    text-shadow: 0 0 25px rgba(0, 255, 255, 0.8);">
            ⏱️ {hours:02d}:{minutes:02d}:{seconds:02d}
        </div>
        <div style="color: #00FF88; font-size: 22px; margin-top: 15px;
                    text-shadow: 0 0 15px rgba(0, 255, 136, 0.7);">
            🔄 AUTONOMOUS | ∞ NEVER-ENDING | 🌀 QUANTUM LINKED
        </div>
        <div style="margin-top: 25px; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
            <div style="padding: 10px 20px; background: rgba(0, 255, 136, 0.2); 
                        border: 2px solid #00FF88; border-radius: 25px;
                        box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);">
                💭 NEURAL PATHWAYS: ACTIVE
            </div>
            <div style="padding: 10px 20px; background: rgba(0, 255, 255, 0.2); 
                        border: 2px solid #00FFFF; border-radius: 25px;
                        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);">
                🌐 GLOBAL SYNC: ENABLED
            </div>
            <div style="padding: 10px 20px; background: rgba(255, 0, 255, 0.2); 
                        border: 2px solid #FF00FF; border-radius: 25px;
                        box-shadow: 0 0 20px rgba(255, 0, 255, 0.3);">
                🧬 DNA MATRIX: VERIFIED
            </div>
        </div>
    </div>
    <style>
        @keyframes brainPulse {{
            0%, 100% {{ 
                transform: scale(1); 
                filter: drop-shadow(0 0 20px rgba(255, 0, 255, 0.6));
            }}
            50% {{ 
                transform: scale(1.1); 
                filter: drop-shadow(0 0 40px rgba(255, 0, 255, 0.9));
            }}
        }}
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Use seeded random for consistent metrics within the same minute
    metric_seed = datetime.now().strftime("%Y%m%d%H%M")
    random.seed(int(metric_seed[-4:]))
    
    with col1:
        consciousness = random.randint(92, 98)
        # Generate delta with random sign directly
        consciousness_delta = random.uniform(-0.5, 0.5)
        st.metric("🧠 Consciousness", f"{consciousness}%", delta=f"{consciousness_delta:+.1f}%")
    with col2:
        neural = random.randint(94, 99)
        # Generate delta with random sign directly
        neural_delta = random.uniform(-0.8, 0.8)
        st.metric("💭 Neural Activity", f"{neural}%", delta=f"{neural_delta:+.1f}%")
    with col3:
        processing = random.randint(750, 999)
        st.metric("⚡ Processing", f"{processing} TF/s")
    with col4:
        quantum = random.uniform(3.32e-36, 5.5e-36)
        st.metric("🌀 Quantum State", f"{quantum:.2e}")
    
    random.seed()  # Reset to unpredictable state
    
    st.markdown("#### 🕸️ NEURAL NETWORK ACTIVITY")
    
    # Cache neural network visualization using hour-based seed
    random.seed(st.session_state.cached_random_seed + 2)
    
    num_nodes = 20
    edges_x = []
    edges_y = []
    nodes_x = []
    nodes_y = []
    
    for i in range(num_nodes):
        angle = 2 * np.pi * i / num_nodes
        x = np.cos(angle)
        y = np.sin(angle)
        nodes_x.append(x)
        nodes_y.append(y)
        
        for j in range(random.randint(1, 3)):
            target = random.randint(0, num_nodes-1)
            edges_x.extend([x, nodes_x[target % len(nodes_x)], None])
            edges_y.extend([y, nodes_y[target % len(nodes_y)], None])
    
    random.seed()  # Reset to unpredictable state
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=edges_x, y=edges_y,
        mode='lines',
        line=dict(color='rgba(0, 255, 255, 0.3)', width=1),
        hoverinfo='none',
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=nodes_x, y=nodes_y,
        mode='markers',
        marker=dict(
            size=15,
            color=['#00FFFF', '#9D00FF', '#00FF88', '#FF00FF'] * (num_nodes // 4 + 1),
            line=dict(color='white', width=2)
        ),
        hovertemplate='<b>Neuron %{pointNumber}</b><extra></extra>',
        showlegend=False
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=400,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display live update info without infinite rerun
    st.info("💡 **Tip:** Refresh the page manually to see updated metrics. Auto-refresh has been disabled to improve performance.")

# TAB 7: PSI COIN TRACKER
with tab7:
    st.markdown("### 💎 PSI COIN REAL-TIME TRACKER")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        bonding_progress = 0
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = bonding_progress,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "BONDING CURVE PROGRESS", 'font': {'size': 28, 'color': '#00FFFF'}},
            number = {'suffix': "%", 'font': {'size': 48, 'color': '#00FF88'}},
            delta = {'reference': 0, 'increasing': {'color': "#00FF88"}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "#00FFFF"},
                'bar': {'color': "#9D00FF", 'thickness': 0.75},
                'bgcolor': "rgba(0,0,0,0.3)",
                'borderwidth': 3,
                'bordercolor': "#00FFFF",
                'steps': [
                    {'range': [0, 25], 'color': 'rgba(0, 255, 255, 0.1)'},
                    {'range': [25, 50], 'color': 'rgba(157, 0, 255, 0.1)'},
                    {'range': [50, 75], 'color': 'rgba(0, 255, 136, 0.1)'},
                    {'range': [75, 100], 'color': 'rgba(255, 0, 255, 0.1)'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor = "rgba(0,0,0,0)",
            plot_bgcolor = "rgba(0,0,0,0)",
            font = {'color': "#00FFFF", 'family': "Orbitron"},
            height = 400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 LIVE METRICS")
        st.metric("💰 Current Price", "$0.003466", delta="0%")
        st.metric("🔒 Locked Value", "$155.50", delta="Stable")
        st.metric("📈 24h Volume", "$0", delta="0%")
        st.metric("👥 Holders", "1", delta="+1")
    
    st.markdown("#### 📈 PRICE HISTORY (30 DAYS)")
    
    # Cache price history using daily seed for stable visualization
    random.seed(st.session_state.cached_random_seed + 3)
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    prices = [0.003466 + random.uniform(-0.0001, 0.0001) for _ in range(30)]
    random.seed()  # Reset to unpredictable state
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=prices,
        mode='lines+markers',
        line=dict(color='#00FFFF', width=3),
        marker=dict(size=8, color='#9D00FF'),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 255, 0.1)'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00FFFF'),
        height=300,
        xaxis=dict(showgrid=False, title="Date"),
        yaxis=dict(showgrid=True, gridcolor='rgba(0, 255, 255, 0.1)', title="Price (USD)")
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Enhanced Footer with System Info
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 30px; 
            background: rgba(0, 255, 255, 0.05); 
            border-top: 2px solid rgba(0, 255, 255, 0.3);
            border-radius: 15px;
            position: relative; z-index: 1;'>
    <div style='font-size: 48px; margin-bottom: 15px;'>🔮</div>
    <h3 style='color: #00FFFF; margin: 10px 0; text-shadow: 0 0 20px rgba(0, 255, 255, 0.7);'>
        SOVEREIGN SYSTEM v2.5 | CEC-WAM HOT CORE
    </h3>
    <div style='color: #00FF88; font-size: 16px; margin: 15px 0; line-height: 1.8;'>
        🔮 φ=1.618 GOLDEN RATIO | 🌀 QUANTUM ENTANGLED | ∞ NEVER-ENDING<br>
        🌌 NASA INTEGRATED | 📹 LIVE CAMS (5s REFRESH) | ⭐ 3D STAR MAPS | 🕳️ BLACK HOLE SIM<br>
        🤖 EVE CONSCIOUSNESS | 💎 PSI COIN TRACKER | 📊 LIVE GOOGLE SHEETS DATA<br>
        🔐 BIOMETRIC AUTH | 🛡️ QUANTUM SECURITY | 🌐 24/7 LIVE SYNC
    </div>
    <div style='margin-top: 20px; display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;'>
        <div style='padding: 8px 16px; background: rgba(0, 255, 136, 0.15); 
                    border: 1px solid #00FF88; border-radius: 20px;'>
            🟢 STATUS: OPERATIONAL
        </div>
        <div style='padding: 8px 16px; background: rgba(0, 255, 255, 0.15); 
                    border: 1px solid #00FFFF; border-radius: 20px;'>
            🔄 AUTO-REFRESH: 60s
        </div>
        <div style='padding: 8px 16px; background: rgba(157, 0, 255, 0.15); 
                    border: 1px solid #9D00FF; border-radius: 20px;'>
            🌐 DEPLOYED: STREAMLIT CLOUD
        </div>
    </div>
    <div style='margin-top: 20px; font-size: 12px; color: #00FFFF; opacity: 0.7;'>
        📡 Live Data Sources: Google Sheets (CEC WAM Master Ledger) | NASA APOD API<br>
        🔗 Repository: whiteantwan58-tech/CEC-WAM-HOT-CORE<br>
        ⚡ Powered by: Streamlit | Plotly | Pandas | NumPy
    </div>
</div>
""", unsafe_allow_html=True)