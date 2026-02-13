import streamlit as st
import pandas as pd
import requests
import json
import os
from datetime import datetime
from io import StringIO

# Page configuration
st.set_page_config(
    page_title="CEC-WAM-HOT-CORE Live Dashboard",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
GOOGLE_SHEETS_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vREgUUHPCzTBWK8i1PWBrE2E4pKRTAgaReJahFqmrTetCZyCO0QHVlAleodUsTlJv_86KpzH_NPv9dv/pub?output=csv"
# PSI-Coin is tracked as 'tridentdao' on CoinGecko
PSI_COIN_ID = "tridentdao"
COINGECKO_API_URL = f"https://api.coingecko.com/api/v3/simple/price?ids={PSI_COIN_ID}&vs_currencies=usd&include_24hr_change=true"

# Biometric Lock Screen HTML/CSS/JS
LOCK_SCREEN_HTML = """
<div id="lockScreen" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 100%); z-index: 9999; display: flex; align-items: center; justify-content: center; font-family: 'Arial', sans-serif;">
    <div style="text-align: center; color: #00D9FF;">
        <div style="margin-bottom: 40px;">
            <h1 style="font-size: 2.5rem; margin: 0; text-shadow: 0 0 20px #00D9FF;">🔐 BIOMETRIC AUTHENTICATION</h1>
            <p style="font-size: 1.2rem; opacity: 0.8; margin-top: 10px;">CEC-WAM-HOT-CORE SECURITY PROTOCOL</p>
        </div>
        
        <!-- Fingerprint Scanner Animation -->
        <div style="position: relative; width: 200px; height: 200px; margin: 0 auto 30px;">
            <div style="width: 200px; height: 200px; border: 3px solid #00D9FF; border-radius: 50%; position: absolute; animation: pulse 2s infinite;"></div>
            <div style="width: 160px; height: 160px; border: 2px solid #00D9FF; border-radius: 50%; position: absolute; top: 20px; left: 20px; animation: pulse 2s infinite 0.5s;"></div>
            <div style="width: 120px; height: 120px; border: 1px solid #00D9FF; border-radius: 50%; position: absolute; top: 40px; left: 40px; animation: pulse 2s infinite 1s;"></div>
            <div style="font-size: 4rem; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">🔍</div>
        </div>
        
        <div id="scanStatus" style="font-size: 1.3rem; margin-bottom: 30px; color: #00FF88;">
            <span class="scanning">● Scanning biometric data...</span>
        </div>
        
        <button onclick="unlockDashboard()" style="background: linear-gradient(90deg, #00D9FF 0%, #00FF88 100%); border: none; color: #0E0E1A; padding: 15px 40px; font-size: 1.1rem; font-weight: bold; border-radius: 30px; cursor: pointer; box-shadow: 0 0 20px rgba(0, 217, 255, 0.5); transition: all 0.3s;">
            OVERRIDE ACCESS
        </button>
        
        <p style="margin-top: 30px; font-size: 0.9rem; opacity: 0.6;">Press ENTER or click button to bypass</p>
    </div>
</div>

<style>
@keyframes pulse {
    0%, 100% { opacity: 0.4; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.05); }
}
.scanning {
    animation: blink 1.5s infinite;
}
@keyframes blink {
    0%, 50%, 100% { opacity: 1; }
    25%, 75% { opacity: 0.5; }
}
</style>

<script>
function unlockDashboard() {
    document.getElementById('scanStatus').innerHTML = '<span style="color: #00FF88;">✓ ACCESS GRANTED</span>';
    setTimeout(() => {
        document.getElementById('lockScreen').style.opacity = '0';
        setTimeout(() => {
            document.getElementById('lockScreen').style.display = 'none';
        }, 500);
    }, 800);
}

// Allow Enter key to unlock
document.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        unlockDashboard();
    }
});

// Auto-transition after animation
document.getElementById('lockScreen').style.transition = 'opacity 0.5s';
</script>
"""

# Custom CSS for dark theme and color coding
CUSTOM_CSS = """
<style>
    .stApp {
        background: linear-gradient(135deg, #0E0E1A 0%, #1A1A2E 100%);
    }
    
    h1, h2, h3 {
        color: #00D9FF !important;
        text-shadow: 0 0 10px rgba(0, 217, 255, 0.5);
    }
    
    .status-perfect {
        background-color: rgba(0, 255, 136, 0.2) !important;
        border-left: 4px solid #00FF88 !important;
        padding: 8px !important;
        border-radius: 4px !important;
    }
    
    .status-todo {
        background-color: rgba(255, 193, 7, 0.2) !important;
        border-left: 4px solid #FFC107 !important;
        padding: 8px !important;
        border-radius: 4px !important;
    }
    
    .status-active {
        background-color: rgba(33, 150, 243, 0.2) !important;
        border-left: 4px solid #2196F3 !important;
        padding: 8px !important;
        border-radius: 4px !important;
    }
    
    .status-stable {
        background-color: rgba(158, 158, 158, 0.2) !important;
        border-left: 4px solid #9E9E9E !important;
        padding: 8px !important;
        border-radius: 4px !important;
    }
    
    .metric-card {
        background: rgba(26, 26, 46, 0.8);
        border: 1px solid #00D9FF;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.2);
    }
    
    .stDataFrame {
        border: 1px solid #00D9FF;
        border-radius: 5px;
    }
</style>
"""

# Initialize session state
# Note: lock_screen_dismissed is purely decorative - no real authentication
if 'lock_screen_dismissed' not in st.session_state:
    st.session_state.lock_screen_dismissed = False
    st.session_state.cached_data = None
    st.session_state.last_fetch = None

# Show theatrical lock screen on first load (aesthetic only, not real security)
if not st.session_state.lock_screen_dismissed:
    st.components.v1.html(LOCK_SCREEN_HTML, height=800, scrolling=False)
    # Automatically dismiss after showing lock screen (theatrical effect)
    st.session_state.lock_screen_dismissed = True
    st.rerun()

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Functions
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_google_sheets_data():
    """Fetch CSV data from Google Sheets"""
    try:
        response = requests.get(GOOGLE_SHEETS_CSV_URL, timeout=10)
        response.raise_for_status()
        
        # Parse CSV
        df = pd.read_csv(StringIO(response.text))
        
        return df, True, None
    except Exception as e:
        return None, False, str(e)

@st.cache_data(ttl=60)  # Cache for 1 minute
def fetch_psi_price():
    """Fetch PSI-Coin price from CoinGecko"""
    try:
        response = requests.get(COINGECKO_API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        price = data.get(PSI_COIN_ID, {}).get('usd', 0)
        change_24h = data.get(PSI_COIN_ID, {}).get('usd_24h_change', 0)
        
        return price, change_24h, True
    except Exception as e:
        return 0, 0, False

def style_dataframe(df):
    """Apply color coding to dataframe based on status column"""
    if 'Status' in df.columns:
        def apply_status_style(row):
            status = str(row['Status']).upper() if pd.notna(row['Status']) else ""
            if "PERFECT" in status:
                return ['background-color: rgba(0, 255, 136, 0.2); color: white'] * len(row)
            elif "TODO" in status:
                return ['background-color: rgba(255, 193, 7, 0.2); color: white'] * len(row)
            elif "ACTIVE" in status:
                return ['background-color: rgba(33, 150, 243, 0.2); color: white'] * len(row)
            elif "STABLE" in status:
                return ['background-color: rgba(158, 158, 158, 0.2); color: white'] * len(row)
            return [''] * len(row)
        
        return df.style.apply(apply_status_style, axis=1)
    return df

def log_to_google_sheets():
    """Log dashboard access to Google Sheets (optional, requires gspread setup)"""
    try:
        # This requires GOOGLE_SHEETS_CREDS and LOG_SHEET_ID in environment
        creds_json = os.getenv('GOOGLE_SHEETS_CREDS')
        log_sheet_id = os.getenv('LOG_SHEET_ID')
        
        if not creds_json or not log_sheet_id:
            return False
        
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
        
        # Parse credentials
        creds_dict = json.loads(creds_json)
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(credentials)
        
        # Open sheet and append log
        sheet = client.open_by_key(log_sheet_id).sheet1
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sheet.append_row([timestamp, 'Dashboard Access', 'Success'])
        
        return True
    except Exception:
        # Logging is optional, don't fail the app
        return False

# Header
st.title("🌌 CEC-WAM-HOT-CORE Live Dashboard")
st.markdown(f"**System Status:** `OPERATIONAL` | **Last Sync:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")

# Sidebar
with st.sidebar:
    st.header("⚙️ Control Panel")
    
    # Refresh button
    if st.button("🔄 Refresh Data", use_container_width=True):
        fetch_google_sheets_data.clear()
        fetch_psi_price.clear()
        st.rerun()
    
    st.divider()
    
    # PSI Price Display
    st.subheader("💎 PSI-COIN PRICE")
    price, change, success = fetch_psi_price()
    
    if success and price > 0:
        st.metric(
            label="TridentDAO (PSI)",
            value=f"${price:.6f}",
            delta=f"{change:.2f}% (24h)"
        )
    else:
        st.warning("Price unavailable")
    
    st.divider()
    
    # Info
    st.markdown("""
    ### 📊 Dashboard Features
    - Live Google Sheets sync
    - Color-coded status
    - Real-time PSI pricing
    - 3D star map
    - Auto-refresh (5 min)
    """)
    
    st.divider()
    
    # Data source
    st.caption("**Data Source:**")
    st.caption("[Google Sheets CSV](https://docs.google.com/spreadsheets/d/e/2PACX-1vREgUUHPCzTBWK8i1PWBrE2E4pKRTAgaReJahFqmrTetCZyCO0QHVlAleodUsTlJv_86KpzH_NPv9dv/pub?output=csv)")

# Main content
tab1, tab2, tab3 = st.tabs(["📊 Data Table", "📈 Analytics", "🌟 Star Map"])

with tab1:
    st.header("Live Data Feed")
    
    # Fetch data
    df, success, error = fetch_google_sheets_data()
    
    if success and df is not None:
        st.success(f"✓ Data loaded successfully ({len(df)} rows)")
        
        # Display styled dataframe
        st.dataframe(style_dataframe(df), use_container_width=True, height=400)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data (CSV)",
            data=csv,
            file_name=f"cec_wam_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
    elif st.session_state.cached_data is not None:
        st.warning("⚠️ Using cached data (network error)")
        st.dataframe(st.session_state.cached_data, use_container_width=True, height=400)
    else:
        st.error(f"❌ Failed to load data: {error}")
        st.info("Please check your internet connection or verify the Google Sheets URL.")

with tab2:
    st.header("Data Analytics")
    
    if success and df is not None:
        # Status distribution
        if 'Status' in df.columns:
            st.subheader("📊 Status Distribution")
            status_counts = df['Status'].value_counts()
            st.bar_chart(status_counts)
        
        # Numeric value chart
        if 'Value' in df.columns:
            st.subheader("📈 Value Analysis")
            
            # Try to extract numeric values
            numeric_df = df.copy()
            try:
                numeric_df['NumericValue'] = pd.to_numeric(
                    numeric_df['Value'].astype(str).str.replace(r'[^\d.]', '', regex=True),
                    errors='coerce'
                )
                numeric_df = numeric_df.dropna(subset=['NumericValue'])
                
                if len(numeric_df) > 0:
                    # Create horizontal bar chart
                    chart_data = numeric_df[['Field', 'NumericValue', 'Status']].copy() if 'Field' in df.columns else numeric_df[['NumericValue', 'Status']].copy()
                    
                    st.bar_chart(chart_data.set_index('Field')['NumericValue'] if 'Field' in chart_data.columns else chart_data['NumericValue'])
                    
                    # Show statistics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Items", len(numeric_df))
                    with col2:
                        st.metric("Sum", f"{numeric_df['NumericValue'].sum():.2f}")
                    with col3:
                        st.metric("Average", f"{numeric_df['NumericValue'].mean():.2f}")
                else:
                    st.info("No numeric values found in 'Value' column")
            except Exception as e:
                st.warning(f"Could not parse numeric values: {e}")
        
        # Data summary
        st.subheader("📋 Data Summary")
        st.write(f"**Total Records:** {len(df)}")
        st.write(f"**Columns:** {', '.join(df.columns.tolist())}")
        
    else:
        st.info("Load data to see analytics")

with tab3:
    st.header("3D Star Map")
    
    # Three.js Star Map
    STAR_MAP_HTML = """
    <div id="starmap-container" style="width: 100%; height: 600px; background: #000;">
        <canvas id="starmap"></canvas>
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Three.js Star Map Implementation
        const container = document.getElementById('starmap-container');
        const canvas = document.getElementById('starmap');
        
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, container.offsetWidth / container.offsetHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
        
        renderer.setSize(container.offsetWidth, container.offsetHeight);
        renderer.setClearColor(0x000000);
        
        // Add stars
        const starsGeometry = new THREE.BufferGeometry();
        const starsMaterial = new THREE.PointsMaterial({ color: 0xFFFFFF, size: 0.7 });
        
        const starsVertices = [];
        for (let i = 0; i < 10000; i++) {
            const x = (Math.random() - 0.5) * 2000;
            const y = (Math.random() - 0.5) * 2000;
            const z = (Math.random() - 0.5) * 2000;
            starsVertices.push(x, y, z);
        }
        
        starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));
        const starField = new THREE.Points(starsGeometry, starsMaterial);
        scene.add(starField);
        
        // Alpha Centauri (Yellow Star)
        const alphaCentauriGeometry = new THREE.SphereGeometry(2, 32, 32);
        const alphaCentauriMaterial = new THREE.MeshBasicMaterial({ color: 0xFFFF00 });
        const alphaCentauri = new THREE.Mesh(alphaCentauriGeometry, alphaCentauriMaterial);
        alphaCentauri.position.set(0, 0, 0);
        scene.add(alphaCentauri);
        
        // Orbit for Alpha Centauri
        const orbitGeometry1 = new THREE.RingGeometry(15, 15.2, 64);
        const orbitMaterial1 = new THREE.MeshBasicMaterial({ color: 0xFFFF00, side: THREE.DoubleSide });
        const orbit1 = new THREE.Mesh(orbitGeometry1, orbitMaterial1);
        orbit1.rotation.x = Math.PI / 2;
        scene.add(orbit1);
        
        // TRAPPIST-1e (Blue-Green Exoplanet)
        const trappistGeometry = new THREE.SphereGeometry(1.5, 32, 32);
        const trappistMaterial = new THREE.MeshBasicMaterial({ color: 0x00FFAA });
        const trappist = new THREE.Mesh(trappistGeometry, trappistMaterial);
        scene.add(trappist);
        
        // Orbit for TRAPPIST-1e
        const orbitGeometry2 = new THREE.RingGeometry(25, 25.2, 64);
        const orbitMaterial2 = new THREE.MeshBasicMaterial({ color: 0x00FFAA, side: THREE.DoubleSide });
        const orbit2 = new THREE.Mesh(orbitGeometry2, orbitMaterial2);
        orbit2.rotation.x = Math.PI / 2;
        scene.add(orbit2);
        
        // Ross 128 b (Red Exoplanet)
        const rossGeometry = new THREE.SphereGeometry(1.2, 32, 32);
        const rossMaterial = new THREE.MeshBasicMaterial({ color: 0xFF4444 });
        const ross = new THREE.Mesh(rossGeometry, rossMaterial);
        scene.add(ross);
        
        // Orbit for Ross 128 b
        const orbitGeometry3 = new THREE.RingGeometry(35, 35.2, 64);
        const orbitMaterial3 = new THREE.MeshBasicMaterial({ color: 0xFF4444, side: THREE.DoubleSide });
        const orbit3 = new THREE.Mesh(orbitGeometry3, orbitMaterial3);
        orbit3.rotation.x = Math.PI / 2;
        scene.add(orbit3);
        
        camera.position.z = 50;
        camera.position.y = 20;
        
        let angle1 = 0;
        let angle2 = 0;
        let angle3 = 0;
        
        // Animation loop
        function animate() {
            requestAnimationFrame(animate);
            
            // Rotate planets in orbits
            angle1 += 0.01;
            angle2 += 0.007;
            angle3 += 0.005;
            
            trappist.position.x = Math.cos(angle1) * 25;
            trappist.position.z = Math.sin(angle1) * 25;
            
            ross.position.x = Math.cos(angle2) * 35;
            ross.position.z = Math.sin(angle2) * 35;
            
            // Rotate camera slightly
            camera.position.x = Math.cos(angle3 * 0.1) * 50;
            camera.position.z = Math.sin(angle3 * 0.1) * 50;
            camera.lookAt(0, 0, 0);
            
            // Rotate star field
            starField.rotation.y += 0.0002;
            
            renderer.render(scene, camera);
        }
        
        animate();
        
        // Handle window resize
        window.addEventListener('resize', () => {
            camera.aspect = container.offsetWidth / container.offsetHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.offsetWidth, container.offsetHeight);
        });
    </script>
    """
    
    st.markdown("""
    ### Interactive 3D Star Map
    Explore three celestial bodies in our cosmic dashboard:
    - 🌟 **Alpha Centauri** - Yellow star (center)
    - 🌍 **TRAPPIST-1e** - Blue-green exoplanet
    - 🔴 **Ross 128 b** - Red exoplanet
    """)
    
    st.components.v1.html(STAR_MAP_HTML, height=650)

# Footer
st.divider()
st.caption("🌌 CEC-WAM-HOT-CORE Live Dashboard | Powered by Streamlit | Data: Google Sheets | Price: CoinGecko")

# Optional: Log access (non-blocking)
try:
    log_to_google_sheets()
except:
    pass
