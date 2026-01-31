#!/usr/bin/env python3
"""
test_automation.py
------------------
Basic tests for the automation system.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing module imports...")
    
    try:
        import config
        print("  ✓ config")
    except Exception as e:
        print(f"  ❌ config: {e}")
        return False
    
    try:
        import logging_config
        print("  ✓ logging_config")
    except Exception as e:
        print(f"  ❌ logging_config: {e}")
        return False
    
    try:
        import slack_notifier
        print("  ✓ slack_notifier")
    except Exception as e:
        print(f"  ❌ slack_notifier: {e}")
        return False
    
    try:
        import grok_parser
        print("  ✓ grok_parser")
    except Exception as e:
        print(f"  ❌ grok_parser: {e}")
        return False
    
    try:
        import csv_operations
        print("  ✓ csv_operations")
    except Exception as e:
        print(f"  ❌ csv_operations: {e}")
        return False
    
    try:
        import google_sheets_sync
        print("  ✓ google_sheets_sync")
    except Exception as e:
        print(f"  ❌ google_sheets_sync: {e}")
        return False
    
    try:
        import eve_enhanced
        print("  ✓ eve_enhanced")
    except Exception as e:
        print(f"  ❌ eve_enhanced: {e}")
        return False
    
    try:
        import automation_main
        print("  ✓ automation_main")
    except Exception as e:
        print(f"  ❌ automation_main: {e}")
        return False
    
    return True


def test_config():
    """Test configuration."""
    print("\nTesting configuration...")
    
    try:
        from config import Config
        
        print(f"  DATA_DIR: {Config.DATA_DIR}")
        print(f"  EXPORTS_DIR: {Config.EXPORTS_DIR}")
        print(f"  LOGS_DIR: {Config.LOGS_DIR}")
        print(f"  CSV_FILES: {len(Config.CSV_FILES)} files configured")
        print(f"  EXCEL_FILES: {len(Config.EXCEL_FILES)} files configured")
        print(f"  ENABLE_SLACK_NOTIFICATIONS: {Config.ENABLE_SLACK_NOTIFICATIONS}")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_csv_operations():
    """Test CSV operations."""
    print("\nTesting CSV operations...")
    
    try:
        from csv_operations import CSVOperations
        import pandas as pd
        
        csv_ops = CSVOperations()
        
        # Create test CSV
        test_file = 'test_data.csv'
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'value': [100, 200, 300],
            'category': ['A', 'B', 'A']
        })
        df.to_csv(test_file, index=False)
        
        # Test get statistics
        stats = csv_ops.get_csv_statistics(test_file)
        assert stats['rows'] == 3, "Row count mismatch"
        assert stats['columns'] == 3, "Column count mismatch"
        print("  ✓ get_csv_statistics")
        
        # Clean up
        os.remove(test_file)
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        if os.path.exists('test_data.csv'):
            os.remove('test_data.csv')
        return False


def test_grok_parser():
    """Test Grok parser."""
    print("\nTesting Grok parser...")
    
    try:
        from grok_parser import GrokParser
        import pandas as pd
        
        grok = GrokParser()
        
        # Create test CSV
        test_file = 'test_grok.csv'
        df = pd.DataFrame({
            'timestamp': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'event': ['login', 'error', 'logout'],
            'user': ['alice', 'bob', 'charlie']
        })
        df.to_csv(test_file, index=False)
        
        # Test parse_csv_file
        insights = grok.parse_csv_file(test_file)
        assert 'statistics' in insights, "Missing statistics"
        assert insights['statistics']['rows'] == 3, "Row count mismatch"
        print("  ✓ parse_csv_file")
        
        # Clean up
        os.remove(test_file)
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        if os.path.exists('test_grok.csv'):
            os.remove('test_grok.csv')
        return False


def test_eve_enhanced():
    """Test EVE enhanced."""
    print("\nTesting EVE enhanced...")
    
    try:
        from eve_enhanced import EveEnhanced
        
        eve = EveEnhanced()
        
        # Test process_user_prompt
        response = eve.process_user_prompt("status")
        assert 'response' in response, "Missing response"
        assert 'EVE' in response['response'], "Invalid response"
        print("  ✓ process_user_prompt")
        
        # Test recommendations
        recommendations = eve.get_real_time_recommendations()
        assert isinstance(recommendations, list), "Recommendations should be a list"
        print("  ✓ get_real_time_recommendations")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("CEC-WAM-HOT-CORE Automation Tests")
    print("=" * 60)
    
    results = {
        'imports': test_imports(),
        'config': test_config(),
        'csv_operations': test_csv_operations(),
        'grok_parser': test_grok_parser(),
        'eve_enhanced': test_eve_enhanced()
    }
    
    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{test_name:20s}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("All tests passed!")
        return 0
    else:
        print("Some tests failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
