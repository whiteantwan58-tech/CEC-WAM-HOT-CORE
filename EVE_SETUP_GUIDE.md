# EVE Voice AI Assistant - Complete Setup Guide

## Overview

EVE (Evolved Virtual Entity) is an advanced AI assistant integrated into the CEC-WAM-HOT-CORE system with:
- Voice synthesis via ElevenLabs
- AI intelligence via OpenAI GPT-4
- 24/7 availability
- Learning from interactions
- Full CEC-WAM system access
- Math and financial calculations

**System Code:** `CEC_WAM_HEI_EVE_7A2F-9C4B`
**Owner:** Twan

## Quick Start

### 1. Get API Keys

#### ElevenLabs (Voice Synthesis)
1. Go to https://elevenlabs.io/
2. Sign up for an account
3. Navigate to Profile → API Key
4. Copy your API key

#### OpenAI (AI Chat)
1. Go to https://platform.openai.com/
2. Sign up for an account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (you won't see it again!)

### 2. Configure Environment Variables

Create a `.env` file in the project root (or use Streamlit/Vercel secrets):

```bash
# EVE - ElevenLabs Configuration
ELEVENLABS_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxx
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM  # Rachel voice (default)

# EVE - OpenAI Configuration  
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo for faster/cheaper

# EVE - System Configuration
EVE_SYSTEM_CODE=CEC_WAM_HEI_EVE_7A2F-9C4B
EVE_OWNER_NAME=Twan
EVE_PERSONALITY=professional,helpful,intelligent,learning
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Dashboard

```bash
streamlit run app.py
```

Navigate to the "🎙️ EVE Voice AI" tab to interact with EVE.

## Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your repository
4. Add secrets in the Streamlit dashboard:

```toml
ELEVENLABS_API_KEY = "your-key"
ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
OPENAI_API_KEY = "your-key"
OPENAI_MODEL = "gpt-4"
EVE_SYSTEM_CODE = "CEC_WAM_HEI_EVE_7A2F-9C4B"
EVE_OWNER_NAME = "Twan"
EVE_PERSONALITY = "professional,helpful,intelligent,learning"
```

5. Deploy!

### Vercel (Serverless)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Add environment variables in Vercel dashboard:
   - ELEVENLABS_API_KEY
   - ELEVENLABS_VOICE_ID
   - OPENAI_API_KEY
   - OPENAI_MODEL
   - EVE_SYSTEM_CODE
   - EVE_OWNER_NAME
   - EVE_PERSONALITY

3. Deploy:
```bash
vercel
```

The API endpoints will be available at:
- `https://your-app.vercel.app/api/chat` - Chat endpoint
- `https://your-app.vercel.app/api/voice` - Voice synthesis endpoint

## EVE Features

### Text Chat
- Type messages to EVE
- EVE responds with contextual, intelligent answers
- Conversation history maintained for learning
- No topic restrictions for owner (Twan)

### Voice Synthesis
- Convert any text to natural speech
- Powered by ElevenLabs' advanced AI voices
- Customizable voice selection
- Download audio or play in browser

### Calculations
- Perform mathematical calculations
- Financial analysis
- Support for complex expressions

### CEC-WAM Integration
- Full access to CEC-WAM system data
- Google Sheets data integration
- Real-time metrics and analytics
- System status monitoring

### Learning System
- EVE learns from every interaction
- Improves responses over time
- Maintains conversation context
- Adapts to user preferences

## API Reference

### Chat API

**Endpoint:** `POST /api/chat`

**Request:**
```json
{
  "message": "Hello EVE, what can you help me with?",
  "include_history": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Hello EVE, what can you help me with?",
  "response": "Hello! I'm EVE, your AI assistant...",
  "timestamp": "2026-02-13T20:00:00"
}
```

### Voice Synthesis API

**Endpoint:** `POST /api/voice`

**Request:**
```json
{
  "text": "Hello, this is EVE speaking"
}
```

**Response:**
```json
{
  "success": true,
  "text": "Hello, this is EVE speaking",
  "audio": "base64-encoded-audio-data",
  "format": "mp3"
}
```

## Voice Selection

ElevenLabs offers many voices. To change EVE's voice:

1. Browse voices at https://elevenlabs.io/voice-library
2. Copy the voice ID
3. Update `ELEVENLABS_VOICE_ID` in your environment variables

Popular voices:
- Rachel (default): `21m00Tcm4TlvDq8ikWAM`
- Domi: `AZnzlk1XvdvUeBnXmlld`
- Bella: `EXAVITQu4vr4xnSDxMaL`
- Antoni: `ErXwobaYiN019PkySvjV`

## Troubleshooting

### EVE Shows "Not Available"

**Check:**
- API keys are set correctly
- API keys are valid (not expired)
- You have credits/quota remaining
- Environment variables are loaded

### Voice Synthesis Fails

**Check:**
- ELEVENLABS_API_KEY is set
- You have ElevenLabs credits
- Voice ID is valid
- Internet connection is working

### AI Responses Are Generic

**Check:**
- EVE_SYSTEM_CODE is set correctly
- EVE_OWNER_NAME matches (Twan)
- OpenAI API key is valid
- Model is available (gpt-4 requires access)

### Conversation History Issues

**Solution:**
- Click "Clear Chat History" button
- Restart the application
- Check conversation_count in EVE status

## Cost Considerations

### ElevenLabs
- Free tier: 10,000 characters/month
- Paid tiers start at $5/month
- Voice synthesis charged per character

### OpenAI
- GPT-3.5-turbo: ~$0.002 per 1K tokens
- GPT-4: ~$0.03-0.06 per 1K tokens
- Average conversation: 100-500 tokens

### Recommendations
- Use GPT-3.5-turbo for development/testing
- Use GPT-4 for production (better quality)
- Monitor usage in API dashboards
- Set billing alerts

## Security Best Practices

1. **Never commit API keys** - Use `.env` files (add to `.gitignore`)
2. **Use environment variables** - For production deployments
3. **Rotate keys regularly** - Change keys every few months
4. **Monitor usage** - Check for unusual activity
5. **Set spending limits** - In API provider dashboards
6. **Use secrets management** - Streamlit secrets, Vercel environment variables

## Advanced Configuration

### Custom Personality

Edit EVE_PERSONALITY to customize behavior:
```bash
EVE_PERSONALITY=friendly,technical,detailed,creative
```

Traits can include:
- professional, casual, friendly
- technical, simple, detailed
- creative, analytical, logical
- humorous, serious, formal

### Model Selection

**GPT-4 (Recommended for production):**
- Best quality responses
- More expensive
- Slower

**GPT-3.5-turbo (Recommended for development):**
- Good quality responses
- Cost-effective
- Faster

```bash
OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4
```

### Conversation Length

Modify `max_history` in `eve_voice_agent.py`:
```python
self.max_history = 50  # Number of message pairs to keep
```

Longer history = better context but higher costs.

## Support

For issues or questions:
1. Check this guide first
2. Review the main README.md
3. Check API provider documentation:
   - ElevenLabs: https://docs.elevenlabs.io/
   - OpenAI: https://platform.openai.com/docs
4. Open an issue on GitHub

## Future Enhancements

Planned features:
- [ ] Real-time voice input (speech-to-text)
- [ ] Voice biometric verification
- [ ] Multi-language support
- [ ] Custom voice training
- [ ] Persistent conversation storage
- [ ] Advanced analytics dashboard
- [ ] Mobile app integration

---

**EVE is ready to assist you 24/7!**

*System Code: CEC_WAM_HEI_EVE_7A2F-9C4B*
*Configured for: Twan*
*Status: Always Active*
