# CEC-WAM System Deployment Guide

## 🚀 Quick Start

### Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Main Dashboard**
   ```bash
   streamlit run app.py
   ```

3. **Run Alternative Dashboards**
   ```bash
   # EVE 1010_WAKE Dashboard
   streamlit run EVE_1010_WAKE_dashboard.py
   
   # OMEGA EVE Dashboard
   streamlit run omega_eve.py
   ```

4. **View HTML Interface**
   ```bash
   # Open in browser
   open index.html
   
   # Or serve with Python
   python -m http.server 8000
   ```

## ⚡ New Features

### 1. Performance Optimizations
- **st.cache_data(ttl=10)**: All data loading functions now use caching with 10-second TTL
- **Auto-refresh**: System automatically refreshes every 5 seconds
- **Efficient data filtering**: Data is filtered from Nov 6, 2025 to today

### 2. Voice Input
- **Web Speech API Integration**: Click the 🎤 button to use voice commands
- **Supported in**: Chrome, Edge, Safari (requires HTTPS in production)
- **Commands**: All terminal commands can be spoken

### 3. Three.js Star Map
- **HD Visuals**: 10,000+ star particles with HD rendering
- **Animated**: Smooth rotation and camera movement
- **Responsive**: Adapts to different screen sizes

### 4. EVE Agent Access
- **Full Access**: EVE agent has complete system access
- **Auto-Fix**: Automatic error handling and recovery
- **Status Monitoring**: Real-time system health checks

### 5. Live Data Management
- **Date Filtering**: Only shows data from Nov 6, 2025 onwards
- **Real-time Updates**: Data refreshes automatically
- **CSV Export**: Export filtered data with one click

## 🔧 Configuration

### Streamlit Config (.streamlit/config.toml)
```toml
[theme]
primaryColor = "#28f0ff"      # Cyan accent
backgroundColor = "#0E1117"    # Dark background
font = "monospace"             # Monospace font

[server]
headless = true
port = 8501
enableCORS = true
enableXsrfProtection = false
maxUploadSize = 200
enableWebsocketCompression = true
runOnSave = true

[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"
```

### Environment Variables
Create a `.env` file (optional):
```env
GROQ_API_KEY=your_api_key_here
GEMINI_API_KEY=your_api_key_here
```

## 📊 Data Flow

1. **CSV Files**: All CSV files in the repo are auto-detected
2. **Date Filtering**: Data filtered from Nov 6, 2025 to present
3. **Caching**: Data cached for 10 seconds to improve performance
4. **Auto-Refresh**: UI refreshes every 5 seconds
5. **Error Recovery**: Automatic error handling and retry logic

## 🌐 Deployment Options

### Option 1: Streamlit Cloud
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy

### Option 2: Docker
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### Option 3: Local Server (24/7)
```bash
# Install PM2 for process management
npm install -g pm2

# Start with PM2
pm2 start "streamlit run app.py" --name cec-wam

# Auto-restart on reboot
pm2 startup
pm2 save
```

## 🎨 Customization

### Change Auto-Refresh Interval
In `app.py`, modify:
```python
remaining_time = auto_refresh_timer(refresh_interval=5)  # Change 5 to desired seconds
```

### Change Cache TTL
In `app.py`, modify:
```python
@st.cache_data(ttl=10)  # Change 10 to desired seconds
```

### Change Date Filter
In `app.py`, modify:
```python
cutoff_date = datetime(2025, 11, 6)  # Change to desired date
```

## 🔍 Troubleshooting

### Issue: Voice input not working
- **Solution**: Ensure you're using HTTPS (required in production)
- **Workaround**: Use localhost for testing

### Issue: Data not refreshing
- **Solution**: Clear cache with the "Clear Cache" button
- **Check**: Ensure CSV files have Timestamp column

### Issue: Three.js not loading
- **Solution**: Check internet connection (CDN required)
- **Workaround**: Download Three.js locally

### Issue: Auto-refresh causing UI flicker
- **Solution**: Increase refresh interval to 10-30 seconds
- **Adjust**: Modify `refresh_interval` parameter

## 📝 File Structure

```
CEC-WAM-HOT-CORE/
├── app.py                          # Main enhanced dashboard
├── EVE_1010_WAKE_dashboard.py     # Alternative dashboard
├── omega_eve.py                    # OMEGA EVE dashboard
├── index.html                      # HTML interface with voice & Three.js
├── eve_agent.py                    # EVE agent utilities
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
├── data/
│   ├── ledger.csv                  # Ledger data
│   ├── timeline.csv                # Timeline data
│   └── live.json                   # Live JSON data
└── DEPLOYMENT_GUIDE.md             # This file
```

## 🚨 Important Notes

1. **Data Privacy**: Never commit `.env` files or API keys
2. **Performance**: Cache TTL is optimized for real-time data
3. **Auto-Refresh**: 5-second refresh may impact server load
4. **Voice Input**: Requires HTTPS in production environments
5. **Three.js**: Requires internet connection for CDN access

## 🎯 Best Practices

1. **Use caching**: All data loading should use `@st.cache_data`
2. **Error handling**: Wrap API calls in try-except blocks
3. **Auto-refresh**: Balance between real-time and performance
4. **Data validation**: Always validate and clean data before display
5. **Security**: Use environment variables for sensitive data

## 📞 Support

For issues or questions:
- Check the main README.md
- Review error logs in terminal
- Use EVE agent for automated diagnostics

---

**Last Updated**: 2026-02-11  
**Version**: 2.0.0  
**Status**: Production Ready ✅
