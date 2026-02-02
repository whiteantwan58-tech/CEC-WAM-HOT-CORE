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
