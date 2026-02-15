"""
EVE Voice AI - Voice Synthesis API Endpoint
Serverless function for Vercel deployment
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import base64

# Add parent directory to path to import eve_voice_agent
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from eve_voice_agent import get_eve
except ImportError:
    get_eve = None


class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler for voice synthesis"""
    
    def _set_cors_headers(self):
        """Set CORS headers for cross-origin requests"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_OPTIONS(self):
        """Handle preflight OPTIONS request"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_POST(self):
        """Handle POST request for voice synthesis"""
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Get text to synthesize
            text = data.get('text', '')
            
            if not text:
                self.send_response(400)
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": "No text provided"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Get EVE instance and generate speech
            if get_eve is None:
                audio_data = None
            else:
                eve = get_eve()
                audio_data = eve.speak(text)
            
            # Send response
            if audio_data:
                # Encode audio as base64 for JSON transport
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                
                self.send_response(200)
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                response = {
                    "success": True,
                    "text": text,
                    "audio": audio_base64,
                    "format": "mp3"
                }
                
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(503)
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                response = {
                    "success": False,
                    "error": "Voice synthesis not available. Please check ElevenLabs API configuration."
                }
                
                self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self._set_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                "success": False,
                "error": str(e)
            }
            
            self.wfile.write(json.dumps(response).encode())
