#!/bin/bash

# Otto Clean No OpenAI Startskript
echo "🧠 Starte Otto Clean (No OpenAI)..."
echo "🎯 Keine OpenAI-Integration - nur lokale Logik"
echo "🗣️  Nur eine Stimme - keine doppelten Stimmen"

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
# Otto Clean - Umgebungsvariablen
ELEVENLABS_API_KEY=sk_7f784c3c4dc74dde1d037474d515709047ad9b577fb48f28
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
    pip3 install SpeechRecognition pyttsx3 python-dotenv requests
fi

# Prüfe Mikrofon
echo "🎤 Teste Mikrofon..."
python3 -c "
import speech_recognition as sr
try:
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
    print('✅ Mikrofon funktioniert')
except Exception as e:
    print(f'❌ Mikrofon-Fehler: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Mikrofon-Test fehlgeschlagen"
    exit 1
fi

echo "✅ Alle Tests erfolgreich"
echo "🚀 Starte Otto Clean..."
echo ""

# Starte Otto
python3 otto_clean_no_openai.py 