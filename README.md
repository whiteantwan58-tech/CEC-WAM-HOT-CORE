# CEC-WAM EVE 1010_WAKE - Live Blockchain Dashboard

A production-ready, autonomous live data dashboard that displays real-time blockchain data from Solana with comprehensive error handling and clear status indicators.

## 🌟 NEW Enhanced Features (v2.0)

### ⚡ Performance Optimizations
- **st.cache_data (ttl=10)**: All data loading functions use intelligent caching with 10-second TTL
- **Auto-refresh every 5 seconds**: Real-time updates without manual refresh
- **Efficient data filtering**: Automatic filtering from Nov 6, 2025 to today
- **Batch loading**: Multiple CSV files loaded in parallel

### 🎤 Voice Input
- **Web Speech API**: Fully integrated voice command system
- **Hands-free control**: Control the dashboard using voice commands
- **Multi-browser support**: Works in Chrome, Edge, Safari (requires HTTPS)
- **Real-time feedback**: Visual indication of listening state

### 🌟 Three.js Star Map HD Visuals
- **10,000+ HD particles**: High-definition star field visualization
- **Smooth animation**: 60 FPS smooth rotation and movement
- **Responsive design**: Adapts to any screen size
- **Interactive**: Real-time 3D rendering

### 🤖 EVE Agent Full Access
- **Full system access**: EVE agent has complete control
- **Auto-fix mechanisms**: Automatic error detection and repair
- **Status monitoring**: Real-time health checks
- **Command interface**: Terminal and voice command support

### 📊 Live Data Management
- **Date filtering**: Automatic filtering from Nov 6, 2025
- **Real-time updates**: Data refreshes every 5 seconds
- **CSV export**: One-click export of filtered data
- **Error handling**: Graceful fallback and recovery

## 🌟 Original Features

- **Real-time Blockchain Data**: Live integration with Solana blockchain via RPC
- **Token Tracking**: PSI-Coin holdings and price monitoring
- **Wallet Monitoring**: SOL balance tracking
- **Smart Fallback**: Automatic CSV backup when APIs are unavailable
- **Health Monitoring**: Real-time system health checks and status indicators
- **Error Handling**: Robust retry logic and user-friendly error messages
- **Security**: Environment-based configuration with no hardcoded secrets

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE.git
   cd CEC-WAM-HOT-CORE
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables (optional)**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys if needed
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the dashboard**
   - Open your browser to `http://localhost:8501`

### Run Alternative Dashboards

```bash
# EVE 1010_WAKE Dashboard (with enhanced features)
streamlit run EVE_1010_WAKE_dashboard.py

# OMEGA EVE Dashboard (with voice control)
streamlit run omega_eve.py
```

### Testing and Utilities

```bash
# Run comprehensive system tests
python test_system.py

# Generate data report
python data_manager.py report

# Filter all CSV files (Nov 6 onwards)
python data_manager.py filter

# Filter specific file
python data_manager.py input.csv output.csv
```

### Testing Locally

To test locally with a simple server:
```bash
python -m http.server 8000
# Then browse to http://localhost:8000
```

## ☁️ Streamlit Cloud Deployment

### Step 1: Prepare Your Repository

1. Ensure all files are committed:
   ```bash
   git add .
   git commit -m "Prepare for Streamlit Cloud deployment"
   git push origin main
   ```

2. Verify these files exist in your repo:
   - ✅ `app.py` (main application)
   - ✅ `requirements.txt` (Python dependencies)
   - ✅ `.streamlit/config.toml` (Streamlit configuration)
   - ✅ `pump.fun.csv` (backup data)
   - ✅ `.gitignore` (excludes sensitive files)

### Step 2: Deploy to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**

2. **Sign in** with your GitHub account

3. **Click "New app"**

4. **Configure your app:**
   - Repository: `whiteantwan58-tech/CEC-WAM-HOT-CORE`
   - Branch: `main`
   - Main file path: `app.py`

5. **Advanced settings** (optional):
   - Python version: 3.9+ (recommended: 3.12)

6. **Click "Deploy"**

### Step 3: Configure Environment Variables (Optional)

If you need to add API keys:

1. In Streamlit Cloud, go to your app settings
2. Click on "Secrets" in the left sidebar
3. Add your secrets in TOML format:
   ```toml
   GROQ_API_KEY = "your-api-key-here"
   ```

### Step 4: Verify Deployment

1. **Check the sidebar status panel:**
   - 🟢 Solana RPC: Should show "Connected"
   - 🟢 Solscan API: Should show "Active"
   - 🟢 Data Source: Should show "LIVE"

2. **Test functionality:**
   - Verify PSI-Coin price updates
   - Check wallet balance displays correctly
   - Test the "Refresh Live Data" button
   - Verify auto-refresh works

## 🔐 Environment Variables

The application uses the following environment variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | No | API key for Groq AI features (optional) |

### Setting Up Environment Variables

**For Local Development:**
1. Copy `.env.example` to `.env`
2. Fill in your API keys
3. Never commit `.env` to version control

**For Streamlit Cloud:**
1. Go to app settings → Secrets
2. Add variables in TOML format
3. Restart the app to apply changes

## 📊 Data Flow

1. **Primary Data Source**: Live Solana blockchain via RPC
2. **Secondary Data Source**: Solscan public API for token metadata
3. **Fallback**: `pump.fun.csv` local CSV data when APIs are unavailable

## 🏥 System Health Checks

The dashboard includes comprehensive health monitoring:

- **Solana RPC Connectivity**: Verifies blockchain connection
- **Solscan API Availability**: Checks token data API status
- **CSV Data Integrity**: Validates backup data structure
- **Token Address Validation**: Ensures token addresses are valid

View the health check in the sidebar under "System Health Check".

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. "Solana RPC: Disconnected"
- **Cause**: Cannot connect to Solana blockchain
- **Solution**: Check internet connection, verify RPC endpoint is accessible
- **Fallback**: App will use CSV backup data

#### 2. "Solscan API: Failed"
- **Cause**: API rate limit or service unavailable
- **Solution**: Wait a few minutes and refresh, or check Solscan status
- **Fallback**: App will use cached data and CSV backup

#### 3. "Data Source: CSV Backup"
- **Cause**: Live APIs are unavailable
- **Solution**: This is normal fallback behavior, data is still functional
- **Note**: Price data may be outdated

#### 4. CSV Parsing Errors
- **Symptom**: Warnings about missing columns
- **Solution**: Verify `pump.fun.csv` has required columns:
  - Token Address, Flow, Amount, Decimals, Value
- **Fix**: Re-export CSV with correct structure

#### 5. Missing Dependencies
- **Error**: `ModuleNotFoundError`
- **Solution**: Run `pip install -r requirements.txt`
- **Note**: Ensure Python 3.9+ is installed

### Live Data Verification Checklist

- [ ] Sidebar shows "Solana RPC: Connected"
- [ ] Sidebar shows "Solscan API: Active"
- [ ] Data Source indicates "LIVE"
- [ ] Last Update timestamp is recent
- [ ] PSI-Coin price shows as "Live Price"
- [ ] Wallet balance displays correctly
- [ ] Auto-refresh working (check timestamp updates)
- [ ] Manual refresh button works
- [ ] Error messages are clear and helpful

## 🔒 Security Best Practices

### What We've Implemented

✅ **No Hardcoded Secrets**: All sensitive data uses environment variables  
✅ **`.env` in `.gitignore`**: Environment files never committed  
✅ **`.env.example`**: Template provided for configuration  
✅ **HTTPS APIs**: All external calls use secure connections  
✅ **Input Validation**: CSV data validated before processing  
✅ **Error Handling**: Graceful degradation without exposing internals  

### Security Guidelines

1. **Never commit secrets** to version control
2. **Use environment variables** for all API keys and sensitive data
3. **Rotate API keys** regularly if exposed
4. **Monitor access logs** on Streamlit Cloud
5. **Review dependencies** regularly for vulnerabilities
6. **Use HTTPS** for all deployments

## 🎨 Customization

### Theme Configuration

Edit `.streamlit/config.toml` to customize appearance:

```toml
[theme]
primaryColor = "#FF4B4B"      # Main accent color
backgroundColor = "#0E1117"    # App background
secondaryBackgroundColor = "#262730"  # Sidebar/widgets
textColor = "#FAFAFA"          # Text color
font = "sans serif"            # Font family
```

### Adding New Data Sources

To add new blockchain or API data:

1. Create a new function in the "LIVE DATA FETCHING FUNCTIONS" section
2. Add retry logic and error handling (see existing functions as templates)
3. Update `SystemStatus` class if needed
4. Add health check for the new source
5. Display the data in the metrics section

## 📱 PWA Version

This repository also includes a PWA (Progressive Web App) frontend:

- **Files**: `index.html`, `manifest.json`, `service-worker.js`
- **Features**: Offline support, voice input, local storage, Three.js star map
- **Usage**: Open `index.html` in browser or deploy to web server

## 📚 Additional Documentation

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**: Comprehensive deployment guide with Docker, PM2, and cloud options
- **[test_system.py](test_system.py)**: Automated test suite for all features
- **[data_manager.py](data_manager.py)**: Utility for managing and filtering CSV data
- **[formulas.md](formulas.md)**: Core system formulas and calculations

## 🛠️ Utilities

### test_system.py
Comprehensive test suite that validates:
- Dependencies installation
- File structure integrity
- CSV data validity
- Streamlit app syntax
- Cache functionality
- Auto-refresh implementation
- Voice input integration
- Three.js visualization

Run with: `python test_system.py`

### data_manager.py
Data management utility for:
- Filtering CSV files by date (Nov 6 onwards)
- Generating data reports
- Batch processing multiple files
- Data validation and cleanup

Run with: `python data_manager.py report`

## 🧪 Testing

### Manual Testing Procedures

**Test Live Data Connectivity:**
1. Open the app and check sidebar status indicators
2. Verify all systems show green (connected)
3. Check "Last Update" timestamp is current
4. Click "Refresh Live Data" and verify update

**Test CSV Fallback:**
1. Disconnect from internet
2. Restart the app
3. Verify "Data Source" shows "CSV Backup"
4. Confirm data still displays (from CSV)

**Test Error Handling:**
1. Modify CSV to remove required columns
2. Restart app and check for validation warnings
3. Verify app doesn't crash
4. Restore CSV and verify recovery

**Test Token Calculations:**
1. Compare PSI-Coin holdings with CSV data
2. Verify live price updates when API active
3. Check Total Spendable calculation
4. Export data and verify accuracy

## 📄 License

This project is part of the CEC-WAM system.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review Streamlit Cloud logs for deployment issues

---

**Status**: Production Ready ✅  
**Last Updated**: 2026-02-11  
**Version**: 2.0.0
