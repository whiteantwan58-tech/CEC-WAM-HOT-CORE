# CEC-WAM LIVE — EVE HEI (PWA)

This repository contains a PWA frontend to connect the CEC WAM Living Calculator (Google Sheet / CSV / local file), providing:

- Live fetch & merge from a published Google Sheet (CSV) URL.
- Import local CSV/XLSX (CSV parsing included; for XLSX use a converter).
- Voice input (Web Speech API) and TTS for EVE HEI interactions.
- Persistent local storage (IndexedDB via localForage) so it works offline.
- Charts (Chart.js) and export of logs (CSV).
- PWA manifest + Service Worker for installable app.
- **NEW: Automated chart and data management system**

## 🎯 Chart Automation System

This repository now includes an automated system for linking and updating charts across all data sources:

### Features

✅ **Automated Data Discovery** - Automatically finds and processes all CSV files
✅ **Chart.xlsx Updates** - Keeps Excel file synchronized with latest data  
✅ **Live Chart Data** - Generates JSON data for web visualization
✅ **REST API** - Flask-based API for data access
✅ **Frontend Integration** - Terminal commands for chart access
✅ **Scheduled Updates** - Automatic periodic data refreshes

### Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run automation:**
```bash
python chart_automation.py
```

3. **Start all services:**
```bash
./start_services.sh
```

This will start:
- Frontend at `http://localhost:8000`
- API server at `http://localhost:5000`

### Terminal Commands

Access chart data through the EVE terminal in the web interface:

- `charts` - Display available chart datasets
- `automation` - Show automation status and last update
- `help` - Show all available commands

### Documentation

For complete documentation, see [CHART_AUTOMATION_DOCS.md](CHART_AUTOMATION_DOCS.md)

## Important security notes

- Do not commit secrets (API keys or passcodes) into the repo. The app provides a device-only PIN you can set locally (stored as a salted hash in IndexedDB).
- If you want server-based integrations or remote access, configure secure auth (OAuth2) and server-side credentials — not stored in the client.

## Quick start (Original Features)

1. Publish your Google Sheet:
   - In Google Sheets: File → Publish to web → Choose sheet → Comma-separated values (CSV) → Publish.
   - Copy the CSV URL (it will include `output=csv`).
2. Open `index.html` in a web server (recommended), or push to GitHub Pages.
   - To test locally: run `python -m http.server 8000` in the folder and browse to `http://localhost:8000`.
   - To run from a flash drive offline: copy the folder to the drive and run a local static server from that machine.
3. Paste the CSV URL in the UI, click Link → Fetch Now.
4. To import local data, use the Import file input.
5. Use the "Talk (Mic)" button to add voice-entered log entries; the app will reply via TTS.

## Offline use

- The app caches the UI shell and the most recent CSV. Data is persisted in IndexedDB.
- If you need a fully offline central server, run a small Raspberry Pi or laptop with a local static server and keep it powered; this app will access it via local network.

## Data Sources

The automation system processes these CSV files:

- `pump.fun.csv` - Solana transaction data
- `BlackHoles.csv` - Discovery and research data  
- `CEC Matrix System Operational Metrics and Assets - FINANCE_HUB (1).csv` - Financial assets
- `data/ledger.csv` - System ledger
- `data/timeline.csv` - Project timeline

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/chart-data` - Chart visualization data
- `GET /api/automation-status` - Automation status report
- `GET /api/datasets` - List available datasets
- `GET /api/live-data` - Aggregated live metrics
- `POST /api/run-automation` - Trigger automation

## Architecture

```
┌─────────────────┐
│  index.html     │ ← Frontend (Port 8000)
│  (Terminal UI)  │
└────────┬────────┘
         │
         ↓ REST API
┌─────────────────┐
│  api_server.py  │ ← Flask API (Port 5000)
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│chart_automation │ ← Data Processing
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   CSV Files     │ → Chart.xlsx
│   Chart Data    │
└─────────────────┘
```

## Next steps

- Add XLSX parsing (SheetJS) and map known spreadsheet columns into dashboard KPIs.
- Implement row-level filters (only CEC WAM rows and date = Nov 6).
- Add charts per-sheet (pie/line/time series) and a detailed Log tab with date & time per imported/received row.
- Add user-friendly export ZIP of full static site + data for flash drive transfer.
