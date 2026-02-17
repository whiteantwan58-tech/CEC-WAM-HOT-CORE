# Streamlit Cloud Deployment Guide

## 🚀 Quick Start: Deploy to Streamlit Cloud

### Prerequisites
- A Streamlit Cloud account (sign up at [share.streamlit.io](https://share.streamlit.io))
- Access to this GitHub repository

### Deployment Steps

#### 1. Connect to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"

#### 2. Configure Your App

**IMPORTANT: Use these exact settings to avoid the "blank screen" issue**

```
Repository: whiteantwan58-tech/CEC-WAM-HOT-CORE
Branch: main
Main file path: streamlit_app.py
```

**App URL (optional):** 
- You can customize this to: `cec-wam-hot-core` or similar
- Example: `https://your-username-cec-wam-hot-core.streamlit.app`

#### 3. Advanced Settings (Optional)

Click "Advanced settings" to add:

**Python version:** 3.11 (recommended)

**Secrets (if needed):**
```toml
# Add any API keys here
NASA_API_KEY = "your-key-here"
GOOGLE_SHEETS_URL = "your-sheets-url"
```

#### 4. Deploy

1. Click "Deploy!"
2. Wait for the build to complete (2-5 minutes)
3. Your app will be live at: `https://[your-app-name].streamlit.app`

---

## 🔧 Fixing "23 Open Sessions" / Blank Screen Issue

### Problem Description
If you see a blank screen or have multiple deployments/sessions running, this is usually caused by:
1. **Wrong repository configured** - Streamlit is looking at an old/different repo
2. **Multiple deployment instances** - Old deployments still running
3. **Cached build issues** - Old builds interfering with new ones

### Solution: Clean Slate Deployment

#### Step 1: Delete Old Deployments

1. Go to [share.streamlit.io/manage](https://share.streamlit.io/manage)
2. Find ALL old instances of your app
3. Delete each one by clicking the "⋮" menu → "Delete"
4. Confirm deletion for each instance

#### Step 2: Clear GitHub Actions (if applicable)

1. Go to this repository's Actions tab on GitHub
2. Click on any running/queued workflows
3. Click "Cancel workflow" for all in-progress runs
4. This clears the "session jam"

#### Step 3: Create Fresh Deployment

1. Go back to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Use the EXACT configuration above:
   - Repository: `whiteantwan58-tech/CEC-WAM-HOT-CORE`
   - Branch: `main`
   - Main file: `streamlit_app.py`
4. Deploy!

---

## 📊 Verifying Live Data

Once deployed, your dashboard should show these real-time metrics:

| Metric | Expected Value |
|--------|----------------|
| Psi Peg | $0.003466 |
| System Mass | 100,001.33 |
| Area Rate | 14.29% |
| Status | 🟢 SYNCHRONIZED |

### If Data Looks Wrong

1. **Hard refresh your browser:**
   - Windows/Linux: `Ctrl + Shift + R`
   - Mac: `Cmd + Shift + R`

2. **Check the data source toggle:**
   - Look for "🔒 Use Frozen/Locked Data" checkbox
   - Enable it to use the secure, locked data source

3. **Force a rerun:**
   - Click the "⋮" menu in top-right of Streamlit app
   - Select "Rerun"

---

## 🔍 Troubleshooting

### Blank Screen After Deployment

**Cause:** Streamlit is still loading or there's a Python error

**Solution:**
1. Check the deployment logs in Streamlit Cloud dashboard
2. Look for Python errors or missing dependencies
3. Ensure `requirements.txt` is present and complete
4. Try restarting the app from Streamlit Cloud dashboard

### "Repository not found" Error

**Cause:** Streamlit doesn't have permission to access the repo

**Solution:**
1. Go to GitHub Settings → Applications → Streamlit
2. Grant repository access to `whiteantwan58-tech/CEC-WAM-HOT-CORE`
3. Retry deployment

### Data Not Loading

**Cause:** Google Sheets or API endpoints not accessible

**Solution:**
1. Verify Google Sheets is published publicly (CSV export)
2. Check that the sheet URL in `app.py` is correct
3. Test the URL manually in a browser
4. Ensure frozen sheet ID is valid: `14nNp33Dk2YoYcVcQI0lUEp208m-VvZboi_Te8jt_flg2NkNm8WieN0sX`

### Charts Not Rendering

**Cause:** Plotly or other dependencies missing

**Solution:**
1. Check `requirements.txt` includes:
   ```
   streamlit>=1.28.0
   pandas>=2.0.0
   plotly>=5.18.0
   requests>=2.31.0
   ```
2. Redeploy the app to reinstall dependencies

---

## 🔄 Updating Your Deployed App

Streamlit Cloud automatically redeploys when you push to GitHub:

```bash
git add .
git commit -m "Update dashboard"
git push origin main
```

The app will automatically rebuild within 1-2 minutes.

---

## 🌐 Multiple Deployment Options

This repository supports multiple deployment methods:

### 1. **Streamlit Cloud** (Dynamic Python App)
- **URL:** `https://[your-app].streamlit.app`
- **Entry:** `streamlit_app.py`
- **Best for:** Interactive Python-based dashboards
- **Guide:** This document

### 2. **GitHub Pages** (Static HTML)
- **URL:** `https://whiteantwan58-tech.github.io/CEC-WAM-HOT-CORE/`
- **Entry:** `index.html`
- **Best for:** Fast, static HTML dashboard
- **Guide:** See `VERCEL_DEPLOYMENT.md`

### 3. **Vercel** (Static HTML with Edge)
- **URL:** Custom domain via Vercel
- **Entry:** `index.html`
- **Best for:** Production static deployments
- **Guide:** See `VERCEL_DEPLOYMENT.md`

**Note:** Choose ONE primary deployment method to avoid confusion.

---

## 📞 Support

### Streamlit Cloud Issues
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community Forum](https://discuss.streamlit.io)
- [GitHub Issues](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/issues)

### Repository Issues
- Open an issue on [GitHub](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/issues)
- Check existing issues for solutions

---

## ✅ Deployment Checklist

Before deploying to Streamlit Cloud, ensure:

- [ ] Repository is `whiteantwan58-tech/CEC-WAM-HOT-CORE`
- [ ] Branch is set to `main`
- [ ] Main file path is `streamlit_app.py`
- [ ] `requirements.txt` includes all dependencies
- [ ] `.streamlit/config.toml` is configured
- [ ] Google Sheets URLs are correct in `app.py`
- [ ] Old deployments are deleted
- [ ] GitHub Actions are not queued/running

---

**🔮 Built for the CEC-WAM SOVEREIGN SYSTEM | OMEGA_LOCK**

*One repository, multiple deployment options. Choose Streamlit for dynamic Python dashboards.*
