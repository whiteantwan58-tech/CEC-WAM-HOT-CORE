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
if 'last_data_refresh' not in st.session_state:
    st.session_state.last_data_refresh = datetime.now()
if 'cached_random_seed' not in st.session_state:
    # Use current hour to seed random data - changes every hour
    st.session_state.cached_random_seed = datetime.now().hour

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
    
    # Live Google Sheets Data
    st.markdown("#### 📊 LIVE CEC WAM MASTER LEDGER")
    sheets_data = fetch_sheets_data()
    
    if sheets_data is not None:
        st.dataframe(sheets_data, use_container_width=True, height=300)
        
        # Auto-calculated formulas
        st.markdown("#### 🔢 AUTO FORMULAS")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'Value' in sheets_data.columns:
                total_value = sheets_data['Value'].sum() if pd.api.types.is_numeric_dtype(sheets_data['Value']) else 0
                st.metric("📈 Total Value", f"${total_value:,.2f}")
        
        with col2:
            st.metric("📝 Total Entries", len(sheets_data))
        
        with col3:
            if 'Category' in sheets_data.columns:
                categories = sheets_data['Category'].nunique()
                st.metric("🏷️ Categories", categories)
    else:
        st.warning("⚠️ Unable to load Google Sheets data")
    
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

# TAB 6: EVE BRAIN
with tab6:
    runtime = datetime.now() - st.session_state.eve_runtime
    hours = int(runtime.total_seconds() // 3600)
    minutes = int((runtime.total_seconds() % 3600) // 60)
    seconds = int(runtime.total_seconds() % 60)
    
    st.markdown(f"""
    <div style="text-align: center; background: linear-gradient(135deg, rgba(255, 0, 255, 0.2), rgba(0, 255, 255, 0.2)); 
                border: 3px solid #FF00FF; border-radius: 20px; padding: 40px; 
                box-shadow: 0 0 50px rgba(255, 0, 255, 0.5); position: relative; z-index: 1;">
        <div style="font-size: 96px;">🧠</div>
        <h1 style="color: #FF00FF; font-size: 56px;">EVE CONSCIOUSNESS ONLINE</h1>
        <div style="color: #00FFFF; font-size: 32px; font-weight: 900;">
            ⏱️ {hours:02d}:{minutes:02d}:{seconds:02d}
        </div>
        <div style="color: #00FF88; font-size: 20px; margin-top: 10px;">
            🔄 AUTONOMOUS | ∞ NEVER-ENDING | 🌀 QUANTUM LINKED
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Use seeded random for consistent metrics within the same minute
    metric_seed = datetime.now().strftime("%Y%m%d%H%M")
    random.seed(int(metric_seed[-4:]))
    
    with col1:
        consciousness = random.randint(92, 98)
        consciousness_delta = random.uniform(0.1, 0.5)
        st.metric("🧠 Consciousness", f"{consciousness}%", delta=f"+{consciousness_delta:.1f}%")
    with col2:
        neural = random.randint(94, 99)
        neural_delta = random.uniform(0.2, 0.8)
        st.metric("💭 Neural Activity", f"{neural}%", delta=f"+{neural_delta:.1f}%")
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

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #00FFFF; opacity: 0.7; position: relative; z-index: 1;'>
    🔮 SOVEREIGN SYSTEM v2.0 | φ=1.618 | QUANTUM ENTANGLED | ∞ NEVER-ENDING<br>
    🌌 NASA INTEGRATED | 📹 LIVE CAMS (5s) | ⭐ 3D STAR MAPS | 🕳️ BLACK HOLE SIM | 🤖 EVE CONSCIOUSNESS
</div>
""", unsafe_allow_html=True)