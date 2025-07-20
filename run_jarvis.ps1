# PowerShell script to run Voice Assistant with Jarvis conda environment

Write-Host "🎤 Starting Voice Assistant with Jarvis environment..." -ForegroundColor Green
Write-Host ""

# Activate conda environment
try {
    conda activate jarvis
    Write-Host "✅ Conda environment 'jarvis' activated successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to activate conda environment 'jarvis'" -ForegroundColor Red
    Write-Host "Please make sure the environment exists:" -ForegroundColor Yellow
    Write-Host "  conda create -n jarvis python=3.9" -ForegroundColor Cyan
    Write-Host "  conda activate jarvis" -ForegroundColor Cyan
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check if voice_assistant.py exists
if (-not (Test-Path "voice_assistant.py")) {
    Write-Host "❌ voice_assistant.py not found in current directory" -ForegroundColor Red
    Write-Host "Please run this script from the voice-assistant folder" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "🚀 Starting Voice Assistant..." -ForegroundColor Green
Write-Host ""
Write-Host "📝 Instructions:" -ForegroundColor Yellow
Write-Host "- Wake word: 'hey assistant'" -ForegroundColor White
Write-Host "- Say 'help' for available commands" -ForegroundColor White
Write-Host "- Press Ctrl+C to exit" -ForegroundColor White
Write-Host ""

# Run the voice assistant
try {
    python voice_assistant.py
} catch {
    Write-Host ""
    Write-Host "⚠️  Voice assistant failed. Trying text-only mode..." -ForegroundColor Yellow
    Write-Host ""
    try {
        python voice_assistant_simple.py
    } catch {
        Write-Host "❌ Both voice assistant versions failed" -ForegroundColor Red
        Write-Host "Please check your installation and dependencies" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "👋 Voice Assistant stopped." -ForegroundColor Green
Read-Host "Press Enter to exit" 