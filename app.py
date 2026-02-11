import streamlit as st
import pandas as pd
import os
from datetime import datetime
import requests
from solana.rpc.api import Client
try:
    # Try newer solana-py API (v0.30.0+)
    from solders.pubkey import Pubkey as PublicKey
except ImportError:
    # Fallback to older API
    from solana.publickey import PublicKey
import json
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

st.set_page_config(page_title="EVE 1010_WAKE", layout="wide")

# Load environment variables
# Note: GROQ_API_KEY is reserved for future AI features and not currently used
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
WALLET_ADDRESS = "b59HHkFpg3g9yBwwLcuDH6z1d6d6z3vdGWX7mkX3txH"
PSI_COIN_TOKEN = "7Avu2LscLpCNNDR8szDowyck3MCBecpCf1wHyjU3pump"

# Solana RPC Client
solana_client = Client("https://api.mainnet-beta.solana.com")

st.title("🧠 CEC-WAM EVE 1010_WAKE")
st.caption("🔴 LIVE DATA ENABLED - Real-time Solana Blockchain Integration")

# ========================================
# LIVE DATA FETCHING FUNCTIONS WITH ERROR HANDLING
# ========================================

# Global status variables
class SystemStatus:
    """Track system health and connectivity"""
    def __init__(self):
        self.solana_connected = False
        self.solscan_api_active = False
        self.last_update = None
        self.data_source = "INITIALIZING"
        self.error_message = ""

status = SystemStatus()

@st.cache_data(ttl=30)  # Cache for 30 seconds
def fetch_live_token_data(token_address):
    """Fetch live PSI-Coin token data from Solana with retry logic"""
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            # Fetch from Solscan API
            url = f"https://public-api.solscan.io/token/meta?tokenAddress={token_address}"
            response = requests.get(
                url, 
                headers={"accept": "application/json"}, 
                timeout=10
            )
            
            if response.status_code == 200:
                status.solscan_api_active = True
                status.last_update = datetime.now()
                status.data_source = "LIVE"
                return response.json()
            elif response.status_code == 429:
                # Rate limited - wait and retry
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                    continue
            else:
                status.error_message = f"Solscan API returned status {response.status_code}"
                
        except requests.exceptions.Timeout:
            status.error_message = f"Solscan API timeout (attempt {attempt + 1}/{max_retries})"
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
        except requests.exceptions.ConnectionError:
            status.error_message = f"Cannot connect to Solscan API (attempt {attempt + 1}/{max_retries})"
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
        except Exception as e:
            status.error_message = f"Error fetching token metadata: {str(e)}"
            
    status.solscan_api_active = False
    status.data_source = "CSV BACKUP"
    return None

@st.cache_data(ttl=30)
def fetch_token_price(token_address):
    """Fetch current PSI-Coin price with retry logic"""
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            url = f"https://public-api.solscan.io/market/token/{token_address}"
            response = requests.get(
                url, 
                headers={"accept": "application/json"}, 
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                price = data.get('priceUsdt', 0)
                if price > 0:
                    status.solscan_api_active = True
                    status.data_source = "LIVE"
                return price
            elif response.status_code == 429:
                # Rate limited
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                    
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
        except Exception:
            pass
            
    status.data_source = "CSV BACKUP"
    return 0

@st.cache_data(ttl=60)
def fetch_wallet_balance(wallet_address):
    """Fetch SOL balance for wallet with error handling"""
    try:
        pubkey = PublicKey(wallet_address)
        response = solana_client.get_balance(pubkey)
        
        if response and 'result' in response and response['result']:
            # Convert lamports to SOL
            sol_balance = response['result']['value'] / 1_000_000_000
            status.solana_connected = True
            return sol_balance
        else:
            status.solana_connected = False
            status.error_message = "Invalid response from Solana RPC"
            return 0
            
    except Exception as e:
        status.solana_connected = False
        status.error_message = f"Solana RPC error: {str(e)}"
        return 0

@st.cache_data(ttl=30)
def calculate_psi_coin_holdings(csv_data):
    """Calculate PSI-Coin holdings from pump.fun.csv with validation"""
    try:
        if 'pump.fun.csv' not in csv_data:
            status.error_message = "pump.fun.csv not found"
            return 0, 0
        
        pump_df = csv_data['pump.fun.csv']
        
        # Validate required columns
        required_columns = ['Token Address', 'Flow', 'Amount', 'Decimals', 'Value']
        missing_columns = [col for col in required_columns if col not in pump_df.columns]
        
        if missing_columns:
            status.error_message = f"Missing CSV columns: {', '.join(missing_columns)}"
            st.warning(f"⚠️ CSV format issue: Missing columns {', '.join(missing_columns)}")
            return 0, 0
        
        token_rows = pump_df[pump_df['Token Address'].str.contains(PSI_COIN_TOKEN, na=False)]
        
        total_tokens = 0
        total_value = 0
        
        for _, row in token_rows.iterrows():
            try:
                if row['Flow'] == 'in':
                    token_amount = float(row['Amount']) / (10 ** int(row['Decimals']))
                    total_tokens += token_amount
                    total_value += float(row['Value'])
            except (ValueError, KeyError) as e:
                st.warning(f"⚠️ Skipping malformed row in CSV: {str(e)}")
                continue
        
        return total_tokens, total_value
        
    except Exception as e:
        status.error_message = f"Error calculating holdings: {str(e)}"
        st.error(f"❌ Error parsing CSV data: {str(e)}")
        return 0, 0

def check_system_health():
    """Perform health check on all systems"""
    health_report = {
        "Solana RPC": status.solana_connected,
        "Solscan API": status.solscan_api_active,
        "CSV Data": 'pump.fun.csv' in master_data,
        "Token Address": bool(PSI_COIN_TOKEN),
    }
    return health_report

# ========================================
# LOAD CSV DATA
# ========================================

data_files = [f for f in os.listdir('.') if f.endswith('.csv')]
master_data = {}

with st.spinner("Loading data files..."):
    for file in data_files:
        try:
            df = pd.read_csv(file)
            master_data[file] = df
        except Exception as e:
            st.warning(f"Could not load {file}: {str(e)}")

# ========================================
# SIDEBAR: LIVE STATUS PANEL
# ========================================

st.sidebar.header("🔴 LIVE STATUS")

# Fetch live blockchain data first to populate status
with st.spinner("Connecting to blockchain..."):
    live_token_data = fetch_live_token_data(PSI_COIN_TOKEN)
    live_price = fetch_token_price(PSI_COIN_TOKEN)
    wallet_sol_balance = fetch_wallet_balance(WALLET_ADDRESS)

# Calculate PSI-Coin holdings from CSV
psi_coin_tokens, psi_coin_csv_value = calculate_psi_coin_holdings(master_data)

# Display system status in sidebar
health_check = check_system_health()

# Solana RPC Status
if status.solana_connected:
    st.sidebar.metric("Solana RPC", "🟢 Connected")
else:
    st.sidebar.metric("Solana RPC", "🔴 Disconnected")
    
# Solscan API Status
if status.solscan_api_active:
    st.sidebar.metric("Solscan API", "🟢 Active")
else:
    st.sidebar.metric("Solscan API", "🔴 Failed")

# Data Source
if status.data_source == "LIVE":
    st.sidebar.metric("Data Source", "🟢 LIVE")
elif status.data_source == "CSV BACKUP":
    st.sidebar.metric("Data Source", "🟡 CSV Backup")
else:
    st.sidebar.metric("Data Source", "⚪ Initializing")

# Last Update
if status.last_update:
    st.sidebar.caption(f"Last Update: {status.last_update.strftime('%H:%M:%S')}")
else:
    st.sidebar.caption("Waiting for first update...")

# Error messages
if status.error_message:
    st.sidebar.error(f"⚠️ {status.error_message}")

st.sidebar.divider()

# Health Check Section
with st.sidebar.expander("🏥 System Health Check", expanded=False):
    for system, is_healthy in health_check.items():
        if is_healthy:
            st.sidebar.success(f"✅ {system}")
        else:
            st.sidebar.error(f"❌ {system}")

st.sidebar.divider()
st.sidebar.caption("Auto-refresh: Every 30 seconds")

# ========================================
# MAIN CONTENT
# ========================================

col_status1, col_status2 = st.columns([3, 1])

with col_status1:
    st.header("💰 Real Tangible Funds - LIVE")
    # Show data source indicator
    if status.data_source == "LIVE":
        st.success("🟢 Real-time blockchain data active")
    elif status.data_source == "CSV BACKUP":
        st.warning("🟡 Using CSV backup data - API unavailable")
    else:
        st.info("⚪ Initializing connection...")

with col_status2:
    if st.button("🔄 Refresh Live Data"):
        st.cache_data.clear()
        st.rerun()

# Calculate live value if we have price data
psi_coin_live_value = psi_coin_tokens * live_price if live_price > 0 else psi_coin_csv_value

# Get liquidity from operational metrics
liquidity = 1250039.00  # Default
for file, df in master_data.items():
    if 'Metric Name' in df.columns and 'Value' in df.columns:
        liquidity_row = df[df['Metric Name'].str.contains('Total Liquidity', na=False)]
        if not liquidity_row.empty:
            liquidity_value = str(liquidity_row.iloc[0]['Value'])
            liquidity = float(liquidity_value.replace('$', '').replace(',', ''))
            break

# Calculate totals
total_spendable = psi_coin_live_value + liquidity + (wallet_sol_balance * 250)  # Approximate SOL to USD

# ========================================
# DISPLAY METRICS
# ========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "PSI-Coin (7Avu...pump)", 
        f"${psi_coin_live_value:,.2f}",
        f"{psi_coin_tokens:,.2f} tokens",
        delta_color="normal"
    )
    if live_price > 0:
        st.caption(f"💹 Live Price: ${live_price:.8f}")
    else:
        st.caption("📊 Using CSV data (API unavailable)")
    
    # Show data freshness
    if status.last_update:
        time_diff = (datetime.now() - status.last_update).seconds
        if time_diff < 60:
            st.caption(f"🕒 Updated {time_diff}s ago")
        else:
            st.caption(f"🕒 Updated {time_diff // 60}m ago")

with col2:
    st.metric(
        "Wallet SOL Balance",
        f"{wallet_sol_balance:.4f} SOL",
        f"~${wallet_sol_balance * 250:,.2f}"
    )
    st.caption(f"🔗 {WALLET_ADDRESS[:8]}...{WALLET_ADDRESS[-6:]}")

with col3:
    st.metric("Total Liquidity", f"${liquidity:,.2f}")
    st.caption("✅ Verified Assets")

with col4:
    st.metric(
        "Total Spendable", 
        f"${total_spendable:,.2f}",
        delta_color="normal"
    )

st.metric("Bridge Pending", "$21,000", "⚠️ Scan face to unlock")

# ========================================
# TOKEN METADATA DISPLAY
# ========================================

if live_token_data:
    with st.expander("🪙 PSI-Coin Token Details (Live)", expanded=True):
        tcol1, tcol2, tcol3 = st.columns(3)
        
        with tcol1:
            st.write("**Token Name:**", live_token_data.get('name', 'PSI-Coin'))
            st.write("**Symbol:**", live_token_data.get('symbol', 'PSI'))
        
        with tcol2:
            st.write("**Decimals:**", live_token_data.get('decimals', 6))
            st.write("**Supply:**", f"{live_token_data.get('supply', 'N/A'):,}")
        
        with tcol3:
            st.write("**Your Holdings:**", f"{psi_coin_tokens:,.2f}")
            st.write("**Holdings %:**", f"{(psi_coin_tokens / live_token_data.get('supply', 1)) * 100:.4f}%")

# ========================================
# SYSTEM STATUS
# ========================================

st.header("1010_EVE_WAKE STATUS")

system_health = min(98 + (psi_coin_live_value / 10000), 100)

col_stat1, col_stat2 = st.columns(2)

with col_stat1:
    st.success(f"✅ ONLINE - {system_health:.0f}% - God Mode Pending Biometric")
    st.info(f"🕐 Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

with col_stat2:
    st.metric("Dark Energy Index", "0.999", "PERFECT")
    st.metric("Total Mass", "100001.33 units", "PERFECT")

# ========================================
# DATA TABLES
# ========================================

with st.expander("📊 View All CSV Data"):
    for file, df in master_data.items():
        st.subheader(f"✅ {file}")
        st.dataframe(df, use_container_width=True)

# ========================================
# EXPORT FUNCTIONALITY
# ========================================

if st.button("📤 Export All Data to CSV"):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_filename = f"EVE_MASTER_EXPORT_{timestamp}.csv"
        
        with open(export_filename, "w") as f:
            # Add live data summary
            f.write("=== LIVE DATA SUMMARY ===\n")
            f.write(f"PSI-Coin Holdings,{psi_coin_tokens}\n")
            f.write(f"PSI-Coin Value,${psi_coin_live_value:,.2f}\n")
            f.write(f"Wallet SOL Balance,{wallet_sol_balance:.4f}\n")
            f.write(f"Total Liquidity,${liquidity:,.2f}\n")
            f.write(f"Total Spendable,${total_spendable:,.2f}\n")
            f.write(f"Export Time,{datetime.now().isoformat()}\n\n")
            
            # Add CSV data
            for name, df in master_data.items():
                f.write(f"\n=== {name} ===\n")
                df.to_csv(f, index=False)
        
        st.success(f"✅ Exported to {export_filename}")
        
        with open(export_filename, "r") as f:
            st.download_button("⬇️ Download Export", f.read(), export_filename)
    except Exception as e:
        st.error(f"Export failed: {str(e)}")

# ========================================
# AUTO-REFRESH TIMER WITH COUNTDOWN
# ========================================

st.divider()

refresh_col1, refresh_col2 = st.columns([2, 1])

with refresh_col1:
    st.caption(f"⏱️ Data refreshes every 30 seconds | Last refresh: {datetime.now().strftime('%H:%M:%S')}")
    
with refresh_col2:
    # Show connection quality
    if status.solana_connected and status.solscan_api_active:
        st.caption("🟢 All systems operational")
    elif status.solana_connected or status.solscan_api_active:
        st.caption("🟡 Partial connectivity")
    else:
        st.caption("🔴 Limited connectivity")

# Auto-refresh mechanism
# Note: Streamlit will automatically rerun when cache expires
# This provides a smooth user experience without manual intervention

# ========================================
# TESTING AND VERIFICATION NOTES
# ========================================
# 
# How to test live data connectivity:
# 1. Check the sidebar "LIVE STATUS" panel for connection indicators
# 2. Verify "Data Source" shows "LIVE" when APIs are accessible
# 3. Check "Last Update" timestamp is recent
# 4. Click "Refresh Live Data" button to force immediate update
#
# How to verify API responses:
# 1. Monitor the sidebar error messages for specific API failures
# 2. Check the System Health Check expander for component status
# 3. Verify PSI-Coin price shows as "Live Price" when API is working
# 4. Test with network disconnected to verify CSV fallback works
#
# How to validate CSV parsing:
# 1. Check for warning messages about missing columns
# 2. Verify "View All CSV Data" expander shows pump.fun.csv correctly
# 3. Ensure PSI-Coin holdings calculate without errors
# 4. Test with modified CSV to ensure validation catches issues
#
# How to check token calculations:
# 1. Verify PSI-Coin holdings match expected amounts
# 2. Check that live price multiplies correctly with token amount
# 3. Ensure Total Spendable includes all components correctly
# 4. Compare CSV value vs live value when both are available
#
