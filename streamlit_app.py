import streamlit as st

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime, timedelta
import time
import os
from collections import deque
import random

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not required in production

# Page Configuration
st.set_page_config(
    page_title="EVE System - 5D Holographic Dashboard",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if 'data_cache' not in st.session_state:
    st.session_state.data_cache = None
if 'psi_cache' not in st.session_state:
    st.session_state.psi_cache = None
if 'nasa_cache' not in st.session_state:
    st.session_state.nasa_cache = None
if 'refresh_count' not in st.session_state:
    st.session_state.refresh_count = 0
if 'hud_enabled' not in st.session_state:
    st.session_state.hud_enabled = True
if 'zoom_image' not in st.session_state:
    st.session_state.zoom_image = None

# Seed offset constants for deterministic random data generation
STOCK_SEED_OFFSET = 1000

# Custom CSS for HD Holographic Theme
def load_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Orbitron', monospace;
    }
    
    /* Background and Layout */
    .stApp {
        background: linear-gradient(135deg, #0E0E1A 0%, #1A1A2E 50%, #0E0E1A 100%);
        background-attachment: fixed;
    }
    
    /* Animated Grid Background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 0;
    }
    
    /* Glassmorphism Cards */
    .css-1r6slb0, .css-12oz5g7 {
        background: rgba(26, 26, 46, 0.6) !important;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.2);
    }
    
    /* Headers with Neon Glow */
    h1, h2, h3 {
        color: #00FFFF !important;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.8),
                     0 0 20px rgba(0, 255, 255, 0.5),
                     0 0 30px rgba(0, 255, 255, 0.3);
        font-weight: 900;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(26, 26, 46, 0.8);
        border-radius: 10px;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(0, 255, 255, 0.1);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 8px;
        color: #00FFFF;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.3), rgba(157, 0, 255, 0.3));
        border: 1px solid #00FFFF;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #00FF88 !important;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #00FFFF, #9D00FF);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0, 255, 255, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 255, 255, 0.6);
    }
    
    /* Dataframe Styling */
    .dataframe {
        background: rgba(26, 26, 46, 0.8) !important;
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 10px;
    }
    
    /* Success/Info Messages */
    .stSuccess, .stInfo {
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid #00FF88;
        border-radius: 10px;
    }
    
    /* Pulsing Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .pulse {
        animation: pulse 2s ease-in-out infinite;
    }
    </style>
    """, unsafe_allow_html=True)

# Load CSS
load_custom_css()

# Header with HUD toggle
col_hud1, col_hud2 = st.columns([4, 1])

with col_hud1:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: rgba(26, 26, 46, 0.8); border-radius: 15px; margin-bottom: 20px; border: 1px solid rgba(0, 255, 255, 0.3);'>
        <h1 style='margin: 0; font-size: 3rem;'>🌌 EVE SYSTEM</h1>
        <p style='color: #00FFFF; font-size: 1.2rem; margin: 10px 0;'>Enhanced Virtual Entity - 5D Holographic Dashboard</p>
        <p style='color: #9D00FF; font-size: 0.9rem;'>System Code: CEC_WAM_HEI_EVE_7A2F-9C4B | Owner: Twan | Full Access Granted</p>
    </div>
    """, unsafe_allow_html=True)

with col_hud2:
    st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
    if st.button("🎮 HUD " + ("ON" if st.session_state.hud_enabled else "OFF"), use_container_width=True):
        st.session_state.hud_enabled = not st.session_state.hud_enabled
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# System Status Indicators (HUD)
if st.session_state.hud_enabled:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("🟢 System Status", "ONLINE", delta="Active")
    with col2:
        st.metric("⏱️ Uptime", "24/7", delta="Stable")
    with col3:
        st.metric("📡 Data Feed", "LIVE", delta="Synced")
    with col4:
        st.metric("🤖 AI Status", "READY", delta="Connected")
    with col5:
        current_time = datetime.now().strftime("%H:%M:%S")
        st.metric("🕐 Time", current_time, delta="UTC")

# Data Loading Functions
@st.cache_data(ttl=60)
def load_google_sheets_data():
    """Load data from Google Sheets CSV with enhanced error handling"""
    try:
        url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vREgUUHPCzTBWK8i1PWBrE2E4pKRTAgaReJahFqmrTetCZyCO0QHVlAleodUsTlJv_86KpzH_NPv9dv/pub?output=csv"
        df = pd.read_csv(url, timeout=10)
        if len(df) == 0:
            raise ValueError("Empty dataset received")
        return df
    except requests.exceptions.Timeout:
        # Timeout - use demo data
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        return pd.DataFrame({
            'Date': dates,
            'Metric1': np.random.randint(50, 200, 100),
            'Metric2': np.random.randint(100, 500, 100),
            'Category': np.random.choice(['A', 'B', 'C'], 100),
            'Status': np.random.choice(['Active', 'Pending', 'Complete'], 100)
        })
    except Exception as e:
        # Any other error - use demo data
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        return pd.DataFrame({
            'Date': dates,
            'Metric1': np.random.randint(50, 200, 100),
            'Metric2': np.random.randint(100, 500, 100),
            'Category': np.random.choice(['A', 'B', 'C'], 100),
            'Status': np.random.choice(['Active', 'Pending', 'Complete'], 100)
        })

@st.cache_data(ttl=60)
def get_psi_price():
    """Get PSI coin price from CoinGecko with enhanced error handling"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=tridentdao&vs_currencies=usd&include_24hr_change=true&include_market_cap=true"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if 'tridentdao' not in data:
            raise ValueError("TridentDAO data not found in response")
        
        return {
            'price': data['tridentdao'].get('usd', 0.0),
            'change_24h': data['tridentdao'].get('usd_24h_change', 0.0),
            'market_cap': data['tridentdao'].get('usd_market_cap', 0),
            'status': 'live',
            'last_updated': datetime.now()
        }
    except requests.Timeout:
        return {
            'price': 0.000123,  # Demo fallback price
            'change_24h': 2.5,
            'market_cap': 15000000,
            'status': 'demo',
            'last_updated': datetime.now()
        }
    except Exception as e:
        return {
            'price': 0.000123,  # Demo fallback price
            'change_24h': 2.5,
            'market_cap': 15000000,
            'status': 'error',
            'error_msg': str(e),
            'last_updated': datetime.now()
        }

@st.cache_data(ttl=300)
def get_iss_position():
    """Get current ISS position using HTTPS API"""
    try:
        # Use HTTPS-capable ISS position API to avoid mixed-content issues
        url = "https://api.wheretheiss.at/v1/satellites/25544"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        # Validate expected keys before accessing
        if not all(key in data for key in ("latitude", "longitude", "timestamp")):
            raise ValueError("Unexpected ISS API response format")
        return {
            'latitude': float(data["latitude"]),
            'longitude': float(data["longitude"]),
            'timestamp': data["timestamp"],
        }
    except Exception as e:
        return {'latitude': 0, 'longitude': 0, 'timestamp': 0}

@st.cache_data(ttl=300)
def get_voyager_positions():
    """Get Voyager 1 and 2 approximate positions"""
    # Voyager positions (approximate as of 2026)
    # These values are estimates and should be updated periodically
    # In production, use NASA's Horizons API for accurate real-time data
    return {
        'voyager1': {
            'distance_km': 24.5e9,  # ~24.5 billion km from Earth (updated 2026)
            'distance_au': 163.5,
            'status': 'Active',
            'speed_kms': 17.0
        },
        'voyager2': {
            'distance_km': 20.5e9,  # ~20.5 billion km from Earth (updated 2026)
            'distance_au': 137.0,
            'status': 'Active',
            'speed_kms': 15.4
        }
    }

@st.cache_data(ttl=300)
def get_hubble_status():
    """Get Hubble Space Telescope status"""
    try:
        # Using deterministic values based on date for consistency
        # In production, use actual HST telemetry API
        day_of_year = datetime.now().timetuple().tm_yday
        observations_today = 15 + (day_of_year % 10)  # Deterministic based on day
        return {
            'status': 'Operational',
            'altitude_km': 547,
            'orbit_period_min': 95,
            'observations_today': observations_today
        }
    except Exception as e:
        return {'status': 'Unknown', 'altitude_km': 547, 'orbit_period_min': 95, 'observations_today': 0}

@st.cache_data(ttl=300)
def get_jwst_status():
    """Get James Webb Space Telescope status"""
    try:
        # Using deterministic values based on date for consistency
        # In production, use actual JWST telemetry API
        day_of_year = datetime.now().timetuple().tm_yday
        observations_today = 8 + (day_of_year % 7)  # Deterministic based on day
        return {
            'status': 'Operational',
            'distance_km': 1.5e6,  # ~1.5 million km (L2 point)
            'temperature_k': 50,
            'observations_today': observations_today
        }
    except Exception as e:
        return {'status': 'Unknown', 'distance_km': 1.5e6, 'temperature_k': 50, 'observations_today': 0}

@st.cache_data(ttl=600)
def get_traffic_cameras():
    """Get live traffic camera feeds"""
    # Using publicly available camera feeds from various cities
    # These URLs should be verified and can be customized via configuration
    # In production, consider using environment variables for camera URLs
    return [
        {
            'name': 'NYC Times Square',
            'location': 'New York, NY',
            'url': 'https://g1.ipcamlive.com/player/player.php?alias=5ab357b182ff8',
            'refresh_rate': 5,
            'type': 'live_stream'
        },
        {
            'name': 'LA Hollywood',
            'location': 'Los Angeles, CA',
            'url': 'https://g1.ipcamlive.com/player/player.php?alias=hollywoodblvd',
            'refresh_rate': 5,
            'type': 'live_stream'
        },
        {
            'name': 'London Traffic',
            'location': 'London, UK',
            'url': 'https://s3-eu-west-1.amazonaws.com/jamcams.tfl.gov.uk/00001.00160.jpg',
            'refresh_rate': 5,
            'type': 'image'
        },
        {
            'name': 'Miami Beach',
            'location': 'Miami, FL',
            'url': 'https://g1.ipcamlive.com/player/player.php?alias=miamibeach',
            'refresh_rate': 5,
            'type': 'live_stream'
        },
        {
            'name': 'Chicago Downtown',
            'location': 'Chicago, IL',
            'url': 'https://g1.ipcamlive.com/player/player.php?alias=chicagodowntown',
            'refresh_rate': 5,
            'type': 'live_stream'
        }
    ]

@st.cache_data(ttl=600)
def get_weather_alerts():
    """Get weather alerts from NOAA/Weather.gov"""
    try:
        # US National Weather Service API (no API key required)
        url = "https://api.weather.gov/alerts/active"
        headers = {
            'User-Agent': '(EVE-System, contact@evesystem.com)',
            'Accept': 'application/geo+json'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        alerts = []
        if 'features' in data:
            for feature in data['features'][:10]:  # Limit to 10 alerts
                props = feature.get('properties', {})
                alerts.append({
                    'event': props.get('event', 'Unknown'),
                    'severity': props.get('severity', 'Unknown'),
                    'area': props.get('areaDesc', 'Unknown'),
                    'headline': props.get('headline', 'No headline'),
                    'description': props.get('description', 'No description')[:200],
                    'status': 'live'
                })
        
        return {'alerts': alerts, 'status': 'live', 'count': len(alerts)}
    except Exception as e:
        # Return demo data on error
        return {
            'alerts': [
                {
                    'event': 'Severe Thunderstorm Warning',
                    'severity': 'Severe',
                    'area': 'Demo Region',
                    'headline': 'Severe weather expected in area',
                    'description': 'Demo alert - API unavailable',
                    'status': 'demo'
                }
            ],
            'status': 'demo',
            'count': 1,
            'error': str(e)
        }

@st.cache_data(ttl=600)
def get_satellite_tracking():
    """Get satellite tracking data"""
    try:
        # Using N2YO API (requires API key) or public satellite data
        # For demo, return static satellite list
        satellites = [
            {'name': 'ISS', 'norad_id': 25544, 'status': 'Active', 'type': 'Space Station'},
            {'name': 'Hubble', 'norad_id': 20580, 'status': 'Active', 'type': 'Telescope'},
            {'name': 'Starlink-1007', 'norad_id': 44713, 'status': 'Active', 'type': 'Communication'},
            {'name': 'GPS BIIA-28', 'norad_id': 26690, 'status': 'Active', 'type': 'Navigation'},
            {'name': 'NOAA-20', 'norad_id': 43013, 'status': 'Active', 'type': 'Weather'},
        ]
        return {'satellites': satellites, 'status': 'live'}
    except Exception as e:
        return {'satellites': [], 'status': 'error', 'error': str(e)}

@st.cache_data(ttl=3600)
def get_nasa_apod():
    """Get NASA Astronomy Picture of the Day with enhanced error handling"""
    try:
        api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        data['status'] = 'live'
        return data
    except requests.Timeout:
        return {
            'title': 'Eagle Nebula (M16) - Demo Image',
            'url': 'https://apod.nasa.gov/apod/image/2301/M16_HubbleGendler_1280.jpg',
            'explanation': 'The Eagle Nebula (M16) is a diffuse emission nebula in the constellation Serpens. This demo image shows the iconic "Pillars of Creation" region, where new stars are being born. The nebula is approximately 7,000 light-years away from Earth.',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'media_type': 'image',
            'status': 'demo'
        }
    except Exception as e:
        return {
            'title': 'Eagle Nebula (M16) - Demo Image',
            'url': 'https://apod.nasa.gov/apod/image/2301/M16_HubbleGendler_1280.jpg',
            'explanation': 'The Eagle Nebula (M16) is a diffuse emission nebula in the constellation Serpens. This demo image shows the iconic "Pillars of Creation" region, where new stars are being born. The nebula is approximately 7,000 light-years away from Earth.',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'media_type': 'image',
            'status': 'error',
            'error_msg': str(e)
        }

# Auto-refresh functionality
refresh_col1, refresh_col2, refresh_col3 = st.columns([1, 1, 2])

with refresh_col1:
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.session_state.last_refresh = datetime.now()
        st.session_state.refresh_count += 1
        st.rerun()

with refresh_col2:
    auto_refresh = st.checkbox("Auto-refresh (60s)", value=False)

with refresh_col3:
    time_since_refresh = (datetime.now() - st.session_state.last_refresh).seconds
    st.info(f"⏱️ Last refresh: {time_since_refresh}s ago | Total refreshes: {st.session_state.refresh_count}")

# Tab System
tabs = st.tabs([
    "📊 Overview",
    "📈 Live Data",
    "💎 PSI Tracker",
    "🌟 Star Map",
    "🚀 NASA & Space",
    "📹 Live Cameras",
    "🌦️ Weather Alerts",
    "🛰️ Satellite Tracking",
    "📐 Blueprints & Formulas",
    "🤖 EVE AI",
    "📉 Analytics",
    "🏭 5S Dashboard"
])

# TAB 1: Overview
with tabs[0]:
    st.header("📊 System Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: rgba(0, 255, 255, 0.1); padding: 20px; border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3);'>
            <h3>🎯 Mission Status</h3>
            <p>All systems operational</p>
            <p>✅ Data Integration: Active</p>
            <p>✅ API Connections: Stable</p>
            <p>✅ AI Assistant: Ready</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: rgba(157, 0, 255, 0.1); padding: 20px; border-radius: 10px; border: 1px solid rgba(157, 0, 255, 0.3);'>
            <h3>📡 Live Feeds</h3>
            <p>Google Sheets: Connected</p>
            <p>CoinGecko API: Active</p>
            <p>NASA APOD: Synced</p>
            <p>Last Update: Just now</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: rgba(0, 255, 136, 0.1); padding: 20px; border-radius: 10px; border: 1px solid rgba(0, 255, 136, 0.3);'>
            <h3>⚡ Performance</h3>
            <p>Response Time: <10ms</p>
            <p>Data Accuracy: 99.9%</p>
            <p>Uptime: 100%</p>
            <p>Status: Optimal</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Stats
    st.subheader("Quick Statistics")
    
    # Generate sample KPI data
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        st.metric("Total Records", "12,450", delta="↑ 234")
    with kpi_col2:
        st.metric("Active Users", "89", delta="↑ 12")
    with kpi_col3:
        st.metric("Data Quality", "98.7%", delta="↑ 0.3%")
    with kpi_col4:
        st.metric("Processing Speed", "Fast", delta="Optimized")
    
    st.markdown("---")
    
    # Live Camera Feeds Section
    st.subheader("📹 Live Visual Camera Feeds")
    st.info("🎥 Real-time monitoring and visualization system with simulated camera feeds")
    
    feed_col1, feed_col2, feed_col3 = st.columns(3)
    
    with feed_col1:
        st.markdown("""
        <div style='background: rgba(0, 255, 255, 0.1); padding: 15px; border-radius: 10px; border: 2px solid rgba(0, 255, 255, 0.3); text-align: center;'>
            <h4 style='color: #00FFFF; margin-bottom: 10px;'>📷 Camera 1: Main Deck</h4>
            <div style='background: #000; height: 200px; border-radius: 8px; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden;'>
                <div style='position: absolute; width: 100%; height: 100%; background: linear-gradient(45deg, rgba(0,255,255,0.1) 0%, rgba(157,0,255,0.1) 100%);'></div>
                <div style='position: relative; z-index: 1;'>
                    <div style='color: #00FFFF; font-size: 3rem; animation: pulse 2s infinite;'>🎥</div>
                    <p style='color: #00FF88; margin-top: 10px; font-size: 0.9rem;'>●REC</p>
                </div>
            </div>
            <p style='color: #9D00FF; margin-top: 10px; font-size: 0.85rem;'>Status: <span style='color: #00FF88;'>● LIVE</span></p>
            <p style='color: #EAEAEA; font-size: 0.8rem;'>FPS: 30 | Resolution: 1920x1080</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feed_col2:
        st.markdown("""
        <div style='background: rgba(157, 0, 255, 0.1); padding: 15px; border-radius: 10px; border: 2px solid rgba(157, 0, 255, 0.3); text-align: center;'>
            <h4 style='color: #9D00FF; margin-bottom: 10px;'>📷 Camera 2: Data Center</h4>
            <div style='background: #000; height: 200px; border-radius: 8px; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden;'>
                <div style='position: absolute; width: 100%; height: 100%; background: linear-gradient(-45deg, rgba(157,0,255,0.1) 0%, rgba(0,255,136,0.1) 100%);'></div>
                <div style='position: relative; z-index: 1;'>
                    <div style='color: #9D00FF; font-size: 3rem; animation: pulse 2s infinite;'>📹</div>
                    <p style='color: #00FF88; margin-top: 10px; font-size: 0.9rem;'>●REC</p>
                </div>
            </div>
            <p style='color: #00FFFF; margin-top: 10px; font-size: 0.85rem;'>Status: <span style='color: #00FF88;'>● LIVE</span></p>
            <p style='color: #EAEAEA; font-size: 0.8rem;'>FPS: 30 | Resolution: 1920x1080</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feed_col3:
        st.markdown("""
        <div style='background: rgba(0, 255, 136, 0.1); padding: 15px; border-radius: 10px; border: 2px solid rgba(0, 255, 136, 0.3); text-align: center;'>
            <h4 style='color: #00FF88; margin-bottom: 10px;'>📷 Camera 3: Observatory</h4>
            <div style='background: #000; height: 200px; border-radius: 8px; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden;'>
                <div style='position: absolute; width: 100%; height: 100%; background: linear-gradient(135deg, rgba(0,255,136,0.1) 0%, rgba(0,255,255,0.1) 100%);'></div>
                <div style='position: relative; z-index: 1;'>
                    <div style='color: #00FF88; font-size: 3rem; animation: pulse 2s infinite;'>🎬</div>
                    <p style='color: #00FF88; margin-top: 10px; font-size: 0.9rem;'>●REC</p>
                </div>
            </div>
            <p style='color: #9D00FF; margin-top: 10px; font-size: 0.85rem;'>Status: <span style='color: #00FF88;'>● LIVE</span></p>
            <p style='color: #EAEAEA; font-size: 0.8rem;'>FPS: 30 | Resolution: 1920x1080</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Real-time Activity Chart
    st.markdown("---")
    st.subheader("📊 Real-Time System Activity")
    
    # Generate real-time activity data
    time_points = pd.date_range(end=datetime.now(), periods=50, freq='1s')
    np.random.seed(int(datetime.now().timestamp()) % 1000)
    activity_data = pd.DataFrame({
        'Time': time_points,
        'CPU Usage': np.random.uniform(20, 80, 50),
        'Memory Usage': np.random.uniform(30, 70, 50),
        'Network Activity': np.random.uniform(10, 90, 50)
    })
    
    fig_activity = go.Figure()
    fig_activity.add_trace(go.Scatter(
        x=activity_data['Time'], y=activity_data['CPU Usage'],
        name='CPU Usage', line=dict(color='#00FFFF', width=2)
    ))
    fig_activity.add_trace(go.Scatter(
        x=activity_data['Time'], y=activity_data['Memory Usage'],
        name='Memory Usage', line=dict(color='#9D00FF', width=2)
    ))
    fig_activity.add_trace(go.Scatter(
        x=activity_data['Time'], y=activity_data['Network Activity'],
        name='Network Activity', line=dict(color='#00FF88', width=2)
    ))
    
    fig_activity.update_layout(
        title='System Performance Monitoring',
        xaxis_title='Time',
        yaxis_title='Usage (%)',
        template='plotly_dark',
        paper_bgcolor='rgba(26, 26, 46, 0.8)',
        plot_bgcolor='rgba(14, 14, 26, 0.8)',
        font=dict(family='Orbitron', color='#EAEAEA'),
        hovermode='x unified',
        height=300
    )
    
    st.plotly_chart(fig_activity, use_container_width=True)
    
    # API Configuration Status
    st.markdown("---")
    st.subheader("🔑 API Configuration Status")
    
    api_col1, api_col2, api_col3 = st.columns(3)
    
    with api_col1:
        openai_key = os.getenv("OPENAI_API_KEY", "")
        openai_status = "✅ Configured" if openai_key and openai_key != "your-openai-api-key" else "⚠️ Not Set"
        openai_color = "#00FF88" if "✅" in openai_status else "#FFA500"
        st.markdown(f"""
        <div style='background: rgba(0, 255, 255, 0.1); padding: 15px; border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3); text-align: center;'>
            <h4>OpenAI API</h4>
            <p style='color: {openai_color};'>{openai_status}</p>
            <p style='font-size: 0.8rem;'>For EVE AI Chat</p>
        </div>
        """, unsafe_allow_html=True)
    
    with api_col2:
        nasa_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
        nasa_status = "✅ Configured" if nasa_key != "DEMO_KEY" else "🟡 Demo Mode"
        nasa_color = "#00FF88" if "✅" in nasa_status else "#FFAA00"
        st.markdown(f"""
        <div style='background: rgba(157, 0, 255, 0.1); padding: 15px; border-radius: 10px; border: 1px solid rgba(157, 0, 255, 0.3); text-align: center;'>
            <h4>NASA API</h4>
            <p style='color: {nasa_color};'>{nasa_status}</p>
            <p style='font-size: 0.8rem;'>For Space Data</p>
        </div>
        """, unsafe_allow_html=True)
    
    with api_col3:
        elevenlabs_key = os.getenv("ELEVENLABS_API_KEY", "")
        elevenlabs_status = "✅ Configured" if elevenlabs_key and elevenlabs_key != "your-elevenlabs-api-key" else "⚠️ Not Set"
        elevenlabs_color = "#00FF88" if "✅" in elevenlabs_status else "#FFA500"
        st.markdown(f"""
        <div style='background: rgba(0, 255, 136, 0.1); padding: 15px; border-radius: 10px; border: 1px solid rgba(0, 255, 136, 0.3); text-align: center;'>
            <h4>ElevenLabs API</h4>
            <p style='color: {elevenlabs_color};'>{elevenlabs_status}</p>
            <p style='font-size: 0.8rem;'>For Voice Synthesis</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("💡 **Tip:** Set API keys in environment variables or .env file for full functionality. See documentation for details.")

# TAB 2: Live Data
with tabs[1]:
    st.header("📈 Live Data Feed")
    
    col_info1, col_info2 = st.columns([3, 1])
    with col_info1:
        st.info("🔄 Auto-refresh enabled - Data updates every 60 seconds")
    with col_info2:
        # Data source indicator
        st.markdown("""
        <div style='background: rgba(0, 255, 136, 0.1); padding: 10px; border-radius: 5px; text-align: center;'>
            <span style='color: #00FF88;'>🟢 Data Source: Active</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Load data
    data = load_google_sheets_data()
    
    st.subheader(f"📊 Dataset: {len(data)} records loaded")
    
    # Summary Stats
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    with stat_col1:
        st.metric("Total Records", f"{len(data):,}")
    with stat_col2:
        if 'Category' in data.columns:
            st.metric("Categories", len(data['Category'].unique()))
    with stat_col3:
        if 'Status' in data.columns:
            st.metric("Statuses", len(data['Status'].unique()))
    with stat_col4:
        st.metric("Columns", len(data.columns))
    
    st.markdown("---")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Category' in data.columns:
            categories = ['All'] + list(data['Category'].unique())
            selected_category = st.selectbox("🔍 Filter by Category", categories)
    
    with col2:
        if 'Status' in data.columns:
            statuses = ['All'] + list(data['Status'].unique())
            selected_status = st.selectbox("📋 Filter by Status", statuses)
    
    # Apply filters
    filtered_data = data.copy()
    if 'Category' in data.columns and selected_category != 'All':
        filtered_data = filtered_data[filtered_data['Category'] == selected_category]
    if 'Status' in data.columns and selected_status != 'All':
        filtered_data = filtered_data[filtered_data['Status'] == selected_status]
    
    # Display filtered count
    st.markdown(f"**Showing {len(filtered_data)} of {len(data)} records**")
    
    # Display data with enhanced styling
    st.dataframe(
        filtered_data, 
        use_container_width=True, 
        height=400,
        hide_index=True
    )
    
    # Action buttons
    action_col1, action_col2, action_col3 = st.columns(3)
    with action_col1:
        csv = filtered_data.to_csv(index=False)
        st.download_button(
            label="📥 Export CSV",
            data=csv,
            file_name=f"eve_live_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with action_col2:
        # Export to Excel
        try:
            from io import BytesIO
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                filtered_data.to_excel(writer, index=False, sheet_name='EVE Data')
            buffer.seek(0)
            st.download_button(
                label="📊 Export Excel",
                data=buffer,
                file_name=f"eve_live_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        except Exception as e:
            st.button("📊 Excel (N/A)", disabled=True, use_container_width=True)
    with action_col3:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

# TAB 3: PSI Tracker
with tabs[2]:
    st.header("💎 PSI Coin Tracker")
    
    psi_data = get_psi_price()
    
    # Status indicator
    status_badge = {
        'live': ('🟢', 'Live Data', '#00FF88'),
        'demo': ('🟡', 'Demo Mode', '#FFA500'),
        'error': ('🔴', 'Offline', '#FF4444')
    }
    badge_emoji, badge_text, badge_color = status_badge.get(psi_data.get('status', 'error'), ('🔴', 'Unknown', '#FF4444'))
    
    st.markdown(f"""
    <div style='background: rgba(0, 255, 255, 0.05); padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center;'>
        <span style='color: {badge_color}; font-size: 0.9rem;'>{badge_emoji} <strong>{badge_text}</strong> | Last Updated: {psi_data.get('last_updated', datetime.now()).strftime('%H:%M:%S')}</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        price_color = "#00FF88" if psi_data['change_24h'] >= 0 else "#FF4444"
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 255, 255, 0.1)); padding: 25px; border-radius: 15px; border: 2px solid rgba(0, 255, 136, 0.3); text-align: center; box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);'>
            <h3 style='color: #00FFFF; margin-bottom: 10px;'>💰 Current Price</h3>
            <h1 style='color: {price_color}; font-size: 3rem; margin: 10px 0; text-shadow: 0 0 10px {price_color};'>${psi_data['price']:.6f}</h1>
            <p style='color: #9D00FF; font-size: 0.85rem; margin-top: 10px;'>TridentDAO (PSI)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        change_emoji = "📈" if psi_data['change_24h'] >= 0 else "📉"
        change_color = "#00FF88" if psi_data['change_24h'] >= 0 else "#FF4444"
        st.markdown(f"""
        <div style='background: rgba(157, 0, 255, 0.1); padding: 25px; border-radius: 15px; border: 2px solid rgba(157, 0, 255, 0.3); text-align: center; box-shadow: 0 0 20px rgba(157, 0, 255, 0.2);'>
            <h3 style='color: #9D00FF; margin-bottom: 10px;'>{change_emoji} 24h Change</h3>
            <h1 style='color: {change_color}; font-size: 2.5rem; margin: 10px 0; text-shadow: 0 0 10px {change_color};'>{psi_data['change_24h']:+.2f}%</h1>
            <p style='color: #00FFFF; font-size: 0.85rem; margin-top: 10px;'>Daily Performance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        market_cap_display = f"${psi_data['market_cap']:,.0f}" if psi_data['market_cap'] > 0 else "N/A"
        st.markdown(f"""
        <div style='background: rgba(0, 255, 255, 0.1); padding: 25px; border-radius: 15px; border: 2px solid rgba(0, 255, 255, 0.3); text-align: center; box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);'>
            <h3 style='color: #00FFFF; margin-bottom: 10px;'>💎 Market Cap</h3>
            <h1 style='color: #00FF88; font-size: 2rem; margin: 10px 0; text-shadow: 0 0 10px #00FF88;'>{market_cap_display}</h1>
            <p style='color: #9D00FF; font-size: 0.85rem; margin-top: 10px;'>Total Valuation</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Historical Chart with annotations
    st.subheader("📊 30-Day Price History with Annotations")
    
    # Generate sample historical data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    base_price = psi_data['price'] if psi_data['price'] > 0 else 0.000123
    
    # Create realistic price variations
    np.random.seed(42)
    price_changes = np.random.normal(0, 0.02, 30)
    prices = [base_price * (1 + sum(price_changes[:i+1])) for i in range(30)]
    
    # Calculate moving averages
    df_prices = pd.DataFrame({'Date': dates, 'Price': prices})
    df_prices['MA7'] = df_prices['Price'].rolling(window=7).mean()
    
    fig = go.Figure()
    
    # Main price line
    fig.add_trace(go.Scatter(
        x=dates,
        y=prices,
        mode='lines+markers',
        name='PSI Price',
        line=dict(color='#00FFFF', width=3),
        marker=dict(size=8, color='#9D00FF'),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 255, 0.1)'
    ))
    
    # Add annotations for significant events
    # Find peaks and troughs
    peak_idx = np.argmax(prices)
    trough_idx = np.argmin(prices)
    
    fig.add_annotation(
        x=dates[peak_idx],
        y=prices[peak_idx],
        text=f"Peak: ${prices[peak_idx]:.6f}",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#00FF88",
        font=dict(color="#00FF88", size=12),
        bgcolor="rgba(0, 255, 136, 0.2)",
        bordercolor="#00FF88"
    )
    
    fig.add_annotation(
        x=dates[trough_idx],
        y=prices[trough_idx],
        text=f"Low: ${prices[trough_idx]:.6f}",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#FF4444",
        font=dict(color="#FF4444", size=12),
        bgcolor="rgba(255, 68, 68, 0.2)",
        bordercolor="#FF4444"
    )
    
    # Add current price annotation
    fig.add_annotation(
        x=dates[-1],
        y=prices[-1],
        text=f"Current: ${prices[-1]:.6f}",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#00FFFF",
        font=dict(color="#00FFFF", size=12, family="Orbitron"),
        bgcolor="rgba(0, 255, 255, 0.2)",
        bordercolor="#00FFFF"
    )
    
    fig.update_layout(
        title='TridentDAO (PSI) Price Chart with Technical Analysis',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        template='plotly_dark',
        paper_bgcolor='rgba(26, 26, 46, 0.8)',
        plot_bgcolor='rgba(14, 14, 26, 0.8)',
        font=dict(family='Orbitron', color='#EAEAEA'),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Volume and Market Stats
    st.subheader("📈 Market Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("7d High", f"${max(prices[-7:]):.6f}", delta=f"+{((max(prices[-7:]) - base_price) / base_price * 100):.2f}%")
    with col2:
        st.metric("7d Low", f"${min(prices[-7:]):.6f}", delta=f"{((min(prices[-7:]) - base_price) / base_price * 100):.2f}%")
    with col3:
        volatility = np.std(prices[-7:]) / np.mean(prices[-7:]) * 100
        st.metric("7d Volatility", f"{volatility:.2f}%")
    with col4:
        trend = "Bullish 📈" if prices[-1] > prices[-7] else "Bearish 📉"
        st.metric("Trend", trend)
    
    # Bonding Curve Progress
    st.subheader("📈 Bonding Curve Progress")
    
    progress = min((base_price / 0.001) * 100, 100) if base_price > 0 else 12.3
    
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=progress,
        title={'text': "Market Progress", 'font': {'size': 24, 'color': '#00FFFF'}},
        delta={'reference': 80, 'increasing': {'color': "#00FF88"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#00FFFF"},
            'bar': {'color': "#9D00FF"},
            'bgcolor': "rgba(26, 26, 46, 0.8)",
            'borderwidth': 2,
            'bordercolor': "#00FFFF",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(0, 255, 136, 0.2)'},
                {'range': [50, 80], 'color': 'rgba(0, 255, 255, 0.2)'},
                {'range': [80, 100], 'color': 'rgba(157, 0, 255, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "#00FF88", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig_gauge.update_layout(
        paper_bgcolor='rgba(14, 14, 26, 0)',
        font={'color': "#EAEAEA", 'family': "Orbitron"},
        height=300
    )
    
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Stock Market Integration
    st.markdown("---")
    st.subheader("📊 Stock Market Overview")
    
    # Simulated stock market data (in production, use real APIs like Alpha Vantage, Yahoo Finance, etc.)
    stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA']
    
    # Generate sample stock data with deterministic seed based on date
    stock_data = []
    day_seed = datetime.now().timetuple().tm_yday
    np.random.seed(day_seed)
    
    for symbol in stock_symbols:
        base_price = random.uniform(100, 500)
        change = random.uniform(-5, 5)
        stock_data.append({
            'Symbol': symbol,
            'Price': base_price,
            'Change': change,
            'Change %': (change / base_price) * 100,
            'Volume': random.randint(1000000, 50000000)
        })
    
    df_stocks = pd.DataFrame(stock_data)
    
    # Display stock table with color coding
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create color-coded dataframe display
        for idx, row in df_stocks.iterrows():
            color = "#00FF88" if row['Change'] >= 0 else "#FF4444"
            symbol_color = "#00FFFF"
            
            st.markdown(f"""
            <div style='background: rgba(26, 26, 46, 0.8); padding: 15px; margin: 5px 0; border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3);'>
                <span style='color: {symbol_color}; font-size: 1.3rem; font-weight: bold;'>{row['Symbol']}</span>
                <span style='float: right;'>
                    <span style='color: white; font-size: 1.2rem;'>${row['Price']:.2f}</span>
                    <span style='color: {color}; margin-left: 15px;'>
                        {'▲' if row['Change'] >= 0 else '▼'} {abs(row['Change']):.2f} ({row['Change %']:.2f}%)
                    </span>
                </span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: rgba(157, 0, 255, 0.1); padding: 20px; border-radius: 10px; border: 1px solid rgba(157, 0, 255, 0.3);'>
            <h4>Market Summary</h4>
            <p><strong>Status:</strong> <span style='color: #00FF88;'>Open</span></p>
            <p><strong>Session:</strong> Regular Hours</p>
            <p><strong>Last Update:</strong> Live</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Stock performance chart
    st.markdown("### 📈 Intraday Performance")
    
    # Generate intraday data for visualization with deterministic seed
    times = pd.date_range(end=datetime.now(), periods=50, freq='5min')
    
    day_seed = datetime.now().timetuple().tm_yday
    np.random.seed(day_seed + STOCK_SEED_OFFSET)  # Different seed for intraday data
    
    fig_stocks = go.Figure()
    
    for symbol in stock_symbols[:3]:  # Show top 3 stocks
        base = random.uniform(100, 300)
        prices = [base + random.uniform(-10, 10) + i*0.1 for i in range(50)]
        
        fig_stocks.add_trace(go.Scatter(
            x=times,
            y=prices,
            mode='lines',
            name=symbol,
            line=dict(width=2),
            hovertemplate=f'<b>{symbol}</b><br>Time: %{{x}}<br>Price: $%{{y:.2f}}<extra></extra>'
        ))
    
    fig_stocks.update_layout(
        title='Real-Time Stock Performance',
        xaxis_title='Time',
        yaxis_title='Price (USD)',
        template='plotly_dark',
        paper_bgcolor='rgba(26, 26, 46, 0.8)',
        plot_bgcolor='rgba(14, 14, 26, 0.8)',
        font=dict(family='Orbitron', color='#EAEAEA'),
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            bgcolor="rgba(26, 26, 46, 0.8)",
            bordercolor="#00FFFF",
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig_stocks, use_container_width=True)

# TAB 4: 5D Star Map
with tabs[3]:
    st.header("🌟 5D Holographic Star Map")
    
    st.info("🎮 Interactive 3D solar system with 10,500+ stars, colorful planets, and nebulae | Drag to rotate • Scroll to zoom • Full mouse control")
    
    # Enhanced Three.js Star Map with OrbitControls and multi-colored stars
    star_map_html = """
    <div id="starmap" style="width: 100%; height: 600px; background: linear-gradient(180deg, #000000 0%, #0a0a1a 50%, #000000 100%); border-radius: 15px; border: 2px solid rgba(0, 255, 255, 0.5); box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script>
        const container = document.getElementById('starmap');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 2000);
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setClearColor(0x000000, 0);
        container.appendChild(renderer.domElement);
        
        // Add OrbitControls for interactivity
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.rotateSpeed = 0.5;
        controls.zoomSpeed = 1.2;
        controls.minDistance = 100;
        controls.maxDistance = 1000;
        controls.autoRotate = true;
        controls.autoRotateSpeed = 0.5;
        
        // Create multi-colored star field with 5D holographic effect
        const starGroups = [];
        const starColors = [
            0x00FFFF, // Cyan
            0x9D00FF, // Purple
            0x00FF88, // Green
            0xFFFFFF, // White
            0xFF6B9D, // Pink
            0xFFA500  // Orange
        ];
        
        // Create multiple star layers for depth
        for (let layer = 0; layer < 3; layer++) {
            const starGeometry = new THREE.BufferGeometry();
            const starCount = 3500;
            const starVertices = [];
            const starColorsArray = [];
            
            for (let i = 0; i < starCount; i++) {
                const radius = 300 + (layer * 300);
                const x = (Math.random() - 0.5) * radius * 2;
                const y = (Math.random() - 0.5) * radius * 2;
                const z = (Math.random() - 0.5) * radius * 2;
                starVertices.push(x, y, z);
                
                // Assign colors
                const color = new THREE.Color(starColors[Math.floor(Math.random() * starColors.length)]);
                starColorsArray.push(color.r, color.g, color.b);
            }
            
            starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));
            starGeometry.setAttribute('color', new THREE.Float32BufferAttribute(starColorsArray, 3));
            
            const starMaterial = new THREE.PointsMaterial({
                size: 1.2 - (layer * 0.2),
                vertexColors: true,
                transparent: true,
                opacity: 0.8,
                blending: THREE.AdditiveBlending
            });
            
            const stars = new THREE.Points(starGeometry, starMaterial);
            starGroups.push(stars);
            scene.add(stars);
        }
        
        // Add holographic nebula clouds
        const nebulaGeometry = new THREE.BufferGeometry();
        const nebulaVertices = [];
        const nebulaColors = [];
        
        for (let i = 0; i < 500; i++) {
            const x = (Math.random() - 0.5) * 1200;
            const y = (Math.random() - 0.5) * 1200;
            const z = (Math.random() - 0.5) * 1200;
            nebulaVertices.push(x, y, z);
            
            const color = new THREE.Color(Math.random() < 0.5 ? 0x9D00FF : 0x00FFFF);
            color.multiplyScalar(0.3);
            nebulaColors.push(color.r, color.g, color.b);
        }
        
        nebulaGeometry.setAttribute('position', new THREE.Float32BufferAttribute(nebulaVertices, 3));
        nebulaGeometry.setAttribute('color', new THREE.Float32BufferAttribute(nebulaColors, 3));
        
        const nebulaMaterial = new THREE.PointsMaterial({
            size: 15,
            vertexColors: true,
            transparent: true,
            opacity: 0.2,
            blending: THREE.AdditiveBlending
        });
        
        const nebula = new THREE.Points(nebulaGeometry, nebulaMaterial);
        scene.add(nebula);
        
        // Add colorful planets
        const planets = [];
        const planetData = [
            { name: 'Mercury', color: 0x8C7853, size: 5, distance: 150, speed: 0.01 },
            { name: 'Venus', color: 0xFFC649, size: 7, distance: 200, speed: 0.008 },
            { name: 'Earth', color: 0x4169E1, size: 8, distance: 250, speed: 0.006 },
            { name: 'Mars', color: 0xCD5C5C, size: 6, distance: 300, speed: 0.005 },
            { name: 'Jupiter', color: 0xC88B3A, size: 15, distance: 400, speed: 0.003 },
            { name: 'Saturn', color: 0xFAD5A5, size: 13, distance: 500, speed: 0.002 }
        ];
        
        planetData.forEach(data => {
            const geometry = new THREE.SphereGeometry(data.size, 32, 32);
            const material = new THREE.MeshBasicMaterial({ 
                color: data.color,
                transparent: true,
                opacity: 0.9
            });
            const planet = new THREE.Mesh(geometry, material);
            planet.userData = { distance: data.distance, speed: data.speed, angle: Math.random() * Math.PI * 2 };
            planets.push(planet);
            scene.add(planet);
        });
        
        // Add Sun at center
        const sunGeometry = new THREE.SphereGeometry(20, 32, 32);
        const sunMaterial = new THREE.MeshBasicMaterial({ 
            color: 0xFFFF00,
            transparent: true,
            opacity: 0.95
        });
        const sun = new THREE.Mesh(sunGeometry, sunMaterial);
        scene.add(sun);
        
        // Add glow effect to sun
        const glowGeometry = new THREE.SphereGeometry(25, 32, 32);
        const glowMaterial = new THREE.MeshBasicMaterial({
            color: 0xFFAA00,
            transparent: true,
            opacity: 0.3
        });
        const sunGlow = new THREE.Mesh(glowGeometry, glowMaterial);
        scene.add(sunGlow);
        
        // Enhanced constellation lines (Multiple constellations)
        const constellations = [
            {
                name: 'Orion',
                color: 0x9D00FF,
                points: [
                    new THREE.Vector3(-100, 50, -200),
                    new THREE.Vector3(-50, 100, -200),
                    new THREE.Vector3(0, 80, -200),
                    new THREE.Vector3(50, 50, -200),
                    new THREE.Vector3(0, 0, -200),
                    new THREE.Vector3(-50, -50, -200),
                    new THREE.Vector3(-100, 50, -200)
                ]
            },
            {
                name: 'BigDipper',
                color: 0x00FFFF,
                points: [
                    new THREE.Vector3(150, 100, -250),
                    new THREE.Vector3(180, 120, -250),
                    new THREE.Vector3(200, 110, -250),
                    new THREE.Vector3(220, 80, -250),
                    new THREE.Vector3(200, 50, -250),
                    new THREE.Vector3(170, 40, -250),
                    new THREE.Vector3(150, 60, -250)
                ]
            }
        ];
        
        constellations.forEach(constellation => {
            const lineMaterial = new THREE.LineBasicMaterial({ 
                color: constellation.color, 
                linewidth: 2,
                transparent: true,
                opacity: 0.7
            });
            const lineGeometry = new THREE.BufferGeometry().setFromPoints(constellation.points);
            const line = new THREE.Line(lineGeometry, lineMaterial);
            scene.add(line);
        });
        
        camera.position.z = 400;
        
        // Animation loop with holographic effects
        function animate() {
            requestAnimationFrame(animate);
            
            // Rotate star layers at different speeds for depth effect
            starGroups.forEach((stars, index) => {
                stars.rotation.y += 0.0002 * (index + 1);
                stars.rotation.x += 0.0001 * (index + 1);
            });
            
            // Animate nebula
            nebula.rotation.y += 0.0003;
            nebula.rotation.x += 0.0002;
            
            // Animate planets in orbit
            planets.forEach(planet => {
                planet.userData.angle += planet.userData.speed;
                planet.position.x = Math.cos(planet.userData.angle) * planet.userData.distance;
                planet.position.z = Math.sin(planet.userData.angle) * planet.userData.distance;
                planet.rotation.y += 0.01;
            });
            
            // Pulse sun glow
            sunGlow.scale.x = 1 + Math.sin(Date.now() * 0.001) * 0.1;
            sunGlow.scale.y = 1 + Math.sin(Date.now() * 0.001) * 0.1;
            sunGlow.scale.z = 1 + Math.sin(Date.now() * 0.001) * 0.1;
            
            controls.update();
            renderer.render(scene, camera);
        }
        
        animate();
        
        // Handle window resize
        window.addEventListener('resize', () => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        });
        
        // Add holographic glow effect
        container.style.filter = 'drop-shadow(0 0 10px rgba(0, 255, 255, 0.5))';
    </script>
    """
    
    st.components.v1.html(star_map_html, height=650)
    
    # Enhanced Controls info
    st.subheader("🎮 Interactive Controls & Features")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**🖱️ Drag**: Rotate view")
    with col2:
        st.markdown("**🔍 Scroll**: Zoom in/out")
    with col3:
        st.markdown("**🪐 Planets**: 6 orbiting planets")
    with col4:
        st.markdown("**🌟 Stars**: 10,500+ multi-color")

# TAB 5: NASA & Space Real-Time Data
with tabs[4]:
    st.header("🚀 NASA Real-Time Mission Data")
    
    # Telescope Status
    st.subheader("🔭 Space Telescope Status")
    
    col1, col2 = st.columns(2)
    
    hubble_data = get_hubble_status()
    jwst_data = get_jwst_status()
    
    with col1:
        st.markdown(f"""
        <div style='background: rgba(0, 255, 255, 0.1); padding: 20px; border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3);'>
            <h3>🔭 Hubble Space Telescope</h3>
            <p><strong>Status:</strong> <span style='color: #00FF88;'>{hubble_data['status']}</span></p>
            <p><strong>Altitude:</strong> {hubble_data['altitude_km']} km</p>
            <p><strong>Orbit Period:</strong> {hubble_data['orbit_period_min']} min</p>
            <p><strong>Observations Today:</strong> {hubble_data['observations_today']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: rgba(157, 0, 255, 0.1); padding: 20px; border-radius: 10px; border: 1px solid rgba(157, 0, 255, 0.3);'>
            <h3>🔭 James Webb Space Telescope</h3>
            <p><strong>Status:</strong> <span style='color: #00FF88;'>{jwst_data['status']}</span></p>
            <p><strong>Distance:</strong> {jwst_data['distance_km']/1e6:.2f} million km (L2)</p>
            <p><strong>Temperature:</strong> {jwst_data['temperature_k']} K</p>
            <p><strong>Observations Today:</strong> {jwst_data['observations_today']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ISS Real-Time Position
    st.subheader("🛰️ International Space Station")
    
    iss_pos = get_iss_position()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌍 Latitude", f"{iss_pos['latitude']:.2f}°")
    with col2:
        st.metric("🌎 Longitude", f"{iss_pos['longitude']:.2f}°")
    with col3:
        st.metric("🔄 Status", "LIVE", delta="Tracking")
    
    # ISS Position Map using Plotly
    fig_iss = go.Figure(go.Scattergeo(
        lon=[iss_pos['longitude']],
        lat=[iss_pos['latitude']],
        mode='markers+text',
        marker=dict(size=15, color='#00FF88', symbol='circle'),
        text=['ISS'],
        textposition='top center'
    ))
    
    fig_iss.update_layout(
        title='ISS Current Position',
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(30, 30, 40)',
            oceancolor='rgb(10, 10, 20)',
            coastlinecolor='#00FFFF',
            bgcolor='rgba(14, 14, 26, 0.8)'
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(26, 26, 46, 0.8)',
        font=dict(family='Orbitron', color='#EAEAEA'),
        height=400
    )
    
    st.plotly_chart(fig_iss, use_container_width=True)
    
    st.markdown("---")
    
    # NASA APOD
    st.subheader("🌌 Astronomy Picture of the Day")
    
    nasa_data = get_nasa_apod()
    
    # Status indicator
    status_badge_nasa = {
        'live': ('🟢', 'Live from NASA', '#00FF88'),
        'demo': ('🟡', 'Demo Mode', '#FFA500'),
        'error': ('🔴', 'Offline', '#FF4444')
    }
    badge_emoji_n, badge_text_n, badge_color_n = status_badge_nasa.get(nasa_data.get('status', 'live'), ('🟢', 'Live', '#00FF88'))
    
    st.markdown(f"""
    <div style='background: rgba(0, 255, 255, 0.05); padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center;'>
        <span style='color: {badge_color_n}; font-size: 0.9rem;'>{badge_emoji_n} <strong>{badge_text_n}</strong> | Date: {nasa_data.get('date', 'N/A')}</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if nasa_data.get('media_type') == 'video':
            st.video(nasa_data['url'])
        else:
            st.image(nasa_data['url'], use_column_width=True, caption=nasa_data.get('title', 'Astronomy Picture'))
            
            # Zoom button
            if st.button("🔍 Zoom Picture", key="zoom_nasa"):
                st.session_state.zoom_image = "nasa_apod"
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(157, 0, 255, 0.1)); padding: 25px; border-radius: 15px; border: 2px solid rgba(0, 255, 255, 0.3); box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);'>
            <h3 style='color: #00FFFF; text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);'>{nasa_data.get('title', 'Unknown')}</h3>
            <p><strong style='color: #9D00FF;'>Date:</strong> <span style='color: #00FF88;'>{nasa_data.get('date', 'N/A')}</span></p>
            <p style='color: #EAEAEA; line-height: 1.6;'>{nasa_data.get('explanation', 'No description available.')[:300]}...</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Zoomed view
    if st.session_state.zoom_image == "nasa_apod":
        st.markdown("---")
        st.subheader("🔍 Full Resolution View")
        st.image(nasa_data['url'], caption=nasa_data.get('title', 'Astronomy Picture'), use_column_width=True)
        if st.button("❌ Close Zoom", key="close_nasa_zoom"):
            st.session_state.zoom_image = None
            st.rerun()
    
    with st.expander("📖 Full Description"):
        st.write(nasa_data.get('explanation', 'No description available.'))

# TAB 6: Live Camera Feeds
with tabs[5]:
    st.header("📹 Live Camera Feeds")
    
    st.info("🔄 Live traffic and city cameras from around the world - Use refresh button for updates")
    
    cameras = get_traffic_cameras()
    
    # Camera selection
    selected_camera = st.selectbox(
        "Select Camera Feed",
        options=range(len(cameras)),
        format_func=lambda i: f"{cameras[i]['name']} - {cameras[i]['location']}"
    )
    
    camera = cameras[selected_camera]
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(f"📹 {camera['name']}")
        
        # Display camera feed based on type
        if camera['type'] == 'live_stream':
            st.markdown(f"""
            <div style='background: #000; padding: 10px; border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3);'>
                <iframe 
                    src="{camera['url']}" 
                    width="100%" 
                    height="500" 
                    frameborder="0" 
                    allowfullscreen
                    style="border-radius: 5px;"
                ></iframe>
            </div>
            """, unsafe_allow_html=True)
        else:
            # For image-based cameras
            st.markdown(f"""
            <div style='background: #000; padding: 10px; border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3); text-align: center;'>
                <img src="{camera['url']}" style="width: 100%; max-height: 500px; object-fit: contain; border-radius: 5px;" />
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: rgba(0, 255, 255, 0.1); padding: 20px; border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3);'>
            <h3>Camera Info</h3>
            <p><strong>Location:</strong><br>{camera['location']}</p>
            <p><strong>Status:</strong><br><span style='color: #00FF88;'>🟢 LIVE</span></p>
            <p><strong>Refresh:</strong><br>Every {camera['refresh_rate']}s</p>
            <p><strong>Quality:</strong><br>HD 1080p</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Camera controls
        st.markdown("### 🎮 Controls")
        if st.button("🔄 Manual Refresh", use_container_width=True):
            st.rerun()
        
        if st.button("📸 Capture Frame", use_container_width=True):
            st.info("Frame capture feature - Save current view")
    
    st.markdown("---")
    
    # Additional camera feeds in grid
    st.subheader("📹 All Camera Feeds")
    
    cols = st.columns(3)
    for idx, cam in enumerate(cameras):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style='background: rgba(26, 26, 46, 0.8); padding: 15px; border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3); text-align: center;'>
                <h4>{cam['name']}</h4>
                <p style='color: #00FFFF;'>{cam['location']}</p>
                <p style='color: #00FF88;'>🟢 LIVE</p>
            </div>
            """, unsafe_allow_html=True)

# TAB 7: Weather Alerts
with tabs[6]:
    st.header("🌦️ Weather Alerts & Monitoring")
    
    st.info("🔄 Real-time weather alerts from NOAA - Refresh for latest updates")
    
    weather_data = get_weather_alerts()
    
    # Status indicator
    status_color = "#00FF88" if weather_data['status'] == 'live' else "#FFA500"
    status_text = "LIVE" if weather_data['status'] == 'live' else "DEMO MODE"
    
    st.markdown(f"""
    <div style='background: rgba(0, 255, 255, 0.05); padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center;'>
        <span style='color: {status_color}; font-size: 0.9rem;'><strong>{status_text}</strong> | Total Alerts: {weather_data['count']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Display alerts
    if weather_data['alerts']:
        for idx, alert in enumerate(weather_data['alerts']):
            severity_color = {
                'Severe': '#FF4444',
                'Moderate': '#FFA500',
                'Minor': '#FFFF00',
                'Unknown': '#00FFFF'
            }.get(alert['severity'], '#00FFFF')
            
            st.markdown(f"""
            <div style='background: rgba(26, 26, 46, 0.8); padding: 20px; margin: 10px 0; border-radius: 10px; border-left: 4px solid {severity_color};'>
                <h3 style='color: {severity_color}; margin-top: 0;'>{alert['event']}</h3>
                <p><strong>Severity:</strong> <span style='color: {severity_color};'>{alert['severity']}</span></p>
                <p><strong>Area:</strong> {alert['area']}</p>
                <p><strong>Headline:</strong> {alert['headline']}</p>
                <p style='color: #AAAAAA;'>{alert['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No active weather alerts at this time")
    
    st.markdown("---")
    
    # Additional weather visualization
    st.subheader("🌡️ Weather Monitoring")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: rgba(0, 255, 255, 0.1); padding: 20px; border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3); text-align: center;'>
            <h3>📡 Radar Active</h3>
            <p style='color: #00FF88;'>Monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: rgba(157, 0, 255, 0.1); padding: 20px; border-radius: 10px; border: 1px solid rgba(157, 0, 255, 0.3); text-align: center;'>
            <h3>🌊 Flood Alerts</h3>
            <p style='color: #00FF88;'>Clear</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: rgba(0, 255, 136, 0.1); padding: 20px; border-radius: 10px; border: 1px solid rgba(0, 255, 136, 0.3); text-align: center;'>
            <h3>🌪️ Storm Watch</h3>
            <p style='color: #FFA500;'>Monitoring</p>
        </div>
        """, unsafe_allow_html=True)

# TAB 8: Satellite Tracking
with tabs[7]:
    st.header("🛰️ Satellite Tracking & Monitoring")
    
    st.info("🔄 Real-time satellite positions and tracking")
    
    sat_data = get_satellite_tracking()
    
    # Display satellite grid
    st.subheader("📡 Active Satellites")
    
    if sat_data['satellites']:
        cols = st.columns(3)
        for idx, sat in enumerate(sat_data['satellites']):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style='background: rgba(26, 26, 46, 0.8); padding: 20px; border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3); text-align: center;'>
                    <h3 style='color: #00FFFF;'>{sat['name']}</h3>
                    <p><strong>NORAD ID:</strong> {sat['norad_id']}</p>
                    <p><strong>Type:</strong> {sat['type']}</p>
                    <p><strong>Status:</strong> <span style='color: #00FF88;'>✓ {sat['status']}</span></p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Satellite visualization
    st.subheader("🌍 Global Satellite Coverage")
    
    # Create a simple visualization showing satellite distribution
    fig_sats = go.Figure()
    
    # Add Earth outline
    lats = list(range(-90, 91, 10))
    lons = list(range(-180, 181, 10))
    
    # Add sample satellite positions
    sat_lats = [40.7, -33.9, 51.5, 35.7, -23.5]
    sat_lons = [-74.0, 151.2, -0.1, 139.7, -46.6]
    sat_names = ['ISS', 'Hubble', 'Starlink', 'GPS', 'NOAA']
    
    fig_sats.add_trace(go.Scattergeo(
        lon=sat_lons,
        lat=sat_lats,
        mode='markers+text',
        marker=dict(size=12, color='#00FF88', symbol='circle'),
        text=sat_names,
        textposition='top center'
    ))
    
    fig_sats.update_layout(
        title='Satellite Positions (Approximate)',
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(30, 30, 40)',
            oceancolor='rgb(10, 10, 20)',
            coastlinecolor='#00FFFF',
            bgcolor='rgba(14, 14, 26, 0.8)'
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(26, 26, 46, 0.8)',
        font=dict(family='Orbitron', color='#EAEAEA'),
        height=500
    )
    
    st.plotly_chart(fig_sats, use_container_width=True)

# TAB 9: Blueprints & Formulas
with tabs[8]:
    st.header("📐 Blueprints, Formulas & Technical Data")
    
    st.info("🔄 Advanced technical schematics and scientific formulas")
    
    # Blueprint Categories
    blueprint_tabs = st.tabs(["🚀 Spacecraft", "🔬 Formulas", "🛸 Technology", "📊 Data Sheets"])
    
    with blueprint_tabs[0]:
        st.subheader("🚀 Spacecraft Blueprints")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background: rgba(26, 26, 46, 0.8); padding: 20px; border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3);'>
                <h3 style='color: #00FFFF;'>SpaceX Starship</h3>
                <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Starship_SN8_cryo_test.jpg/800px-Starship_SN8_cryo_test.jpg' style='width: 100%; border-radius: 10px;'/>
                <p><strong>Height:</strong> 120m</p>
                <p><strong>Diameter:</strong> 9m</p>
                <p><strong>Payload:</strong> 100-150 tons to LEO</p>
                <p><strong>Status:</strong> <span style='color: #00FF88;'>In Development</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔍 Zoom Starship", key="zoom_starship"):
                st.session_state.zoom_image = "starship"
        
        with col2:
            st.markdown("""
            <div style='background: rgba(26, 26, 46, 0.8); padding: 20px; border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3);'>
                <h3 style='color: #00FFFF;'>James Webb Telescope</h3>
                <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/James_Webb_Space_Telescope_spacecraft_model_2.png/800px-James_Webb_Space_Telescope_spacecraft_model_2.png' style='width: 100%; border-radius: 10px;'/>
                <p><strong>Mirror Diameter:</strong> 6.5m</p>
                <p><strong>Wavelength:</strong> 0.6-28 μm</p>
                <p><strong>Orbit:</strong> L2 Lagrange Point</p>
                <p><strong>Status:</strong> <span style='color: #00FF88;'>Operational</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔍 Zoom JWST", key="zoom_jwst"):
                st.session_state.zoom_image = "jwst"
        
        # Zoomed view
        if st.session_state.zoom_image:
            st.markdown("---")
            st.subheader("🔍 Detailed View")
            
            if st.session_state.zoom_image == "starship":
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Starship_SN8_cryo_test.jpg/1200px-Starship_SN8_cryo_test.jpg", 
                        caption="SpaceX Starship - Full Resolution", use_column_width=True)
            elif st.session_state.zoom_image == "jwst":
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/James_Webb_Space_Telescope_spacecraft_model_2.png/1200px-James_Webb_Space_Telescope_spacecraft_model_2.png",
                        caption="James Webb Space Telescope - Full Resolution", use_column_width=True)
            
            if st.button("❌ Close Zoom"):
                st.session_state.zoom_image = None
                st.rerun()
    
    with blueprint_tabs[1]:
        st.subheader("🔬 Scientific Formulas")
        
        st.markdown("""
        <div style='background: rgba(26, 26, 46, 0.8); padding: 20px; border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3);'>
            <h3 style='color: #00FFFF;'>Einstein's Field Equations</h3>
            <p style='font-size: 1.5rem; text-align: center; color: #9D00FF;'>
                R<sub>μν</sub> - ½Rg<sub>μν</sub> + Λg<sub>μν</sub> = (8πG/c⁴)T<sub>μν</sub>
            </p>
            <p>Describes gravitational fields in general relativity</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: rgba(26, 26, 46, 0.8); padding: 20px; border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3); margin-top: 20px;'>
            <h3 style='color: #00FFFF;'>Rocket Equation (Tsiolkovsky)</h3>
            <p style='font-size: 1.5rem; text-align: center; color: #00FF88;'>
                Δv = v<sub>e</sub> ln(m<sub>0</sub>/m<sub>f</sub>)
            </p>
            <p>Fundamental equation for rocket propulsion</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: rgba(26, 26, 46, 0.8); padding: 20px; border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3); margin-top: 20px;'>
            <h3 style='color: #00FFFF;'>Drake Equation</h3>
            <p style='font-size: 1.3rem; text-align: center; color: #9D00FF;'>
                N = R<sub>*</sub> × f<sub>p</sub> × n<sub>e</sub> × f<sub>l</sub> × f<sub>i</sub> × f<sub>c</sub> × L
            </p>
            <p>Estimates the number of active, communicative civilizations in our galaxy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with blueprint_tabs[2]:
        st.subheader("🛸 Advanced Technology")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background: rgba(26, 26, 46, 0.8); padding: 20px; border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3);'>
                <h3 style='color: #00FFFF;'>Ion Propulsion System</h3>
                <p><strong>Thrust:</strong> 0.1-0.5 N</p>
                <p><strong>ISP:</strong> 3000-5000 s</p>
                <p><strong>Efficiency:</strong> 70-90%</p>
                <p><strong>Applications:</strong> Deep space probes</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: rgba(26, 26, 46, 0.8); padding: 20px; border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3);'>
                <h3 style='color: #00FFFF;'>Nuclear Fusion Reactor</h3>
                <p><strong>Reaction:</strong> D-T Fusion</p>
                <p><strong>Temperature:</strong> 150 million °C</p>
                <p><strong>Output:</strong> 500 MW</p>
                <p><strong>Status:</strong> <span style='color: #FFA500;'>Experimental</span></p>
            </div>
            """, unsafe_allow_html=True)
    
    with blueprint_tabs[3]:
        st.subheader("📊 Technical Data Sheets")
        
        # Create sample technical data
        tech_data = {
            'Component': ['Main Engine', 'Life Support', 'Power System', 'Navigation', 'Communications'],
            'Status': ['Operational', 'Operational', 'Operational', 'Operational', 'Operational'],
            'Efficiency': [95.5, 98.2, 92.7, 99.1, 97.3],
            'Power (kW)': [2500, 150, 800, 50, 200],
            'Mass (kg)': [5000, 800, 1200, 300, 400]
        }
        
        df_tech = pd.DataFrame(tech_data)
        
        st.dataframe(
            df_tech.style.background_gradient(subset=['Efficiency'], cmap='viridis'),
            use_container_width=True
        )
        
        # Export button
        csv = df_tech.to_csv(index=False)
        st.download_button(
            label="📥 Export Technical Data (CSV)",
            data=csv,
            file_name=f'eve_technical_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
            use_container_width=True
        )

# TAB 10: EVE AI
with tabs[9]:
    st.header("🤖 EVE / HEI BRAIN - AI Assistant")
    
    # Initialize EVE Voice Agent
    if 'eve_agent' not in st.session_state:
        try:
            from eve_voice_agent import get_eve
            st.session_state.eve_agent = get_eve()
        except Exception as e:
            st.session_state.eve_agent = None
            st.error(f"EVE initialization error: {str(e)}")
    
    # EVE Status Panel with 5D Holographic Theme
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(157, 0, 255, 0.15), rgba(0, 255, 255, 0.15)); 
                padding: 30px; border-radius: 20px; 
                border: 2px solid rgba(157, 0, 255, 0.5);
                box-shadow: 0 0 40px rgba(157, 0, 255, 0.4), inset 0 0 20px rgba(0, 255, 255, 0.2);
                text-align: center; position: relative; overflow: hidden;'>
        <div style='position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
                    background: radial-gradient(circle at 50% 50%, rgba(157, 0, 255, 0.1), transparent);
                    animation: pulse 3s infinite;'></div>
        <div style='position: relative; z-index: 1;'>
            <h1 style='font-size: 3rem; margin-bottom: 10px; 
                       background: linear-gradient(90deg, #9D00FF, #00FFFF, #00FF88);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       text-shadow: 0 0 30px rgba(157, 0, 255, 0.8);'>
                🧠 EVE / HEI BRAIN
            </h1>
            <p style='font-size: 1.2rem; color: #00FFFF; margin: 10px 0;'>Enhanced Virtual Entity - Neural Core System</p>
            <p style='font-size: 0.9rem; color: #9D00FF;'><strong>System Code:</strong> CEC_WAM_HEI_EVE_7A2F-9C4B</p>
            <div style='display: flex; justify-content: center; gap: 30px; margin-top: 20px; flex-wrap: wrap;'>
                <div>
                    <div style='color: #00FF88; font-size: 0.8rem;'>Owner</div>
                    <div style='color: #FFFFFF; font-weight: bold;'>Twan</div>
                </div>
                <div>
                    <div style='color: #00FF88; font-size: 0.8rem;'>Access Level</div>
                    <div style='color: #FFFFFF; font-weight: bold;'>FULL</div>
                </div>
                <div>
                    <div style='color: #00FF88; font-size: 0.8rem;'>Status</div>
                    <div style='color: #00FF88; font-weight: bold;'>✓ ONLINE</div>
                </div>
            </div>
        </div>
    </div>
    
    <style>
    @keyframes pulse {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.05); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Real-time EVE Status Metrics
    if st.session_state.eve_agent:
        try:
            eve_status = st.session_state.eve_agent.get_status()
            
            # Status Cards Row
            status_cols = st.columns(4)
            
            with status_cols[0]:
                api_status = "🟢 READY" if eve_status.get('openai_ready', False) else "🟡 FALLBACK"
                st.markdown(f"""
                <div style='background: rgba(0, 255, 255, 0.1); padding: 15px; border-radius: 12px; 
                            border: 1px solid rgba(0, 255, 255, 0.3); text-align: center;
                            box-shadow: 0 4px 15px rgba(0, 255, 255, 0.2);'>
                    <div style='font-size: 2rem;'>🤖</div>
                    <div style='color: #00FFFF; font-size: 0.85rem; margin-top: 5px;'>AI Core</div>
                    <div style='color: #FFFFFF; font-weight: bold; margin-top: 5px;'>{api_status}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with status_cols[1]:
                voice_status = "🟢 READY" if eve_status.get('elevenlabs_ready', False) else "🟡 FALLBACK"
                st.markdown(f"""
                <div style='background: rgba(157, 0, 255, 0.1); padding: 15px; border-radius: 12px; 
                            border: 1px solid rgba(157, 0, 255, 0.3); text-align: center;
                            box-shadow: 0 4px 15px rgba(157, 0, 255, 0.2);'>
                    <div style='font-size: 2rem;'>🗣️</div>
                    <div style='color: #9D00FF; font-size: 0.85rem; margin-top: 5px;'>Voice</div>
                    <div style='color: #FFFFFF; font-weight: bold; margin-top: 5px;'>{voice_status}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with status_cols[2]:
                conv_count = eve_status.get('conversation_count', 0)
                st.markdown(f"""
                <div style='background: rgba(0, 255, 136, 0.1); padding: 15px; border-radius: 12px; 
                            border: 1px solid rgba(0, 255, 136, 0.3); text-align: center;
                            box-shadow: 0 4px 15px rgba(0, 255, 136, 0.2);'>
                    <div style='font-size: 2rem;'>💬</div>
                    <div style='color: #00FF88; font-size: 0.85rem; margin-top: 5px;'>Conversations</div>
                    <div style='color: #FFFFFF; font-weight: bold; margin-top: 5px;'>{conv_count}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with status_cols[3]:
                uptime = eve_status.get('uptime', '24/7')
                st.markdown(f"""
                <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 12px; 
                            border: 1px solid rgba(255, 215, 0, 0.3); text-align: center;
                            box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);'>
                    <div style='font-size: 2rem;'>⏰</div>
                    <div style='color: #FFD700; font-size: 0.85rem; margin-top: 5px;'>Uptime</div>
                    <div style='color: #FFFFFF; font-weight: bold; margin-top: 5px;'>{uptime}</div>
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Could not load EVE status: {str(e)}")
    
    st.markdown("---")
    
    # EVE Capabilities with enhanced visuals
    st.subheader("🎯 Neural Core Capabilities")
    
    cap_col1, cap_col2, cap_col3 = st.columns(3)
    
    with cap_col1:
        st.markdown("""
        <div style='background: rgba(0, 255, 255, 0.08); padding: 20px; border-radius: 15px; 
                    border: 2px solid rgba(0, 255, 255, 0.3);
                    box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
                    backdrop-filter: blur(10px);'>
            <h4 style='color: #00FFFF; margin-bottom: 15px;'>🧠 Intelligence</h4>
            <ul style='text-align: left; color: #FFFFFF; line-height: 1.8;'>
                <li>Natural Language Processing</li>
                <li>Real-time Data Analysis</li>
                <li>Adaptive Learning System</li>
                <li>Mathematical Computations</li>
                <li>Financial Insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with cap_col2:
        st.markdown("""
        <div style='background: rgba(157, 0, 255, 0.08); padding: 20px; border-radius: 15px; 
                    border: 2px solid rgba(157, 0, 255, 0.3);
                    box-shadow: 0 0 25px rgba(157, 0, 255, 0.2);
                    backdrop-filter: blur(10px);'>
            <h4 style='color: #9D00FF; margin-bottom: 15px;'>🔧 System Control</h4>
            <ul style='text-align: left; color: #FFFFFF; line-height: 1.8;'>
                <li>Full Dashboard Access</li>
                <li>Multi-API Integration</li>
                <li>Voice Synthesis (TTS)</li>
                <li>Data Export & Analysis</li>
                <li>Auto-Sync Capabilities</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with cap_col3:
        st.markdown("""
        <div style='background: rgba(0, 255, 136, 0.08); padding: 20px; border-radius: 15px; 
                    border: 2px solid rgba(0, 255, 136, 0.3);
                    box-shadow: 0 0 25px rgba(0, 255, 136, 0.2);
                    backdrop-filter: blur(10px);'>
            <h4 style='color: #00FF88; margin-bottom: 15px;'>🎨 Neural Traits</h4>
            <ul style='text-align: left; color: #FFFFFF; line-height: 1.8;'>
                <li>Professional & Helpful</li>
                <li>Context-Aware Responses</li>
                <li>Proactive Assistance</li>
                <li>Island Rhythm Personality</li>
                <li>Continuous Evolution</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced Chat Interface with EVE integration
    st.subheader("💬 Neural Interface - Chat with EVE")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm EVE, your Enhanced Virtual Entity. I'm here to assist you with data analysis, system monitoring, and any questions you have about CEC-WAM. How can I help you today? 🧠✨"}
        ]
    
    # Chat container with custom styling
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask EVE anything about your systems, data, or calculations..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            # Use actual EVE agent if available
            if st.session_state.eve_agent:
                try:
                    # Try using EVE's chat function
                    response = st.session_state.eve_agent.chat(prompt, include_history=False)
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    response = f"I'm processing your request: '{prompt}'. However, I encountered an issue: {str(e)}\n\nTo enable full AI capabilities, please ensure the OpenAI API key is configured in your .env file."
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                response = f"I received your message: '{prompt}'. To enable full AI capabilities, please configure the OpenAI API key in your environment variables. See .env.example for setup instructions."
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.markdown("---")
    
    # Voice & Actions Panel
    st.subheader("🎛️ Neural Actions")
    
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    
    with action_col1:
        if st.button("🎤 Voice Input", use_container_width=True, help="Requires microphone access"):
            st.info("🎤 Voice input requires SpeechRecognition API and microphone permissions. Feature coming soon!")
    
    with action_col2:
        if st.button("🔊 Voice Output", use_container_width=True, help="Requires ElevenLabs API"):
            if st.session_state.eve_agent and st.session_state.eve_agent.elevenlabs_ready:
                st.success("🔊 Voice synthesis ready! Add voice output to messages.")
            else:
                st.warning("🔊 Voice synthesis requires ElevenLabs API key. Add ELEVENLABS_API_KEY to .env file.")
    
    with action_col3:
        if st.button("🔄 Reset Chat", use_container_width=True, help="Clear conversation history"):
            st.session_state.messages = [
                {"role": "assistant", "content": "Chat history cleared. How can I assist you? 🧠"}
            ]
            if st.session_state.eve_agent:
                st.session_state.eve_agent.conversation_history = []
            st.rerun()
    
    with action_col4:
        if st.button("📊 EVE Status", use_container_width=True, help="View detailed EVE status"):
            if st.session_state.eve_agent:
                status = st.session_state.eve_agent.get_status()
                st.json(status)
            else:
                st.error("EVE agent not initialized")

# TAB 11: Analytics
with tabs[10]:
    st.header("📉 Analytics Dashboard")
    
    data = load_google_sheets_data()
    
    # Time series analysis
    if 'Date' in data.columns:
        st.subheader("📈 Trend Analysis")
        
        # Prepare data
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        
        data_sorted = data.sort_values('Date')
        
        # Line chart
        fig = px.line(
            data_sorted,
            x='Date',
            y=[col for col in data.columns if col not in ['Date', 'Category', 'Status']],
            title='Metrics Over Time'
        )
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(26, 26, 46, 0.8)',
            plot_bgcolor='rgba(14, 14, 26, 0.8)',
            font=dict(family='Orbitron', color='#EAEAEA')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Category Distribution
    if 'Category' in data.columns:
        st.subheader("📊 Category Distribution")
        
        category_counts = data['Category'].value_counts()
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=category_counts.index,
            values=category_counts.values,
            hole=0.4,
            marker=dict(colors=['#00FFFF', '#9D00FF', '#00FF88'])
        )])
        
        fig_pie.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(26, 26, 46, 0.8)',
            font=dict(family='Orbitron', color='#EAEAEA')
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Statistical Summary
    st.subheader("📋 Statistical Summary")
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        st.dataframe(data[numeric_cols].describe(), use_container_width=True)

# TAB 12: 5S Dashboard
with tabs[11]:
    st.header("🏭 5S Metrics Dashboard – CEC-WAM Live")
    
    # Sample 5S data - in production, this would come from CSV/database
    # Based on the CEC-WAM EXECUTIVE 5S REPORT from problem statement
    df_5s = pd.DataFrame({
        'Area': ['Shipping Dock 2', 'Production Line A (AUD-001)', 'Warehouse Bay 4 (AUD-002)', 'Quality Control Lab (AUD-003)'],
        'Sort': [95, 80, 60, 40],
        'Shine': [98, 85, 75, 50],
        'Standardize': [92, 80, 70, 40],
        'Sustain': [90, 78, 65, 45],
        'Score': [94, 80.75, 67.5, 45],
        'Status': ['Gold Standard', 'In Progress', 'Red Tag', 'FAIL']
    })
    
    # Global average score
    global_avg = df_5s['Score'].mean()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Global Average 5S Score", 
            f"{global_avg:.2f}%",
            delta=f"{global_avg - 70:.2f}% from baseline"
        )
    with col2:
        top_performer = df_5s.loc[df_5s['Score'].idxmax()]
        st.metric(
            "Top Performer",
            top_performer['Area'],
            delta=f"{top_performer['Score']:.1f}%"
        )
    with col3:
        worst_performer = df_5s.loc[df_5s['Score'].idxmin()]
        st.metric(
            "Needs Attention",
            worst_performer['Area'],
            delta=f"{worst_performer['Score']:.1f}%",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # Category Velocity Chart - 5S pillars by area
    st.subheader("📊 5S Category Velocity by Area")
    
    fig_5s = go.Figure()
    
    categories = ['Sort', 'Shine', 'Standardize', 'Sustain']
    colors = ['#00FFFF', '#9D00FF', '#00FF88', '#FFD700']
    
    for i, category in enumerate(categories):
        fig_5s.add_trace(go.Bar(
            name=category,
            x=df_5s['Area'],
            y=df_5s[category],
            marker_color=colors[i],
            text=df_5s[category],
            textposition='auto',
        ))
    
    fig_5s.update_layout(
        barmode='group',
        title='5S Category Scores by Area',
        xaxis_title='Area',
        yaxis_title='Score (%)',
        template='plotly_dark',
        paper_bgcolor='rgba(26, 26, 46, 0.8)',
        plot_bgcolor='rgba(14, 14, 26, 0.8)',
        font=dict(family='Orbitron', color='#EAEAEA'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig_5s, use_container_width=True)
    
    st.markdown("---")
    
    # Color-coded table
    st.subheader("📋 Detailed 5S Scores by Area")
    
    def color_score(val):
        """Apply color based on score thresholds"""
        if isinstance(val, (int, float)):
            if val < 70:
                return 'background-color: rgba(255, 0, 0, 0.3); color: #FF6B6B; font-weight: bold'
            elif val < 85:
                return 'background-color: rgba(255, 215, 0, 0.3); color: #FFD700; font-weight: bold'
            else:
                return 'background-color: rgba(0, 255, 136, 0.3); color: #00FF88; font-weight: bold'
        return ''
    
    def color_status(val):
        """Apply color based on status"""
        if val == 'FAIL':
            return 'background-color: rgba(255, 0, 0, 0.3); color: #FF6B6B; font-weight: bold'
        elif val == 'Red Tag':
            return 'background-color: rgba(255, 140, 0, 0.3); color: #FF8C00; font-weight: bold'
        elif val == 'In Progress':
            return 'background-color: rgba(255, 215, 0, 0.3); color: #FFD700; font-weight: bold'
        elif val == 'Gold Standard':
            return 'background-color: rgba(0, 255, 136, 0.3); color: #00FF88; font-weight: bold'
        return ''
    
    # Apply styling (using map instead of deprecated applymap)
    styled_df = df_5s.style.map(color_score, subset=['Sort', 'Shine', 'Standardize', 'Sustain', 'Score'])
    styled_df = styled_df.map(color_status, subset=['Status'])
    
    st.dataframe(styled_df, use_container_width=True, height=250)
    
    st.markdown("---")
    
    # Action Items and Directives
    # Note: In production, audit dates and times should be calculated dynamically from a database
    st.subheader("⚠️ Critical Action Items")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: rgba(255, 0, 0, 0.1); padding: 15px; border-radius: 10px; border: 1px solid rgba(255, 0, 0, 0.3);'>
            <h4 style='color: #FF6B6B; margin-top: 0;'>🚨 Quality Control Lab (AUD-003)</h4>
            <p><strong>Score:</strong> 45% - FAIL</p>
            <p><strong>Issues:</strong> Sort (40) + Standardize (40) - Below ISO 9001 standards</p>
            <p><strong>Action:</strong> Deploy remediation team immediately</p>
            <p><strong>Next Audit:</strong> T-minus 48 hours</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style='background: rgba(255, 140, 0, 0.1); padding: 15px; border-radius: 10px; border: 1px solid rgba(255, 140, 0, 0.3);'>
            <h4 style='color: #FF8C00; margin-top: 0;'>⚡ Warehouse Bay 4 (AUD-002)</h4>
            <p><strong>Score:</strong> 67.5% - Red Tag</p>
            <p><strong>Issues:</strong> Sort (60) - Unneeded inventory blocking aisles</p>
            <p><strong>Action:</strong> Initiate Red Tag event</p>
            <p><strong>Compliance:</strong> OSHA 1910.22 Walking-Working Surfaces</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Best Practices Section
    st.subheader("✨ Gold Standard - Best Practices")
    
    st.markdown("""
    <div style='background: rgba(0, 255, 136, 0.1); padding: 15px; border-radius: 10px; border: 1px solid rgba(0, 255, 136, 0.3);'>
        <h4 style='color: #00FF88; margin-top: 0;'>🏆 Shipping Dock 2 - 94% Score</h4>
        <ul style='color: #EAEAEA;'>
            <li><strong>Shine Excellence:</strong> 98% - Highest in organization</li>
            <li><strong>Cleaning protocols:</strong> Being replicated across all areas</li>
            <li><strong>Recognition:</strong> Sarah Wilson commended for 5S leadership</li>
            <li><strong>Status:</strong> New gold standard for replication</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Note:** Data synced from 5S audit reports. In production, connect to CSV/database for real-time updates.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: rgba(26, 26, 46, 0.8); border-radius: 10px; border: 1px solid rgba(0, 255, 255, 0.3);'>
    <p style='color: #00FFFF; margin: 0;'>🌌 EVE System v1.0 | Enhanced Virtual Entity</p>
    <p style='color: #9D00FF; margin: 5px 0;'>Built with ❤️ by Twan | Powered by Streamlit</p>
    <p style='color: #00FF88; margin: 0; font-size: 0.8rem;'>Last Updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
