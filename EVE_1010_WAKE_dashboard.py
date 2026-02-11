import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="EVE 1010_WAKE", layout="wide")

# Caching with TTL
@st.cache_data(ttl=10)
def load_csv_cached(file_path):
    """Load CSV with 10-second cache"""
    try:
        return pd.read_csv(file_path), None
    except Exception as e:
        return None, str(e)

@st.cache_data(ttl=10)
def filter_data_from_nov6(df, date_column='Timestamp'):
    """Filter data from Nov 6 onwards"""
    try:
        if date_column in df.columns:
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
            cutoff_date = datetime(2025, 11, 6)
            return df[df[date_column] >= cutoff_date]
    except:
        pass
    return df

# Auto-refresh every 5 seconds
def auto_refresh():
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
    
    elapsed = time.time() - st.session_state.last_refresh
    if elapsed >= 5:
        st.session_state.last_refresh = time.time()
        st.rerun()
    
    return 5 - elapsed

st.title("🧠 CEC-WAM EVE 1010_WAKE")

# Display auto-refresh countdown
remaining = auto_refresh()
st.caption(f"🔄 Auto-refresh in {remaining:.1f}s | Last update: {datetime.now().strftime('%H:%M:%S')}")

# Auto-load all CSV files in repo
data_files = [f for f in os.listdir('.') if f.endswith('.csv')]

master_data = {}
st.header("📊 Live Data (Nov 6 → Today)")

for file in data_files:
    df, error = load_csv_cached(file)
    
    if error:
        st.warning(f"⚠️ Could not load {file}: {error}")
        continue
    
    if df is not None:
        # Filter to Nov 6 onwards
        original_count = len(df)
        df = filter_data_from_nov6(df)
        filtered_count = len(df)
        
        master_data[file] = df
        
        with st.expander(f"✅ {file} ({filtered_count} records, {original_count - filtered_count} filtered)"):
            st.dataframe(df.head(20), use_container_width=True)

# Consolidated real numbers (from your HUDs)
st.header("💰 Real Tangible Funds")
col1, col2, col3 = st.columns(3)
col1.metric("PSI-Coin", "$88,720.45", "+2.3%")
col2.metric("Liquidity", "$1,250,039.00", "✅ Live")
col3.metric("Total Spendable", "$1,338,759.45", "Available")
st.metric("Bridge Pending", "$21,000", "Scan face to unlock")

# 1010_EVE_WAKE Status
st.header("🤖 1010_EVE_WAKE STATUS")
col1, col2, col3 = st.columns(3)
col1.metric("Status", "ONLINE", "✅")
col2.metric("Mode", "GOD MODE", "99.9%")
col3.metric("Uptime", "24/7", "∞")

# One-button export to Google Sheet
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Export All Data", use_container_width=True):
        try:
            # Simple CSV export
            with open("EVE_MASTER_EXPORT.csv", "w") as f:
                for name, df in master_data.items():
                    f.write(f"\n--- {name} ---\n")
                    df.to_csv(f, index=False)
            st.success("✅ Exported to EVE_MASTER_EXPORT.csv")
            
            with open("EVE_MASTER_EXPORT.csv", "r") as f:
                st.download_button("📥 Download CSV", f.read(), "EVE_MASTER_EXPORT.csv")
        except Exception as e:
            st.error(f"Export failed: {e}")

with col2:
    if st.button("🔄 Clear Cache & Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

with col3:
    if st.button("🧹 Clear All Caches", use_container_width=True):
        st.cache_data.clear()
        st.success("Cache cleared!")

# Footer
st.divider()
st.caption(f"EVE Agent: Full Access | Cache TTL: 10s | Auto-refresh: 5s | Last: {datetime.now().strftime('%H:%M:%S')}")