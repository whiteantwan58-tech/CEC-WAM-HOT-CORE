# 🔮 CEC-WAM-HOT-CORE Repository Setup

## Quick Reference: Deployment URLs

This repository supports **multiple deployment types**. Make sure you're accessing the right one!

### 🌐 Live Deployments

| Platform | Purpose | URL | Entry File |
|----------|---------|-----|------------|
| **Streamlit Cloud** | Dynamic Python Dashboard | `https://[your-app].streamlit.app` | `streamlit_app.py` |
| **GitHub Pages** | Static HTML Dashboard | `https://whiteantwan58-tech.github.io/CEC-WAM-HOT-CORE/` | `index.html` |

---

## 🚨 IMPORTANT: Fixing "23 Open Sessions" / Blank Screen

### The Problem

If you're seeing:
- ❌ Blank screen on your Streamlit app
- ❌ "23 open sessions" error
- ❌ Old data showing instead of new data
- ❌ App not updating after pushing changes

**This means:** Your Streamlit Cloud deployment is pointing to the **wrong repository** or has **multiple stale instances** running.

### The Solution (3 Steps)

#### Step 1: Delete ALL Old Streamlit Deployments

1. Go to: https://share.streamlit.io/manage
2. Look for ANY app related to "CEC-WAM", "PSI", "HOT-CORE", etc.
3. Click the "⋮" menu on each → "Delete"
4. Delete ALL old instances (this clears the 23 sessions)

#### Step 2: Clear GitHub Actions Queue

1. Go to: https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/actions
2. Click on any "In Progress" or "Queued" workflows
3. Click "Cancel workflow" for each one
4. This stops the session jam

#### Step 3: Deploy Fresh Instance

1. Go to: https://share.streamlit.io
2. Click "New app"
3. **USE THESE EXACT SETTINGS:**
   ```
   Repository: whiteantwan58-tech/CEC-WAM-HOT-CORE
   Branch: main
   Main file path: streamlit_app.py
   ```
4. Click "Deploy!"
5. Wait 2-5 minutes for build

#### Step 4: Verify Live Data

Once deployed, check these metrics are showing:

| Metric | Expected Value |
|--------|----------------|
| 💎 PSI Peg | $0.003466 |
| 📊 System Mass | 100,001.33 |
| 📈 Area Rate | 14.29% |
| 🟢 Status | SYNCHRONIZED |

If data looks wrong:
- Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
- Enable "🔒 Use Frozen/Locked Data" checkbox in the app

---

## 📚 Full Documentation

### For Streamlit Cloud Deployment
→ See: **[STREAMLIT_DEPLOYMENT.md](./STREAMLIT_DEPLOYMENT.md)**

Covers:
- Complete deployment guide
- Troubleshooting blank screens
- Fixing repository mismatch
- Clearing multiple sessions
- Configuring data sources

### For Static HTML Deployment (GitHub Pages)
→ See: [`.github/workflows/deploy-dashboard.yml`](.github/workflows/deploy-dashboard.yml)

For setup instructions, see the [GitHub Pages documentation](https://docs.github.com/en/pages).

Covers:
- Static site deployment
- GitHub Pages setup
- Custom domains

---

## 🔧 Repository Structure

```
CEC-WAM-HOT-CORE/
├── streamlit_app.py          # ← Streamlit Cloud entry point (NEW!)
├── app.py                     # Main Streamlit dashboard code
├── index.html                 # Static HTML dashboard
├── dashboard.html             # Alternative HTML dashboard
├── requirements.txt           # Python dependencies
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── .github/workflows/
│   └── deploy-dashboard.yml  # GitHub Pages deployment
├── data/                      # CSV data files
├── js/                        # JavaScript modules
└── README.md                  # This file
```

---

## 🎯 Which Deployment Should I Use?

### Use **Streamlit Cloud** if:
- ✅ You want live Python data processing
- ✅ You need real-time Google Sheets integration
- ✅ You want NASA API, PSI prices, and dynamic charts
- ✅ You need the full interactive dashboard

### Use **GitHub Pages** if:
- ✅ You want the fastest loading times
- ✅ You prefer pure HTML/CSS/JS (no Python)
- ✅ You need guaranteed 24/7 uptime
- ✅ You want to serve from custom domain

**Recommendation:** Use **Streamlit Cloud** for the full interactive experience!

---

## 🚀 Quick Start Commands

### Test Streamlit App Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py

# Access at: http://localhost:8501
```

### Test Static HTML Locally

```bash
# Option 1: Python HTTP server
python3 -m http.server 8080

# Option 2: Node.js server
npx http-server -p 8080

# Access at: http://localhost:8080/index.html
```

---

## 🔒 Security & Data Sources

### Data Sources

1. **Frozen/Locked Sheet** (Recommended)
   - Sheet ID: `14nNp33Dk2YoYcVcQI0lUEp208m-VvZboi_Te8jt_flg2NkNm8WieN0sX`
   - Secure, validated data
   - Enable with checkbox in app

2. **Primary Sheet** (Alternative)
   - Public CSV export
   - Live editing capabilities
   - Toggle in app settings

### API Endpoints

- NASA APOD: `api.nasa.gov/planetary/apod`
- CoinGecko (PSI): `api.coingecko.com/api/v3/simple/price`
- Google Sheets: Published CSV URLs

---

## 📞 Support & Issues

### Deployment Problems?

1. **Check this guide first:** [STREAMLIT_DEPLOYMENT.md](./STREAMLIT_DEPLOYMENT.md)
2. **GitHub Issues:** [Create an issue](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/issues)
3. **Streamlit Docs:** [docs.streamlit.io](https://docs.streamlit.io)

### Common Issues

| Problem | Solution |
|---------|----------|
| Blank screen | See "Fixing 23 Open Sessions" above |
| Old data showing | Hard refresh browser, toggle data source |
| App won't load | Check deployment logs, verify requirements.txt |
| Permission error | Grant Streamlit access to repo in GitHub settings |

---

## ✅ Pre-Deployment Checklist

Before deploying to Streamlit Cloud:

- [ ] Deleted all old Streamlit app instances
- [ ] Cancelled any running GitHub Actions workflows
- [ ] Repository is: `whiteantwan58-tech/CEC-WAM-HOT-CORE`
- [ ] Branch is: `main`
- [ ] Entry point is: `streamlit_app.py`
- [ ] `requirements.txt` is complete
- [ ] `.streamlit/config.toml` exists
- [ ] Granted Streamlit access to this repo

---

## 🌟 What's New

### Recent Updates

- ✅ Added `streamlit_app.py` - Official Streamlit Cloud entry point
- ✅ Added `STREAMLIT_DEPLOYMENT.md` - Complete deployment guide
- ✅ Enhanced `.streamlit/config.toml` - Better performance settings
- ✅ Added `DEPLOYMENT_QUICK_START.md` - This file!

---

**🔮 SOVEREIGN SYSTEM v2.0 | φ=1.618 | QUANTUM ENTANGLED**

*One repository. Multiple deployments. Always synchronized.*

---

## 🧪 5D Interface Live Check (All Repositories)

If your mobile deploy flow shows multiple repos and you need to verify which one is truly live, run:

```bash
# Optional but recommended for higher GitHub API rate limits
export GITHUB_TOKEN=your_token_here

python3 tools/repo_interface_audit.py --owner whiteantwan58-tech
```

What this checks for each repository:
- write/admin vs read-only permission (helps identify deploy-key lockouts)
- Streamlit entry point (`streamlit_app.py` or `app.py`)
- static interface entry point (`index.html` or `dashboard.html`)
- GitHub Pages status
- archived state

A JSON report is saved to:

```text
reports/repo_interface_audit.json
```

Use this to quickly confirm `CEC-WAM-HOT-CORE` is the active repo for the 5D interface deployment.
