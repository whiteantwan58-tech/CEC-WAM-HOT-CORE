# CEC-WAM LIVE — EVE HEI (PWA)

## 🌌 CEC Matrix Dashboard (Streamlit)

A complete operational dashboard system for the Conscious Energy Continuum (CEC) Matrix. This dashboard provides real-time monitoring, data visualization, and export capabilities for all CEC system metrics.

### Features
- **Financial HUD**: Live KPIs including PSI-Coin Balance, Liquidity Reserves, Total Spendable, CEC_WAM Status, Net Worth, and Current Valuation
- **System Metrics**: Full operational metrics and asset tracking
- **Task Management**: EVE unfinished tasks with priority-based color coding
- **Physics Modules**: Interactive tabs for DarkEnergy, BlackHoles, QuantumField, Conscious, Synth, Interface, and Log modules
- **Data Export**: Download buttons for HUD, Metrics, and Tasks data in CSV format
- **Modern Design**: Clean, wide-layout interface optimized for operational monitoring

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run cec_dashboard.py
```

The dashboard will automatically load data from:
- `data/CEC_WAM_MASTER_LEDGER_LIVE.xlsx` - Main Excel file with all physics modules
- `data/EVE_UNFINISHED_TASKS.csv` - Task management data
- `data/CEC_Matrix_System_Operational_Metrics_and_Assets.csv` - System metrics

### Deploy to Streamlit Cloud
1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository and select `cec_dashboard.py`
4. Deploy!

---

## PWA Frontend

This repository also contains a PWA frontend to connect the CEC WAM Living Calculator (Google Sheet / CSV / local file), providing:

- Live fetch & merge from a published Google Sheet (CSV) URL.
- Import local CSV/XLSX (CSV parsing included; for XLSX use a converter).
- Voice input (Web Speech API) and TTS for EVE HEI interactions.
- Persistent local storage (IndexedDB via localForage) so it works offline.
- Charts (Chart.js) and export of logs (CSV).
- PWA manifest + Service Worker for installable app.

Important security notes:
- Do not commit secrets (API keys or passcodes) into the repo. The app provides a device-only PIN you can set locally (stored as a salted hash in IndexedDB).
- If you want server-based integrations or remote access, configure secure auth (OAuth2) and server-side credentials — not stored in the client.

Quick start
1. Publish your Google Sheet:
   - In Google Sheets: File → Publish to web → Choose sheet → Comma-separated values (CSV) → Publish.
   - Copy the CSV URL (it will include `output=csv`).
2. Open `index.html` in a web server (recommended), or push to GitHub Pages.
   - To test locally: run `python -m http.server 8000` in the folder and browse to `http://localhost:8000`.
   - To run from a flash drive offline: copy the folder to the drive and run a local static server from that machine.
3. Paste the CSV URL in the UI, click Link → Fetch Now.
4. To import local data, use the Import file input.
5. Use the "Talk (Mic)" button to add voice-entered log entries; the app will reply via TTS.

Offline use
- The app caches the UI shell and the most recent CSV. Data is persisted in IndexedDB.
- If you need a fully offline central server, run a small Raspberry Pi or laptop with a local static server and keep it powered; this app will access it via local network.

If you'd like:
- I can add automatic Excel (.xlsx) parsing using the SheetJS (xlsx) library.
- I can add tighter filtering to only ingest rows from Nov 6 and where the dataset is "CEC WAM" specifically — if you paste a sample CSV (or share the Sheet columns), I will tune the ingestion rules.

Security & PIN
- The app sets a device PIN stored locally (hashed). Do not use secret system bypass codes stored in the repo. If you want, I can provide an optional encrypted backup flow.

Next steps I can do for you
- Add XLSX parsing (SheetJS) and map known spreadsheet columns into dashboard KPIs.
- Implement row-level filters (only CEC WAM rows and date = Nov 6).
- Add charts per-sheet (pie/line/time series) and a detailed Log tab with date & time per imported/received row.
- Add user-friendly export ZIP of full static site + data for flash drive transfer.
# 🌌 CEC-WAM-HOT-CORE Live Dashboard

A cutting-edge, real-time dashboard featuring live Google Sheets data synchronization, interactive 3D star maps, cryptocurrency pricing, a theatrical biometric lock screen interface, and **EVE - an advanced AI voice assistant**.

## ✨ Features

### 🤖 Automated Workflows (NEW!)

**All repository changes are now automatically approved and merged!**

This repository includes comprehensive automation for:

- ✅ **Auto-Approve PRs** - All pull requests are automatically approved
- 🔄 **Auto-Merge** - PRs are automatically merged after approval
- 🔧 **Auto-Fix Errors** - Code formatting and error fixes are applied automatically
- ⬆️ **Auto-Upgrade Dependencies** - Dependencies are upgraded daily and auto-merged
- 🤖 **Dependabot Integration** - Dependency updates are automatically approved and merged
- 🚀 **CI/CD Auto-Approval** - All continuous integration checks auto-approve changes
- 📦 **Interface Auto-Approval** - Interface changes are automatically approved after upgrades

**No manual approval needed!** All workflows run automatically:
- Push to any branch triggers auto-fix and auto-formatting
- Pull requests are auto-approved within seconds
- Dependencies update daily at 2 AM UTC
- Failed builds are auto-retried with fixes
- GitHub Pages deploys automatically without approval

### Core Functionality
- **Live Google Sheets Integration** - Auto-fetches CSV data from Google Sheets with 5-minute auto-refresh
- **Color-Coded Status System** - Visual status indicators (PERFECT=Green, TODO=Yellow, ACTIVE=Blue, STABLE=Gray)
- **Real-Time PSI-Coin Pricing** - Live cryptocurrency prices from CoinGecko API with historical chart
- **Interactive 3D Star Map** - Three.js-powered visualization of celestial bodies
- **Advanced Data Visualizations** - Multiple chart types (line, doughnut, bar charts) using Chart.js
- **Data Filtering & Export** - Filter data by status and export to CSV format
- **Real-Time Performance Metrics** - Live tracking of load times, data points, and system status
- **Biometric Lock Screen** - Theatrical security interface (aesthetic only, press Enter to bypass)
- **EVE Voice AI Assistant** - Advanced AI with voice synthesis and natural language understanding
- **Responsive Design** - Optimized for desktop, tablet, and mobile devices
- **Dark Cosmic Theme** - Professional space aesthetic with neon accents

### EVE Voice AI Assistant (NEW! 🎙️)
**System Code:** `CEC_WAM_HEI_EVE_7A2F-9C4B`

EVE is your always-on AI assistant featuring:
- 🎙️ **Voice Synthesis** - Natural voice output via ElevenLabs
- 🤖 **Advanced AI** - Powered by OpenAI GPT-4
- 🧠 **Learning Capability** - Learns from interactions and improves over time
- 📊 **CEC WAM Integration** - Full access to system data and analytics
- 🔢 **Math & Finance** - Performs calculations and financial analysis
- 🔒 **Voice Recognition** - Biometric voice verification for owner (Twan)
- ⚡ **24/7 Availability** - Always-on, never sleeps, auto-updating
- 🌐 **Serverless API** - Vercel-ready API endpoints with hidden keys

EVE is designed specifically for **Twan** with full access to all CEC-WAM system data, no restrictions, and continuous learning capabilities.

### Technical Features
- Data caching and error handling
- Optional Google Sheets logging (requires service account)
- Downloadable data exports (CSV format)
- Status distribution analytics with doughnut charts
- Numeric value analysis and trend charting
- Real-time price history tracking with line charts
- Interactive data filtering by status
- Performance monitoring (load times, data points)
- Voice-enabled chat interface
- API endpoints for serverless deployment

### New Dashboard Features (Latest Update 🆕)
- **📊 Multiple Interactive Charts**:
  - Price history line chart for PSI-COIN
  - Status distribution doughnut chart
  - Data trends bar chart
- **🎛️ Advanced Controls**:
  - Filter buttons (All, Perfect, To-Do, Active, Stable)
  - Export to CSV functionality
  - Real-time metrics dashboard
- **⚡ Performance Monitoring**:
  - Load time tracking
  - Data points counter
  - Live status indicator
  - Auto-refresh rate display
- **💎 Enhanced Data Cards**:
  - Average and total value calculations
  - Market cap visualization
  - Multi-metric displays

## 🚀 Live Demo

### Screenshot
![Enhanced Dashboard](https://github.com/user-attachments/assets/4cc709d9-60cb-470d-8ba1-462d847e173e)

*The enhanced dashboard features multiple data visualization cards, real-time performance metrics, interactive filtering, and data export capabilities.*

### Deployments
- **Streamlit Cloud**: [Deploy to Streamlit](https://streamlit.io/)
- **GitHub Pages**: View the standalone HTML version at your GitHub Pages URL
- **Vercel**: Alternative deployment option for Streamlit apps

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

A production-ready, autonomous live data dashboard that displays real-time blockchain data from Solana with comprehensive error handling, clear status indicators, and integrated traffic monitoring with live camera feeds, weather, and traffic data.

1. **Clone the repository**
```bash
git clone https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE.git
cd CEC-WAM-HOT-CORE
```

### Core Features
- **Real-time Blockchain Data**: Live integration with Solana blockchain via RPC
- **Token Tracking**: PSI-Coin holdings and price monitoring
- **Wallet Monitoring**: SOL balance tracking
- **Smart Fallback**: Automatic CSV backup when APIs are unavailable
- **Health Monitoring**: Real-time system health checks and status indicators
- **Error Handling**: Robust retry logic and user-friendly error messages
- **Auto-refresh**: Automatic data updates every 30 seconds
- **Security**: Environment-based configuration with no hardcoded secrets

### 🗺️ New: Map & Camera Integration
- **Interactive Map**: Visualize Washington State DOT traffic camera locations
- **Live Camera Feeds**: Click map markers to view individual camera feeds with metadata
- **Camera Details**: Display location, direction, coordinates, and timestamps
- **Real-time Updates**: Auto-refresh camera feeds every 60 seconds

### 🌤️ New: Weather Integration
- **Live Weather Data**: Real-time weather information from OpenWeatherMap API
- **Location-based**: Weather data for camera locations and selected areas
- **Detailed Information**: Temperature, conditions, humidity, wind speed
- **Auto-refresh**: Weather updates every 5 minutes

### 🚗 New: Traffic Assistance
- **Traffic Monitoring**: Live traffic and incident data from WSDOT
- **Traffic Statistics**: Active incidents, average speeds, flow status
- **Real-time Updates**: Traffic data refreshes every 45 seconds
- **Traffic Insights**: Monitor incidents and vehicle speeds near camera points

## 🚀 Quick Start
### 🆕 Real-time Enhancements (NEW)
- **Star Map Visualization**: Animated 3D star field with HD visuals and constellation transitions
  - Real-time celestial body tracking
  - Smooth constellation animations (Orion, Ursa Major, Cassiopeia)
  - Interactive 3D scene with 8,000+ stars
  
- **Federal Way Live Feed**: HD camera feed integration framework
  - Multiple camera location support (Main St, City Hall, Transit Center)
  - Auto-cycling between feeds every 15 seconds
  - Screenshot capture functionality
  - Animated placeholder with scan-line effects
  
- **Crime Alert System**: Real-time crime alerts and police scanner integration
  - Live Federal Way police scanner feed simulation
  - Severity-based alerts (Critical, High, Medium, Low)
  - Alert categorization (Theft, Assault, Traffic, Suspicious Activity)
  - Real-time notifications with timestamps and locations
  - Filtering by severity and type
  - Audio alert toggle
  - Export alerts to CSV
  
- **Export & Backup System**: Data export and cloud integration
  - Screenshot capture from live feeds
  - Crime data export to CSV/JSON
  - Star map data export
  - Google Drive integration framework
  - AppSheet sync capability
  - Auto-export settings with customizable intervals
  - Export history tracking

## 🚀 Quick Start
2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables (optional)**
```bash
cp .env.example .env
# Edit .env with your Google Sheets credentials if using logging feature
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open in browser**
```
http://localhost:8501
```

2. **Install dependencies** (for Streamlit version)
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys:
   # - OPENWEATHER_API_KEY for weather data (get free key at openweathermap.org)
   # - GROQ_API_KEY (optional, for AI features)
   ```

4. **Run the Streamlit application** (backend)
   ```bash
   OPENAI_API_KEY=your-openai-api-key
   OPENAI_MODEL=gpt-4
   ```

### EVE Configuration

Edit your `.env` file with EVE-specific settings:

To test the full HTML dashboard with a simple server:
```bash
# EVE System Configuration
EVE_SYSTEM_CODE=CEC_WAM_HEI_EVE_7A2F-9C4B
EVE_OWNER_NAME=Twan
EVE_PERSONALITY=professional,helpful,intelligent,learning
```

### For Streamlit Cloud Deployment

Add EVE secrets in TOML format in your Streamlit Cloud app settings:

```toml
ELEVENLABS_API_KEY = "your-elevenlabs-api-key"
ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
OPENAI_API_KEY = "your-openai-api-key"
OPENAI_MODEL = "gpt-4"
EVE_SYSTEM_CODE = "CEC_WAM_HEI_EVE_7A2F-9C4B"
EVE_OWNER_NAME = "Twan"
EVE_PERSONALITY = "professional,helpful,intelligent,learning"
```

### For Vercel Deployment

1. **Add environment variables in Vercel dashboard:**
   - Go to your project settings
   - Navigate to "Environment Variables"
   - Add all EVE-related variables:
     - `ELEVENLABS_API_KEY`
     - `ELEVENLABS_VOICE_ID`
     - `OPENAI_API_KEY`
     - `OPENAI_MODEL`
     - `EVE_SYSTEM_CODE`
     - `EVE_OWNER_NAME`
     - `EVE_PERSONALITY`

2. **Redeploy** to apply the new environment variables

### EVE Features

Once configured, EVE provides:

- **Voice Chat**: Talk to EVE and get voice responses
- **Text Chat**: Type messages and get AI-powered responses
- **Calculations**: Ask EVE to perform math and financial calculations
- **CEC WAM Data Access**: EVE has full access to all system data
- **Learning**: EVE learns from each interaction to improve responses
- **Always Available**: 24/7 operation with no downtime
- **Personality**: Consistent, professional, and helpful personality locked in
- **Voice Recognition**: Designed to recognize and respond only to Twan's voice (owner)

### Security Notes

- **API Keys**: Never commit API keys to version control
- **Environment Variables**: Always use `.env` files (local) or secrets (cloud)
- **Voice Biometric**: EVE includes voice recognition capabilities (requires additional setup)
- **Owner Access**: EVE is configured to recognize Twan as the primary owner
- **No Restrictions**: EVE has full access to all CEC-WAM system data for Twan

### Troubleshooting EVE

**EVE not responding:**
- Check that all API keys are configured correctly
- Verify API keys are valid and have available quota
- Check the EVE status panel in the dashboard

**Voice synthesis not working:**
- Ensure `ELEVENLABS_API_KEY` is set
- Check ElevenLabs account quota/credits
- Try a different voice ID if needed

**AI responses are generic:**
- Ensure `EVE_SYSTEM_CODE` and `EVE_OWNER_NAME` are set
- Clear conversation history and start fresh
- Check OpenAI API quota/credits

## 🔐 Google Sheets API Setup (Optional Logging)

### Create Service Account

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**

2. **Create a new project** (or use existing)

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | No | API key for Groq AI features (optional) |
| `OPENWEATHER_API_KEY` | Recommended | API key for OpenWeatherMap weather data (get free key at [openweathermap.org/api](https://openweathermap.org/api)) |

**Note:** WSDOT traffic camera and traffic data APIs are public and don't require API keys.
3. **Enable Google Sheets API**
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

4. **Create Service Account**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in details and create

5. **Download JSON Key**
   - Click on the service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Choose JSON format
   - Save the file

6. **Share Google Sheet with Service Account**
   - Open your Google Sheet
   - Click "Share"
   - Add service account email (from JSON file)
   - Give "Editor" permissions

### Configure Credentials

#### For Local Development
Edit `.env` file:
```bash
GOOGLE_SHEETS_CREDS='{"type": "service_account", "project_id": "...", ...}'
LOG_SHEET_ID=your-sheet-id-here
```

#### For Streamlit Cloud
Add to app secrets in TOML format:
```toml
GOOGLE_SHEETS_CREDS = '{"type": "service_account", ...}'
LOG_SHEET_ID = "your-sheet-id"
```

## 📊 Data Source Configuration

### Google Sheets CSV URL
The dashboard fetches data from this public Google Sheets URL:
```
https://docs.google.com/spreadsheets/d/e/2PACX-1vREgUUHPCzTBWK8i1PWBrE2E4pKRTAgaReJahFqmrTetCZyCO0QHVlAleodUsTlJv_86KpzH_NPv9dv/pub?output=csv
```

### Expected CSV Structure
The dashboard expects these columns (will adapt to actual structure):
- `Field` - Item/metric name
- `Value` - Numeric or text value
- `Status` - Status indicator (PERFECT/TODO/ACTIVE/STABLE)
- `Notes` - Additional information (optional)

### To Use Your Own Sheet

1. **Publish your Google Sheet as CSV**
   - File > Share > Publish to web
   - Choose "Comma-separated values (.csv)"
   - Copy the URL

2. **Update the URL in `app.py`**
   ```python
   GOOGLE_SHEETS_CSV_URL = "your-csv-url-here"
   ```

3. **Update the URL in `index.html`**
   ```javascript
   const GOOGLE_SHEETS_CSV_URL = 'your-csv-url-here';
   ```

## 🎨 Customization

### Theme Colors
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#00D9FF"          # Accent color
backgroundColor = "#0E0E1A"       # Main background
secondaryBackgroundColor = "#1A1A2E"  # Card background
textColor = "#EAEAEA"             # Text color
```

### Status Colors
Edit color mappings in `app.py` and `index.html`:
- PERFECT: Green (`#00FF88`)
- TODO: Yellow (`#FFC107`)
- ACTIVE: Blue (`#2196F3`)
- STABLE: Gray (`#9E9E9E`)

### Auto-Refresh Interval
Change cache TTL in `app.py`:
```python
@st.cache_data(ttl=300)  # 300 seconds = 5 minutes
```

## 🛠️ Troubleshooting

### Common Issues

**CSV Data Not Loading**
- Check internet connection
- Verify Google Sheets URL is public and published as CSV
- Check browser console for CORS errors

**PSI Price Not Displaying**
- CoinGecko API may be rate-limited (free tier)
- Check if `tridentdao` token ID is correct
- Try again after a few minutes

**Lock Screen Won't Dismiss**
- Press Enter key
- Click "OVERRIDE ACCESS" button
- Refresh page if stuck

## 🎯 Real-time Modules Usage

### Star Map Visualization
The star map is automatically initialized and displays:
- 8,000+ animated stars with varied colors (white, blue, yellow)
- Three major constellations that auto-cycle every 8 seconds
- Smooth camera movements and constellation transitions
- Interactive 3D rendering using Three.js

### Federal Way Live Feed
Access the live camera feed module:
1. Use the ◀ ▶ buttons to switch between camera locations
2. Click 📷 to capture screenshots
3. Feeds auto-cycle every 15 seconds
4. Screenshots are automatically timestamped

**Available Camera Locations:**
- Federal Way Main St & Pacific Highway
- City Hall Campus
- Transit Center Plaza

### Crime Alert System
Monitor real-time crime alerts:
1. View active alerts with severity indicators
2. Filter alerts by severity (Critical, High, Medium, Low) or type
3. Toggle audio alerts with 🔇/🔊 button
4. Click 🔄 to manually refresh alerts
5. Export data with 💾 button

**Alert Information Includes:**
- Location and timestamp
- Number of responding units
- Alert severity and type
- Real-time status updates

### Export & Backup
Click the 📤 floating button to access export features:
1. **Capture Screenshot**: Take screenshots from live feeds
2. **Export Crime Data**: Download alerts as CSV
3. **Export Star Map Data**: Save celestial data as JSON
4. **Export All Data**: Complete system data export

**Integration Options:**
- Connect to Google Drive for cloud storage
- Sync with AppSheet for mobile access
- Configure auto-export intervals
- View export history

## 🧪 Testing
**Google Sheets Logging Fails**
- Verify service account credentials are correct
- Check if sheet is shared with service account email
- Ensure `gspread` and `oauth2client` are installed
- Logging is optional - dashboard will continue without it

**Three.js Star Map Not Rendering**
- Check if Three.js CDN is accessible
- Verify browser supports WebGL
- Try a different browser (Chrome/Firefox recommended)

### Debug Mode

Run Streamlit in debug mode:
```bash
streamlit run app.py --logger.level=debug
```

Check browser console (F12) for JavaScript errors.

## 📁 Project Structure

```
CEC-WAM-HOT-CORE/
├── app.py                    # Main Streamlit application
├── index.html                # Standalone HTML dashboard
├── requirements.txt          # Python dependencies
├── vercel.json              # Vercel deployment config
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── .streamlit/
│   └── config.toml          # Streamlit theme configuration
└── README.md                # This file
```

## 📚 API Documentation

### Google Sheets CSV
- **URL Format**: `https://docs.google.com/spreadsheets/d/e/{SHEET_ID}/pub?output=csv`
- **Method**: GET
- **Response**: CSV text
- **Rate Limit**: None (public sheets)

### CoinGecko API
- **Endpoint**: `https://api.coingecko.com/api/v3/simple/price`
- **Parameters**: `ids=tridentdao&vs_currencies=usd&include_24hr_change=true`
- **Method**: GET
- **Response**: JSON
- **Rate Limit**: 10-50 calls/minute (free tier)

## 🔒 Security Notes

- **Lock Screen**: Theatrical UI only, not real security
- **Environment Variables**: Never commit `.env` file
- **Service Account**: Keep JSON credentials secret
- **HTTPS**: Always use HTTPS in production
- **CORS**: Ensure proper CORS headers for API calls

## 🗺️ Map, Camera, Weather & Traffic Features

### Interactive Map Controls

The dashboard includes an interactive map with the following controls:
- **🗺️ TOGGLE MAP**: Show/hide the map view
- **📹 REFRESH CAMS**: Reload all traffic camera locations and feeds
- **🌤️ WEATHER**: Toggle weather overlay layer
- **🚗 TRAFFIC**: Toggle traffic overlay layer

### Using the Camera System

1. **View Camera Locations**: When the map loads, you'll see markers for each WSDOT traffic camera
2. **Select a Camera**: Click any marker to view detailed information
3. **View Live Feed**: Selected camera will display its live image feed
4. **Check Details**: View location, direction, coordinates, and last update time
5. **Close Panel**: Click the close button to deselect the camera

### Weather Integration

Weather data automatically updates for:
- The selected camera location (when a camera is selected)
- Default location (Seattle, WA when no camera is selected)
- Updates every 5 minutes automatically

The weather panel shows:
- Current temperature
- Weather condition description
- Humidity percentage
- Wind speed

### Traffic Monitoring

The traffic system provides:
- **Active Incidents**: Real-time count of traffic incidents
- **Average Speed**: Current average traffic speed
- **Traffic Flow**: Overall flow status (GOOD/MODERATE/SLOW)
- **Auto-refresh**: Updates every 45 seconds

### Auto-Refresh Intervals

The system automatically refreshes:
- Traffic cameras: Every 60 seconds
- Traffic data: Every 45 seconds
- Weather data: Every 5 minutes
- Crypto prices: Every 15 seconds

## 🚀 GitHub Pages Deployment

This repository is configured to automatically deploy to GitHub Pages **with no manual approval required**.

### Automated Deployment Features

✅ **Fully Automated Pipeline**
- Deploys automatically on every push to `main` branch
- No environment approval gates
- No manual intervention needed
- Deployment completes in minutes

### Available Workflows

The repository includes these automated workflows in `.github/workflows/`:

1. **`deploy-dashboard.yml`** - Auto-deploys to GitHub Pages (no approval needed)
2. **`auto-approve.yml`** - Auto-approves all pull requests
3. **`auto-merge.yml`** - Auto-merges approved PRs
4. **`auto-fix-errors.yml`** - Auto-fixes code formatting and errors
5. **`auto-upgrade-dependencies.yml`** - Daily dependency upgrades
6. **`auto-approve-dependabot.yml`** - Auto-approves Dependabot PRs
7. **`ci-auto-approve.yml`** - CI with automatic approval

All workflows have proper permissions and run automatically without manual approval.

### Enable GitHub Pages

1. Go to your repository Settings
2. Navigate to "Pages" in the left sidebar
3. Under "Build and deployment":
   - Source: Deploy from a branch
   - Branch: `main` / `(root)`
4. Click "Save"
5. Your site will be published at: `https://whiteantwan58-tech.github.io/CEC-WAM-HOT-CORE/`

### Automated Deployment

The repository includes a GitHub Actions workflow (`.github/workflows/deploy-dashboard.yml`) that:
- Automatically deploys on every push to the `main` branch
- Can be manually triggered from the Actions tab
- Deploys the complete dashboard with all features

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Streamlit** - Web app framework
- **Three.js** - 3D graphics library
- **CoinGecko** - Cryptocurrency data API
- **Google Sheets** - Data storage and sync
- **Vercel** - Deployment platform

## 📞 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/issues)
- Contact: [GitHub Profile](https://github.com/whiteantwan58-tech)

## 🗺️ Roadmap

- [ ] Add more celestial bodies to star map
- [ ] Implement real-time WebSocket updates
- [ ] Add user authentication system
- [ ] Create mobile app version
- [ ] Integrate more cryptocurrency exchanges
- [ ] Add data visualization charts
- [ ] Implement export to PDF feature
- [ ] Add multi-language support

---

**Built with ❤️ by the CEC-WAM Team**

🌌 *Exploring the cosmos, one datapoint at a time* 🌌
