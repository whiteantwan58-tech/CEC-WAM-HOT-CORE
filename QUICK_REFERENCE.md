# Quick Reference Guide - Chart Automation System

## For End Users

### Starting the System

**One-Command Start:**
```bash
./start_services.sh
```

This will:
- Install dependencies
- Run initial automation
- Start API server (port 5000)
- Start frontend (port 8000)

**Access the System:**
- Open browser: http://localhost:8000
- Use the EVE terminal for commands

### Terminal Commands

| Command | Description | Example Output |
|---------|-------------|----------------|
| `help` | Show all commands | List of available commands |
| `charts` | View chart datasets | Shows 3 available charts with details |
| `automation` | Check automation status | Status: SUCCESS, Last update time |
| `status` | System status | CEC-WAM CORE: NOMINAL |
| `prices` | Crypto prices | BTC/ETH/SOL current prices |
| `clear` | Clear terminal log | Clears the terminal |

### Running Automation Manually

**Run Once:**
```bash
python chart_automation.py
```

**Run Continuously (every 30 minutes):**
```bash
python scheduled_automation.py
```

**Run Continuously (custom interval):**
```bash
python scheduled_automation.py --interval 15
```

## For Developers

### Project Structure

```
CEC-WAM-HOT-CORE/
├── chart_automation.py      # Main automation script
├── api_server.py             # Flask API server
├── scheduled_automation.py   # Scheduler
├── start_services.sh         # Startup script
├── test_integration.py       # Integration tests
├── index.html                # Frontend
├── requirements.txt          # Dependencies
├── Chart.xlsx                # Generated Excel file
├── data/
│   ├── chart_data.json      # Chart data for web
│   ├── automation_report.json # Status report
│   ├── ledger.csv           # System ledger
│   └── timeline.csv         # Timeline data
├── pump.fun.csv             # Transaction data
├── BlackHoles.csv           # Research data
└── CEC Matrix System...csv  # Financial data
```

### API Endpoints

```bash
# Health check
curl http://localhost:5000/api/health

# Get chart data
curl http://localhost:5000/api/chart-data

# Get automation status
curl http://localhost:5000/api/automation-status

# List datasets
curl http://localhost:5000/api/datasets

# Get live aggregated data
curl http://localhost:5000/api/live-data

# Trigger automation
curl -X POST http://localhost:5000/api/run-automation
```

### Running Tests

```bash
# Run all integration tests
python test_integration.py

# Expected output: 15/15 tests passed
```

### Adding New Data Sources

1. Add CSV file to repository root or `data/` directory
2. Run automation:
   ```bash
   python chart_automation.py
   ```
3. New sheet will be added to Chart.xlsx automatically
4. Chart data will be generated if applicable

### Customizing Chart Generation

Edit `chart_automation.py` in the `generate_chart_data_json()` method:

```python
# Add your custom chart logic
my_file = os.path.join(self.base_dir, 'my_data.csv')
if os.path.exists(my_file):
    df = pd.read_csv(my_file)
    chart_data['datasets']['my_chart'] = {
        'labels': df['column_name'].tolist(),
        'values': df['value_column'].tolist(),
        'type': 'line',  # or 'bar', 'pie'
        'title': 'My Chart Title'
    }
```

### Environment Variables

| Variable | Purpose | Default | Production |
|----------|---------|---------|------------|
| `FLASK_ENV` | Flask mode | `production` | `production` |

**Development Mode:**
```bash
FLASK_ENV=development python api_server.py
```

**Production Mode:**
```bash
python api_server.py  # Debug off by default
```

## Troubleshooting

### Issue: Chart data not showing in terminal

**Solution:**
1. Check if API server is running:
   ```bash
   curl http://localhost:5000/api/health
   ```
2. If not running, start it:
   ```bash
   python api_server.py &
   ```

### Issue: Automation failed

**Solution:**
1. Check logs:
   ```bash
   cat automation.log
   ```
2. Verify CSV files exist
3. Check file permissions
4. Run test:
   ```bash
   python test_integration.py
   ```

### Issue: Chart.xlsx not updating

**Solution:**
1. Run automation manually:
   ```bash
   python chart_automation.py
   ```
2. Check for errors in output
3. Verify write permissions

### Issue: API server not responding

**Solution:**
1. Check if port 5000 is in use:
   ```bash
   lsof -i :5000
   ```
2. Kill existing process:
   ```bash
   kill <PID>
   ```
3. Restart API server:
   ```bash
   python api_server.py
   ```

### Issue: Frontend not loading

**Solution:**
1. Check if port 8000 is in use:
   ```bash
   lsof -i :8000
   ```
2. Start HTTP server:
   ```bash
   python -m http.server 8000
   ```
3. Open browser to http://localhost:8000

## Common Tasks

### Update Chart Data

```bash
# Quick update
python chart_automation.py

# View results
curl http://localhost:5000/api/automation-status
```

### Check System Status

```bash
# Via API
curl http://localhost:5000/api/health

# Via terminal
# Open http://localhost:8000
# Type: automation
```

### Export All Data

```bash
# Chart.xlsx contains all CSV data
# Located at: ./Chart.xlsx

# Chart data JSON
cat data/chart_data.json | python -m json.tool
```

### Stop All Services

```bash
# If started with start_services.sh
# Press Ctrl+C

# Manual stop
pkill -f "python api_server.py"
pkill -f "python -m http.server"
```

## Performance Tips

1. **Large CSV files**: Automation limits to 1000 rows per sheet
2. **Frequent updates**: Use scheduled_automation.py with longer intervals
3. **API rate limiting**: Consider adding rate limiting in production
4. **Caching**: Chart data is cached in JSON for fast access

## Security Best Practices

1. ✅ Never commit secrets to repository
2. ✅ Use environment variables for sensitive data
3. ✅ Disable debug mode in production
4. ✅ Configure CORS properly for production
5. ✅ Add authentication for API in production
6. ✅ Use HTTPS in production
7. ✅ Validate all input data

## Support

For issues or questions:
1. Check logs: `automation.log`
2. Run tests: `python test_integration.py`
3. Review documentation: `CHART_AUTOMATION_DOCS.md`
4. Check implementation: `IMPLEMENTATION_SUMMARY.md`

---
Last Updated: 2026-01-31
Version: 1.0.0
