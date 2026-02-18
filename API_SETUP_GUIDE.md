# API Setup & Configuration Guide

## Overview
This guide provides step-by-step instructions for configuring all APIs used in the CEC-WAM-HOT-CORE system to ensure full functionality of the Streamlit app (Eve) and all integrated services.

## Table of Contents
1. [Quick Setup](#quick-setup)
2. [Required APIs](#required-apis)
3. [Optional APIs](#optional-apis)
4. [API Configuration](#api-configuration)
5. [Testing APIs](#testing-apis)
6. [Troubleshooting](#troubleshooting)

---

## Quick Setup

### Step 1: Create .env File
```bash
# Copy the example file
cp .env.example .env

# Edit with your favorite editor
nano .env  # or vim, code, etc.
```

### Step 2: Run Test Suite
```bash
# Test all API configurations
python test_eve.py
```

### Step 3: Launch Application
```bash
# Start Streamlit app
streamlit run app.py
# or
streamlit run streamlit_app.py
```

---

## Required APIs

### 1. NASA API
**Purpose:** Space imagery, astronomical data, APOD (Astronomy Picture of the Day)

**Get Your Key:**
1. Visit: https://api.nasa.gov/
2. Click "Get API Key" (instant, no approval needed)
3. Enter your name and email
4. Copy your API key

**Configuration:**
```env
NASA_API_KEY=YOUR_NASA_API_KEY_HERE
```

**Free Tier Limits:**
- 1,000 requests per hour
- Rate limit: 30 requests per IP per hour with DEMO_KEY
- Custom keys have higher limits

**Default Fallback:** Uses `DEMO_KEY` with rate limits

---

### 2. OpenAI API (for EVE AI Chat)
**Purpose:** AI-powered chat, natural language processing, intelligent responses

**Get Your Key:**
1. Visit: https://platform.openai.com/api-keys
2. Sign up / Log in
3. Click "Create new secret key"
4. Name it (e.g., "CEC-WAM-EVE")
5. Copy and save immediately (shown only once)

**Configuration:**
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo for lower costs
```

**Pricing (as of 2024):**
- GPT-4: $0.03 per 1K prompt tokens, $0.06 per 1K completion tokens
- GPT-3.5-turbo: $0.0005 per 1K prompt tokens, $0.0015 per 1K completion tokens

**Without This:** EVE will work but provide fallback messages instead of AI responses

---

### 3. ElevenLabs API (for EVE Voice Synthesis)
**Purpose:** Text-to-speech, voice synthesis for EVE responses

**Get Your Key:**
1. Visit: https://elevenlabs.io/
2. Sign up for free account
3. Go to Profile → API Keys
4. Copy your API key

**Configuration:**
```env
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM  # Rachel (default)
```

**Popular Voice IDs:**
- `21m00Tcm4TlvDq8ikWAM` - Rachel (professional female)
- `pNInz6obpgDQGcFmaJgB` - Adam (professional male)
- `TX3LPaxmHKxFdv7VOQHJ` - Elli (friendly female)
- `EXAVITQu4vr4xnSDxMaL` - Bella (expressive female)

**Free Tier:**
- 10,000 characters per month
- Commercial use allowed on paid plans

**Without This:** Voice synthesis unavailable, text-only mode

---

## Optional APIs

### 4. OpenWeatherMap API
**Purpose:** Weather alerts, forecasts, current conditions

**Get Your Key:**
1. Visit: https://openweathermap.org/api
2. Sign up for free account
3. Navigate to API Keys section
4. Copy your key (may take 10 minutes to activate)

**Configuration:**
```env
OPENWEATHER_API_KEY=your_openweathermap_api_key_here
```

**Free Tier:**
- 1,000 API calls per day
- 60 calls per minute
- Current weather + 5-day forecast

**Fallback:** App includes NOAA Weather API (no key required) and demo data

---

### 5. Google Sheets API (for Data Integration)
**Purpose:** Real-time data from Google Sheets, live ledger updates

**Get Your Key:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable Google Sheets API
4. Create Service Account:
   - IAM & Admin → Service Accounts → Create
   - Grant "Editor" role
   - Create JSON key
5. Share your Google Sheet with service account email

**Configuration Option 1 (JSON inline):**
```env
GOOGLE_SHEETS_CREDS={"type":"service_account","project_id":"your-project",...}
```

**Configuration Option 2 (File path - RECOMMENDED):**
```env
GOOGLE_SHEETS_CREDS_FILE=/path/to/service-account-key.json
```

**Sheet ID:**
```env
LOG_SHEET_ID=your-published-sheet-id-here
```

**Public Sheets:** The app can also read published CSV exports without API keys

---

### 6. CoinGecko API
**Purpose:** Cryptocurrency prices, market data for PSI coin tracking

**Get Your Key:**
1. Visit: https://www.coingecko.com/en/api
2. Sign up for free account
3. Navigate to developer dashboard
4. Copy API key

**Configuration:**
```env
COINGECKO_API_KEY=your_coingecko_api_key_here
```

**Free Tier:**
- 10,000 requests per month
- Rate limit: 50 calls per minute

**Fallback:** Uses demo/cached data without API key

---

## API Configuration

### Environment Variables Loading Order

1. **System Environment Variables** (highest priority)
2. **.env file** in project root
3. **Default/Fallback values** in code

### Security Best Practices

✅ **DO:**
- Store API keys in `.env` file
- Add `.env` to `.gitignore`
- Use separate keys for dev/production
- Rotate keys regularly
- Use environment-specific keys

❌ **DON'T:**
- Commit `.env` to git
- Share keys publicly
- Use production keys in development
- Hardcode keys in source code
- Share keys via email/chat

### Production Deployment

**Streamlit Cloud:**
```
1. Go to app settings
2. Click "Secrets"
3. Add TOML format:
   NASA_API_KEY = "your_key"
   OPENAI_API_KEY = "sk-..."
```

**Vercel:**
```
1. Project Settings → Environment Variables
2. Add each key-value pair
3. Select environment (Production/Preview/Development)
```

**Heroku:**
```bash
heroku config:set NASA_API_KEY=your_key
heroku config:set OPENAI_API_KEY=sk-...
```

---

## Testing APIs

### Run Full Test Suite
```bash
python test_eve.py
```

**Expected Output:**
```
============================================================
  API Configuration Tests
============================================================

🛰️  Testing NASA API...
  ✓ NASA API: Connected

🌦️  Testing NOAA Weather API...
  ✓ NOAA Weather API: Connected

⛅ Testing OpenWeatherMap API...
  ✓ OpenWeatherMap API: Connected

🗣️  Testing ElevenLabs API...
  ✓ ElevenLabs API: Connected

🤖 Testing OpenAI API...
  ✓ OpenAI API: Connected

📊 Testing Google Sheets Data Feed...
  ✓ Google Sheets CSV: Accessible

============================================================
  API Test Summary
============================================================
  Total Tests: 6
  ✓ Passed: 6
  ✗ Failed: 0
  ⊘ Skipped: 0
```

### Test Individual APIs

**Test NASA API:**
```bash
curl "https://api.nasa.gov/planetary/apod?api_key=YOUR_KEY"
```

**Test OpenWeather:**
```bash
curl "https://api.openweathermap.org/data/2.5/weather?q=Seattle&appid=YOUR_KEY"
```

**Test ElevenLabs:**
```bash
curl -X GET "https://api.elevenlabs.io/v1/voices" \
  -H "xi-api-key: YOUR_KEY"
```

**Test OpenAI:**
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_KEY"
```

---

## Troubleshooting

### Common Issues

#### 1. "API Key Invalid" Error

**NASA API:**
```
Error: 403 Forbidden - API_KEY_INVALID
```
**Solution:**
- Verify key is correctly copied (no spaces)
- Check if using correct environment variable name: `NASA_API_KEY`
- DEMO_KEY has rate limits - get your own key

**OpenAI API:**
```
Error: 401 Unauthorized - Incorrect API key
```
**Solution:**
- Ensure key starts with `sk-` or `sk-proj-`
- Key might be revoked - create new one
- Check organization ID if applicable

---

#### 2. Rate Limit Exceeded

**Error:**
```
Error: 429 Too Many Requests
```

**Solutions:**
- **NASA DEMO_KEY:** Get your own API key (1000 req/hr vs 30 req/hr)
- **OpenAI:** Implement caching, reduce frequency
- **ElevenLabs:** Upgrade plan or reduce TTS requests
- **OpenWeather:** Stay within 60 req/min limit

---

#### 3. Environment Variables Not Loading

**Check:**
```bash
# Verify .env file exists
ls -la .env

# Check if python-dotenv is installed
pip show python-dotenv

# Install if missing
pip install python-dotenv
```

**Debug in Python:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
print("NASA Key:", os.getenv('NASA_API_KEY'))
print("OpenAI Key:", os.getenv('OPENAI_API_KEY')[:10] if os.getenv('OPENAI_API_KEY') else None)
```

---

#### 4. CORS / Network Errors

**Error:**
```
requests.exceptions.ConnectionError
```

**Solutions:**
1. Check internet connection
2. Verify firewall settings
3. Test with curl/Postman first
4. Check if API endpoint is correct
5. Some corporate networks block external APIs

---

#### 5. Google Sheets Access Denied

**Error:**
```
Error: 403 - The caller does not have permission
```

**Solutions:**
1. Share sheet with service account email
2. Verify service account has "Editor" role
3. Check if Sheet ID is correct
4. Ensure Google Sheets API is enabled in project

---

#### 6. Streamlit Secrets Not Loading

**For Streamlit Cloud:**

Create `.streamlit/secrets.toml`:
```toml
NASA_API_KEY = "your_key"
OPENAI_API_KEY = "sk-..."
ELEVENLABS_API_KEY = "your_key"
```

**Important:** Add to `.gitignore`:
```
.streamlit/secrets.toml
```

---

### Debug Mode

Enable verbose logging:
```env
DEBUG_MODE=true
```

This will print detailed API request/response information.

---

## Getting Help

### Resources
- **NASA API Docs:** https://api.nasa.gov/
- **OpenAI API Docs:** https://platform.openai.com/docs
- **ElevenLabs Docs:** https://docs.elevenlabs.io/
- **OpenWeather Docs:** https://openweathermap.org/api
- **Google Sheets API:** https://developers.google.com/sheets/api

### Support
- Check `test_eve.py` output for specific errors
- Review logs in Streamlit app
- Test individual APIs with curl/Postman
- Verify all keys are in `.env` file
- Ensure no typos in environment variable names

---

## API Costs Summary

| API | Free Tier | Paid Plans | Best For |
|-----|-----------|------------|----------|
| NASA | Unlimited* | N/A | Free forever |
| NOAA Weather | Unlimited | N/A | Free forever |
| OpenWeather | 1K/day | $40+/mo | Free tier sufficient |
| OpenAI GPT-4 | None | Pay-per-use | Production apps |
| OpenAI GPT-3.5 | None | Very cheap | Cost-effective |
| ElevenLabs | 10K chars/mo | $5+/mo | Testing/light use |
| Google Sheets | Free | N/A | Small datasets |
| CoinGecko | 10K/mo | $129+/mo | Free tier sufficient |

*NASA and NOAA are completely free public APIs

---

## Next Steps

1. ✅ Configure required APIs (NASA, OpenAI, ElevenLabs)
2. ✅ Run `python test_eve.py` to verify
3. ✅ Launch app: `streamlit run app.py`
4. ✅ Check EVE AI tab for functionality
5. ✅ Monitor API usage and costs
6. ✅ Upgrade to paid tiers as needed

---

**Last Updated:** February 2026
**Version:** 1.0.0
