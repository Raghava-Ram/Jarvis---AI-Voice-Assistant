#!/usr/bin/env python3
"""
AI Helper module for Jarvis using GitHub AI inference API with fallback
"""

import requests
import json
import random
from config import config

class AIHelper:
    def __init__(self):
        self.endpoint = config.get_api_key("github_endpoint") or "https://models.github.ai/inference"
        self.model = config.get_api_key("github_model") or "gpt-4o"
        self.token = config.get_api_key("github_token")
        
    def is_available(self):
        """Check if AI is available"""
        return bool(self.token)
    
    def get_fallback_response(self, user_message):
        """Get intelligent fallback response when AI is not available"""
        user_message_lower = user_message.lower()
        
        # Knowledge-based responses
        responses = {
            "hello": [
                "Hello! I'm Jarvis, your AI assistant. How can I help you today?",
                "Greetings! I'm here to assist you with various tasks.",
                "Hello there! I'm Jarvis, ready to help you!"
            ],
            "how are you": [
                "I'm functioning perfectly, thank you for asking! I'm always ready to help you.",
                "I'm doing great! My systems are running smoothly and I'm here to assist you.",
                "I'm excellent! I'm always ready to help you with whatever you need."
            ],
            "what can you do": [
                "I can help you with many things! I can open and close applications, search the web, take screenshots, control volume, get time and date, lock your computer, and chat with you. I'm also great at answering questions and having conversations!",
                "I'm your personal assistant! I can control your computer, search the web, manage applications, and have conversations with you. Just ask me what you need!",
                "I can assist you with computer tasks, web searches, system control, and general questions. I'm here to make your life easier!"
            ],
            "time": [
                "I can tell you the current time. Just say 'time' after my wake word!",
                "I can check the time for you. Try saying 'hey jarvis, time'!"
            ],
            "weather": [
                "I can help you find weather information. I can search the web for current weather conditions.",
                "I can search for weather information online for you. Just ask me to search for weather in your area!"
            ],
            "joke": [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "What do you call a fake noodle? An impasta!"
            ]
        }
        
        # Check for specific topics
        for topic, response_list in responses.items():
            if topic in user_message_lower:
                return random.choice(response_list)
        
        # General intelligent responses
        general_responses = [
            "That's an interesting question! I'm here to help you with various tasks and answer your questions.",
            "I'd be happy to help you with that! I can assist with computer tasks, searches, and general questions.",
            "I understand what you're asking. I'm here to help you with whatever you need!",
            "That's a great question! I'm your AI assistant and I'm here to help you with various tasks.",
            "I'm here to assist you! I can help with computer control, web searches, and answering questions."
        ]
        
        return random.choice(general_responses)
    
    def get_ai_response(self, user_message, context=""):
        """Get AI response from GitHub AI API or fallback"""
        if not self.is_available():
            return self.get_fallback_response(user_message)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            # Create system message for Jarvis personality
            system_message = """You are Jarvis, a helpful AI assistant inspired by Iron Man's AI. 
            You have a friendly, professional personality and speak naturally.
            You can help with various tasks, answer questions, and have conversations.
            Keep responses concise (2-3 sentences max) and speech-friendly. Be conversational and engaging."""
            
            if context:
                system_message += f"\n\nContext: {context}"
            
            payload = {
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.7,
                "top_p": 1,
                "model": self.model,
                "max_tokens": 100
            }
            
            response = requests.post(
                f"{self.endpoint}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                print(f"❌ AI API Error: {response.status_code}")
                print(f"Response: {response.text}")
                # Fallback to intelligent responses
                return self.get_fallback_response(user_message)
                
        except Exception as e:
            print(f"❌ AI API Error: {e}")
            # Fallback to intelligent responses
            return self.get_fallback_response(user_message)
    
    def test_connection(self):
        """Test the AI connection"""
        if not self.is_available():
            return False, "No API token configured"
        
        try:
            response = self.get_ai_response("Hello")
            if response and not response.startswith("❌"):
                return True, "AI connection successful"
            else:
                return False, "Using fallback responses"
        except Exception as e:
            return False, f"Connection error: {e}"

# Global AI helper instance
ai_helper = AIHelper() 