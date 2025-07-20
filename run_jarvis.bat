@echo off
echo 🎤 Starting Voice Assistant with Jarvis environment...
echo.

REM Activate conda environment
call conda activate jarvis

REM Check if activation was successful
if errorlevel 1 (
    echo ❌ Failed to activate conda environment 'jarvis'
    echo Please make sure the environment exists:
    echo   conda create -n jarvis python=3.9
    echo   conda activate jarvis
    pause
    exit /b 1
)

echo ✅ Conda environment 'jarvis' activated successfully!
echo.

REM Check if voice_assistant.py exists
if not exist "voice_assistant.py" (
    echo ❌ voice_assistant.py not found in current directory
    echo Please run this script from the voice-assistant folder
    pause
    exit /b 1
)

echo 🚀 Starting Voice Assistant...
echo.
echo 📝 Instructions:
echo - Wake word: "hey assistant"
echo - Say "help" for available commands
echo - Press Ctrl+C to exit
echo.

REM Run the voice assistant
python voice_assistant.py

REM If voice assistant fails, try the simple version
if errorlevel 1 (
    echo.
    echo ⚠️  Voice assistant failed. Trying text-only mode...
    echo.
    python voice_assistant_simple.py
)

echo.
echo 👋 Voice Assistant stopped.
pause 