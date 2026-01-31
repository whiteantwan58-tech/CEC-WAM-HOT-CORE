# Chart Automation System Documentation

## Overview

This documentation describes the automated chart and data management system for the CEC-WAM-HOT-CORE repository. The system automatically links and updates charts, cross-references data across multiple CSV files, and provides live data integration with the frontend.

## Features

1. **Automated Data Discovery**
   - Automatically discovers all CSV files in the repository
   - Cross-references data with Chart.xlsx
   - Identifies missing or outdated information

2. **Chart.xlsx Updates**
   - Dynamically updates Chart.xlsx with CSV data
   - Creates separate sheets for each data source
   - Maintains data integrity and validation

3. **Live Chart Data**
   - Generates JSON-formatted chart data for web visualization
   - Supports multiple chart types (line, bar, pie)
   - Provides real-time data updates

4. **API Integration**
   - Flask-based REST API for data access
   - CORS-enabled for frontend integration
   - Health monitoring and status reporting

5. **Frontend Integration**
   - Integrated with index.html via terminal commands
   - Dynamic chart data loading
   - Status monitoring and reporting

## System Components

### 1. chart_automation.py

Main automation script that handles:
- CSV file discovery and loading
- Chart.xlsx analysis and updates
- JSON chart data generation
- Automation reporting

**Usage:**
```bash
python chart_automation.py
```

**Output:**
- Updated `Chart.xlsx` with all CSV data
- `data/chart_data.json` - JSON chart data for web
- `data/automation_report.json` - Automation status report

### 2. api_server.py

Flask API server providing:
- `/api/health` - Health check endpoint
- `/api/chart-data` - Chart data for visualization
- `/api/automation-status` - Automation status report
- `/api/datasets` - List of available datasets
- `/api/run-automation` - Trigger automation via API
- `/api/live-data` - Aggregated live metrics

**Usage:**
```bash
python api_server.py
```

**Access:**
- API runs on `http://localhost:5000`
- All endpoints return JSON responses

### 3. scheduled_automation.py

Automated scheduler for periodic updates:
- Runs chart automation at regular intervals
- Logs all operations
- Handles errors and retries

**Usage:**
```bash
# Run every 30 minutes (default)
python scheduled_automation.py

# Run every 15 minutes
python scheduled_automation.py --interval 15

# Run once and exit
python scheduled_automation.py --once
```

### 4. start_services.sh

Startup script that:
- Installs dependencies
- Runs initial automation
- Starts API server
- Starts frontend server

**Usage:**
```bash
./start_services.sh
```

**Services Started:**
- Frontend: `http://localhost:8000`
- API: `http://localhost:5000`

## Data Sources

The system processes the following CSV files:

1. **pump.fun.csv**
   - Transaction data from Solana pump.fun
   - Columns: Signature, Block Time, Human Time, Action, From, To, Amount, Value, etc.
   - Used for: Transaction timeline charts

2. **BlackHoles.csv**
   - Discovery and research data
   - Columns: TIMESTAMP, DISCOVERY_ID, DESCRIPTION, VALUE, STATUS
   - Used for: Status distribution charts

3. **CEC Matrix System Operational Metrics and Assets - FINANCE_HUB (1).csv**
   - Financial asset tracking
   - Columns: ASSET CLASS, LOCATION, SECURITY PROTOCOL, VALUE
   - Used for: Asset distribution charts

4. **data/ledger.csv**
   - System ledger entries
   - Columns: Timestamp, Asset, Status, Entropy_Level, Buffer_Check
   - Used for: System status monitoring

5. **data/timeline.csv**
   - Project timeline and milestones
   - Columns: Date, Event, Description
   - Used for: Timeline visualization

## Chart Data Format

The system generates chart data in JSON format:

```json
{
  "timestamp": "2026-01-31T06:38:44.909705",
  "datasets": {
    "pump_fun_timeline": {
      "labels": ["2025-12-22 13:46:04+00:00", ...],
      "values": [5.288, 0.4175, ...],
      "type": "line",
      "title": "Pump.fun Transaction Values"
    },
    "blackholes_status": {
      "labels": ["STABLE", "LOCKED", ...],
      "values": [1, 1, ...],
      "type": "pie",
      "title": "BlackHole Discovery Status"
    }
  }
}
```

## Frontend Integration

### Terminal Commands

The index.html terminal supports these commands:

- `charts` - Display available chart datasets
- `automation` - Show automation status
- `help` - Show all available commands

### Example Usage:

```
EVE> charts
EVE: Loading chart data...
EVE: Available charts: 3
EVE: - Pump.fun Transaction Values: line chart with 20 points
EVE: - BlackHole Discovery Status: pie chart with 6 points
EVE: - CEC Asset Distribution: bar chart with 5 points

EVE> automation
EVE: Checking automation status...
EVE: Status: SUCCESS
EVE: CSV Files: 5
EVE: Last update: 1/31/2026, 6:38:44 AM
```

## Installation

### Requirements

- Python 3.8+
- pip package manager

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- pandas>=2.0.0
- openpyxl>=3.1.0
- xlsxwriter>=3.1.0
- matplotlib>=3.7.0
- plotly>=5.14.0
- flask>=2.3.0
- flask-cors>=4.0.0
- numpy>=1.24.0
- streamlit>=1.22.0

2. Run initial automation:
```bash
python chart_automation.py
```

3. Start services:
```bash
./start_services.sh
```

## Deployment

### Local Development

1. Start services using `start_services.sh`
2. Access frontend at `http://localhost:8000`
3. API available at `http://localhost:5000`

### Production Deployment

1. **Environment Variables:**
   - Set `FLASK_ENV=production` for API server
   - Configure proper CORS origins in `api_server.py`

2. **Process Management:**
   - Use systemd, supervisor, or PM2 for process management
   - Set up scheduled_automation.py as a service

3. **Web Server:**
   - Use nginx or Apache as reverse proxy
   - Serve static files from document root
   - Proxy API requests to Flask server

### Example systemd Service

```ini
[Unit]
Description=CEC-WAM Chart Automation
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/cec-wam
ExecStart=/usr/bin/python3 scheduled_automation.py --interval 30
Restart=always

[Install]
WantedBy=multi-user.target
```

## Monitoring and Maintenance

### Logs

- Automation logs: `automation.log`
- API logs: stdout/stderr
- Check logs regularly for errors

### Error Handling

The system includes:
- Automatic error logging
- Retry mechanisms
- Status reporting
- Health check endpoints

### Troubleshooting

**Problem:** Chart data not updating

**Solution:**
1. Check if CSV files exist
2. Run `python chart_automation.py` manually
3. Check `automation.log` for errors

**Problem:** API server not responding

**Solution:**
1. Check if port 5000 is available
2. Verify Flask dependencies installed
3. Check CORS configuration

**Problem:** Frontend not displaying charts

**Solution:**
1. Verify API server is running
2. Check browser console for errors
3. Ensure chart_data.json exists in data/ directory

## Security Considerations

1. **API Security:**
   - No authentication required for local development
   - Add authentication for production deployment
   - Restrict CORS origins in production

2. **Data Privacy:**
   - CSV files may contain sensitive data
   - Use appropriate file permissions
   - Do not commit secrets to repository

3. **Input Validation:**
   - CSV data is validated during processing
   - Malformed data is logged and skipped
   - Error messages do not expose sensitive information

## Future Enhancements

Potential improvements:
1. Real-time chart updates using WebSockets
2. Chart visualization in index.html UI
3. User-configurable automation intervals
4. Email/Slack notifications on errors
5. Database storage for historical data
6. Advanced data analytics and predictions
7. Chart export to PDF/PNG

## Support

For issues or questions:
1. Check automation.log for errors
2. Review API endpoints in api_server.py
3. Test automation manually with chart_automation.py
4. Verify all CSV files are properly formatted

## License

See repository LICENSE file for details.
