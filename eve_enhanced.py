"""
eve_enhanced.py
---------------
Enhanced EVE agent with real-time prompts, dynamic responses, and data-driven recommendations.
Extends existing eve_agent.py and eve_cec_wam_live.py functionality.
"""

import os
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
import pandas as pd

from eve_agent import export_and_cleanup, get_disk_usage
from config import Config
from logging_config import get_logger
from grok_parser import GrokParser
from csv_operations import CSVOperations
from slack_notifier import SlackNotifier

logger = get_logger('eve_enhanced')


class EveEnhanced:
    """Enhanced EVE agent with automation and intelligence capabilities."""
    
    def __init__(self):
        """Initialize enhanced EVE agent."""
        self.grok = GrokParser()
        self.csv_ops = CSVOperations()
        self.slack = SlackNotifier() if Config.ENABLE_SLACK_NOTIFICATIONS else None
        self.state = {
            'last_check': None,
            'insights_cache': {},
            'recommendations': []
        }
        logger.info("EVE Enhanced initialized")
    
    def process_user_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Process a user prompt and generate intelligent response.
        
        Args:
            prompt: User input prompt
        
        Returns:
            Dictionary with response and actions
        """
        logger.info(f"Processing user prompt: {prompt[:100]}")
        
        response = {
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt,
            'response': '',
            'actions': [],
            'recommendations': []
        }
        
        prompt_lower = prompt.lower()
        
        # Handle system status queries
        if any(word in prompt_lower for word in ['status', 'health', 'check']):
            response['response'] = self._get_system_status()
            response['actions'].append('system_check')
        
        # Handle data analysis requests
        elif any(word in prompt_lower for word in ['analyze', 'insights', 'patterns']):
            insights = self._analyze_system_data()
            response['response'] = self._format_insights(insights)
            response['actions'].append('data_analysis')
        
        # Handle data queries
        elif any(word in prompt_lower for word in ['show', 'data', 'csv', 'file']):
            data_summary = self._get_data_summary()
            response['response'] = data_summary
            response['actions'].append('data_query')
        
        # Handle cleanup requests
        elif any(word in prompt_lower for word in ['clean', 'cleanup', 'export']):
            cleanup_result = export_and_cleanup()
            response['response'] = cleanup_result
            response['actions'].append('cleanup')
        
        # Handle recommendations
        elif any(word in prompt_lower for word in ['recommend', 'suggest', 'advice']):
            recommendations = self._generate_recommendations()
            response['response'] = self._format_recommendations(recommendations)
            response['recommendations'] = recommendations
            response['actions'].append('recommendations')
        
        # Default response
        else:
            response['response'] = (
                "EVE ONLINE: I'm monitoring the CEC-WAM system. "
                "Ask me about status, insights, data, or recommendations."
            )
        
        return response
    
    def _get_system_status(self) -> str:
        """Get current system status."""
        disk_usage = get_disk_usage()
        
        status_parts = [
            "EVE SYSTEM STATUS:",
            f"• Disk Usage: {disk_usage*100:.1f}%",
            f"• Status: {'⚠️ HIGH' if disk_usage > 0.85 else '✓ OK'}",
            f"• Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ]
        
        # Check data files
        missing_files = []
        for csv_file in Config.CSV_FILES:
            if not os.path.exists(csv_file):
                missing_files.append(csv_file)
        
        if missing_files:
            status_parts.append(f"• ⚠️ Missing files: {len(missing_files)}")
        else:
            status_parts.append("• ✓ All data files present")
        
        return "\n".join(status_parts)
    
    def _analyze_system_data(self) -> Dict[str, Any]:
        """Analyze system data and extract insights."""
        logger.info("Analyzing system data")
        
        insights = {
            'timestamp': datetime.now().isoformat(),
            'files_analyzed': [],
            'total_rows': 0,
            'anomalies': [],
            'key_insights': []
        }
        
        # Analyze CSV files
        for csv_file in Config.CSV_FILES:
            if os.path.exists(csv_file):
                file_insights = self.grok.parse_csv_file(csv_file)
                insights['files_analyzed'].append(csv_file)
                
                if 'statistics' in file_insights:
                    insights['total_rows'] += file_insights['statistics'].get('rows', 0)
                
                if 'anomalies' in file_insights and file_insights['anomalies']:
                    insights['anomalies'].extend(file_insights['anomalies'])
        
        # Generate key insights
        if insights['total_rows'] > 0:
            insights['key_insights'].append(f"Total data records: {insights['total_rows']:,}")
        
        if insights['anomalies']:
            insights['key_insights'].append(f"Detected {len(insights['anomalies'])} anomalies")
        
        return insights
    
    def _get_data_summary(self) -> str:
        """Get summary of available data."""
        summary_parts = ["EVE DATA SUMMARY:"]
        
        for csv_file in Config.CSV_FILES:
            if os.path.exists(csv_file):
                stats = self.csv_ops.get_csv_statistics(csv_file)
                if 'error' not in stats:
                    summary_parts.append(
                        f"• {csv_file}: {stats['rows']:,} rows, {stats['columns']} columns"
                    )
        
        return "\n".join(summary_parts) if len(summary_parts) > 1 else "No data files found."
    
    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        """Generate data-driven recommendations."""
        recommendations = []
        
        # Check disk usage
        disk_usage = get_disk_usage()
        if disk_usage > 0.80:
            recommendations.append({
                'priority': 'high' if disk_usage > 0.90 else 'medium',
                'category': 'storage',
                'title': 'High Disk Usage',
                'description': f'Disk usage at {disk_usage*100:.1f}%. Consider running cleanup.',
                'action': 'Run export_and_cleanup()'
            })
        
        # Check for data anomalies
        for csv_file in Config.CSV_FILES[:3]:  # Check first 3 files
            if os.path.exists(csv_file):
                insights = self.grok.parse_csv_file(csv_file)
                if 'anomalies' in insights and insights['anomalies']:
                    for anomaly in insights['anomalies']:
                        recommendations.append({
                            'priority': anomaly.get('severity', 'medium'),
                            'category': 'data_quality',
                            'title': anomaly['type'],
                            'description': anomaly['description'],
                            'action': f'Review {csv_file}'
                        })
        
        # Recommend updates if files are old
        for csv_file in Config.CSV_FILES:
            if os.path.exists(csv_file):
                mtime = os.path.getmtime(csv_file)
                age_days = (time.time() - mtime) / 86400
                if age_days > 7:
                    recommendations.append({
                        'priority': 'low',
                        'category': 'data_freshness',
                        'title': 'Stale Data',
                        'description': f'{csv_file} not updated in {int(age_days)} days',
                        'action': 'Consider updating with fresh data'
                    })
        
        return recommendations
    
    def _format_insights(self, insights: Dict[str, Any]) -> str:
        """Format insights for display."""
        parts = ["EVE ANALYSIS INSIGHTS:"]
        
        if insights.get('files_analyzed'):
            parts.append(f"• Analyzed {len(insights['files_analyzed'])} files")
        
        if insights.get('total_rows'):
            parts.append(f"• Total records: {insights['total_rows']:,}")
        
        if insights.get('anomalies'):
            parts.append(f"• Anomalies detected: {len(insights['anomalies'])}")
            for anomaly in insights['anomalies'][:3]:  # Show first 3
                parts.append(f"  - {anomaly['type']}: {anomaly['description']}")
        
        if insights.get('key_insights'):
            for insight in insights['key_insights']:
                parts.append(f"• {insight}")
        
        return "\n".join(parts)
    
    def _format_recommendations(self, recommendations: List[Dict[str, Any]]) -> str:
        """Format recommendations for display."""
        if not recommendations:
            return "EVE: All systems operating optimally. No recommendations at this time."
        
        parts = ["EVE RECOMMENDATIONS:"]
        
        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        sorted_recs = sorted(
            recommendations,
            key=lambda x: priority_order.get(x['priority'], 3)
        )
        
        for rec in sorted_recs[:5]:  # Show top 5
            priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
            parts.append(f"\n{priority_emoji} {rec['title']}")
            parts.append(f"  {rec['description']}")
            parts.append(f"  Action: {rec['action']}")
        
        return "\n".join(parts)
    
    def monitor_and_notify(self) -> Dict[str, Any]:
        """
        Monitor system and send notifications for important events.
        
        Returns:
            Dictionary with monitoring results
        """
        logger.info("Running system monitoring cycle")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'notifications_sent': 0,
            'issues_detected': []
        }
        
        # Check for anomalies
        for csv_file in Config.CSV_FILES:
            if os.path.exists(csv_file):
                insights = self.grok.real_time_monitor(csv_file)
                
                if 'anomalies' in insights and insights['anomalies']:
                    for anomaly in insights['anomalies']:
                        results['issues_detected'].append({
                            'file': csv_file,
                            'anomaly': anomaly
                        })
                        
                        # Send Slack notification
                        if self.slack:
                            self.slack.send_anomaly_alert(
                                anomaly_type=anomaly['type'],
                                description=f"In {csv_file}: {anomaly['description']}",
                                severity=anomaly.get('severity', 'warning')
                            )
                            results['notifications_sent'] += 1
        
        # Check disk usage
        disk_usage = get_disk_usage()
        if disk_usage > 0.85:
            results['issues_detected'].append({
                'type': 'high_disk_usage',
                'usage': disk_usage
            })
            
            if self.slack:
                self.slack.send_anomaly_alert(
                    anomaly_type='High Disk Usage',
                    description=f'Disk usage at {disk_usage*100:.1f}%',
                    severity='warning' if disk_usage < 0.90 else 'error'
                )
                results['notifications_sent'] += 1
        
        self.state['last_check'] = datetime.now().isoformat()
        
        return results
    
    def get_real_time_recommendations(self) -> List[Dict[str, Any]]:
        """
        Get real-time recommendations based on current system state.
        
        Returns:
            List of recommendations
        """
        return self._generate_recommendations()
