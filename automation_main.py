"""
automation_main.py
------------------
Main automation script for CEC-WAM-HOT-CORE system.
Ties together all automation features and runs monitoring cycles.
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Import automation modules
from config import Config
from logging_config import setup_logging, get_logger
from slack_notifier import SlackNotifier
from grok_parser import GrokParser
from csv_operations import CSVOperations
from google_sheets_sync import GoogleSheetsSync
from eve_enhanced import EveEnhanced


def initialize_system():
    """Initialize all system components."""
    print("=" * 60)
    print("CEC-WAM-HOT-CORE Automation System")
    print("Initializing...")
    print("=" * 60)
    
    # Validate configuration
    if not Config.validate():
        print("⚠️  Warning: Configuration validation failed. Check your settings.")
    
    # Create necessary directories
    for directory in [Config.DATA_DIR, Config.EXPORTS_DIR, Config.LOGS_DIR]:
        Path(directory).mkdir(exist_ok=True)
    
    # Initialize logging
    slack_notifier = SlackNotifier() if Config.ENABLE_SLACK_NOTIFICATIONS else None
    logger = setup_logging(
        log_dir=Config.LOGS_DIR,
        enable_slack=Config.ENABLE_SLACK_NOTIFICATIONS,
        slack_notifier=slack_notifier
    )
    
    logger.info("System initialization started")
    
    # Initialize components
    components = {
        'eve': EveEnhanced(),
        'grok': GrokParser(),
        'csv_ops': CSVOperations(),
        'slack': slack_notifier,
        'google_sheets': GoogleSheetsSync() if Path(Config.GOOGLE_SHEETS_CREDENTIALS_PATH).exists() else None
    }
    
    logger.info("All components initialized successfully")
    print("✓ System initialization complete")
    print()
    
    return logger, components


def run_monitoring_cycle(logger, components):
    """Run a single monitoring cycle."""
    logger.info("Starting monitoring cycle")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running monitoring cycle...")
    
    try:
        # Run EVE monitoring
        results = components['eve'].monitor_and_notify()
        
        if results['issues_detected']:
            print(f"  ⚠️  Detected {len(results['issues_detected'])} issues")
            for issue in results['issues_detected']:
                print(f"    - {issue}")
        else:
            print("  ✓ No issues detected")
        
        if results['notifications_sent'] > 0:
            print(f"  📨 Sent {results['notifications_sent']} notifications")
        
        logger.info(f"Monitoring cycle complete: {results}")
        
    except Exception as e:
        logger.error(f"Error in monitoring cycle: {e}")
        print(f"  ❌ Error: {e}")


def run_data_analysis(logger, components):
    """Run data analysis on CSV files."""
    logger.info("Starting data analysis")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Analyzing data files...")
    
    try:
        # Get list of CSV files
        csv_files = [f for f in Config.CSV_FILES if os.path.exists(f)]
        
        if not csv_files:
            print("  ⚠️  No CSV files found to analyze")
            return
        
        # Run batch analysis
        results = components['grok'].batch_analyze(csv_files)
        
        print(f"  ✓ Analyzed {results['files_analyzed']} files")
        print(f"  📊 Total rows: {results['total_rows']:,}")
        
        if results['total_anomalies'] > 0:
            print(f"  ⚠️  Found {results['total_anomalies']} anomalies")
            
            # Send Grok insights to Slack
            if components['slack']:
                components['slack'].send_grok_insights(
                    source="Batch Analysis",
                    patterns={
                        'files_analyzed': results['files_analyzed'],
                        'total_rows': results['total_rows'],
                        'anomalies': results['total_anomalies']
                    }
                )
        
        logger.info(f"Data analysis complete: {results}")
        
    except Exception as e:
        logger.error(f"Error in data analysis: {e}")
        print(f"  ❌ Error: {e}")


def sync_with_google_sheets(logger, components):
    """Sync data with Google Sheets."""
    if not components['google_sheets'] or not components['google_sheets'].service:
        print("  ℹ️  Google Sheets sync not configured")
        return
    
    logger.info("Starting Google Sheets sync")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Syncing with Google Sheets...")
    
    try:
        if not Config.GOOGLE_SHEETS_ID:
            print("  ⚠️  Google Sheets ID not configured")
            return
        
        # Sync first available CSV to Google Sheets
        for csv_file in Config.CSV_FILES:
            if os.path.exists(csv_file):
                success = components['google_sheets'].sync_csv_to_sheet(
                    csv_path=csv_file,
                    spreadsheet_id=Config.GOOGLE_SHEETS_ID,
                    range_name='Sheet1!A1',
                    clear_existing=True
                )
                
                if success:
                    print(f"  ✓ Synced {csv_file} to Google Sheets")
                    logger.info(f"Synced {csv_file} to Google Sheets")
                    break
                else:
                    print(f"  ❌ Failed to sync {csv_file}")
        
    except Exception as e:
        logger.error(f"Error in Google Sheets sync: {e}")
        print(f"  ❌ Error: {e}")


def interactive_mode(logger, components):
    """Run in interactive mode with EVE."""
    print("\n" + "=" * 60)
    print("EVE Interactive Mode")
    print("Type 'quit' or 'exit' to stop")
    print("=" * 60 + "\n")
    
    while True:
        try:
            prompt = input("YOU> ").strip()
            
            if prompt.lower() in ['quit', 'exit', 'q']:
                print("EVE: Shutting down. Goodbye.")
                break
            
            if not prompt:
                continue
            
            # Process prompt through EVE
            response = components['eve'].process_user_prompt(prompt)
            print(f"\nEVE: {response['response']}\n")
            
            logger.info(f"Interactive prompt: {prompt}")
            logger.info(f"EVE response: {response['response']}")
            
        except KeyboardInterrupt:
            print("\n\nEVE: Interrupted. Shutting down.")
            break
        except Exception as e:
            logger.error(f"Error in interactive mode: {e}")
            print(f"EVE: Error processing request: {e}")


def main():
    """Main entry point."""
    # Parse command line arguments
    mode = sys.argv[1] if len(sys.argv) > 1 else 'monitor'
    
    # Initialize system
    logger, components = initialize_system()
    
    try:
        if mode == 'monitor':
            # Run monitoring once
            run_monitoring_cycle(logger, components)
            
        elif mode == 'monitor-loop':
            # Continuous monitoring
            print("Starting continuous monitoring (Ctrl+C to stop)...")
            print()
            while True:
                run_monitoring_cycle(logger, components)
                time.sleep(300)  # Run every 5 minutes
                
        elif mode == 'analyze':
            # Run data analysis
            run_data_analysis(logger, components)
            
        elif mode == 'sync':
            # Sync with Google Sheets
            sync_with_google_sheets(logger, components)
            
        elif mode == 'interactive':
            # Interactive EVE mode
            interactive_mode(logger, components)
            
        elif mode == 'full':
            # Run all operations once
            run_monitoring_cycle(logger, components)
            print()
            run_data_analysis(logger, components)
            print()
            sync_with_google_sheets(logger, components)
            
        else:
            print(f"Unknown mode: {mode}")
            print("Available modes: monitor, monitor-loop, analyze, sync, interactive, full")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\nShutdown requested. Exiting...")
        logger.info("System shutdown by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("CEC-WAM-HOT-CORE Automation System - Stopped")
    print("=" * 60)


if __name__ == "__main__":
    main()
