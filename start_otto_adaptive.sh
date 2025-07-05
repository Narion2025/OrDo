#!/bin/bash

# Otto Adaptive Learning Version Startskript
echo "🚀 Starte Otto Adaptive Learning Version..."
echo "🧠 Lokales LLM mit schnellem Lernen, Mind-System und MCP-Integration"

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
# Otto Adaptive Learning Version - Umgebungsvariablen
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=pNInz6obpgDQGcFmaJgB
EOF
    echo "✅ .env Template erstellt"
    echo "📝 Bitte trage deine ElevenLabs API-Keys in die .env Datei ein"
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
python3 -c "import speech_recognition, pyaudio, yaml, dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installiere fehlende Abhängigkeiten..."
    pip3 install speechrecognition pyaudio pyyaml python-dotenv
fi

# Prüfe ElevenLabs (optional)
if [ -z "$ELEVENLABS_API_KEY" ] || [ "$ELEVENLABS_API_KEY" = "your_elevenlabs_api_key_here" ]; then
    echo "⚠️  ElevenLabs API Key nicht gesetzt - Otto wird ohne Sprachausgabe laufen"
    echo "🎵 Optional: Setze ELEVENLABS_API_KEY in .env für Sprachausgabe"
else
    echo "✅ ElevenLabs API Key gefunden"
fi

# Erstelle Mind-System Verzeichnis
if [ ! -d "mind_system" ]; then
    mkdir -p mind_system
    echo "✅ Mind-System Verzeichnis erstellt"
fi

echo ""
echo "🧠 Otto Adaptive Learning Features:"
echo "   • Lokales LLM ohne externe APIs"
echo "   • Schnelles Lernen aus Konversationen"
echo "   • Mind-System mit MCP-Integration"
echo "   • Adaptive Antwortgenerierung"
echo "   • Systemische Intelligenz"
echo ""

echo "🎤 Starte Otto Adaptive Learning..."
echo "🔊 Sage 'Otto' um zu beginnen"
echo "⏹️  Drücke Ctrl+C zum Beenden"
echo ""

# Starte Otto
python3 otto_adaptive_learning.py 