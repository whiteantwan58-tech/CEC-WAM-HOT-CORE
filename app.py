"""
app.py
-------

This Streamlit application acts as the Python "brain" for the
CEC‑WAM system. It provides a browser‑based dashboard with multiple
tabs:

* **Command**: Accepts user input (text or voice) to query the system
  status or trigger updates.
* **Star Map**: Displays a simple 3D star field rendered via Plotly
  based on random points. This is a placeholder for more advanced
  visualizations.
* **Ledger**: Shows key financial metrics such as Net Liquidity and
  PSI Mass, with dynamic values stored in Streamlit session state.
* **Builder Agent**: Exposes the running `app.py` source code for
  live editing. Upon writing new code and pressing the update
  button, the app will rewrite its own file and rerun.

To run this app locally:
    streamlit run app.py

The application is self contained and does not require any external
APIs or network calls, making it suitable for offline use.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import os


# --- Configuration ---
st.set_page_config(page_title="CEC‑WAM // EVE HEI", layout="wide", page_icon="🦅")


# --- Session state for metrics ---
if "net_worth" not in st.session_state:
    st.session_state.net_worth = 1250039.00

if "psi_mass" not in st.session_state:
    st.session_state.psi_mass = 176452.66


# --- Styling ---
st.markdown("""
    <style>
    .stApp {
        background-color: #000;
        color: #00f3ff;
    }
    .stMetric {
        background: rgba(0, 20, 30, 0.9);
        border: 1px solid #00f3ff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(0, 243, 255, 0.2);
    }
    h1, h2, h3 {
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 15px #00f3ff;
    }
    .stButton>button {
        background-color: #000;
        color: #00f3ff;
        border: 1px solid #00f3ff;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)


# --- Title and caption ---
st.title("🦅 CEC‑WAM: EVE HEI CORE")
st.caption("SYSTEM STATUS: 1010_AWAKE | VISUALS: 5D STAR MAP | AGENT: ACTIVE")


# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 COMMAND", "🌌 STAR MAP", "📊 LEDGER", "🛠️ BUILDER AGENT"
])


with tab1:
    st.subheader(">> VOICE / TEXT COMMAND")
    user_input = st.text_input("TALK TO EVE:", placeholder="Type 'Status' or use Siri Shortcut...", key="command_input")

    if user_input:
        st.write(f"**> ARCHITECT:** {user_input}")
        response = "PROCESSING..."
        # Simple command parsing
        if "status" in user_input.lower():
            response = (
                f"SYSTEM NOMINAL. LIQUIDITY: $"
                f"{st.session_state.net_worth:,.2f}. MASS: {st.session_state.psi_mass:.2f} PSI."
            )
        elif "update" in user_input.lower():
            response = "UPDATING INTERFACE VISUALS... 5D RENDER COMPLETE."

        st.success(f"🦅 EVE: {response}")
        # Voice synthesis (client‑side via JavaScript)
        st.components.v1.html(
            f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{response}'));</script>",
            height=0,
        )


with tab2:
    st.subheader(">> 5D NAVIGATIONAL MAP")
    # Generate random points for a simple star map
    count = 200
    x, y, z = np.random.randn(count), np.random.randn(count), np.random.randn(count)
    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="markers",
                marker=dict(size=3, color="#00f3ff", opacity=0.8, line=dict(width=0)),
            )
        ]
    )
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor="black",
        scene=dict(
            bgcolor="black",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        ),
    )
    st.plotly_chart(fig, use_container_width=True)


with tab3:
    st.subheader(">> UNIFIED LEDGER (NOV 6 - TODAY)")
    col1, col2, col3 = st.columns(3)
    col1.metric("NET LIQUIDITY", f"${st.session_state.net_worth:,.2f}", "+1.33 BTC")
    col2.metric("PSI COIN MASS", f"{st.session_state.psi_mass:,.2f}", "EXPANDING")
    col3.metric("DARK ENERGY", "0.999", "STABLE")


with tab4:
    st.subheader("🛠️ EVE SELF‑HEALING AGENT")
    st.warning(">> SYSTEM BRAIN ACCESS. PASTE UPDATES HERE.")

    # Display current app source code for editing
    with open(__file__, "r") as f:
        current_code = f.read()

    new_code = st.text_area("INJECT NEW CODE:", value=current_code, height=300)

    if st.button("🧬 EXECUTE SYSTEM UPDATE"):
        # Write the new code back to this file
        with open(__file__, "w") as f:
            f.write(new_code)
        st.toast("REWRITING KERNEL... REBOOTING...", icon="🔄")
        time.sleep(2)
        st.rerun()
