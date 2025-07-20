# 🤖 Jarvis - AI Voice Assistant

A powerful, intelligent voice assistant inspired by Iron Man's Jarvis, built with Python and integrated with GitHub AI.

## ✨ Features

- **🎤 Voice Recognition**: Wake word detection with "hey jarvis"
- **🗣️ Text-to-Speech**: Natural voice responses using Windows PowerShell
- **🧠 AI Integration**: Powered by GitHub AI (GPT-4o) for intelligent conversations
- **💻 System Control**: Open/close applications, search web, take screenshots
- **🎛️ Volume Control**: Adjust system volume, mute/unmute
- **🔒 Security**: Lock computer, manage system settings
- **🌐 Web Search**: Search the internet with voice commands
- **📱 Quick Apps**: Calculator, Notepad, and more
- **🎭 Personality**: Friendly, professional responses with variety

## 🚀 Quick Start

### Prerequisites
- Windows 10/11
- Python 3.9+
- Conda (recommended)
- Microphone and speakers

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Raghava-Ram/Jarvis---AI-Voice-Assistant
   cd voice-assistant
   ```

2. **Create conda environment**
   ```bash
   conda create -n jarvis python=3.9
   conda activate jarvis
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure GitHub AI**
   - Get your GitHub token from: https://github.com/settings/tokens
   - Create `.env` file with: `GITHUB_AI_TOKEN=your_token_here`

5. **Run Jarvis**
   ```bash
   python voice_assistant.py
   ```

## 🎤 Usage

### Wake Jarvis
Say: **"hey jarvis"**

### Basic Commands
- **"time"** - Get current time
- **"date"** - Get current date
- **"how are you"** - Check on Jarvis
- **"what can you do"** - Learn about capabilities

### System Control
- **"open notepad"** - Open applications
- **"close notepad"** - Close applications
- **"screenshot"** - Take a screenshot
- **"lock"** - Lock your computer
- **"volume up/down/mute"** - Control volume

### Web & Search
- **"search for weather"** - Search the web
- **"search python tutorials"** - Find information

### AI Conversations
- **Ask any question** - Get intelligent AI responses
- **"explain quantum computing"** - Detailed explanations
- **"tell me a joke"** - Entertainment
- **"who is the PM of India"** - Current information

## 🛠️ Configuration

### Environment Variables
Create a `.env` file in the project root:
```
GITHUB_AI_TOKEN=your_github_token_here
```

### Customization
- Modify `voice_assistant.py` to add new commands
- Update `ai_helper.py` to change AI behavior
- Edit `config.py` for configuration settings

## 📁 Project Structure

```
voice-assistant/
├── voice_assistant.py    # Main Jarvis program
├── ai_helper.py          # AI integration
├── config.py             # Configuration system
├── requirements.txt      # Dependencies
├── .env                  # API keys (not in git)
├── .gitignore           # Git ignore rules
├── COMMANDS.md          # Command reference
├── README.md            # This file
├── run_jarvis.ps1      # PowerShell runner
└── run_jarvis.bat      # Batch runner
```

## 🔧 Troubleshooting

### Speech Issues
- Ensure Windows Speech Recognition is enabled
- Check microphone permissions
- Verify speakers are working

### AI Issues
- Verify GitHub token is valid
- Check internet connection
- Ensure `.env` file is properly configured

### PyAudio Issues
- Install Microsoft Visual C++ Build Tools
- Use conda: `conda install pyaudio`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## �� Acknowledgments

- Inspired by Iron Man's Jarvis
- Built with Python speech recognition
- Powered by GitHub AI
- Windows PowerShell TTS integration

---

**Made with ❤️ for AI enthusiasts and voice assistant lovers!**
