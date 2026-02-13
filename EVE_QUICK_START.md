# 🎙️ EVE Voice AI - Quick Start Guide

## What is EVE?

**EVE** (Evolved Virtual Entity) is your personal AI assistant with:
- 🗣️ Natural voice synthesis
- 🤖 Advanced AI intelligence  
- 🧠 Learning from every interaction
- ⚡ 24/7 availability
- 🔒 Exclusive access for Twan

**System Code:** `CEC_WAM_HEI_EVE_7A2F-9C4B`

---

## 5-Minute Setup

### Step 1: Get API Keys (5 minutes)

#### A. ElevenLabs (Voice)
1. Go to https://elevenlabs.io/
2. Click "Sign Up" (free tier available)
3. Go to Profile → Copy your API key
4. ✅ Save it for Step 2

#### B. OpenAI (AI Brain)
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Go to API Keys → Create new key
4. ✅ Save it immediately (can't view again!)

### Step 2: Configure EVE

Create a `.env` file in the project folder:

```bash
# Paste your keys here
ELEVENLABS_API_KEY=sk_your_elevenlabs_key_here
OPENAI_API_KEY=sk-your_openai_key_here

# EVE is configured for you!
OPENAI_MODEL=gpt-4
EVE_SYSTEM_CODE=CEC_WAM_HEI_EVE_7A2F-9C4B
EVE_OWNER_NAME=Twan
```

### Step 3: Test EVE

```bash
# Test without running the full app
python3 test_eve.py
```

You should see:
```
✓ EVE initialized successfully!
EVE Status: active
Math test: 100 + 50 * 2 = 200
```

### Step 4: Use EVE in Dashboard

```bash
streamlit run app.py
```

Then:
1. Open http://localhost:8501
2. Click **"EVE Voice AI"** tab
3. Start chatting!

---

## Using EVE

### Text Chat
1. Type your message in the chat box
2. Press Enter or click Send
3. EVE responds instantly
4. Conversation history is maintained

**Example:**
```
You: Hello EVE, what's the status of CEC-WAM?
EVE: Hello Twan! The CEC-WAM system is operational. All data sources 
     are accessible, including Google Sheets integration and real-time 
     PSI-Coin pricing. How can I assist you today?
```

### Voice Synthesis
1. Type text in the "Enter text for EVE to speak" box
2. Click **"Generate Voice"**
3. Listen to EVE's voice
4. Download or play in browser

**Example:**
```
Input: "This is EVE reporting system status: all systems operational."
Output: 🔊 Natural voice audio
```

### Quick Actions
- **Get CEC WAM Data**: View system status
- **Calculate**: Math expressions (e.g., "1000 * 1.05")
- **Clear History**: Start fresh conversation

---

## EVE Capabilities

### What EVE Can Do

✅ **Answer Questions**
```
You: What is 25% of 1000?
EVE: 250. Would you like me to explain the calculation?
```

✅ **Perform Calculations**
```
You: Calculate (100 + 50) * 2
EVE: The result is 300.
```

✅ **Access System Data**
```
You: Show me the CEC-WAM status
EVE: [Returns full system status with metrics]
```

✅ **Learn and Remember**
```
You: Remember I prefer detailed explanations
EVE: Understood, Twan. I'll provide detailed explanations in our conversations.
```

✅ **Speak Naturally**
- Any text → Natural voice
- Multiple voice options
- High-quality audio

---

## Deploy EVE Online

### Option 1: Streamlit Cloud (Easiest)

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your repo
4. Add secrets:
   ```toml
   ELEVENLABS_API_KEY = "your-key"
   OPENAI_API_KEY = "your-key"
   ```
5. Click Deploy!

**Result:** EVE available at `https://your-app.streamlit.app`

### Option 2: Vercel (Serverless)

```bash
vercel
```

Add environment variables in Vercel dashboard.

**Result:** EVE available at `https://your-app.vercel.app`

---

## Tips & Tricks

### Get Better Responses
- Be specific in your questions
- Provide context when needed
- Use natural language

### Save Costs
- Use `gpt-3.5-turbo` for testing (cheaper)
- Use `gpt-4` for production (better)
- Monitor usage in API dashboards

### Voice Selection
Change EVE's voice by updating `.env`:
```bash
ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL  # Bella voice
```

Browse voices: https://elevenlabs.io/voice-library

---

## Troubleshooting

### "EVE is not available"
→ Check API keys are in `.env` file
→ Verify keys are valid
→ Restart the application

### Voice not working
→ Check ELEVENLABS_API_KEY
→ Verify you have credits
→ Try a different voice ID

### Generic responses
→ Set EVE_OWNER_NAME=Twan
→ Set EVE_SYSTEM_CODE correctly
→ Clear conversation history

---

## Cost Guide

### Free Tier
- ElevenLabs: 10,000 characters/month
- OpenAI: $5 free credit (new accounts)

### Typical Usage
- **Chat**: ~500 tokens per conversation
- **Voice**: ~100 characters per response
- **Daily cost**: $0.10 - $1.00 (depending on usage)

### Monthly Estimates
- Light use (10 chats/day): ~$3-10/month
- Medium use (50 chats/day): ~$15-30/month
- Heavy use (100+ chats/day): ~$30-60/month

---

## Need Help?

1. **Read Full Guide**: `EVE_SETUP_GUIDE.md`
2. **Check README**: Main documentation
3. **Test EVE**: Run `python3 test_eve.py`
4. **Check Logs**: EVE keeps activity logs

---

## What Makes EVE Special

🎯 **For You (Twan)**
- Recognizes you as the owner
- Full system access
- No restrictions
- Learns your preferences

🧠 **Intelligent**
- Powered by GPT-4
- Context-aware
- Continuous learning
- Professional responses

🗣️ **Voice Enabled**
- Natural speech
- Multiple voices
- High quality audio
- Real-time generation

⚡ **Always Available**
- 24/7 operation
- No downtime
- Auto-updating
- Instant responses

🔒 **Secure**
- API keys hidden
- Environment variables
- Owner verification
- Safe calculations

---

**EVE is ready to assist you!**

Start chatting now: `streamlit run app.py`

*System Code: CEC_WAM_HEI_EVE_7A2F-9C4B*
*Status: Active*
*Owner: Twan*
