import os
import json
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("   Environment variables will be loaded from system only.")

class Config:
    def __init__(self):
        self.config_file = Path("jarvis_config.json")
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file or create default"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.get_default_config()
        else:
            return self.get_default_config()
    
    def get_default_config(self):
        """Get default configuration"""
        return {
            "github_endpoint": "https://models.github.ai/inference",
            "github_model": "gpt-4o",
            "weather_api_key": "",
            "news_api_key": "",
            "voice_settings": {
                "rate": 170,
                "volume": 0.9
            }
        }
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            print("✅ Configuration saved successfully!")
        except Exception as e:
            print(f"❌ Error saving config: {e}")
    
    def get_api_key(self, key_name):
        """Get API key from environment or config"""
        # Map key names to environment variable names
        env_mapping = {
            "github_token": "GITHUB_AI_TOKEN",
            "weather_api_key": "WEATHER_API_KEY",
            "news_api_key": "NEWS_API_KEY"
        }
        
        # First try environment variable
        env_key = env_mapping.get(key_name, f"{key_name.upper()}")
        env_value = os.getenv(env_key)
        if env_value:
            return env_value
        
        # Fallback to config file
        return self.config.get(key_name, "")
    
    def set_api_key(self, key_name, value):
        """Set API key in config (for non-env keys)"""
        self.config[key_name] = value
        self.save_config()
    
    def has_api_key(self, key_name):
        """Check if API key exists in env or config"""
        return bool(self.get_api_key(key_name))

# Global config instance
config = Config() 