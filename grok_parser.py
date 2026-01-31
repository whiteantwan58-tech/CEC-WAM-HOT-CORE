"""
grok_parser.py
--------------
Grok-style pattern extraction and insights from system logs and CSV files.
Provides real-time parsing and anomaly detection capabilities.
"""

import re
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import Counter

from config import Config
from logging_config import get_logger

logger = get_logger('grok_parser')


class GrokParser:
    """Pattern extraction and analysis for logs and structured data."""
    
    def __init__(self):
        """Initialize the Grok parser."""
        self.patterns = Config.LOG_PATTERNS
        self.insights_cache: Dict[str, Any] = {}
    
    def parse_log_file(self, log_file: str) -> Dict[str, Any]:
        """
        Parse a log file and extract patterns.
        
        Args:
            log_file: Path to log file
        
        Returns:
            Dictionary of extracted patterns and insights
        """
        logger.info(f"Parsing log file: {log_file}")
        
        if not Path(log_file).exists():
            logger.warning(f"Log file not found: {log_file}")
            return {}
        
        insights = {
            'file': log_file,
            'timestamp': datetime.now().isoformat(),
            'patterns': {},
            'statistics': {},
            'anomalies': []
        }
        
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Extract pattern matches
            for pattern_name, pattern_regex in self.patterns.items():
                matches = []
                for i, line in enumerate(lines, 1):
                    if re.search(pattern_regex, line, re.IGNORECASE):
                        matches.append({
                            'line_number': i,
                            'content': line.strip()[:200]
                        })
                
                insights['patterns'][pattern_name] = {
                    'count': len(matches),
                    'samples': matches[:5]  # Keep first 5 samples
                }
            
            # Basic statistics
            insights['statistics'] = {
                'total_lines': len(lines),
                'non_empty_lines': sum(1 for line in lines if line.strip()),
                'patterns_found': sum(p['count'] for p in insights['patterns'].values())
            }
            
            # Detect anomalies (high error rate)
            error_count = insights['patterns'].get('error', {}).get('count', 0)
            if error_count > 10:
                insights['anomalies'].append({
                    'type': 'high_error_rate',
                    'severity': 'warning' if error_count < 50 else 'error',
                    'description': f'Detected {error_count} errors in log file'
                })
            
            logger.info(f"Log parsing complete: {insights['statistics']}")
            
        except Exception as e:
            logger.error(f"Error parsing log file: {e}")
            insights['error'] = str(e)
        
        return insights
    
    def parse_csv_file(self, csv_file: str) -> Dict[str, Any]:
        """
        Parse a CSV file and extract insights.
        
        Args:
            csv_file: Path to CSV file
        
        Returns:
            Dictionary of insights and statistics
        """
        logger.info(f"Parsing CSV file: {csv_file}")
        
        if not Path(csv_file).exists():
            logger.warning(f"CSV file not found: {csv_file}")
            return {}
        
        insights = {
            'file': csv_file,
            'timestamp': datetime.now().isoformat(),
            'statistics': {},
            'data_quality': {},
            'anomalies': []
        }
        
        try:
            df = pd.read_csv(csv_file)
            
            # Basic statistics
            insights['statistics'] = {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': list(df.columns),
                'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
            }
            
            # Data quality metrics
            insights['data_quality'] = {
                'missing_values': df.isnull().sum().to_dict(),
                'duplicate_rows': int(df.duplicated().sum()),
                'data_types': df.dtypes.astype(str).to_dict()
            }
            
            # Detect numeric columns for statistics
            numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_columns) > 0:
                insights['numeric_summary'] = df[numeric_columns].describe().to_dict()
            
            # Detect anomalies
            total_missing = df.isnull().sum().sum()
            missing_percentage = (total_missing / (len(df) * len(df.columns))) * 100
            
            if missing_percentage > 10:
                insights['anomalies'].append({
                    'type': 'high_missing_data',
                    'severity': 'warning' if missing_percentage < 30 else 'error',
                    'description': f'{missing_percentage:.1f}% of data is missing'
                })
            
            if insights['data_quality']['duplicate_rows'] > 0:
                insights['anomalies'].append({
                    'type': 'duplicate_rows',
                    'severity': 'warning',
                    'description': f"Found {insights['data_quality']['duplicate_rows']} duplicate rows"
                })
            
            logger.info(f"CSV parsing complete: {insights['statistics']}")
            
        except Exception as e:
            logger.error(f"Error parsing CSV file: {e}")
            insights['error'] = str(e)
        
        return insights
    
    def analyze_csv_patterns(self, csv_file: str, column: str) -> Dict[str, Any]:
        """
        Analyze patterns in a specific CSV column.
        
        Args:
            csv_file: Path to CSV file
            column: Column name to analyze
        
        Returns:
            Dictionary of pattern analysis results
        """
        logger.info(f"Analyzing patterns in {csv_file}, column: {column}")
        
        try:
            df = pd.read_csv(csv_file)
            
            if column not in df.columns:
                logger.warning(f"Column '{column}' not found in {csv_file}")
                return {'error': f"Column '{column}' not found"}
            
            series = df[column].dropna()
            
            analysis = {
                'column': column,
                'timestamp': datetime.now().isoformat(),
                'value_counts': series.value_counts().head(10).to_dict(),
                'unique_values': int(series.nunique()),
                'most_common': series.mode().tolist() if not series.empty else []
            }
            
            # Pattern detection for string columns
            if series.dtype == 'object':
                # Detect common patterns
                patterns = []
                for value in series.head(100):
                    value_str = str(value)
                    if re.match(r'^\d+$', value_str):
                        patterns.append('numeric')
                    elif re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value_str):
                        patterns.append('email')
                    elif re.match(r'^\d{4}-\d{2}-\d{2}', value_str):
                        patterns.append('date')
                    elif re.match(r'^https?://', value_str):
                        patterns.append('url')
                    else:
                        patterns.append('text')
                
                pattern_counts = Counter(patterns)
                analysis['pattern_distribution'] = dict(pattern_counts)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing CSV patterns: {e}")
            return {'error': str(e)}
    
    def real_time_monitor(self, file_path: str) -> Dict[str, Any]:
        """
        Monitor a file for real-time updates and extract patterns.
        
        Args:
            file_path: Path to file to monitor
        
        Returns:
            Latest insights from the file
        """
        path = Path(file_path)
        
        if not path.exists():
            return {'error': 'File not found'}
        
        # Check if file was modified recently
        file_time = path.stat().st_mtime
        cached_time = self.insights_cache.get(f'{file_path}_time', 0)
        
        if file_time > cached_time:
            logger.info(f"File updated, re-analyzing: {file_path}")
            
            if file_path.endswith('.csv'):
                insights = self.parse_csv_file(file_path)
            else:
                insights = self.parse_log_file(file_path)
            
            self.insights_cache[file_path] = insights
            self.insights_cache[f'{file_path}_time'] = file_time
            
            return insights
        else:
            return self.insights_cache.get(file_path, {})
    
    def batch_analyze(self, file_list: List[str]) -> Dict[str, Any]:
        """
        Analyze multiple files and provide consolidated insights.
        
        Args:
            file_list: List of file paths to analyze
        
        Returns:
            Consolidated insights from all files
        """
        logger.info(f"Batch analyzing {len(file_list)} files")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'files_analyzed': 0,
            'total_rows': 0,
            'total_anomalies': 0,
            'file_insights': {}
        }
        
        for file_path in file_list:
            if Path(file_path).exists():
                if file_path.endswith('.csv'):
                    insights = self.parse_csv_file(file_path)
                else:
                    insights = self.parse_log_file(file_path)
                
                results['file_insights'][file_path] = insights
                results['files_analyzed'] += 1
                
                if 'statistics' in insights:
                    results['total_rows'] += insights['statistics'].get('rows', 0) or \
                                            insights['statistics'].get('total_lines', 0)
                
                if 'anomalies' in insights:
                    results['total_anomalies'] += len(insights['anomalies'])
        
        logger.info(f"Batch analysis complete: {results['files_analyzed']} files analyzed")
        
        return results
