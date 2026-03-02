# 🔮 CEC-WAM-HOT-CORE — EVE HEI Live Dashboard

> **The operational command center for the CEC-WAM system** — live data, 5D holographic interface, and EVE AI voice assistant.

[![Deploy to GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-success?logo=github)](https://whiteantwan58-tech.github.io/CEC-WAM-HOT-CORE/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-red?logo=streamlit)](https://streamlit.io/cloud)
[![Secret Scanning](https://img.shields.io/badge/Secret%20Scanning-gitleaks-blue)](https://github.com/gitleaks/gitleaks)

---

## 🚀 Quick Start

### Option 1 — Streamlit Cloud (Recommended)

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Set **Main file** to `streamlit_app.py`
4. Add your secrets (see [🔑 Environment Variables](#-environment-variables))
5. Click **Deploy**

### Option 2 — Local Development

```bash
# Clone the repo
git clone https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE.git
cd CEC-WAM-HOT-CORE

# Install dependencies
pip install -r requirements.txt

# Copy and fill in your environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the dashboard
streamlit run streamlit_app.py
```

### Option 3 — Static HTML (GitHub Pages)

Push to `main` — the GitHub Actions workflow automatically deploys `index.html` to GitHub Pages.

---

## 🌟 Features

| Feature | Description |
|---------|-------------|
| 📊 **Live Data** | Real-time Google Sheets integration with 30-second auto-refresh |
| 🌌 **5D Holographic UI** | Premium glassmorphic design with animated particle system |
| 🔮 **EVE AI Assistant** | Voice-enabled AI with ElevenLabs synthesis and OpenAI reasoning |
| 🛰️ **NASA APOD** | Live Astronomy Picture of the Day with stellar visuals |
| 🪙 **PSI Token Price** | Real-time TridentDAO / PSI price via CoinGecko |
| 🌤️ **Weather** | OpenWeatherMap integration for live conditions |
| 🗺️ **Interactive Map** | Federal Way real-time map with asset overlays |
| 🔐 **Biometric UI** | Visual authentication panel with verification badges |
| 📈 **Asset Ledger** | CSV / Excel ledger display with live refresh |
| ♻️ **Auto-Refresh** | Configurable 30-second live data cycle with toggle control |

---

## 🔑 Environment Variables

Copy `.env.example` to `.env` and fill in your values. **Never commit `.env`** — it is listed in `.gitignore`.

```bash
cp .env.example .env
```

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_SHEETS_URL` | ✅ | Published CSV URL for the live data sheet |
| `FROZEN_SHEET_ID` | ⬜ | Sheet ID for the secure/locked ledger sheet |
| `NASA_API_KEY` | ⬜ | Free key from [api.nasa.gov](https://api.nasa.gov/) |
| `OPENWEATHER_API_KEY` | ⬜ | Free key from [openweathermap.org](https://openweathermap.org/api) |
| `OPENAI_API_KEY` | ⬜ | For EVE AI reasoning |
| `OPENAI_MODEL` | ⬜ | Default: `gpt-4` |
| `ELEVENLABS_API_KEY` | ⬜ | For EVE voice synthesis |
| `ELEVENLABS_VOICE_ID` | ⬜ | ElevenLabs voice ID (default: Adam) |
| `GROQ_API_KEY` | ⬜ | For Groq-powered EVE Sovereign mode |
| `GROQ_MODEL` | ⬜ | Default: `llama-3.1-70b-versatile` |
| `EVE_SYSTEM_CODE` | ⬜ | EVE identifier code |
| `EVE_OWNER_NAME` | ⬜ | Owner name displayed in EVE responses |
| `EVE_PERSONALITY` | ⬜ | Comma-separated personality traits |

### For Streamlit Cloud

Add the variables above as secrets in the **Streamlit Cloud app settings** (TOML format):

```toml
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/e/<ID>/pub?output=csv"
NASA_API_KEY = "your-key"
OPENAI_API_KEY = "your-key"
ELEVENLABS_API_KEY = "your-key"
```

### Setting Up Google Sheets Live Data

1. Open your Google Sheet
2. **File → Share → Publish to web → Comma-separated values (.csv)**
3. Copy the published URL
4. Set it as `GOOGLE_SHEETS_URL` in your `.env` or Streamlit secrets

Expected CSV columns: `Category`, `Item`, `Value`, `Status`, `Date`, `Notes`

---

## 📁 Project Structure

```
CEC-WAM-HOT-CORE/
├── streamlit_app.py          # 🎯 Primary entry point (Streamlit Cloud)
├── app.py                    # Alternative Streamlit dashboard
├── index.html                # Static HTML dashboard (GitHub Pages)
├── dashboard.html            # Full-featured HTML dashboard
├── eve_voice_agent.py        # EVE AI voice assistant
├── Eve_sovereign_v6_updated.py # EVE Sovereign mode (Groq)
├── cec_dashboard.py          # CEC Matrix dashboard
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
├── .gitleaks.toml            # Secret scanning configuration
├── .streamlit/
│   └── config.toml           # Streamlit server configuration
├── api/
│   ├── chat.py               # Chat API endpoint
│   └── voice.py              # Voice API endpoint
├── js/
│   ├── starmap.js            # 3D star map visualization
│   ├── crime-alerts.js       # Crime alert feed
│   ├── federal-way-feed.js   # Federal Way live data
│   └── google-drive-export.js # Google Drive export
├── data/
│   ├── CEC_Matrix_System_Operational_Metrics_and_Assets.csv
│   ├── CEC_WAM_MASTER_LEDGER_LIVE.xlsx
│   └── EVE_UNFINISHED_TASKS.csv
└── .github/
    └── workflows/
        ├── deploy-dashboard.yml  # GitHub Pages auto-deploy
        ├── codeql.yml            # CodeQL security analysis
        └── secret-scanning.yml  # Gitleaks secret scanning
```

---

## 🧪 Testing

```bash
python -m pytest test_eve.py -v
```

The test suite validates API configurations, environment variable loading, and EVE agent initialization.

---

## 🔒 Security

- All API keys are loaded from environment variables — **never hardcoded**
- `.env` is excluded from version control via `.gitignore`
- Secret scanning runs on every push via gitleaks
- CodeQL static analysis runs on every PR
- Streamlit server has CSRF protection enabled (`.streamlit/config.toml`)
- See [SECURITY.md](./SECURITY.md) for vulnerability reporting

---

## 🚀 GitHub Actions Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `deploy-dashboard.yml` | Push to `main` | Deploy `index.html` to GitHub Pages |
| `codeql.yml` | Push/PR to `main` | CodeQL security analysis |
| `secret-scanning.yml` | Every push/PR | Gitleaks secret detection |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — open source and free to use.

---

**Built with ❤️ by the CEC-WAM Team**

🌌 *Exploring the cosmos, one datapoint at a time* 🌌
