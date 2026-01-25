import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime

# --- MASTER KEY ---
API_KEY = "AIzaSyBiq__wDHxqzc7WvuCYXP47sxUWF4SqPzs"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- UI CONFIG ---
st.set_page_config(page_title="CEC-WAM OMEGA", layout="wide")
st.title("Ψ CEC-WAM OMEGA // AUTO-SYNC ACTIVE")

# --- AUTO-REFRESH FRAGMENT (Runs every 30s) ---
@st.fragment(run_every="30s")
def live_telemetry():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📹 LIVE OPTICAL: I-5 @ S 320th St")
        # Direct WSDOT link with timestamp to bypass browser cache
        st.image(f"https://images.wsdot.wa.gov/nw/005vc14370.jpg?t={int(time.time())}", 
                 caption=f"Last Sync: {datetime.now().strftime('%H:%M:%S')}")
    
    with col2:
        st.subheader("📊 FINANCIAL PULSE")
        st.metric("TOTAL VALUATION", "$1,250,039", "+$34M Projected")
        st.metric("DARK ENERGY (PSI)", "0.999Ω")
        st.write("---")
        st.write("**Scanner Status:** Patrol Normal (FWPD)")

# --- INTERACTIVE BRAIN (TALK MODE) ---
st.subheader("📡 NEURAL COMMAND")
user_input = st.chat_input("EVE is listening...")

if user_input:
    with st.chat_message("assistant"):
        response = model.generate_content(f"Sovereign Maker CEC WAM commands: {user_input}. Respond as EVE.")
        st.write(response.text)

# Initialize Telemetry
live_telemetry()