# Vercel Deployment Guide - Full Interface with All Add-Ons

This repository is configured for easy deployment to Vercel as a static web application. The `index.html` file contains a complete, full-featured dashboard with all add-ons integrated.

## 🚀 Quick Deploy to Vercel

### Option 1: One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE)

### Option 2: Manual Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to project directory
cd CEC-WAM-HOT-CORE

# Deploy
vercel
```

### Option 3: Deploy via GitHub Integration

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository: `whiteantwan58-tech/CEC-WAM-HOT-CORE`
4. Click "Deploy"
5. That's it! Vercel will automatically detect the static site configuration

## 📦 What's Included - Full Interface with All Add-Ons

The deployment includes a comprehensive dashboard with all features:

### Core Features
- **Live Dashboard Interface** - Real-time data visualization
- **3D Star Map Visualization** - Interactive celestial body tracking with Three.js
- **Financial HUD** - Net liquidity, valuations, BTC allowance, resource metrics
- **Google Sheets Integration** - Live CSV data fetching from published sheets
- **PSI-Coin Price Tracking** - Real-time cryptocurrency pricing via CoinGecko API
- **Chart Visualizations** - Interactive charts with Chart.js
- **Matrix Background Animation** - Dynamic canvas-based visual effects

### Advanced Add-Ons
- **📹 Federal Way Live Feed** - HD camera feed integration with multiple locations
- **🚨 Crime Alert System** - Real-time crime alerts with severity filtering
- **🗺️ Interactive Map** - Leaflet.js-powered mapping with WSDOT traffic cameras
- **🌤️ Weather Integration** - Live weather data from OpenWeatherMap API
- **🚗 Traffic Monitoring** - Real-time traffic and incident tracking
- **⭐ Star Map Module** (`js/starmap.js`) - 8,000+ animated stars with constellations
- **📤 Google Drive Export** (`js/google-drive-export.js`) - Cloud backup and sync
- **🎨 Custom Styling** (`js/modules.css`) - Professional cosmic theme

### Security Features
- XSS Prevention - Safe DOM manipulation
- CSV Injection Prevention - Sanitized exports
- Secure Headers - CORS, X-Frame-Options, CSP
- No exposed secrets - All APIs use environment variables

### Data Sources
- Google Sheets (CSV) - Live data synchronization
- CoinGecko API - Cryptocurrency pricing
- OpenWeatherMap API - Weather data (optional)
- WSDOT API - Traffic cameras and incidents
- Embedded data - Pre-loaded system metrics

## ⚙️ Configuration

### Required Setup (None!)

The site works out-of-the-box with embedded demo data and public APIs.

### Optional Configuration

For enhanced functionality, you can add environment variables in Vercel:

1. Go to your Vercel project settings
2. Navigate to "Environment Variables"
3. Add optional keys:

```bash
# Optional: For weather features
OPENWEATHER_API_KEY=your-api-key-here

# Optional: For enhanced AI features
GROQ_API_KEY=your-groq-key-here
```

**Note:** These are completely optional. The dashboard works fully without them using fallback data.

## 🔧 File Structure

```
/
├── index.html              # Main dashboard (full interface with all features)
├── vercel.json            # Vercel configuration (static site)
├── js/
│   ├── starmap.js         # Star map visualization module
│   ├── federal-way-feed.js # Live camera feed module
│   ├── crime-alerts.js    # Crime alert system
│   ├── google-drive-export.js # Export and backup module
│   └── modules.css        # Add-on styling
├── data/
│   ├── CEC_Matrix_System_Operational_Metrics_and_Assets.csv
│   ├── EVE_UNFINISHED_TASKS.csv
│   └── CEC_WAM_MASTER_LEDGER_LIVE.xlsx
└── README.md
```

## 🌐 Custom Domain

To add a custom domain:

1. Go to your Vercel project settings
2. Click "Domains"
3. Add your domain
4. Update DNS records as instructed
5. Vercel automatically provisions SSL certificates

## 📊 Performance Optimizations

The `vercel.json` configuration includes:
- **Static file caching** - JS/CSS files cached for 1 year
- **Data caching** - CSV files cached for 5 minutes
- **Security headers** - X-Frame-Options, X-XSS-Protection, etc.
- **Gzip compression** - Automatic compression of all assets

## 🔒 Security Headers

Automatically configured security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: SAMEORIGIN`
- `X-XSS-Protection: 1; mode=block`
- `Cache-Control` - Optimized for static assets

## 🧪 Testing Your Deployment

After deployment, verify all features:

1. **Dashboard loads** - Check the main interface appears
2. **Star map renders** - Verify 3D visualization works
3. **Data fetches** - Confirm Google Sheets CSV loads
4. **PSI prices** - Check CoinGecko API integration
5. **Charts display** - Verify Chart.js visualizations
6. **Map loads** - Test Leaflet.js map with cameras
7. **All modules** - Check all add-on modules load

## 📱 Mobile Responsive

The dashboard is fully responsive and works on:
- Desktop (1920x1080+)
- Tablets (768px+)
- Mobile (320px+)

## 🆘 Troubleshooting

### Deployment fails
- Check `vercel.json` is valid JSON
- Ensure all files are committed to git
- Check build logs in Vercel dashboard

### Features not working
- Check browser console (F12) for errors
- Verify API endpoints are accessible
- Check CORS settings if using external APIs

### Maps/Charts not rendering
- Ensure CDN links are accessible
- Check browser supports WebGL (for 3D features)
- Try different browser (Chrome/Firefox recommended)

## 🔄 Updates

To update your deployment:

```bash
git add .
git commit -m "Update dashboard"
git push origin main
```

Vercel automatically redeploys on every push to main branch.

## 📞 Support

For issues with deployment:
- [Vercel Documentation](https://vercel.com/docs)
- [GitHub Issues](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/issues)

## ✅ Deployment Checklist

- [x] `vercel.json` configured for static hosting
- [x] `index.html` contains full interface
- [x] All JavaScript modules included (`js/*.js`)
- [x] All CSS files included (`js/modules.css`)
- [x] Data files accessible (`data/*.csv`)
- [x] CDN resources linked (Three.js, Chart.js, Leaflet)
- [x] Security headers configured
- [x] Caching optimized
- [x] Mobile responsive
- [x] No build step required - Deploy ready!

---

**🌌 Built with ❤️ by the CEC-WAM Team**

*Deploy once, run everywhere. Full interface with all add-ons included.*
