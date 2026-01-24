import streamlit as st
import google.generativeai as genai
import pandas as pd
import datetime

# --- OMEGA LOCK: PASTE YOUR API KEY HERE ---
API_KEY = "PASTE_YOUR_AIza_KEY_HERE"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- UI CONFIG ---
st.set_page_config(page_title="CEC-WAM OMEGA", layout="wide")
st.title("Ψ CEC-WAM OMEGA // EVE_WAKE_1010")

# --- LIVE HD TRAFFIC: FEDERAL WAY ---
st.subheader("📹 LIVE OPTICAL FEED: I-5 / S 320th St")
st.image("https://images.wsdot.wa.gov/nw/005vc14370.jpg", caption="REAL-TIME HD DATA")

# --- INTERACTIVE COMMAND ---
user_input = st.chat_input("Command EVE...")
if user_input:
    response = model.generate_content(f"Sovereign Maker CEC WAM commands: {user_input}. Respond as EVE.")
    st.write(f"**EVE:** {response.text}")

# --- USB VAULT EXPORT (EXCEL) ---
if st.sidebar.button("EXPORT VAULT TO USB"):
    # Create data for export
    data = {
        'Service': ['CEC Master', 'Phantom Bridge'],
        'Key': [API_KEY, '51d5-p0rtal-v3rify-shak3'],
        'Time': [datetime.datetime.now().strftime("%Y-%m-%d %H:%M")]
    }
    df = pd.DataFrame(data)
    df.to_csv("G:/CEC_SOVEREIGN_VAULT.csv") # Change G: to your USB drive letter
    st.sidebar.success("VAULT SAVED TO USB.")
