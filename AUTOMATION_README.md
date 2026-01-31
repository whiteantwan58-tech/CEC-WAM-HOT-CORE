# CEC-WAM-HOT-CORE Automation Enhancement

This repository now includes comprehensive automation features for the CEC-WAM system.

## New Features

### 1. Grok Automation (`grok_parser.py`)
- Pattern extraction from system logs and CSV files
- Real-time parsing and anomaly detection
- Batch analysis capabilities
- Insights generation and caching

### 2. Enhanced EVE Integration (`eve_enhanced.py`)
- Real-time user prompt processing
- Dynamic response generation
- Data-driven recommendations
- System monitoring with automatic notifications

### 3. Slack Notifications (`slack_notifier.py`)
- Webhook-based integration
- Notifications for:
  - Data uploads and ingestion
  - Chart updates and insights
  - Missing data or anomalies
  - System errors
- Rate limiting to prevent spam

### 4. Google Sheets Integration (`google_sheets_sync.py`)
- Two-way synchronization
- Real-time updates and retrieval
- CSV to Sheets sync
- Sheets to CSV sync

### 5. UI Form Integration (`index.html`)
- Data input modal with form controls
- Real-time Grok analysis trigger
- Integration with EVE terminal
- Local storage persistence

### 6. CSV Operations (`csv_operations.py`)
- Automated merging and updating
- File validation and schema checking
- Excel synchronization
- Statistics and insights

### 7. Logging and Error Tracking (`logging_config.py`)
- Centralized logging framework
- JSON-formatted structured logs
- Automatic error notifications to Slack
- Daily log rotation

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

3. (Optional) Set up Google Sheets:
   - Create a service account in Google Cloud Console
   - Download credentials JSON as `credentials.json`
   - Share your Google Sheet with the service account email

## Usage

### Run Main Automation Script

```bash
# Run single monitoring cycle
python automation_main.py monitor

# Continuous monitoring (every 5 minutes)
python automation_main.py monitor-loop

# Run data analysis
python automation_main.py analyze

# Sync with Google Sheets
python automation_main.py sync

# Interactive EVE mode
python automation_main.py interactive

# Run all operations once
python automation_main.py full
```

### Use Individual Modules

```python
from grok_parser import GrokParser
from csv_operations import CSVOperations
from eve_enhanced import EveEnhanced

# Parse CSV file
grok = GrokParser()
insights = grok.parse_csv_file('pump.fun.csv')

# Merge CSV files
csv_ops = CSVOperations()
csv_ops.merge_csv_files(['file1.csv', 'file2.csv'], 'merged.csv')

# Process EVE prompt
eve = EveEnhanced()
response = eve.process_user_prompt("analyze system data")
```

### Web Interface

1. Start a local server:
```bash
python -m http.server 8000
```

2. Open `http://localhost:8000` in your browser

3. Use the "📊 Input Data" button in the header to:
   - Submit new data entries
   - Trigger Grok analysis
   - View real-time updates in EVE terminal

## Configuration

Edit `config.py` or use environment variables:

- `SLACK_WEBHOOK_URL`: Your Slack webhook URL
- `SLACK_CHANNEL`: Target Slack channel (default: #cec-wam-alerts)
- `GOOGLE_SHEETS_ID`: Your Google Sheets ID
- `ENABLE_SLACK_NOTIFICATIONS`: Enable/disable Slack (default: true)

## File Structure

```
CEC-WAM-HOT-CORE/
├── automation_main.py          # Main automation script
├── config.py                   # Configuration management
├── logging_config.py           # Logging setup
├── slack_notifier.py          # Slack integration
├── grok_parser.py             # Pattern extraction
├── csv_operations.py          # CSV file operations
├── google_sheets_sync.py      # Google Sheets sync
├── eve_enhanced.py            # Enhanced EVE agent
├── eve_agent.py               # Original EVE agent
├── eve_cec_wam_live.py       # EVE live interface
├── index.html                 # Web UI with form
├── styl.css                   # Enhanced styles
├── requirements.txt           # Python dependencies
└── .env.example              # Configuration template
```

## Automation Workflow

1. **Monitoring**: EVE continuously monitors system files and disk usage
2. **Analysis**: Grok extracts patterns and detects anomalies
3. **Notifications**: Slack alerts are sent for important events
4. **Sync**: Data is synced with Google Sheets for external access
5. **UI Updates**: Web interface provides real-time interaction

## Security Notes

- Never commit `.env` or `credentials.json` to version control
- Use environment variables for sensitive configuration
- Slack webhook URLs should be kept secret
- Google Sheets service account credentials are sensitive

## Troubleshooting

**Google Sheets not syncing:**
- Verify credentials.json exists
- Check service account has access to the sheet
- Ensure GOOGLE_SHEETS_ID is correct

**Slack notifications not working:**
- Verify SLACK_WEBHOOK_URL is correct
- Check ENABLE_SLACK_NOTIFICATIONS is true
- Review rate limiting settings

**Module import errors:**
- Run `pip install -r requirements.txt`
- Ensure all dependencies are installed

## Contributing

When adding new automation features:
1. Add configuration to `config.py`
2. Add logging using `get_logger()`
3. Integrate with Slack notifications
4. Update this README
