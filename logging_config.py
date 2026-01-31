"""
logging_config.py
-----------------
Centralized logging configuration for CEC-WAM-HOT-CORE automation system.
Provides structured logging with optional Slack integration for errors.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from pythonjsonlogger import jsonlogger

# Import Slack notifier (will be created next)
try:
    from slack_notifier import SlackNotifier
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False


class SlackErrorHandler(logging.Handler):
    """Custom logging handler that sends errors to Slack."""
    
    def __init__(self, slack_notifier: Optional['SlackNotifier'] = None):
        super().__init__()
        self.slack_notifier = slack_notifier
        self.setLevel(logging.ERROR)
    
    def emit(self, record: logging.LogRecord):
        """Send log record to Slack."""
        if self.slack_notifier:
            try:
                log_entry = self.format(record)
                self.slack_notifier.send_error_notification(
                    error_type=record.levelname,
                    error_message=record.getMessage(),
                    details=log_entry
                )
            except Exception:
                # Don't let Slack failures break logging
                pass


def setup_logging(
    log_dir: str = 'logs',
    log_level: int = logging.INFO,
    enable_slack: bool = False,
    slack_notifier: Optional['SlackNotifier'] = None
) -> logging.Logger:
    """
    Set up centralized logging for the CEC-WAM system.
    
    Args:
        log_dir: Directory to store log files
        log_level: Logging level (default: INFO)
        enable_slack: Whether to send errors to Slack
        slack_notifier: SlackNotifier instance for error notifications
    
    Returns:
        Configured logger instance
    """
    # Create logs directory
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger('cec_wam')
    logger.setLevel(log_level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler with standard formatting
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler with JSON formatting for structured logs
    timestamp = datetime.now().strftime('%Y%m%d')
    log_file = log_path / f'cec_wam_{timestamp}.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    json_formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(json_formatter)
    logger.addHandler(file_handler)
    
    # Add Slack handler for errors if enabled
    if enable_slack and SLACK_AVAILABLE and slack_notifier:
        slack_handler = SlackErrorHandler(slack_notifier)
        slack_handler.setFormatter(console_formatter)
        logger.addHandler(slack_handler)
    
    logger.info(f"Logging initialized - Level: {logging.getLevelName(log_level)}, Slack: {enable_slack}")
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Optional logger name, defaults to 'cec_wam'
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name or 'cec_wam')
