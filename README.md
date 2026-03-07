# Quantum Sovereign — CEC-WAM LIVE · EVE HEI

[![Secret Scanning](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/actions/workflows/secret-scanning.yml/badge.svg)](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/actions/workflows/secret-scanning.yml)
[![CodeQL](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/actions/workflows/codeql.yml/badge.svg)](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/actions/workflows/codeql.yml)
[![Deploy Dashboard](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/actions/workflows/deploy-dashboard.yml/badge.svg)](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/actions/workflows/deploy-dashboard.yml)

A high-tech, 5D holographic quantum sovereign logistics dashboard featuring live Google Sheets data, PSI cryptocurrency tracking, biometric UI, and EVE — an advanced AI voice assistant.

---

## Project Structure

```
CEC-WAM-HOT-CORE/
├── app.py                   # Main Streamlit app (30s auto-refresh, recommended)
├── streamlit_app.py         # Alternate Streamlit entry point (60s manual toggle)
├── cec_dashboard.py         # Legacy CEC Matrix dashboard
├── dashboard.html           # Standalone HTML dashboard (no dependencies)
├── index.html               # PWA frontend
├── eve_voice_agent.py       # EVE HEI voice agent
├── Eve_sovereign_v6_updated.py  # EVE Sovereign v6
├── test_eve.py              # EVE smoke-test script (run via __main__)
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── .gitleaks.toml           # Secret scanning configuration
├── data/                    # CSV/XLSX data files
│   ├── CEC_WAM_MASTER_LEDGER_LIVE.xlsx
│   ├── CEC_Matrix_System_Operational_Metrics_and_Assets.csv
│   └── EVE_UNFINISHED_TASKS.csv
├── api/                     # Serverless API endpoints
├── js/                      # JavaScript utilities
└── .github/workflows/       # CI workflows
```

---

## Quick Start

```bash
git clone https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE.git
cd CEC-WAM-HOT-CORE
pip install -r requirements.txt
cp .env.example .env   # fill in your keys — see table below
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Environment Variables

> Copy `.env.example` → `.env` and fill in your values.  
> **Never commit `.env`** — it is listed in `.gitignore`.

| Variable | Required | Default | Where to get it |
|---|---|---|---|
| `GOOGLE_SHEETS_URL` | Recommended | — | Sheets → File → Share → Publish to web → CSV |
| `FROZEN_SHEET_ID` | Optional | — | Sheet URL: `…/spreadsheets/d/<ID>/edit` |
| `NASA_API_KEY` | Optional | `DEMO_KEY` | [api.nasa.gov](https://api.nasa.gov/) — free, instant |
| `OPENWEATHER_API_KEY` | Optional | — | [openweathermap.org/api](https://openweathermap.org/api) — free tier |
| `OPENAI_API_KEY` | Optional (EVE AI) | — | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| `OPENAI_MODEL` | Optional | `gpt-4` | — |
| `ELEVENLABS_API_KEY` | Optional (EVE voice) | — | [elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys) |
| `ELEVENLABS_VOICE_ID` | Optional | `21m00Tcm4TlvDq8ikWAM` | ElevenLabs voice library |
| `GROQ_API_KEY` | Optional (EVE Sovereign) | — | [console.groq.com/keys](https://console.groq.com/keys) |
| `GROQ_MODEL` | Optional | `llama-3.1-70b-versatile` | — |
| `EVE_SYSTEM_CODE` | Optional | `CEC_WAM_HEI_EVE_7A2F-9C4B` | — |
| `EVE_OWNER_NAME` | Optional | — | Your name (e.g. `Twan`) |
| `EVE_PERSONALITY` | Optional | — | Comma-separated traits |

### Streamlit Cloud Secrets

In **Settings → Secrets**, use TOML format:

```toml
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/e/.../pub?output=csv"
NASA_API_KEY      = "your-key"
OPENAI_API_KEY    = "sk-..."
ELEVENLABS_API_KEY = "your-key"
GROQ_API_KEY      = "gsk_..."
EVE_OWNER_NAME    = "Twan"
```

### Google Sheets Setup

1. Open your sheet in Google Sheets.
2. **File → Share → Publish to web → Comma-separated values (.csv) → Publish**.
3. Copy the URL and set it as `GOOGLE_SHEETS_URL` in `.env` or Streamlit Secrets.
4. For the frozen/private sheet, copy the Sheet ID from the URL bar and set `FROZEN_SHEET_ID`.

---

## Deployment

### Streamlit Cloud (recommended)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), connect your repo.
3. Set **Main file path** to `app.py`.
4. Add secrets (see above).
5. Deploy.

### Standalone HTML Dashboard

Open `dashboard.html` directly in a browser — no server required.  
For full API functionality (CORS), serve it locally:

```bash
python3 -m http.server 8080
# Then visit http://localhost:8080/dashboard.html
```

### GitHub Pages

The `deploy-dashboard.yml` workflow publishes the root of the repo to GitHub Pages on every push to `main`.

---

## CI Workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| `secret-scanning.yml` | push / PR / weekly | Gitleaks secret detection |
| `codeql.yml` | push / PR / weekly | CodeQL static analysis |
| `deploy-dashboard.yml` | push to `main` / manual | GitHub Pages deployment |

---

## Testing

`test_eve.py` is a standalone smoke-test script for the EVE agent. Run it directly:

```bash
python test_eve.py
```

---

## Security

- Secrets are managed via `.env` (local) or Streamlit Cloud Secrets (production).
- Gitleaks scans every push and pull request; configuration lives in `.gitleaks.toml`.
- Historical commits containing rotated keys are covered by the commits allowlist in `.gitleaks.toml`.
- See [SECURITY.md](./SECURITY.md) for the vulnerability disclosure policy.

---

## Documentation

| File | Purpose |
|---|---|
| [API_SETUP_GUIDE.md](./API_SETUP_GUIDE.md) | Detailed API key setup |
| [BIOMETRIC_AUTH.md](./BIOMETRIC_AUTH.md) | WebAuthn biometric authentication |
| [DEPLOYMENT_QUICK_START.md](./DEPLOYMENT_QUICK_START.md) | Deployment troubleshooting |
| [ELEVENLABS_CONFIG.md](./ELEVENLABS_CONFIG.md) | ElevenLabs voice configuration |
| [EVE_QUICK_START.md](./EVE_QUICK_START.md) | EVE agent quick-start |
| [EVE_SETUP_GUIDE.md](./EVE_SETUP_GUIDE.md) | Full EVE setup guide |
| [MAP_FEATURES_GUIDE.md](./MAP_FEATURES_GUIDE.md) | Map & camera feature guide |
| [STREAMLIT_DEPLOYMENT.md](./STREAMLIT_DEPLOYMENT.md) | Streamlit deployment guide |
| [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) | Common issues and fixes |
