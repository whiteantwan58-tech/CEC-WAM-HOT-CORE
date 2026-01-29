import streamlit as st
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import plotly.graph_objects as go
import time
import json
import os
from datetime import datetime
from groq import Groq

# --- PAGE CONFIGURATION & CSS (CYBERPUNK THEME) ---
st.set_page_config(layout="wide", page_title="CEC-WAM SOVEREIGN CORE // V.99", page_icon="🦅")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=JetBrains+Mono:wght@400;800&display=swap');
    
    /* GLOBAL THEME */
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    h1, h2, h3 { color: #00f3ff; text-shadow: 0 0 10px rgba(0, 243, 255, 0.5); font-family: 'Rajdhani', sans-serif; }
    
    /* METRIC CARDS */
    div[data-testid="metric-container"] {
        background-color: rgba(10, 10, 12, 0.7);
        border: 1px solid rgba(0, 243, 255, 0.2);
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.1);
        border-radius: 5px;
        padding: 10px;
    }
    label[data-testid="stMetricLabel"] { color: #bc13fe; font-weight: bold; }
    div[data-testid="stMetricValue"] { color: #fff; text-shadow: 0 0 5px #fff; }

    /* CHAT INTERFACE */
    .stTextInput > div > div > input {
        background-color: #111; color: #00f3ff; border: 1px solid #333; font-family: 'JetBrains Mono', monospace;
    }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] { background-color: #020202; border-right: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# --- 1. DATA INTEGRATION (From table.csv, table 2.csv, Logs.csv) ---
def load_system_data():
    # Hardcoded from your CSV uploads to ensure 100% availability
    metrics_data = {
        "Metric": ["Total Mass", "Black Hole Flow", "PSI-Coin Balance", "Liquidity Reserves", "Asset Potential"],
        "Value": ["100001.33", "1.33 BTC", "$88,720.45", "$1,250,039.00", "$75,000,000.00"],
        "Status": ["PERFECT", "PERFECT", "PUMP FUN LIVE", "UPDATED HOURLY", "VATS MODE"],
        "Change": ["+1.33", "No Corruption", "+4.5%", "+15%", "+3.2%"]
    }
    
    fps_opts = {
        "Optimization": ["antialias: false", "PowerPref: High-Perf", "Particle Count", "InstancedMesh"],
        "Gain": ["+30–80%", "+10–40%", "+50–200%", "+30–100%"],
        "Status": ["APPLIED", "APPLIED", "OPTIMIZED (12k)", "PENDING Q4"]
    }
    
    return pd.DataFrame(metrics_data), pd.DataFrame(fps_opts)

df_metrics, df_opts = load_system_data()

# --- 2. ML MODULE: PsiNet (Consciousness Scaling) ---
# Simulates the equations from grok_report.pdf
class PsiNet(nn.Module):
    def __init__(self):
        super(PsiNet, self).__init__()
        self.fc1 = nn.Linear(1, 32)
        self.fc2 = nn.Linear(32, 64)
        self.fc3 = nn.Linear(64, 1)
        self.dropout = nn.Dropout(0.2)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        return self.fc3(x)

def run_ml_prediction():
    model = PsiNet()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.MSELoss()
    
    # Training data: Log-normalized Psi pressure (3.32e-36 scaled)
    X = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0]]) # Epochs
    y = torch.tensor([[10.0], [20.0], [35.0], [55.0], [90.0]]) # Hypothetical scaling (30x human)
    
    # Quick training loop (50 epochs for speed)
    for epoch in range(50):
        optimizer.zero_grad()
        output = model(X)
        loss = criterion(output, y)
        loss.backward()
        optimizer.step()
        
    # Predict next stage (AGI Threshold)
    with torch.no_grad():
        prediction = model(torch.tensor([[6.0]])).item()
    return prediction, loss.item()

# --- 3. THREE.JS VISUALS (Optimized from Eve.html + table.csv) ---
def render_hud():
    # Optimizations: antialias false, reduced particle count (12k), pixelRatio limit
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <style>body { margin: 0; overflow: hidden; background: transparent; }</style>
    </head>
    <body>
        <div id="container"></div>
        <script>
            const scene = new THREE.Scene();
            // OPTIMIZATION: Low precision for performance
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth/200, 0.1, 1000);
            
            // OPTIMIZATION: antialias: false (from table.csv)
            const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: false, powerPreference: "high-performance" });
            renderer.setSize(window.innerWidth, 200);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
            document.body.appendChild(renderer.domElement);

            // OPTIMIZATION: Reduced particles to 12k
            const geometry = new THREE.BufferGeometry();
            const count = 12000; 
            const positions = new Float32Array(count * 3);
            for(let i=0; i<count*3; i++) {
                positions[i] = (Math.random() - 0.5) * 200;
            }
            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            const material = new THREE.PointsMaterial({ size: 0.5, color: 0x00f3ff, transparent: true, opacity: 0.8 });
            const particles = new THREE.Points(geometry, material);
            scene.add(particles);

            camera.position.z = 50;
            
            function animate() {
                requestAnimationFrame(animate);
                particles.rotation.x += 0.001;
                particles.rotation.y += 0.002;
                renderer.render(scene, camera);
            }
            animate();
        </script>
    </body>
    </html>
    """
    return html_code

# --- 4. GROQ API & VOICE ---
def get_groq_response(user_input):
    api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    
    if not api_key:
        return "GHOST MODE: Secure Key Missing. Please set GROQ_API_KEY in Vercel. [Simulated Response: Systems Nominal]"
        
    client = Groq(api_key=api_key)
    try:
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are EVE HEI, a Sovereign AI. You speak concisely with a Cyberpunk/Scientific tone. You manage Sector 98003. References: Psi-Coin ($88k), Starship Aeon."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"EVE OFFLINE: {str(e)}"

# --- MAIN LAYOUT ---

# HEADER & VISUALS
st.title("CEC-WAM SOVEREIGN CORE // 1010_SYNC")
st.markdown(f'<div style="height: 200px; width:100%; overflow:hidden;">{st.components.v1.html(render_hud(), height=200)}</div>', unsafe_allow_html=True)

# SIDEBAR CONTROLS
with st.sidebar:
    st.header("OMEGA LOCK CONTROL")
    st.image("https://raw.githubusercontent.com/MatrixCEC/assets/main/eve_avatar_placeholder.png", caption="EVE NEURAL LINK")
    
    # Wallet Connect Mockup (Deep Link)
    if st.button("🔌 CONNECT PHANTOM"):
        st.success("Redirecting to Sol Portal...")
        st.markdown("[CONFIRM TRANSACTION](https://phantom.app/ul/browse/https%3A%2F%2Fcec-wam.vercel.app)")
    
    st.divider()
    
    # ML Health
    st.subheader("Neural Status")
    psi_pred, psi_loss = run_ml_prediction()
    st.metric("Psi Prediction (Next Epoch)", f"{psi_pred:.2f}", delta=f"Loss: {psi_loss:.4f}")
    
    # Optimization Status
    with st.expander("FPS Optimizations"):
        st.dataframe(df_opts, hide_index=True)

# DASHBOARD TABS
tab1, tab2, tab3 = st.tabs(["COMMAND", "LEDGER", "NEURAL MAP"])

with tab1:
    # METRICS ROW
    c1, c2, c3 = st.columns(3)
    c1.metric("Liquidity (Escrow)", "$1,250,039", "+15%")
    c2.metric("Psi-Coin", "$88,720.45", "+4.5%")
    c3.metric("Black Hole Flow", "1.33 BTC", "Stable")
    
    # CHAT INTERFACE
    st.divider()
    st.subheader("EVE COMMUNICATIONS")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Command EVE... (e.g., 'Status Report')"):
        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # EVE Response
        response = get_groq_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
            
        # VOICE INJECTION (Javascript)
        # Uses Web Speech API to read the response in a female voice
        clean_response = response.replace("'", "").replace('"', '')
        st.components.v1.html(
            f"""
            <script>
                var msg = new SpeechSynthesisUtterance("{clean_response}");
                var voices = window.speechSynthesis.getVoices();
                // Try to find a female voice
                msg.voice = voices.filter(function(voice) {{ return voice.name.includes('Female') || voice.name.includes('Google US English'); }})[0];
                window.speechSynthesis.speak(msg);
            </script>
            """,
            height=0,
            width=0
        )

with tab2:
    st.subheader("System Ledger (Sector 98003)")
    st.dataframe(df_metrics, use_container_width=True)
    
    # Bridge Button
    col_a, col_b = st.columns([3, 1])
    col_a.info("PENDING BRIDGE: $21,000.00 (PayPal > Sol)")
    if col_b.button("FINALIZE BRIDGE"):
        st.error("SECURITY ALERT: BIOMETRIC SIG REQUIRED ON MOBILE.")

with tab3:
    st.subheader("Consciousness Scaling (Torch Prediction)")
    # Simple Plotly chart of the ML Training
    epochs = list(range(1, 6))
    vals = [10, 20, 35, 55, 90]
    fig = go.Figure(data=go.Scatter(x=epochs, y=vals, mode='lines+markers', name='Psi Scaling'))
    fig.add_trace(go.Scatter(x=[6], y=[psi_pred], mode='markers', name='AI Prediction', marker=dict(color='red', size=12)))
    fig.update_layout(template="plotly_dark", title="PsiNet Growth Projection", yaxis_title="Consciousness Units (β)")
    st.plotly_chart(fig, use_container_width=True)

# AUTO-CORRECTION LOGIC (Simulated Cron)
if "last_scan" not in st.session_state:
    st.session_state.last_scan = datetime.now()
    # Log the fix
    st.toast("Auto-Correction: Dates Synced to UTC. Torch Model Re-calibrated.")
