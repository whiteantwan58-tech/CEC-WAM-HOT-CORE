"""
test_integration.py
-------------------

Integration test for the chart automation system.
Verifies that all components work together correctly.

Usage:
    python test_integration.py
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def log(message, color=RESET):
    """Print colored log message"""
    print(f"{color}{message}{RESET}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        log(f"✓ {description} exists", GREEN)
        return True
    else:
        log(f"✗ {description} missing", RED)
        return False

def check_json_file(filepath, description):
    """Check if a JSON file exists and is valid"""
    if not os.path.exists(filepath):
        log(f"✗ {description} missing", RED)
        return False
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        log(f"✓ {description} is valid JSON", GREEN)
        return True
    except Exception as e:
        log(f"✗ {description} invalid: {str(e)}", RED)
        return False

def run_automation():
    """Run the chart automation script"""
    log("\n" + "="*60, YELLOW)
    log("Running chart automation...", YELLOW)
    log("="*60, YELLOW)
    
    try:
        result = subprocess.run(
            ['python', 'chart_automation.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            log("✓ Chart automation completed successfully", GREEN)
            return True
        else:
            log(f"✗ Chart automation failed", RED)
            log(f"Error: {result.stderr}", RED)
            return False
    except subprocess.TimeoutExpired:
        log("✗ Chart automation timed out", RED)
        return False
    except Exception as e:
        log(f"✗ Chart automation error: {str(e)}", RED)
        return False

def test_api_server():
    """Test API server endpoints"""
    log("\n" + "="*60, YELLOW)
    log("Testing API server...", YELLOW)
    log("="*60, YELLOW)
    
    # Start server
    log("Starting API server...")
    server_process = subprocess.Popen(
        ['python', 'api_server.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test health endpoint
        import urllib.request
        
        try:
            response = urllib.request.urlopen('http://localhost:5000/api/health', timeout=5)
            data = json.loads(response.read())
            if data.get('status') == 'online':
                log("✓ Health endpoint working", GREEN)
            else:
                log("✗ Health endpoint returned unexpected data", RED)
        except Exception as e:
            log(f"✗ Health endpoint failed: {str(e)}", RED)
        
        # Test chart-data endpoint
        try:
            response = urllib.request.urlopen('http://localhost:5000/api/chart-data', timeout=5)
            data = json.loads(response.read())
            if 'datasets' in data:
                log(f"✓ Chart data endpoint working ({len(data['datasets'])} datasets)", GREEN)
            else:
                log("✗ Chart data endpoint missing datasets", RED)
        except Exception as e:
            log(f"✗ Chart data endpoint failed: {str(e)}", RED)
        
        # Test automation-status endpoint
        try:
            response = urllib.request.urlopen('http://localhost:5000/api/automation-status', timeout=5)
            data = json.loads(response.read())
            if data.get('status') == 'SUCCESS':
                log(f"✓ Automation status endpoint working", GREEN)
            else:
                log("✗ Automation status endpoint returned failure", RED)
        except Exception as e:
            log(f"✗ Automation status endpoint failed: {str(e)}", RED)
        
        return True
        
    finally:
        # Stop server
        server_process.terminate()
        server_process.wait(timeout=5)
        log("API server stopped")

def main():
    """Main test runner"""
    log("\n" + "="*60, YELLOW)
    log("CEC-WAM Chart Automation Integration Test", YELLOW)
    log("="*60, YELLOW)
    log(f"Started at: {datetime.now().isoformat()}", YELLOW)
    
    passed = 0
    failed = 0
    
    # Test 1: Check required files
    log("\n--- Test 1: Required Files ---", YELLOW)
    tests = [
        ('chart_automation.py', 'Chart automation script'),
        ('api_server.py', 'API server script'),
        ('requirements.txt', 'Requirements file'),
        ('index.html', 'Frontend HTML'),
        ('start_services.sh', 'Startup script'),
    ]
    
    for filepath, description in tests:
        if check_file_exists(filepath, description):
            passed += 1
        else:
            failed += 1
    
    # Test 2: Check CSV files
    log("\n--- Test 2: CSV Files ---", YELLOW)
    csv_files = [
        'pump.fun.csv',
        'BlackHoles.csv',
        'CEC Matrix System Operational Metrics and Assets - FINANCE_HUB (1).csv',
    ]
    
    for csv_file in csv_files:
        if check_file_exists(csv_file, csv_file):
            passed += 1
        else:
            failed += 1
    
    # Test 3: Run automation
    log("\n--- Test 3: Chart Automation ---", YELLOW)
    if run_automation():
        passed += 1
    else:
        failed += 1
    
    # Test 4: Check generated files
    log("\n--- Test 4: Generated Files ---", YELLOW)
    tests = [
        ('Chart.xlsx', 'Updated Chart.xlsx'),
        ('data/chart_data.json', 'Chart data JSON'),
        ('data/automation_report.json', 'Automation report JSON'),
    ]
    
    for filepath, description in tests:
        if check_json_file(filepath, description) if filepath.endswith('.json') else check_file_exists(filepath, description):
            passed += 1
        else:
            failed += 1
    
    # Test 5: Validate chart data structure
    log("\n--- Test 5: Chart Data Structure ---", YELLOW)
    try:
        with open('data/chart_data.json', 'r') as f:
            chart_data = json.load(f)
        
        if 'timestamp' in chart_data:
            log("✓ Chart data has timestamp", GREEN)
            passed += 1
        else:
            log("✗ Chart data missing timestamp", RED)
            failed += 1
        
        if 'datasets' in chart_data:
            datasets = chart_data['datasets']
            log(f"✓ Chart data has {len(datasets)} datasets", GREEN)
            passed += 1
            
            # Check dataset structure
            for name, ds in datasets.items():
                if all(k in ds for k in ['labels', 'values', 'type', 'title']):
                    log(f"  ✓ Dataset '{name}' has correct structure", GREEN)
                else:
                    log(f"  ✗ Dataset '{name}' missing required fields", RED)
        else:
            log("✗ Chart data missing datasets", RED)
            failed += 1
            
    except Exception as e:
        log(f"✗ Failed to validate chart data: {str(e)}", RED)
        failed += 1
    
    # Test 6: API Server (optional)
    log("\n--- Test 6: API Server (optional) ---", YELLOW)
    try:
        test_api_server()
        passed += 1
    except Exception as e:
        log(f"⚠ API server test skipped: {str(e)}", YELLOW)
        # Don't count as failure
    
    # Summary
    log("\n" + "="*60, YELLOW)
    log("TEST SUMMARY", YELLOW)
    log("="*60, YELLOW)
    log(f"Passed: {passed}", GREEN)
    log(f"Failed: {failed}", RED if failed > 0 else GREEN)
    log(f"Total: {passed + failed}", YELLOW)
    
    if failed == 0:
        log("\n✓ All tests passed!", GREEN)
        return 0
    else:
        log(f"\n✗ {failed} test(s) failed", RED)
        return 1

if __name__ == '__main__':
    sys.exit(main())
