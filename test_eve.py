#!/usr/bin/env python3
"""
EVE Voice AI Assistant - Demo Script
Tests EVE's capabilities without API keys (fallback mode)
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from eve_voice_agent import get_eve

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def main():
    """Run EVE demo"""
    
    print_header("EVE Voice AI Assistant Demo")
    print("System Code: CEC_WAM_HEI_EVE_7A2F-9C4B")
    print("Owner: Twan")
    print()
    
    # Initialize EVE
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
