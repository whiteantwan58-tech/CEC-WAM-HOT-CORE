"""
slack_notifier.py
-----------------
Slack integration for CEC-WAM-HOT-CORE automation system.
Sends notifications for various system events.
"""

import time
from datetime import datetime
from typing import Optional, Dict, Any
from slack_sdk import WebhookClient
from slack_sdk.errors import SlackApiError

from config import Config


class SlackNotifier:
    """Handles Slack notifications via webhook."""
    
    def __init__(self, webhook_url: Optional[str] = None):
        """
        Initialize Slack notifier.
        
        Args:
            webhook_url: Slack webhook URL (defaults to config)
        """
        self.webhook_url = webhook_url or Config.SLACK_WEBHOOK_URL
        self.client = None
        self.last_notification_time: Dict[str, float] = {}
        
        if self.webhook_url:
            self.client = WebhookClient(self.webhook_url)
        else:
            print("Warning: Slack webhook URL not configured")
    
    def _should_send(self, notification_type: str) -> bool:
        """
        Check if notification should be sent based on rate limiting.
        
        Args:
            notification_type: Type of notification for rate limiting
        
        Returns:
            True if notification should be sent
        """
        now = time.time()
        last_time = self.last_notification_time.get(notification_type, 0)
        
        if now - last_time < Config.NOTIFICATION_RATE_LIMIT_SECONDS:
            return False
        
        self.last_notification_time[notification_type] = now
        return True
    
    def _send_message(self, text: str, blocks: Optional[list] = None) -> bool:
        """
        Send a message to Slack.
        
        Args:
            text: Fallback text for the message
            blocks: Optional rich message blocks
        
        Returns:
            True if message sent successfully
        """
        if not self.client or not Config.ENABLE_SLACK_NOTIFICATIONS:
            return False
        
        try:
            if blocks:
                response = self.client.send(text=text, blocks=blocks)
            else:
                response = self.client.send(text=text)
            return response.status_code == 200
        except SlackApiError as e:
            print(f"Error sending Slack notification: {e}")
            return False
    
    def send_data_upload_notification(self, filename: str, record_count: int) -> bool:
        """
        Notify about new data upload.
        
        Args:
            filename: Name of uploaded file
            record_count: Number of records in the file
        
        Returns:
            True if notification sent successfully
        """
        if not self._should_send('data_upload'):
            return False
        
        text = f"📊 New Data Upload: {filename}"
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📊 New Data Upload"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*File:*\n{filename}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Records:*\n{record_count:,}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Time:*\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    }
                ]
            }
        ]
        
        return self._send_message(text, blocks)
    
    def send_chart_update_notification(self, chart_name: str, insights: str) -> bool:
        """
        Notify about chart updates and insights.
        
        Args:
            chart_name: Name of the updated chart
            insights: Insights from analysis
        
        Returns:
            True if notification sent successfully
        """
        if not self._should_send('chart_update'):
            return False
        
        text = f"📈 Chart Update: {chart_name}"
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📈 Chart Update"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Chart:*\n{chart_name}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Time:*\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Insights:*\n{insights}"
                }
            }
        ]
        
        return self._send_message(text, blocks)
    
    def send_anomaly_alert(self, anomaly_type: str, description: str, severity: str = "warning") -> bool:
        """
        Send alert for anomalies or missing data.
        
        Args:
            anomaly_type: Type of anomaly detected
            description: Detailed description
            severity: Severity level (warning, error, critical)
        
        Returns:
            True if notification sent successfully
        """
        if not self._should_send(f'anomaly_{anomaly_type}'):
            return False
        
        emoji = "⚠️" if severity == "warning" else "🚨" if severity == "error" else "🔴"
        text = f"{emoji} Anomaly Alert: {anomaly_type}"
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} Anomaly Alert"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Type:*\n{anomaly_type}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Severity:*\n{severity.upper()}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Time:*\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Description:*\n{description}"
                }
            }
        ]
        
        return self._send_message(text, blocks)
    
    def send_error_notification(self, error_type: str, error_message: str, details: str = "") -> bool:
        """
        Send error notification.
        
        Args:
            error_type: Type of error
            error_message: Error message
            details: Additional error details
        
        Returns:
            True if notification sent successfully
        """
        if not self._should_send('error'):
            return False
        
        text = f"❌ Error: {error_type}"
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "❌ System Error"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Error Type:*\n{error_type}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Time:*\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Message:*\n```{error_message}```"
                }
            }
        ]
        
        if details:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Details:*\n```{details[:500]}```"
                }
            })
        
        return self._send_message(text, blocks)
    
    def send_grok_insights(self, source: str, patterns: Dict[str, Any]) -> bool:
        """
        Send Grok pattern extraction insights.
        
        Args:
            source: Source file or log
            patterns: Extracted patterns
        
        Returns:
            True if notification sent successfully
        """
        if not self._should_send('grok_insights'):
            return False
        
        text = f"🔍 Grok Analysis: {source}"
        
        pattern_text = "\n".join([f"• {k}: {v}" for k, v in patterns.items()])
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🔍 Grok Pattern Analysis"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Source:*\n{source}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Time:*\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Patterns Detected:*\n{pattern_text[:2000]}"
                }
            }
        ]
        
        return self._send_message(text, blocks)
