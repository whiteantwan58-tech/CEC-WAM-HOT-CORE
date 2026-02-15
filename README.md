# 🌌 CEC-WAM-HOT-CORE Live Dashboard

A cutting-edge, real-time dashboard featuring live Google Sheets data synchronization, interactive 3D star maps, cryptocurrency pricing, a theatrical biometric lock screen interface, and **EVE - an advanced AI voice assistant**.

## ✨ Features

### Core Functionality
- **Live Google Sheets Integration** - Auto-fetches CSV data from Google Sheets with 5-minute auto-refresh
- **Color-Coded Status System** - Visual status indicators (PERFECT=Green, TODO=Yellow, ACTIVE=Blue, STABLE=Gray)
- **Real-Time PSI-Coin Pricing** - Live cryptocurrency prices from CoinGecko API
- **Interactive 3D Star Map** - Three.js-powered visualization of celestial bodies
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
- Downloadable data exports (CSV)
- Status distribution analytics
- Numeric value analysis and charting
- Voice-enabled chat interface
- API endpoints for serverless deployment

## 🚀 Live Demo

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

This repository is configured to automatically deploy to GitHub Pages.

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
