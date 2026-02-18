#!/usr/bin/env python3
"""
EVE Voice AI Assistant - Demo & Test Script
Tests EVE's capabilities and validates API configurations
"""

import sys
import os
import requests
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ Environment variables loaded from .env")
except ImportError:
    print("ℹ️  python-dotenv not installed, using system environment variables")

from eve_voice_agent import get_eve

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def test_api_configurations():
    """Test all API configurations"""
    print_header("API Configuration Tests")
    
    results = {
        'passed': 0,
        'failed': 0,
        'skipped': 0
    }
    
    # Test NASA API
    print("🛰️  Testing NASA API...")
    nasa_key = os.getenv('NASA_API_KEY', 'DEMO_KEY')
    try:
        url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_key}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"  ✓ NASA API: Connected (using {'DEMO_KEY' if nasa_key == 'DEMO_KEY' else 'custom key'})")
            if nasa_key == 'DEMO_KEY':
                print("    ⚠️  Using DEMO_KEY - has rate limits, get your own at https://api.nasa.gov/")
            results['passed'] += 1
        else:
            print(f"  ✗ NASA API: Failed (status {response.status_code})")
            results['failed'] += 1
    except Exception as e:
        print(f"  ✗ NASA API: Error - {str(e)}")
        results['failed'] += 1
    
    # Test NOAA Weather API
    print("\n🌦️  Testing NOAA Weather API...")
    try:
        url = "https://api.weather.gov/alerts/active"
        headers = {
            'User-Agent': '(EVE-System-Test, test@evesystem.com)',
            'Accept': 'application/geo+json'
        }
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            print("  ✓ NOAA Weather API: Connected (no key required)")
            results['passed'] += 1
        else:
            print(f"  ✗ NOAA Weather API: Failed (status {response.status_code})")
            results['failed'] += 1
    except Exception as e:
        print(f"  ✗ NOAA Weather API: Error - {str(e)}")
        results['failed'] += 1
    
    # Test OpenWeatherMap API
    print("\n⛅ Testing OpenWeatherMap API...")
    openweather_key = os.getenv('OPENWEATHER_API_KEY', '')
    if openweather_key:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q=Seattle&appid={openweather_key}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("  ✓ OpenWeatherMap API: Connected")
                results['passed'] += 1
            else:
                print(f"  ✗ OpenWeatherMap API: Failed (status {response.status_code})")
                results['failed'] += 1
        except Exception as e:
            print(f"  ✗ OpenWeatherMap API: Error - {str(e)}")
            results['failed'] += 1
    else:
        print("  ⊘ OpenWeatherMap API: Not configured (optional)")
        print("    Get free key at: https://openweathermap.org/api")
        results['skipped'] += 1
    
    # Test ElevenLabs API
    print("\n🗣️  Testing ElevenLabs API...")
    elevenlabs_key = os.getenv('ELEVENLABS_API_KEY', '')
    if elevenlabs_key:
        try:
            # Test with voices endpoint
            url = "https://api.elevenlabs.io/v1/voices"
            headers = {"xi-api-key": elevenlabs_key}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                print("  ✓ ElevenLabs API: Connected")
                results['passed'] += 1
            else:
                print(f"  ✗ ElevenLabs API: Failed (status {response.status_code})")
                results['failed'] += 1
        except Exception as e:
            print(f"  ✗ ElevenLabs API: Error - {str(e)}")
            results['failed'] += 1
    else:
        print("  ⊘ ElevenLabs API: Not configured")
        print("    Required for voice synthesis - Get key at: https://elevenlabs.io/")
        results['skipped'] += 1
    
    # Test OpenAI API
    print("\n🤖 Testing OpenAI API...")
    openai_key = os.getenv('OPENAI_API_KEY', '')
    if openai_key:
        try:
            # Test with models endpoint
            url = "https://api.openai.com/v1/models"
            headers = {"Authorization": f"Bearer {openai_key}"}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                print("  ✓ OpenAI API: Connected")
                results['passed'] += 1
            else:
                print(f"  ✗ OpenAI API: Failed (status {response.status_code})")
                results['failed'] += 1
        except Exception as e:
            print(f"  ✗ OpenAI API: Error - {str(e)}")
            results['failed'] += 1
    else:
        print("  ⊘ OpenAI API: Not configured")
        print("    Required for AI chat - Get key at: https://platform.openai.com/api-keys")
        results['skipped'] += 1
    
    # Test Google Sheets (public CSV)
    print("\n📊 Testing Google Sheets Data Feed...")
    try:
        url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vREgUUHPCzTBWK8i1PWBrE2E4pKRTAgaReJahFqmrTetCZyCO0QHVlAleodUsTlJv_86KpzH_NPv9dv/pub?output=csv"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("  ✓ Google Sheets CSV: Accessible")
            results['passed'] += 1
        else:
            print(f"  ✗ Google Sheets CSV: Failed (status {response.status_code})")
            results['failed'] += 1
    except Exception as e:
        print(f"  ✗ Google Sheets CSV: Error - {str(e)}")
        results['failed'] += 1
    
    # Print summary
    print_header("API Test Summary")
    total = results['passed'] + results['failed'] + results['skipped']
    print(f"  Total Tests: {total}")
    print(f"  ✓ Passed: {results['passed']}")
    print(f"  ✗ Failed: {results['failed']}")
    print(f"  ⊘ Skipped: {results['skipped']}")
    
    if results['failed'] > 0:
        print("\n  ⚠️  Some APIs failed - check your .env configuration")
    elif results['skipped'] > 0:
        print("\n  ℹ️  Some APIs not configured - app will use fallback data")
    else:
        print("\n  🎉 All configured APIs are working!")
    
    return results

def main():
    """Run EVE demo and tests"""
    
    print_header("EVE Voice AI Assistant - Test Suite")
    print("System Code: CEC_WAM_HEI_EVE_7A2F-9C4B")
    print("Owner: Twan")
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run API configuration tests first
    test_results = test_api_configurations()
    
    # Initialize EVE
    print_header("EVE Initialization")
    print("Initializing EVE...")
    eve = get_eve()
    print("✓ EVE initialized successfully!\n")
    
    # Display EVE Status
    print_header("EVE Status")
    status = eve.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Test Calculations
    print_header("Testing Math Calculations")
    
    calculations = [
        "25 * 4",
        "100 + 50 * 2",
        "(10 + 5) * 3",
        "pow(2, 8)",
        "max(100, 200, 150)"
    ]
    
    for calc in calculations:
        result = eve.calculate(calc)
        print(f"  {calc} = {result}")
    
    # Test CEC WAM Data Access
    print_header("CEC WAM System Data")
    cec_data = eve.get_cec_wam_data()
    print("  System Data Retrieved:")
    for key, value in cec_data.items():
        print(f"    {key}: {value}")
    
    # Test Chat (without API keys, will show availability message)
    print_header("Testing Chat Function")
    
    test_messages = [
        "Hello EVE!",
        "What can you help me with?",
        "Tell me about the CEC-WAM system"
    ]
    
    for message in test_messages:
        print(f"\n  User: {message}")
        response = eve.chat(message, include_history=False)
        print(f"  EVE:  {response[:100]}...")
    
    # Show Conversation Count
    print_header("Conversation Statistics")
    print(f"  Total conversations: {len(eve.conversation_history) // 2}")
    print(f"  Total logs: {len(eve.logs)}")
    
    # Show Recent Logs
    print_header("Recent Activity Logs")
    recent_logs = eve.get_logs(limit=5)
    for log in recent_logs:
        print(f"  [{log['level'].upper()}] {log['message']}")
    
    # Show Capabilities
    print_header("EVE Capabilities")
    for capability in eve.capabilities:
        print(f"  ✓ {capability.replace('_', ' ').title()}")
    
    # API Configuration Status
    print_header("API Configuration Status")
    
    config_status = {
        "ElevenLabs (Voice)": "✓ Configured" if eve.elevenlabs_ready else "✗ Not configured (needs API key)",
        "OpenAI (Chat AI)": "✓ Configured" if eve.openai_ready else "✗ Not configured (needs API key)",
        "Voice Synthesis": "Ready" if eve.elevenlabs_ready else "Unavailable",
        "AI Chat": "Ready" if eve.openai_ready else "Unavailable"
    }
    
    for feature, status in config_status.items():
        print(f"  {feature}: {status}")
    
    if not eve.elevenlabs_ready or not eve.openai_ready:
        print("\n  Note: To enable all features, add API keys to .env file:")
        if not eve.elevenlabs_ready:
            print("    - ELEVENLABS_API_KEY (for voice synthesis)")
        if not eve.openai_ready:
            print("    - OPENAI_API_KEY (for AI chat)")
    
    print_header("Demo Complete")
    print("EVE is ready to assist you 24/7!")
    print("\nTo use EVE in the dashboard:")
    print("  1. Configure API keys in .env file")
    print("  2. Run: streamlit run app.py")
    print("  3. Navigate to 'EVE Voice AI' tab")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        sys.exit(1)
