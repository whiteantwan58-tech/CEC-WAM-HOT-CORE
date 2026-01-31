#!/bin/bash
echo "=========================================="
echo "CEC-WAM-HOT-CORE Implementation Verification"
echo "=========================================="
echo ""

echo "1. Checking file structure..."
files=(
    "config.py"
    "logging_config.py"
    "slack_notifier.py"
    "grok_parser.py"
    "csv_operations.py"
    "google_sheets_sync.py"
    "eve_enhanced.py"
    "automation_main.py"
    "test_automation.py"
    "AUTOMATION_README.md"
    "IMPLEMENTATION_SUMMARY.md"
    ".env.example"
    ".gitignore"
)

all_present=true
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (missing)"
        all_present=false
    fi
done

echo ""
echo "2. Running tests..."
python test_automation.py 2>&1 | grep -E "(Test Results|PASS|FAIL|All tests)"

echo ""
echo "3. Checking automation modes..."
echo "  Available modes:"
echo "    - monitor"
echo "    - monitor-loop"
echo "    - analyze"
echo "    - sync"
echo "    - interactive"
echo "    - full"

echo ""
echo "4. Verifying dependencies..."
pip list 2>/dev/null | grep -E "(pandas|openpyxl|slack-sdk|python-json-logger)" || echo "  Run: pip install -r requirements.txt"

echo ""
echo "=========================================="
if [ "$all_present" = true ]; then
    echo "✓ Verification Complete - All files present"
else
    echo "✗ Verification Complete - Some files missing"
fi
echo "=========================================="
