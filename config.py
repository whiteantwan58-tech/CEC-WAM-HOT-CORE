"""
config.py
---------
Configuration management for CEC-WAM-HOT-CORE automation system.
Handles API keys, webhook URLs, and system settings.
"""

import os
from typing import Optional

class Config:
    """Central configuration for all automation features."""
    
    # Slack Configuration
    SLACK_WEBHOOK_URL: Optional[str] = os.getenv('SLACK_WEBHOOK_URL')
    SLACK_CHANNEL: str = os.getenv('SLACK_CHANNEL', '#cec-wam-alerts')
    
    # Google Sheets Configuration
    GOOGLE_SHEETS_CREDENTIALS_PATH: str = os.getenv(
        'GOOGLE_SHEETS_CREDENTIALS_PATH', 
        'credentials.json'
    )
    GOOGLE_SHEETS_ID: Optional[str] = os.getenv('GOOGLE_SHEETS_ID')
    
    # File paths
    DATA_DIR: str = 'data'
    EXPORTS_DIR: str = 'exports'
    LOGS_DIR: str = 'logs'
    
    # CSV files to monitor
    CSV_FILES = [
        'pump.fun.csv',
        'BlackHoles.csv',
        'CEC_VAULT.CSV',
        'data/ledger.csv',
        'data/timeline.csv',
        'CEC Matrix System Operational Metrics and Assets - FINANCE_HUB (1).csv'
    ]
    
    # Excel files to monitor
    EXCEL_FILES = [
        'Chart.xlsx',
        'CEC_WAM_MASTER_LEDGER_LIVE.xlsx',
        'CEC_Consolidated_Roadmap_Final.xlsx',
        'CEC_WAM_Master_System (1).xlsx'
    ]
    
    # Log file pattern extraction settings
    LOG_PATTERNS = {
        'error': r'ERROR|FAILED|EXCEPTION',
        'warning': r'WARNING|WARN',
        'anomaly': r'ANOMALY|UNUSUAL|SUSPICIOUS',
        'upload': r'UPLOAD|INGESTION|NEW_DATA'
    }
    
    # Notification settings
    ENABLE_SLACK_NOTIFICATIONS: bool = os.getenv('ENABLE_SLACK_NOTIFICATIONS', 'true').lower() == 'true'
    NOTIFICATION_RATE_LIMIT_SECONDS: int = int(os.getenv('NOTIFICATION_RATE_LIMIT_SECONDS', '300'))
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration settings."""
        if cls.ENABLE_SLACK_NOTIFICATIONS and not cls.SLACK_WEBHOOK_URL:
            print("Warning: Slack notifications enabled but SLACK_WEBHOOK_URL not set")
            return False
        return True
