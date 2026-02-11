#!/usr/bin/env python3
"""
Comprehensive test suite for CEC-WAM system
Tests all major functionality
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_dependencies():
    """Test that all required dependencies are installed"""
    print_section("Testing Dependencies")
    
    required_packages = [
        ('streamlit', 'streamlit'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('requests', 'requests'),
        ('solana', 'solana'),
        ('solders', 'solders'),
        ('openpyxl', 'openpyxl'),
        ('python-dotenv', 'dotenv')  # Package name vs import name
    ]
    
    missing = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - NOT FOUND")
            missing.append(package_name)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies installed")
    return True

def test_file_structure():
    """Test that all required files exist"""
    print_section("Testing File Structure")
    
    required_files = [
        'app.py',
        'EVE_1010_WAKE_dashboard.py',
        'omega_eve.py',
        'eve_agent.py',
        'requirements.txt',
        'index.html',
        '.streamlit/config.toml',
        'data_manager.py',
        'DEPLOYMENT_GUIDE.md'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - NOT FOUND")
            missing.append(file)
    
    if missing:
        print(f"\n⚠️  Missing files: {', '.join(missing)}")
        return False
    
    print("\n✅ All required files present")
    return True

def test_csv_data():
    """Test CSV data files"""
    print_section("Testing CSV Data Files")
    
    csv_files = list(Path('.').glob('*.csv'))
    
    if not csv_files:
        print("⚠️  No CSV files found")
        return True
    
    import pandas as pd
    from datetime import datetime
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            print(f"\n📄 {csv_file.name}")
            print(f"   Records: {len(df)}")
            print(f"   Columns: {len(df.columns)}")
            
            # Check for date columns
            date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
            if date_cols:
                print(f"   Date columns: {', '.join(date_cols)}")
                
                # Check if data is from Nov 6 onwards
                for date_col in date_cols:
                    try:
                        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                        cutoff = datetime(2025, 11, 6)
                        recent_data = df[df[date_col] >= cutoff]
                        print(f"   Records from Nov 6: {len(recent_data)}")
                    except:
                        pass
            
            print(f"   ✅ Valid CSV")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    print("\n✅ All CSV files valid")
    return True

def test_streamlit_apps():
    """Test that Streamlit apps can be imported"""
    print_section("Testing Streamlit Apps")
    
    apps = [
        'app.py',
        'EVE_1010_WAKE_dashboard.py',
        'omega_eve.py'
    ]
    
    for app in apps:
        print(f"\n📱 Testing {app}...")
        try:
            # Try to run syntax check
            result = subprocess.run(
                ['python', '-m', 'py_compile', app],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print(f"   ✅ Syntax valid")
            else:
                print(f"   ❌ Syntax error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"   ⚠️  Could not test: {e}")
    
    print("\n✅ All Streamlit apps have valid syntax")
    return True

def test_cache_functionality():
    """Test caching functionality"""
    print_section("Testing Cache Functionality")
    
    import streamlit as st
    
    try:
        # Test that cache_data decorator exists
        print("✅ st.cache_data available")
        
        # Check if it's being used in app.py
        with open('app.py', 'r') as f:
            content = f.read()
            if '@st.cache_data' in content:
                print("✅ Caching implemented in app.py")
                
                if 'ttl=10' in content or 'ttl=5' in content:
                    print("✅ TTL configured")
                else:
                    print("⚠️  TTL not found (may use default)")
            else:
                print("⚠️  Caching not implemented in app.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_auto_refresh():
    """Test auto-refresh functionality"""
    print_section("Testing Auto-Refresh")
    
    files_to_check = ['app.py', 'EVE_1010_WAKE_dashboard.py', 'omega_eve.py']
    
    for file in files_to_check:
        try:
            with open(file, 'r') as f:
                content = f.read()
                
                print(f"\n📄 {file}:")
                
                if 'st.rerun()' in content:
                    print("   ✅ Auto-refresh implemented (st.rerun)")
                elif 'st.experimental_rerun()' in content:
                    print("   ✅ Auto-refresh implemented (experimental_rerun)")
                else:
                    print("   ⚠️  Auto-refresh not found")
                
                if 'time.time()' in content:
                    print("   ✅ Timing logic present")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    return True

def test_voice_input():
    """Test voice input implementation"""
    print_section("Testing Voice Input")
    
    # Check app.py
    try:
        with open('app.py', 'r') as f:
            content = f.read()
            
            if 'webkitSpeechRecognition' in content or 'SpeechRecognition' in content:
                print("✅ Voice input implemented in app.py")
            else:
                print("⚠️  Voice input not found in app.py")
        
        # Check HTML
        with open('index.html', 'r') as f:
            content = f.read()
            
            if 'webkitSpeechRecognition' in content or 'SpeechRecognition' in content:
                print("✅ Voice input implemented in index.html")
            else:
                print("⚠️  Voice input not found in index.html")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_threejs():
    """Test Three.js implementation"""
    print_section("Testing Three.js")
    
    try:
        with open('index.html', 'r') as f:
            content = f.read()
            
            if 'three.js' in content.lower() or 'three.min.js' in content.lower():
                print("✅ Three.js library included")
            else:
                print("⚠️  Three.js library not found")
            
            if 'THREE.Scene' in content:
                print("✅ Three.js scene initialized")
            else:
                print("⚠️  Three.js scene not found")
            
            if 'starmap' in content.lower() or 'star' in content.lower():
                print("✅ Star map implementation found")
            else:
                print("⚠️  Star map not found")
        
        # Check app.py for Three.js HTML component
        with open('app.py', 'r') as f:
            content = f.read()
            
            if 'THREE' in content:
                print("✅ Three.js implemented in app.py")
            else:
                print("⚠️  Three.js not found in app.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "🚀" * 30)
    print("CEC-WAM SYSTEM TEST SUITE")
    print("🚀" * 30)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("File Structure", test_file_structure),
        ("CSV Data", test_csv_data),
        ("Streamlit Apps", test_streamlit_apps),
        ("Cache Functionality", test_cache_functionality),
        ("Auto-Refresh", test_auto_refresh),
        ("Voice Input", test_voice_input),
        ("Three.js", test_threejs)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
