"""
EVE Voice AI - Chat API Endpoint
Serverless function for Vercel deployment
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Add parent directory to path to import eve_voice_agent
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from eve_voice_agent import get_eve
except ImportError:
    get_eve = None


class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler"""
    
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
        """Handle POST request for chat"""
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Get user message
            user_message = data.get('message', '')
            include_history = data.get('include_history', True)
            
            if not user_message:
                self.send_response(400)
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": "No message provided"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Get EVE instance and process message
            if get_eve is None:
                response_text = "EVE is not available. Please check server configuration."
            else:
                eve = get_eve()
                response_text = eve.chat(user_message, include_history=include_history)
            
            # Send response
            self.send_response(200)
            self._set_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                "success": True,
                "message": user_message,
                "response": response_text,
                "timestamp": "now"
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
    
    def do_GET(self):
        """Handle GET request for status"""
        try:
            if get_eve is None:
                status = {"status": "EVE not available"}
            else:
                eve = get_eve()
                status = eve.get_status()
            
            self.send_response(200)
            self._set_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            self.wfile.write(json.dumps(status).encode())
            
        except Exception as e:
            self.send_response(500)
            self._set_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {"error": str(e)}
            self.wfile.write(json.dumps(response).encode())
