"""
scheduled_automation.py
-----------------------

Automated scheduler that runs the chart automation at regular intervals.
This ensures that Chart.xlsx and chart data are continuously updated.

Usage:
    python scheduled_automation.py [--interval MINUTES]
"""

import time
import argparse
import logging
from datetime import datetime
from chart_automation import ChartAutomation

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_scheduled_automation(interval_minutes=30):
    """
    Run chart automation at regular intervals
    
    Args:
        interval_minutes (int): Minutes between automation runs
    """
    logger.info("=" * 60)
    logger.info("Starting Scheduled Chart Automation")
    logger.info(f"Interval: {interval_minutes} minutes")
    logger.info("=" * 60)
    
    automation = ChartAutomation()
    run_count = 0
    
    while True:
        try:
            run_count += 1
            logger.info(f"\n{'=' * 60}")
            logger.info(f"Automation Run #{run_count} - {datetime.now().isoformat()}")
            logger.info(f"{'=' * 60}")
            
            # Run the automation
            report = automation.run_full_automation()
            
            if report.get('status') == 'SUCCESS':
                logger.info(f"✓ Automation completed successfully")
                logger.info(f"  - CSV files processed: {report.get('csv_files_processed', 0)}")
                logger.info(f"  - Chart.xlsx updated: {report.get('chart_xlsx_updated', False)}")
            else:
                logger.error(f"✗ Automation failed: {report.get('error', 'Unknown error')}")
            
            # Wait for next run
            logger.info(f"\nNext run in {interval_minutes} minutes...")
            time.sleep(interval_minutes * 60)
            
        except KeyboardInterrupt:
            logger.info("\n\nScheduled automation stopped by user")
            break
        except Exception as e:
            logger.error(f"Unexpected error in scheduled automation: {str(e)}")
            logger.info("Retrying in 5 minutes...")
            time.sleep(300)  # Wait 5 minutes before retry


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Scheduled chart automation for CEC-WAM'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=30,
        help='Minutes between automation runs (default: 30)'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run once and exit'
    )
    
    args = parser.parse_args()
    
    if args.once:
        logger.info("Running automation once...")
        automation = ChartAutomation()
        report = automation.run_full_automation()
        return 0 if report.get('status') == 'SUCCESS' else 1
    else:
        run_scheduled_automation(args.interval)
        return 0


if __name__ == '__main__':
    exit(main())
