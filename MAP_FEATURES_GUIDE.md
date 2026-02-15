# Map, Camera, Weather & Traffic Integration - User Guide

## Overview

This document provides detailed information about the new real-time monitoring features added to the CEC-WAM dashboard.

## Features

### 1. Interactive Map with Live Cameras

The dashboard now includes an interactive map showing Washington State DOT (WSDOT) traffic camera locations.

**Key Features:**
- Real-time camera location markers on an interactive map
- Click any marker to view the camera feed and details
- Camera metadata includes location, direction, and coordinates
- Auto-refresh every 60 seconds

**How to Use:**
1. The map loads automatically when you open the dashboard
2. Click the **🗺️ TOGGLE MAP** button to show/hide the map
3. Click any blue marker on the map to view that camera
4. Click **📹 REFRESH CAMS** to manually update camera data
5. Click the **✕ CLOSE** button in the camera panel to deselect

### 2. Weather Integration

Real-time weather information is displayed alongside camera feeds.

**Key Features:**
- Current temperature, conditions, humidity, and wind speed
- Location-specific weather for selected cameras
- Fallback demo data if API key is not configured
- Auto-refresh every 5 minutes

**Configuration:**
To use live weather data, you need a free OpenWeatherMap API key:

1. Get a free API key at: https://openweathermap.org/api
2. Add this script tag before the main page script:
   ```html
   <script>window.OPENWEATHER_API_KEY = 'your-api-key-here';</script>
   ```
3. Or set the `OPENWEATHER_API_KEY` environment variable for server-side deployment

**Without API Key:**
The weather feature will still work with demo/fallback data showing reasonable default values.

### 3. Traffic Monitoring

Live traffic data from WSDOT provides real-time incident and flow information.

**Key Features:**
- Active incident count
- Average traffic speed
- Traffic flow status (GOOD/MODERATE/SLOW)
- Last update timestamp
- Auto-refresh every 45 seconds

**How to Use:**
1. View traffic statistics in the **🚗 TRAFFIC STATUS** panel
2. Click **🔄 REFRESH TRAFFIC** to manually update
3. Click **🚗 TRAFFIC** button on map to toggle traffic layer (future enhancement)

## API Information

### WSDOT APIs (No Key Required)

**Traffic Cameras:**
- Endpoint: `https://www.wsdot.wa.gov/Traffic/api/HighwayCameras/HighwayCamerasREST.svc/GetCamerasAsJson`
- Documentation: https://www.wsdot.wa.gov/traffic/api/

**Traffic Data:**
- Endpoint: `https://www.wsdot.wa.gov/Traffic/api/TravelTimes/TravelTimesREST.svc/GetTravelTimesAsJson`
- Documentation: https://www.wsdot.wa.gov/traffic/api/

### OpenWeatherMap API (Optional)

**Weather Data:**
- Endpoint: `https://api.openweathermap.org/data/2.5/weather`
- Documentation: https://openweathermap.org/api
- Free tier: 1,000 calls/day (sufficient for this application)

## Auto-Refresh Schedule

The dashboard automatically refreshes data at these intervals:

| Feature | Refresh Interval |
|---------|-----------------|
| Traffic Cameras | 60 seconds |
| Traffic Data | 45 seconds |
| Weather Data | 5 minutes |
| Crypto Prices | 15 seconds |

## Troubleshooting

### Map Not Loading

**Symptoms:** Map container is blank or shows loading state indefinitely

**Solutions:**
1. Check browser console for errors
2. Ensure internet connection is active
3. Verify Leaflet.js library loaded correctly
4. Try refreshing the page

### Cameras Not Appearing

**Symptoms:** Map loads but no camera markers appear

**Solutions:**
1. Check WSDOT API status: https://www.wsdot.wa.gov/traffic/api/
2. Look for CORS or network errors in console
3. Click **📹 REFRESH CAMS** button
4. Wait a few moments for API response

### Weather Shows "--°F"

**Symptoms:** Weather panel shows placeholder values

**Solutions:**
1. If using API key, verify it's correctly configured
2. Check OpenWeatherMap API status: https://status.openweathermap.org/
3. Without API key, demo data should appear within 10 seconds
4. Check browser console for API errors

### Traffic Data Stuck on "LOADING"

**Symptoms:** Traffic status remains in loading state

**Solutions:**
1. Check WSDOT traffic API status
2. Click **🔄 REFRESH TRAFFIC** button
3. Check browser console for errors
4. Demo fallback data should appear after timeout

## Browser Compatibility

**Fully Supported:**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Required Browser Features:**
- ES6 JavaScript support
- Fetch API
- CSS Grid
- LocalStorage (for PWA features)

## Performance Considerations

### Data Usage

Approximate data usage per hour:
- Camera markers: ~100 KB every 60 seconds = ~6 MB/hour
- Traffic data: ~50 KB every 45 seconds = ~4 MB/hour
- Weather data: ~5 KB every 5 minutes = ~60 KB/hour
- **Total: ~10 MB/hour**

### Memory Management

The application includes automatic cleanup:
- Intervals are cleared on page unload
- Old markers are removed before adding new ones
- Map tiles are cached by Leaflet

## Security

### API Key Safety

**⚠️ Important:** Never commit API keys to version control

**Best Practices:**
1. Use environment variables for production
2. Set keys via build-time injection
3. Use `.env` files (listed in `.gitignore`)
4. Rotate keys regularly if exposed

### Data Privacy

**Data Collection:**
- No personal data is collected
- No tracking or analytics by default
- Camera feeds are public WSDOT data
- Weather API receives only coordinates

**Third-Party Services:**
- OpenStreetMap (map tiles)
- WSDOT (cameras and traffic)
- OpenWeatherMap (weather data)
- CoinGecko (crypto prices)

## Future Enhancements

Potential improvements for future versions:

1. **Traffic Heat Map Overlay**
   - Visual representation of traffic density
   - Color-coded speed indicators
   - Congestion hotspot markers

2. **Weather Radar Layer**
   - Precipitation overlay on map
   - Weather alerts and warnings
   - Forecast data

3. **Camera Filtering**
   - Filter by location or highway
   - Search functionality
   - Favorite cameras

4. **Historical Data**
   - Traffic pattern analysis
   - Weather trends
   - Incident history

5. **Mobile App**
   - Native mobile application
   - Push notifications
   - Offline mode

## Support

For issues or questions:
- Open an issue on GitHub: https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/issues
- Check the main README: https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE#readme
- Review troubleshooting section above

## Credits

### Technologies Used

- **Leaflet.js** - Interactive map library (BSD 2-Clause License)
- **OpenStreetMap** - Map tile provider (ODbL License)
- **WSDOT APIs** - Washington State Department of Transportation public APIs
- **OpenWeatherMap** - Weather data provider
- **Chart.js** - Data visualization
- **Three.js** - 3D graphics and animations

### Data Sources

- Traffic Cameras: Washington State DOT
- Traffic Data: Washington State DOT
- Weather: OpenWeatherMap
- Crypto Prices: CoinGecko
- Map Tiles: OpenStreetMap contributors

## License

This feature is part of the CEC-WAM system. See the main repository for license information.

---

**Version:** 2.1.0  
**Last Updated:** 2026-02-12  
**Status:** Production Ready ✅
