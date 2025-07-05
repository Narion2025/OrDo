#!/bin/bash

# Otto OpenAI Fixed Startskript
echo "🧠 Starte Otto OpenAI Fixed..."
echo "🎯 OpenAI-Integration mit korrekter API-Version"

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
# Otto OpenAI Fixed - Umgebungsvariablen
OPENAI_API_KEY=sk-7f784c3c4dc74dde1d037474d515709047ad9b577fb48f28
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=pNInz6obpgDQGcFmaJgB
EOF
    echo "✅ .env Template erstellt"
    echo "📝 Bitte trage deine API-Keys in die .env Datei ein"
    echo "🔑 OpenAI API Key: https://platform.openai.com/account/api-keys"
    echo "🎵 ElevenLabs API Key: https://elevenlabs.io/"
fi

# Lade .env
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ .env Datei geladen"
else
    echo "⚠️  Keine .env Datei gefunden - verwende Standardeinstellungen"
fi

# Prüfe Abhängigkeiten
echo "🔍 Prüfe Abhängigkeiten..."
python3 -c "import speech_recognition, pyaudio, openai, dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installiere fehlende Abhängigkeiten..."
    pip3 install speechrecognition pyaudio openai==0.28 python-dotenv pyttsx3 requests
fi

# Prüfe OpenAI API Key
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
    echo "⚠️  OpenAI API Key nicht gesetzt"
    echo "🔑 Bitte setze OPENAI_API_KEY in .env"
else
    echo "✅ OpenAI API Key gefunden"
fi

# Prüfe ElevenLabs (optional)
if [ -z "$ELEVENLABS_API_KEY" ] || [ "$ELEVENLABS_API_KEY" = "your_elevenlabs_api_key_here" ]; then
    echo "⚠️  ElevenLabs API Key nicht gesetzt - Otto wird mit pyttsx3 sprechen"
    echo "🎵 Optional: Setze ELEVENLABS_API_KEY in .env für bessere Sprachausgabe"
else
    echo "✅ ElevenLabs API Key gefunden"
fi

echo ""
echo "🧠 Otto OpenAI Fixed Features:"
echo "   • OpenAI GPT-3.5-Turbo Integration"
echo "   • Korrekte API-Version (0.28)"
echo "   • Sprachsteuerung mit Trigger-Wörtern"
echo "   • ElevenLabs Sprachausgabe (optional)"
echo "   • Task-Management System"
echo "   • Konversationsmodus"
echo ""

echo "🎤 Starte Otto OpenAI Fixed..."
echo "🔊 Sage 'Otto' um zu beginnen"
echo "⏹️  Drücke Ctrl+C zum Beenden"
echo ""

# Starte Otto
python3 otto_openai_fixed.py 