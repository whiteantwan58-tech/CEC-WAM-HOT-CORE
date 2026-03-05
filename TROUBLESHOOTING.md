# Troubleshooting Guide — Quantum Sovereign · CEC-WAM

## Overview
This guide addresses common errors and issues when running the Quantum Sovereign /
CEC-WAM Streamlit applications (`app.py` and `streamlit_app.py`).

---

## Table of Contents
1. [.env Configuration](#env-configuration)
2. [Installation Issues](#installation-issues)
3. [Streamlit Runtime Errors](#streamlit-runtime-errors)
4. [Data Loading Errors](#data-loading-errors)
5. [API Integration Errors](#api-integration-errors)
6. [Display & UI Errors](#display--ui-errors)
7. [Performance Issues](#performance-issues)
8. [Deployment Issues](#deployment-issues)

---

## .env Configuration

### Step-by-step First-Time Setup

1. **Copy the template:**
   ```bash
   cp .env.example .env
   ```

2. **Verify the file was created:**
   ```bash
   ls -la .env
   ```

3. **Open and edit `.env`** in your editor and fill in your API keys.
   At minimum you need `GOOGLE_SHEETS_URL` for live data. All other keys are optional
   but unlock additional features (EVE AI, voice synthesis, weather).

4. **Verify values load correctly:**
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   print("Sheets URL:", os.getenv("GOOGLE_SHEETS_URL", "NOT SET"))
   print("NASA key  :", os.getenv("NASA_API_KEY", "DEMO_KEY (default)"))
   ```

### Common `.env` Issues

**Variables not loading (values appear as `None`)**

```
API key is None or empty
```

Checklist:
- The file must be named exactly `.env` (not `.env.txt` or `env`)
- Each line must be `KEY=value` with **no spaces around `=`**
- String values do **not** need quotes in a `.env` file
- Run `pip install python-dotenv` if `load_dotenv` is unavailable
- Make sure you're running the app from the project root directory

**`.env` file is committed to git**

```bash
# Remove it immediately and rotate all exposed keys
git rm --cached .env
echo ".env" >> .gitignore
git commit -m "remove accidentally committed .env"
```

Then rotate every key that was exposed. See [SECURITY.md](./SECURITY.md) for details.

**Google Sheets JSON credentials formatting**

The `GOOGLE_SHEETS_CREDS` value (service-account JSON) must be a **single line** —
no newlines inside the value:

```env
# ✅ Correct — single line
GOOGLE_SHEETS_CREDS={"type":"service_account","project_id":"...","private_key":"-----BEGIN RSA...\\n-----END RSA...\\n","client_email":"..."}

# ❌ Wrong — multi-line breaks .env parsing
GOOGLE_SHEETS_CREDS={
  "type": "service_account",
  ...
}
```

Minify the JSON before pasting it:
```python
import json
with open("service_account.json") as f:
    print(json.dumps(json.load(f)))
```

---


3. [Data Loading Errors](#data-loading-errors)
4. [API Integration Errors](#api-integration-errors)
5. [Display & UI Errors](#display--ui-errors)
6. [Performance Issues](#performance-issues)
7. [Deployment Issues](#deployment-issues)

---

## Installation Issues

### Missing Dependencies

**Error:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
```bash
pip install -r requirements.txt
```

**Verify Installation:**
```bash
pip list | grep streamlit
```

---

### Version Conflicts

**Error:**
```
ImportError: cannot import name 'st_autorefresh'
```

**Solution:**
```bash
pip install streamlit-autorefresh>=1.0.1
# or
pip install --upgrade streamlit-autorefresh
```

---

### Python Version Issues

**Error:**
```
SyntaxError: invalid syntax
```

**Solution:**
Ensure Python 3.8+ is installed:
```bash
python --version  # Should be 3.8 or higher
# If not, install Python 3.8+
```

---

## Streamlit Runtime Errors

### st.dataframe() Errors

#### Error: Empty DataFrame
```python
StreamlitAPIException: Expected bytes, got <class 'NoneType'>
```

**Cause:** DataFrame is None or empty

**Solution in Code:**
```python
# Bad
st.dataframe(df)

# Good - with validation
if df is not None and not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data available")
```

---

#### Error: Column Configuration Mismatch
```python
StreamlitAPIException: Column 'XYZ' not found
```

**Cause:** column_config references non-existent column

**Solution:**
```python
# Check columns exist before configuring
available_columns = df.columns.tolist()
column_config = {}

if 'Value' in available_columns:
    column_config['Value'] = st.column_config.NumberColumn(
        "Value",
        format="$%.2f"
    )

st.dataframe(df, column_config=column_config)
```

---

### Session State Errors

**Error:**
```
AttributeError: st.session_state has no attribute 'messages'
```

**Solution:**
```python
# Always initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'auto_refresh_enabled' not in st.session_state:
    st.session_state.auto_refresh_enabled = True
```

---

### Auto-Refresh Issues

**Error:**
```
Too many reruns - streamlit is stuck in a rerun loop
```

**Cause:** Unconditional st.rerun() or conflicting state updates

**Solution:**
```python
# Bad
if st.button("Refresh"):
    st.rerun()  # Causes loop

# Good
if st.button("Refresh"):
    st.cache_data.clear()
    st.rerun()

# Or use st_autorefresh instead
from streamlit_autorefresh import st_autorefresh
count = st_autorefresh(interval=30000, key="refresh")
```

---

## Data Loading Errors

### Google Sheets CSV Errors

**Error:**
```
ParserError: Error tokenizing data
urllib.error.HTTPError: HTTP Error 404: Not Found
```

**Causes:**
1. Sheet not published
2. Incorrect URL format
3. Sheet deleted or permissions changed

**Solutions:**

**1. Verify Sheet is Published:**
```
File → Share → Publish to web → Entire Document → CSV
```

**2. Check URL Format:**
```python
# Correct format for published sheet
SHEETS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-{SHEET_ID}/pub?output=csv"

# Test in browser first
# Should download CSV file
```

**3. Add Error Handling:**
```python
@st.cache_data(ttl=30)
def fetch_sheets_data():
    try:
        df = pd.read_csv(GOOGLE_SHEETS_URL, timeout=10)
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {e}")
        return None
    except pd.errors.ParserError as e:
        st.error(f"CSV parsing error: {e}")
        return None
    except Exception as e:
        st.warning(f"Data load error: {e}")
        return None
```

---

### NASA API Errors

**Error: Rate limit exceeded**
```
requests.exceptions.HTTPError: 429 Too Many Requests
```

**Cause:** `DEMO_KEY` is limited to 30 requests/hour per IP address.

**Fix:**
1. Get a free key (instant) at <https://api.nasa.gov/>
2. Set it in your `.env`:
   ```env
   NASA_API_KEY=YOUR_KEY_HERE
   ```
   Free keys get **1,000 requests/hour**.

**Error: Connection refused / network unreachable**
```
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='api.nasa.gov', port=443)
```

**Cause:** No internet access or DNS failure in the deployment environment.

**Behaviour in `app.py`:** The `fetch_nasa_apod()` function now returns a demo fallback
image instead of `None`, so the UI remains functional. An informational banner is shown
indicating that live data is unavailable.

**Fix:** Ensure outbound HTTPS traffic to `api.nasa.gov` is allowed in your firewall /
proxy settings. On Streamlit Cloud this is allowed by default.

---

### NOAA Weather API Errors (`api.weather.gov`)

**Error:**
```
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='api.weather.gov', port=443)
```

**Cause:** The NOAA API requires no API key but **does** require a `User-Agent` header
and outbound HTTPS access.

**Behaviour in `streamlit_app.py`:** `get_weather_alerts()` catches all exceptions and
returns demo alert data, so the UI always renders.

**Fix:**
- Ensure `User-Agent` is set (already done in the app):
  ```python
  headers = {'User-Agent': '(EVE-System, contact@evesystem.com)'}
  ```
- Check that outbound HTTPS to `api.weather.gov` is not blocked.

---


## API Integration Errors

### EVE Voice Agent Errors

**Error:**
```
ModuleNotFoundError: No module named 'openai'
AttributeError: module 'openai' has no attribute 'ChatCompletion'
```

**Solutions:**

**1. Install Required Packages:**
```bash
pip install openai>=1.3.0
pip install elevenlabs>=0.2.27
```

**2. Update OpenAI API Calls (v1.x syntax):**
```python
# Old syntax (0.x)
response = openai.ChatCompletion.create(...)

# New syntax (1.x+)
from openai import OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
response = client.chat.completions.create(...)
```

---

### Environment Variable Not Loading

**Error:**
```
API key is None or empty
```

**Debug Steps:**

**1. Check .env file exists:**
```bash
ls -la .env
```

**2. Verify content:**
```bash
cat .env | grep API_KEY
```

**3. Check loading in Python:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
print("NASA Key:", os.getenv('NASA_API_KEY'))
print("OpenAI Key:", os.getenv('OPENAI_API_KEY', 'Not found'))
```

**4. Streamlit-specific:**
For Streamlit Cloud, use `.streamlit/secrets.toml`:
```toml
NASA_API_KEY = "your_key"
OPENAI_API_KEY = "sk-..."
```

---

## Display & UI Errors

### CSS/Styling Issues

**Error:**
```
Markdown rendering broken
Custom CSS not applying
```

**Solutions:**

**1. Verify unsafe_allow_html:**
```python
st.markdown("""
    <style>
        .custom-class { color: #00FFFF; }
    </style>
""", unsafe_allow_html=True)  # Must be True
```

**2. Check for syntax errors:**
```python
# Bad - unclosed tag
st.markdown("<div style='color: red'>Text", unsafe_allow_html=True)

# Good
st.markdown("<div style='color: red;'>Text</div>", unsafe_allow_html=True)
```

**3. Escape special characters:**
```python
# For JavaScript/complex CSS
import html
safe_content = html.escape(user_content)
```

---

### Chart Rendering Errors

**Error:**
```
Plotly charts not displaying
Figure is empty
```

**Solutions:**

**1. Verify Plotly installation:**
```bash
pip install plotly>=5.18.0
```

**2. Check figure creation:**
```python
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=[1,2,3], y=[4,5,6]))
fig.update_layout(title="Test")

# Must call st.plotly_chart, not st.pyplot
st.plotly_chart(fig, use_container_width=True)
```

---

### Image Display Issues

**Error:**
```
Failed to load image
Image not found
```

**Solutions:**

**1. For URLs:**
```python
# Add error handling
try:
    st.image(image_url, use_column_width=True)
except Exception as e:
    st.warning(f"Could not load image: {e}")
    st.image("placeholder.png")  # fallback
```

**2. For NASA images:**
```python
nasa_data = fetch_nasa_data()
if nasa_data and 'url' in nasa_data:
    if nasa_data.get('media_type') == 'image':
        st.image(nasa_data['url'])
    else:
        st.info("Today's APOD is a video")
        st.video(nasa_data['url'])
```

---

## Performance Issues

### Slow Loading / Timeouts

**Symptoms:**
- App takes >10 seconds to load
- Frequent "Connection lost" messages
- Timeouts on data fetches

**Solutions:**

**1. Implement Caching:**
```python
# Cache expensive operations
@st.cache_data(ttl=30)  # 30 seconds
def load_data():
    return pd.read_csv(url)

@st.cache_data(ttl=3600)  # 1 hour
def fetch_api_data():
    return requests.get(api_url).json()
```

**2. Add Timeouts:**
```python
# Always add timeout to requests
response = requests.get(url, timeout=10)  # 10 seconds max
```

**3. Limit Data Size:**
```python
# Don't load entire dataset
df = pd.read_csv(url, nrows=1000)  # First 1000 rows

# Or use sampling
df_sample = df.sample(n=1000)
```

**4. Optimize Auto-Refresh:**
```python
# Don't refresh too frequently
refresh_count = st_autorefresh(interval=30000)  # 30 sec minimum
```

---

### Memory Issues

**Error:**
```
MemoryError
Streamlit crashed
```

**Solutions:**

**1. Clear Cache Periodically:**
```python
# Add cache clear button
if st.button("Clear Cache"):
    st.cache_data.clear()
    st.success("Cache cleared")
```

**2. Limit Session State:**
```python
# Don't store large objects
# Bad
st.session_state.large_df = huge_dataframe

# Good - only store references/IDs
st.session_state.data_timestamp = datetime.now()
```

**3. Use Generators:**
```python
# For large datasets
def data_generator():
    for chunk in pd.read_csv(url, chunksize=1000):
        yield chunk
```

---

## Deployment Issues

### Streamlit Cloud Deployment

**Error:**
```
requirements.txt not found
Build failed
```

**Solutions:**

**1. Verify Files Present:**
```bash
ls -la requirements.txt
ls -la app.py  # or streamlit_app.py
```

**2. Check requirements.txt syntax:**
```
# Good
streamlit>=1.30.0
pandas>=2.0.0

# Bad (version conflicts)
streamlit==1.30.0  # Too specific
pandas<2.0.0  # Conflicting requirement
```

**3. Set Python Version:**
Create `.streamlit/config.toml`:
```toml
[server]
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

---

### Secrets Not Working

**Error:**
```
API keys undefined in deployed app
```

**Solution - Streamlit Cloud:**
1. Go to app settings
2. Click "Secrets"  
3. Add in TOML format:
```toml
NASA_API_KEY = "your_key"
OPENAI_API_KEY = "sk-..."
ELEVENLABS_API_KEY = "your_key"
```

---

### Port Already in Use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solutions:**

**1. Kill existing process:**
```bash
# Find process using port 8501
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run app.py --server.port 8502
```

**2. Use specific port:**
```bash
streamlit run app.py --server.port 8080
```

---

## General Debugging Tips

### Enable Debug Mode

**In code:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Or via config:**
```toml
# .streamlit/config.toml
[global]
developmentMode = true

[logger]
level = "debug"
```

---

### Check Logs

**Local:**
```bash
streamlit run app.py 2>&1 | tee streamlit.log
```

**Streamlit Cloud:**
1. Go to app dashboard
2. Click "Manage app"
3. View logs tab

---

### Test Components Individually

```python
# Comment out sections to isolate issues
if st.checkbox("Show Tab 1"):
    with tab1:
        # Your code here
        pass

if st.checkbox("Show Tab 2"):
    with tab2:
        # Your code here
        pass
```

---

## Quick Fixes Checklist

When app fails to run:

- [ ] Check Python version (3.8+)
- [ ] Verify all dependencies installed
- [ ] Check .env file exists and formatted correctly
- [ ] Test API endpoints individually
- [ ] Clear Streamlit cache: `st.cache_data.clear()`
- [ ] Check for typos in variable names
- [ ] Verify all imports work
- [ ] Check indentation (Python requirement)
- [ ] Look for unclosed brackets/quotes
- [ ] Check for circular imports

---

## Getting Help

### Resources
- **Streamlit Docs:** https://docs.streamlit.io/
- **Community Forum:** https://discuss.streamlit.io/
- **GitHub Issues:** https://github.com/streamlit/streamlit/issues

### Before Asking for Help
1. Check error message carefully
2. Search docs/forum for error
3. Run `python test_eve.py` to isolate API issues
4. Try with minimal example
5. Check browser console (F12) for JavaScript errors

### Provide When Asking
- Full error traceback
- Streamlit version: `streamlit version`
- Python version: `python --version`
- Minimal reproducible code
- Steps to reproduce

---

**Last Updated:** February 2026
**Version:** 1.0.0
