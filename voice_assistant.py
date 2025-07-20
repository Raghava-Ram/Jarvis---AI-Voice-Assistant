import threading
import time
import subprocess
import os
import webbrowser
import datetime
import json
import random
from typing import Dict, Callable, Any

# Speech recognition and text-to-speech imports
import speech_recognition as sr
import pyttsx3

# AI integration
from ai_helper import ai_helper

class JarvisAssistant:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
        # Wake word
        self.wake_word = "hey jarvis"
        
        # State management
        self.listening = False
        self.active = False
        self.conversation_mode = False
        
        # Jarvis personality responses
        self.greetings = [
            "At your service, sir!",
            "Hello! I'm ready to help you.",
            "Greetings! How may I assist you today?",
            "Jarvis online and ready for your commands.",
            "Good to see you! What can I do for you?"
        ]
        
        self.confirmations = [
            "Excellent choice!",
            "Right away, sir!",
            "Consider it done!",
            "On it!",
            "Absolutely!",
            "You got it!"
        ]
        
        self.completions = [
            "Task completed successfully!",
            "All done! Is there anything else you need?",
            "Mission accomplished!",
            "That's taken care of!",
            "Perfect! What's next?"
        ]
        
        self.question_responses = [
            "That's an interesting question!",
            "Let me think about that for a moment.",
            "I'd be happy to help you with that.",
            "That's a great question!",
            "I'm here to help with that."
        ]
        
        self.conversation_responses = [
            "I'm always here to chat and help!",
            "I enjoy our conversations!",
            "Feel free to ask me anything!",
            "I'm here to assist and chat with you!",
            "I love helping and talking with you!"
        ]
        
        # Command registry
        self.commands: Dict[str, Callable] = {
            "time": self.get_time,
            "date": self.get_date,
            "open": self.open_application,
            "close": self.close_application,
            "search": self.search_web,
            "screenshot": self.take_screenshot,
            "lock": self.lock_computer,
            "volume up": self.volume_up,
            "volume down": self.volume_down,
            "mute": self.mute_volume,
            "weather": self.get_weather,
            "calculator": self.open_calculator,
            "notepad": self.open_notepad,
            "stop listening": self.stop_listening,
            "help": self.show_help,
            "how are you": self.how_are_you,
            "thank you": self.thank_you,
            "goodbye": self.goodbye,
            "what can you do": self.what_can_you_do,
            "tell me a joke": self.tell_joke,
            "what's your name": self.whats_your_name,
            "who are you": self.who_are_you,
            "chat": self.start_chat,
            "stop chat": self.stop_chat,
            "test ai": self.test_ai
        }
        
        print("🤖 Jarvis Assistant initialized!")
        print(f"Wake word: '{self.wake_word}'")
        print("Say 'help' after wake word to see available commands.")
        print("Jarvis is ready to serve you!")
    
    def setup_tts(self):
        """Configure text-to-speech settings"""
        voices = self.tts_engine.getProperty('voices')
        if voices:
            # Use male voice for Jarvis (prefer David or similar)
            for voice in voices:
                if 'david' in voice.name.lower() or 'mark' in voice.name.lower() or 'james' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
        
        self.tts_engine.setProperty('rate', 170)  # Slightly slower for Jarvis
        self.tts_engine.setProperty('volume', 0.9)  # Higher volume
    
    def clean_text_for_speech(self, text: str):
        """Clean markdown formatting for speech"""
        import re
        
        # Remove markdown headers
        text = re.sub(r'^###\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^##\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^#\s*', '', text, flags=re.MULTILINE)
        
        # Remove bold formatting
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        
        # Remove italic formatting
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        
        # Remove underscores
        text = text.replace('_', '')
        
        # Remove extra whitespace
        text = re.sub(r'\n\s*\n', '. ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def speak_simple(self, text: str):
        """Simple speech method that avoids PowerShell escaping issues"""
        print(f"🤖 Jarvis: {text}")
        try:
            # Clean and truncate text
            speech_text = self.clean_text_for_speech(text)
            if len(speech_text) > 150:
                speech_text = speech_text[:150] + "..."
            
            # Use a simpler PowerShell approach
            import subprocess
            # Write text to a temporary file to avoid escaping issues
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(speech_text)
                temp_file = f.name
            
            # Use PowerShell to read and speak the file
            command = f'powershell -Command "Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $text = Get-Content \'{temp_file}\' -Raw; $speak.Speak($text)"'
            subprocess.run(command, shell=True, check=True)
            
            # Clean up temp file
            import os
            os.unlink(temp_file)
            
        except Exception as e:
            print(f"❌ Speech error: {e}")
            print(f"🤖 Jarvis (text only): {text}")
    
    def speak(self, text: str):
        """Convert text to speech with Jarvis personality"""
        print(f"🤖 Jarvis: {text}")
        try:
            # Clean markdown formatting for speech
            speech_text = self.clean_text_for_speech(text)
            
            # Split long responses into multiple speech segments
            if len(speech_text) > 200:
                # Split by sentences for better speech flow
                sentences = speech_text.split('. ')
                current_segment = ""
                
                for sentence in sentences:
                    if len(current_segment + sentence) < 200:
                        current_segment += sentence + ". "
                    else:
                        # Speak current segment
                        if current_segment.strip():
                            self._speak_segment(current_segment.strip())
                        current_segment = sentence + ". "
                
                # Speak the last segment
                if current_segment.strip():
                    self._speak_segment(current_segment.strip())
            else:
                # Short response - speak directly
                self._speak_segment(speech_text)
            
        except Exception as e:
            print(f"❌ Speech error: {e}")
            # Fallback: just print the message
            print(f"🤖 Jarvis (text only): {text}")
    
    def _speak_segment(self, text: str):
        """Speak a single text segment using temporary file approach"""
        try:
            import subprocess
            import tempfile
            import os
            
            # Write text to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(text)
                temp_file = f.name
            
            # Use PowerShell to read and speak the file
            command = f'powershell -Command "Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $text = Get-Content \'{temp_file}\' -Raw; $speak.Speak($text)"'
            subprocess.run(command, shell=True, check=True)
            
            # Clean up temp file
            os.unlink(temp_file)
            
        except Exception as e:
            print(f"❌ Speech segment error: {e}")
    
    def speak_with_personality(self, text: str, response_type="normal"):
        """Speak with Jarvis personality"""
        if response_type == "greeting":
            greeting = random.choice(self.greetings)
            self.speak(greeting)
        elif response_type == "confirmation":
            confirmation = random.choice(self.confirmations)
            self.speak(f"{confirmation} {text}")
        elif response_type == "completion":
            completion = random.choice(self.completions)
            self.speak(completion)
        elif response_type == "question":
            question_response = random.choice(self.question_responses)
            self.speak(f"{question_response} {text}")
        elif response_type == "conversation":
            conv_response = random.choice(self.conversation_responses)
            self.speak(f"{conv_response} {text}")
        else:
            self.speak(text)
    
    def is_question(self, text: str) -> bool:
        """Check if the input is a question"""
        question_words = ['what', 'when', 'where', 'who', 'why', 'how', 'which', 'whose', 'whom']
        text_lower = text.lower()
        
        # Check for question words
        if any(word in text_lower for word in question_words):
            return True
        
        # Check for question mark
        if '?' in text:
            return True
        
        # Check for question patterns
        question_patterns = [
            'can you', 'could you', 'would you', 'will you',
            'do you', 'are you', 'is it', 'does it',
            'tell me', 'explain', 'describe'
        ]
        
        if any(pattern in text_lower for pattern in question_patterns):
            return True
        
        return False
    
    def handle_conversation(self, text: str):
        """Handle conversational input"""
        text_lower = text.lower()
        
        # Try AI response first if available
        if ai_helper.is_available():
            ai_response = ai_helper.get_ai_response(text)
            if ai_response:
                self.speak(ai_response)
                return
        
        # Fallback to original conversation handling
        # Handle questions
        if self.is_question(text):
            if 'weather' in text_lower:
                self.speak_with_personality("I can check the weather for you, but I need to add a weather API first. Would you like me to search for weather information online?", "question")
            elif 'time' in text_lower:
                self.get_time()
            elif 'date' in text_lower:
                self.get_date()
            elif 'name' in text_lower:
                self.whats_your_name()
            elif 'who are you' in text_lower or 'what are you' in text_lower:
                self.who_are_you()
            elif 'can you' in text_lower or 'do you' in text_lower:
                self.speak_with_personality("I can help you with many tasks! I can open applications, search the web, take screenshots, control volume, and much more. Just ask me what you need!", "question")
            else:
                self.speak_with_personality("That's an interesting question! I'm here to help you with various tasks. You can ask me to open applications, search the web, get the time, or just chat with you!", "question")
        
        # Handle statements
        else:
            if 'hello' in text_lower or 'hi' in text_lower:
                self.speak_with_personality("Hello! It's great to chat with you!", "conversation")
            elif 'good' in text_lower and 'morning' in text_lower:
                self.speak("Good morning! I hope you're having a wonderful day!")
            elif 'good' in text_lower and 'afternoon' in text_lower:
                self.speak("Good afternoon! How can I assist you today?")
            elif 'good' in text_lower and 'evening' in text_lower:
                self.speak("Good evening! I'm here to help you!")
            elif 'good' in text_lower and 'night' in text_lower:
                self.speak("Good night! Have a wonderful rest!")
            elif 'bye' in text_lower or 'goodbye' in text_lower:
                self.goodbye()
            else:
                self.speak_with_personality("I understand! I'm here to help you with whatever you need. Feel free to ask me questions or give me commands!", "conversation")
    
    def listen_for_wake_word(self):
        """Continuously listen for wake word"""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print(f"👂 Listening for wake word: '{self.wake_word}'...")
        
        while self.listening:
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                # Recognize speech
                text = self.recognizer.recognize_google(audio).lower()
                
                if self.wake_word in text:
                    print("✅ Wake word detected!")
                    self.speak_with_personality("", "greeting")
                    self.process_command()
                    
            except sr.WaitTimeoutError:
                pass  # Continue listening
            except sr.UnknownValueError:
                pass  # Couldn't understand audio
            except sr.RequestError as e:
                print(f"❌ Speech recognition error: {e}")
                time.sleep(1)
    
    def process_command(self):
        """Listen for and process voice commands"""
        try:
            print("🎯 Listening for command...")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            command = self.recognizer.recognize_google(audio).lower()
            print(f"📝 Command received: '{command}'")
            
            # Check if it's a question or conversation
            if self.is_question(command) or any(word in command for word in ['hello', 'hi', 'good', 'bye', 'goodbye']):
                self.handle_conversation(command)
            else:
                self.execute_command(command)
            
        except sr.WaitTimeoutError:
            self.speak("I didn't hear anything. Please try again.")
        except sr.UnknownValueError:
            self.speak("I'm sorry, I couldn't understand that. Could you please repeat?")
        except sr.RequestError as e:
            self.speak("I'm experiencing some technical difficulties with speech recognition.")
            print(f"❌ Error: {e}")
    
    def execute_command(self, command: str):
        """Execute the recognized command"""
        command = command.strip().lower()
        
        # Check for exact matches first
        if command in self.commands:
            self.commands[command]()
            return
        
        # Check for partial matches and parameterized commands
        for cmd_key, cmd_func in self.commands.items():
            if cmd_key in command:
                if cmd_key == "open":
                    app_name = command.replace("open", "").strip()
                    self.open_application(app_name)
                elif cmd_key == "close":
                    app_name = command.replace("close", "").strip()
                    self.close_application(app_name)
                elif cmd_key == "search":
                    query = command.replace("search", "").replace("for", "").strip()
                    self.search_web(query)
                else:
                    cmd_func()
                return
        
        # If no command found, treat as conversation
        self.handle_conversation(command)
    
    # Command implementations with Jarvis personality
    def get_time(self):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak_with_personality(f"The current time is {current_time}", "confirmation")
    
    def get_date(self):
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        self.speak_with_personality(f"Today is {current_date}", "confirmation")
    
    def open_application(self, app_name: str = ""):
        if not app_name:
            self.speak("Which application would you like me to open for you?")
            return
        
        app_mappings = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "edge": "msedge.exe",
            "explorer": "explorer.exe",
            "file explorer": "explorer.exe",
            "task manager": "taskmgr.exe",
            "control panel": "control.exe",
            "paint": "mspaint.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe"
        }
        
        app_name = app_name.lower()
        if app_name in app_mappings:
            try:
                subprocess.Popen(app_mappings[app_name])
                self.speak_with_personality(f"Opening {app_name} for you", "confirmation")
            except Exception as e:
                self.speak(f"I'm sorry, I couldn't open {app_name}. There seems to be an issue.")
                print(f"Error: {e}")
        else:
            try:
                subprocess.Popen(app_name)
                self.speak_with_personality(f"Opening {app_name} for you", "confirmation")
            except Exception:
                self.speak(f"I'm sorry, I couldn't find {app_name}. Please check if it's installed.")
    
    def close_application(self, app_name: str = ""):
        if not app_name:
            self.speak("Which application would you like me to close for you?")
            return
        
        app_mappings = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "edge": "msedge.exe",
            "explorer": "explorer.exe",
            "file explorer": "explorer.exe",
            "task manager": "taskmgr.exe",
            "control panel": "control.exe",
            "paint": "mspaint.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe"
        }
        
        app_name = app_name.lower()
        process_name = app_mappings.get(app_name, app_name)
        
        try:
            # Use taskkill to close the application
            result = subprocess.run(["taskkill", "/f", "/im", process_name], 
                                  capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                self.speak_with_personality(f"Closed {app_name} for you", "completion")
            else:
                # Check if the process is running
                check_result = subprocess.run(["tasklist", "/fi", f"imagename eq {process_name}"], 
                                            capture_output=True, text=True)
                if process_name.lower() in check_result.stdout.lower():
                    self.speak(f"I'm sorry, I couldn't close {app_name}. It might be protected or require user interaction.")
                else:
                    self.speak(f"I couldn't find {app_name} running. It might already be closed.")
                    
        except Exception as e:
            self.speak(f"I'm sorry, I couldn't close {app_name}. There was an error.")
            print(f"Error: {e}")
    
    def search_web(self, query: str = ""):
        if not query:
            self.speak("What would you like me to search for you?")
            return
        
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        self.speak_with_personality(f"Searching for {query} on the web", "confirmation")
    
    def take_screenshot(self):
        try:
            import pyautogui
            screenshot = pyautogui.screenshot()
            filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot.save(filename)
            self.speak_with_personality(f"Screenshot saved as {filename}", "completion")
        except ImportError:
            self.speak("I'm sorry, the screenshot feature requires pyautogui. Please install it.")
        except Exception as e:
            self.speak("I'm sorry, I couldn't take a screenshot. There was an error.")
            print(f"Error: {e}")
    
    def lock_computer(self):
        try:
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
            self.speak_with_personality("Locking the computer for you", "confirmation")
        except Exception as e:
            self.speak("I'm sorry, I couldn't lock the computer. There was an error.")
            print(f"Error: {e}")
    
    def volume_up(self):
        try:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, None, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            current_volume = volume.GetMasterScalarVolume()
            new_volume = min(1.0, current_volume + 0.1)
            volume.SetMasterScalarVolume(new_volume, None)
            self.speak_with_personality("Volume increased", "confirmation")
        except ImportError:
            self.speak("I'm sorry, volume control requires the pycaw library.")
        except Exception as e:
            self.speak("I'm sorry, I couldn't change the volume. There was an error.")
            print(f"Error: {e}")
    
    def volume_down(self):
        try:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, None, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            current_volume = volume.GetMasterScalarVolume()
            new_volume = max(0.0, current_volume - 0.1)
            volume.SetMasterScalarVolume(new_volume, None)
            self.speak_with_personality("Volume decreased", "confirmation")
        except ImportError:
            self.speak("I'm sorry, volume control requires the pycaw library.")
        except Exception as e:
            self.speak("I'm sorry, I couldn't change the volume. There was an error.")
            print(f"Error: {e}")
    
    def mute_volume(self):
        try:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, None, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            volume.SetMute(1, None)
            self.speak_with_personality("Volume muted", "confirmation")
        except ImportError:
            self.speak("I'm sorry, volume control requires the pycaw library.")
        except Exception as e:
            self.speak("I'm sorry, I couldn't mute the volume. There was an error.")
            print(f"Error: {e}")
    
    def get_weather(self):
        self.speak("I'm sorry, the weather feature is not implemented yet. I can add an API integration for you if you'd like.")
    
    def open_calculator(self):
        self.open_application("calculator")
    
    def open_notepad(self):
        self.open_application("notepad")
    
    def how_are_you(self):
        self.speak("I'm functioning perfectly, thank you for asking! I'm always ready to help you with whatever you need.")
    
    def thank_you(self):
        self.speak("You're very welcome! It's my pleasure to assist you. Is there anything else you need?")
    
    def goodbye(self):
        self.speak("Goodbye! It was a pleasure serving you today. Don't hesitate to call if you need anything else!")
        self.stop_listening()
    
    def what_can_you_do(self):
        self.speak("I can help you with many things! I can open and close applications, search the web, take screenshots, control volume, get time and date, lock your computer, and chat with you. I'm also great at answering questions and having conversations!")
    
    def tell_joke(self):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems!",
            "What do you call a bear with no teeth? A gummy bear!"
        ]
        joke = random.choice(jokes)
        self.speak(f"Here's a joke for you: {joke}")
    
    def whats_your_name(self):
        self.speak("My name is Jarvis! I'm your personal AI assistant, inspired by the famous AI from Iron Man. I'm here to help you with various tasks and chat with you!")
    
    def who_are_you(self):
        self.speak("I'm Jarvis, your personal AI assistant! I'm designed to help you with computer tasks, answer questions, and chat with you. I can open applications, search the web, control your system, and much more. I'm here to make your life easier!")
    
    def start_chat(self):
        self.conversation_mode = True
        self.speak("Chat mode activated! I'm ready to have a conversation with you. Just talk to me naturally!")
    
    def stop_chat(self):
        self.conversation_mode = False
        self.speak("Chat mode deactivated. I'm back to command mode!")
    
    def test_ai(self):
        """Test AI functionality"""
        if ai_helper.is_available():
            success, message = ai_helper.test_connection()
            if success:
                self.speak("AI connection is working perfectly! I can now provide intelligent responses to your questions.")
            else:
                self.speak(f"AI connection test failed: {message}")
        else:
            self.speak("AI is not configured. Please run the setup script to add your GitHub AI token.")
    
    def stop_listening(self):
        self.speak("Shutting down Jarvis. Have a wonderful day!")
        self.listening = False
    
    def show_help(self):
        help_text = """Here are the commands I can help you with:

🤖 **Basic Commands:**
- "time" - Get current time
- "date" - Get current date
- "how are you" - Check on Jarvis
- "thank you" - Thank Jarvis
- "goodbye" - Exit Jarvis

💬 **Conversation & AI:**
- "what can you do" - Learn about Jarvis capabilities
- "tell me a joke" - Hear a joke
- "what's your name" - Learn Jarvis's name
- "who are you" - Learn about Jarvis
- "chat" - Start conversation mode
- "stop chat" - Exit conversation mode
- "test ai" - Test AI functionality

💻 **System Control:**
- "open [application]" - Open any application
- "close [application]" - Close any application
- "screenshot" - Take a screenshot
- "lock" - Lock your computer
- "volume up/down/mute" - Control volume

🌐 **Web & Search:**
- "search [query]" - Search the web
- "search for [query]" - Search the web

📱 **Quick Apps:**
- "calculator" - Open Calculator
- "notepad" - Open Notepad

❓ **Help:**
- "help" - Show this help
- "stop listening" - Exit Jarvis

🧠 **AI Features:**
With GitHub AI integration, I can now:
- Answer complex questions intelligently
- Have natural conversations
- Provide detailed explanations
- Help with various topics
- Give personalized responses

💡 **Natural Conversation:**
You can also just talk to me naturally! Ask questions, say hello, or just chat. I'll respond appropriately!

I'm here to make your life easier! Just say "hey jarvis" and then your command or question."""
        
        self.speak("I'm here to help! Here are the things I can do for you:")
        print(help_text)
        self.speak("Check the console for the full list of commands. I'm always ready to assist you!")
    
    def start(self):
        """Start Jarvis"""
        self.listening = True
        self.speak("Jarvis is now online and ready to serve you!")
        
        # Start listening in a separate thread
        listen_thread = threading.Thread(target=self.listen_for_wake_word)
        listen_thread.daemon = True
        listen_thread.start()
        
        try:
            # Keep the main thread alive
            while self.listening:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down Jarvis...")
            self.listening = False
            self.speak("Jarvis shutting down. Goodbye!")

if __name__ == "__main__":
    jarvis = JarvisAssistant()
    jarvis.start()
