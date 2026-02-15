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

## 🌐 Deployment Guide

### Deploy to Streamlit Cloud

1. **Push your code to GitHub**
```bash
git add .
git commit -m "Deploy to Streamlit"
git push origin main
```

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**

3. **Connect your GitHub repository**
   - Click "New app"
   - Select your repository: `whiteantwan58-tech/CEC-WAM-HOT-CORE`
   - Set main file: `app.py`
   - Click "Deploy"

4. **Configure Secrets (optional, for Google Sheets logging)**
   - In Streamlit Cloud dashboard, go to app settings
   - Add secrets in TOML format:
   ```toml
   GOOGLE_SHEETS_CREDS = '{"type": "service_account", "project_id": "...", ...}'
   LOG_SHEET_ID = "your-sheet-id"
   ```

### Deploy to Vercel

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Deploy**
```bash
vercel
```

3. **Follow prompts** to link your GitHub repository

### Deploy to GitHub Pages

1. **Enable GitHub Pages**
   - Go to repository Settings > Pages
   - Source: Deploy from a branch
   - Branch: `main` or `copilot/...`
   - Folder: `/` (root)

2. **Access your site**
   - URL: `https://whiteantwan58-tech.github.io/CEC-WAM-HOT-CORE/`
   - The `index.html` file will be served automatically

## 🎙️ EVE Voice AI Assistant Configuration

### Overview
EVE (Evolved Virtual Entity) is an advanced AI assistant with voice capabilities, designed specifically for **Twan** with the system code `CEC_WAM_HEI_EVE_7A2F-9C4B`.

### Required API Keys

#### 1. ElevenLabs API (Voice Synthesis)
1. **Sign up at [ElevenLabs](https://elevenlabs.io/)**
2. Navigate to your profile and get your API key
3. Browse the voice library and select a voice (default: Rachel - `21m00Tcm4TlvDq8ikWAM`)
4. Add to your `.env` file:
   ```bash
   ELEVENLABS_API_KEY=your-elevenlabs-api-key
   ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
   ```

#### 2. OpenAI API (AI Chat)
1. **Sign up at [OpenAI Platform](https://platform.openai.com/)**
2. Create an API key in your account settings
3. Choose your model (recommended: `gpt-4` or `gpt-3.5-turbo`)
4. Add to your `.env` file:
   ```bash
   OPENAI_API_KEY=your-openai-api-key
   OPENAI_MODEL=gpt-4
   ```

### EVE Configuration

Edit your `.env` file with EVE-specific settings:

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
