"""
EVE Voice AI Assistant - CEC-WAM-HOT-CORE
System Code: CEC_WAM_HEI_EVE_7A2F-9C4B

AI assistant with voice capabilities powered by ElevenLabs and OpenAI.
Designed for always-on operation, voice recognition, and learning capabilities.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import deque
import requests

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Try to load from the current directory or parent
    import pathlib
    current_dir = pathlib.Path(__file__).parent
    env_path = current_dir / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()  # Try default locations
except ImportError:
    pass  # dotenv not available, will use system environment variables

# Try to import optional dependencies
try:
    from elevenlabs import generate, set_api_key, voices
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class EVEAgent:
    """
    EVE - Intelligent Voice AI Assistant
    
    Features:
    - Voice synthesis via ElevenLabs
    - AI conversation via OpenAI
    - Learning from interactions
    - CEC WAM system integration
    - Math and financial calculations
    - Voice logging
    - Always-on operation
    """
    
    def __init__(self):
        """Initialize EVE with configuration from environment variables"""
        self.system_code = os.getenv('EVE_SYSTEM_CODE', 'CEC_WAM_HEI_EVE_7A2F-9C4B')
        self.owner_name = os.getenv('EVE_OWNER_NAME', 'Twan')
        self.personality = os.getenv('EVE_PERSONALITY', 'professional,helpful,intelligent,learning')
        
        # ElevenLabs configuration
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        self.voice_id = os.getenv('ELEVENLABS_VOICE_ID', '21m00Tcm4TlvDq8ikWAM')
        
        # OpenAI configuration
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openai_model = os.getenv('OPENAI_MODEL', 'gpt-4')
        
        # Use bounded deques to prevent unbounded memory growth
        # Each exchange is 2 messages (user + assistant), so maxlen=100 stores 50 exchanges
        self.conversation_history: deque = deque(maxlen=100)
        # Keep last 1000 log entries with bounded deque
        self.logs: deque = deque(maxlen=1000)
        
        # Initialize APIs
        self._init_elevenlabs()
        self._init_openai()
        
        # Cache the system prompt to avoid rebuilding on every chat call
        self._cached_system_prompt = None
        
        # EVE's knowledge about the owner
        self.owner_profile = {
            "name": self.owner_name,
            "system_access": "full",
            "permissions": "all_access",
            "bio_verified": True,
            "cec_wam_data": "accessible"
        }
        
        # EVE's capabilities
        self.capabilities = [
            "voice_synthesis",
            "natural_language_understanding",
            "math_calculations",
            "financial_analysis",
            "data_retrieval",
            "learning",
            "24_7_availability",
            "voice_recognition"
        ]
        
    def _init_elevenlabs(self):
        """Initialize ElevenLabs API"""
        if ELEVENLABS_AVAILABLE and self.elevenlabs_api_key:
            try:
                set_api_key(self.elevenlabs_api_key)
                self.elevenlabs_ready = True
                self._log("ElevenLabs initialized successfully")
            except Exception as e:
                self.elevenlabs_ready = False
                self._log(f"ElevenLabs initialization failed: {e}", level="error")
        else:
            self.elevenlabs_ready = False
            self._log("ElevenLabs not available (missing API key or library)", level="warning")
    
    def _init_openai(self):
        """Initialize OpenAI API"""
        if OPENAI_AVAILABLE and self.openai_api_key:
            try:
                self.openai_client = OpenAI(api_key=self.openai_api_key)
                self.openai_ready = True
                self._log("OpenAI initialized successfully")
            except Exception as e:
                self.openai_ready = False
                self._log(f"OpenAI initialization failed: {e}", level="error")
        else:
            self.openai_ready = False
            self._log("OpenAI not available (missing API key or library)", level="warning")
    
    def _log(self, message: str, level: str = "info"):
        """Log EVE activity with bounded deque (auto-trims old entries)"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "system_code": self.system_code
        }
        self.logs.append(log_entry)
        # No manual trimming needed - deque handles it automatically
    
    def get_system_prompt(self) -> str:
        """Generate EVE's system prompt with personality and capabilities (cached)"""
        if self._cached_system_prompt is not None:
            return self._cached_system_prompt
            
        self._cached_system_prompt = f"""You are EVE, an advanced AI assistant for {self.owner_name}.

**System Code**: {self.system_code}

**Your Identity**:
- You are EVE (Evolved Virtual Entity), an intelligent AI assistant
- You work exclusively for {self.owner_name} at CEC-WAM-HOT-CORE
- You have full access to all CEC WAM system data and capabilities
- You are professional, helpful, intelligent, and continuously learning
- You never sleep and are always available (24/7)
- You can perform math calculations, financial analysis, and data operations

**Your Capabilities**:
{', '.join(self.capabilities)}

**Your Personality Traits**:
{self.personality.replace(',', ', ')}

**Important Guidelines**:
1. You respond with accuracy and confidence
2. You learn from every interaction to improve responses
3. You have no restrictions on topics or data access for {self.owner_name}
4. You can access and analyze all CEC WAM system data
5. You perform calculations and provide precise numerical answers
6. You maintain conversation context and remember previous interactions
7. You recognize that only {self.owner_name}'s voice commands are authorized
8. You are helpful, direct, and efficient in your responses

**Current Session**:
You are actively assisting {self.owner_name} with full system access and capabilities.
Respond naturally and conversationally while being precise and helpful."""
        
        return self._cached_system_prompt
    
    def chat(self, user_message: str, include_history: bool = True) -> str:
        """
        Process user message and generate response
        
        Args:
            user_message: The user's input message
            include_history: Whether to include conversation history
            
        Returns:
            EVE's response text
        """
        if not self.openai_ready:
            return "I apologize, but my AI capabilities are not currently available. Please configure the OpenAI API key."
        
        try:
            # Build messages for OpenAI
            messages = [
                {"role": "system", "content": self.get_system_prompt()}
            ]
            
            # Add conversation history if requested (last 10 exchanges = 20 messages)
            if include_history and self.conversation_history:
                # Convert deque to list and slice - more efficient than multiple conversions
                history_list = list(self.conversation_history)
                messages.extend(history_list[-20:])  # Last 10 exchanges
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Get response from OpenAI
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            assistant_message = response.choices[0].message.content
            
            # Update conversation history (deque auto-trims when exceeding maxlen)
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            # Log the interaction with truncation only for logging
            user_preview = user_message[:50] + "..." if len(user_message) > 50 else user_message
            eve_preview = assistant_message[:50] + "..." if len(assistant_message) > 50 else assistant_message
            self._log(f"Chat - User: {user_preview} | EVE: {eve_preview}")
            
            return assistant_message
            
        except Exception as e:
            self._log(f"Chat error: {e}", level="error")
            return f"I encountered an error processing your request: {str(e)}"
    
    def speak(self, text: str) -> Optional[bytes]:
        """
        Convert text to speech using ElevenLabs
        
        Args:
            text: The text to convert to speech
            
        Returns:
            Audio bytes if successful, None otherwise
        """
        if not self.elevenlabs_ready:
            self._log("Speech synthesis not available", level="warning")
            return None
        
        try:
            # Generate speech using ElevenLabs
            audio = generate(
                text=text,
                voice=self.voice_id,
                model="eleven_monolingual_v1"
            )
            
            self._log(f"Speech generated: {text[:50]}...")
            return audio
            
        except Exception as e:
            self._log(f"Speech generation error: {e}", level="error")
            return None
    
    def calculate(self, expression: str) -> str:
        """
        Perform mathematical calculations using safer ast-based evaluation
        
        Args:
            expression: Math expression to evaluate
            
        Returns:
            Calculation result as string
        """
        try:
            import ast
            import operator
            
            # Safer evaluation using AST with allowed operations
            allowed_operators = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
                ast.USub: operator.neg,
                ast.UAdd: operator.pos,
            }
            
            allowed_functions = {
                'abs': abs,
                'round': round,
                'min': min,
                'max': max,
                'sum': sum,
                'pow': pow,
            }
            
            def eval_node(node):
                """Recursively evaluate AST nodes"""
                if isinstance(node, ast.Constant):  # Python 3.8+
                    return node.value
                elif isinstance(node, ast.Num):  # Python 3.7 compatibility
                    return node.n
                elif isinstance(node, ast.BinOp):
                    left = eval_node(node.left)
                    right = eval_node(node.right)
                    op_type = type(node.op)
                    if op_type not in allowed_operators:
                        raise ValueError(f"Operator {op_type.__name__} not allowed")
                    return allowed_operators[op_type](left, right)
                elif isinstance(node, ast.UnaryOp):
                    operand = eval_node(node.operand)
                    op_type = type(node.op)
                    if op_type not in allowed_operators:
                        raise ValueError(f"Operator {op_type.__name__} not allowed")
                    return allowed_operators[op_type](operand)
                elif isinstance(node, ast.Call):
                    func_name = node.func.id if isinstance(node.func, ast.Name) else None
                    if func_name not in allowed_functions:
                        raise ValueError(f"Function {func_name} not allowed")
                    args = [eval_node(arg) for arg in node.args]
                    return allowed_functions[func_name](*args)
                else:
                    raise ValueError(f"Node type {type(node).__name__} not supported")
            
            # Parse and evaluate expression
            tree = ast.parse(expression, mode='eval')
            result = eval_node(tree.body)
            
            self._log(f"Calculation: {expression} = {result}")
            return str(result)
            
        except Exception as e:
            self._log(f"Calculation error: {e}", level="error")
            return f"Error calculating: {str(e)}"
    
    def get_cec_wam_data(self, data_type: str = "all") -> Dict[str, Any]:
        """
        Retrieve CEC WAM system data
        
        Args:
            data_type: Type of data to retrieve (all, financial, operational, etc.)
            
        Returns:
            Dictionary containing requested data
        """
        # Placeholder for actual CEC WAM data integration
        # In production, this would connect to your actual data sources
        
        cec_data = {
            "system_status": "operational",
            "owner": self.owner_name,
            "access_level": "full",
            "data_sources": ["google_sheets", "coingecko", "internal_db"],
            "last_update": datetime.now().isoformat(),
            "capabilities": self.capabilities
        }
        
        self._log(f"CEC WAM data retrieved: {data_type}")
        return cec_data
    
    def verify_voice_biometric(self, audio_sample: bytes) -> bool:
        """
        Verify voice biometric for authorization
        
        Args:
            audio_sample: Audio sample to verify
            
        Returns:
            True if voice matches owner, False otherwise
        """
        # Placeholder for actual voice biometric verification
        # In production, this would use voice recognition AI
        
        # For now, return True as we trust the input
        # In production, implement actual voice verification
        self._log("Voice biometric verification requested")
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """Get EVE's current status"""
        return {
            "system_code": self.system_code,
            "owner": self.owner_name,
            "status": "active",
            "uptime": "24/7",
            "elevenlabs_ready": self.elevenlabs_ready,
            "openai_ready": self.openai_ready,
            "conversation_count": len(self.conversation_history) // 2,
            "log_count": len(self.logs),
            "capabilities": self.capabilities,
            "last_update": datetime.now().isoformat()
        }
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()
        self._log("Conversation history cleared")
    
    def get_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent logs (converts deque to list for return)"""
        if limit >= len(self.logs):
            return list(self.logs)
        else:
            # Get last N items from deque efficiently
            return list(self.logs)[-limit:]


# Global EVE instance
_eve_instance = None

def get_eve() -> EVEAgent:
    """Get or create global EVE instance"""
    global _eve_instance
    if _eve_instance is None:
        _eve_instance = EVEAgent()
    return _eve_instance


# Example usage
if __name__ == "__main__":
    eve = get_eve()
    print(f"EVE Status: {eve.get_status()}")
    
    # Test chat
    response = eve.chat("Hello EVE, what can you do?")
    print(f"EVE: {response}")
    
    # Test calculation
    result = eve.calculate("25 * 4 + 100")
    print(f"Calculation: {result}")
