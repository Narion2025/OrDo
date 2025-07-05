#!/bin/bash

# Otto Single Voice Startskript
echo "🧠 Starte Otto Single Voice..."
echo "🎯 Nur eine Stimme - keine doppelten Stimmen"

# Prüfe Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nicht gefunden"
    exit 1
fi

# Prüfe .env Datei
if [ ! -f ".env" ]; then
    echo "⚠️  .env Datei nicht gefunden"
    echo "📝 Erstelle .env Template..."
    cat > .env << EOF
# Otto Single Voice - Umgebungsvariablen
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=pNInz6obpgDQGcFmaJgB
EOF
    echo "✅ .env Template erstellt"
    echo "📝 Bitte trage deine API-Keys in die .env Datei ein"
    echo "🔑 ElevenLabs API Key: https://elevenlabs.io/"
fi

# Prüfe Abhängigkeiten
echo "🔍 Prüfe Abhängigkeiten..."
python3 -c "import speech_recognition, pyttsx3, dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installiere fehlende Abhängigkeiten..."
    pip3 install SpeechRecognition pyttsx3 python-dotenv
fi

# Starte Otto
echo "🚀 Starte Otto Single Voice..."
python3 otto_single_voice.py 