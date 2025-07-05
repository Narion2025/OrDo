#!/bin/bash

# Otto Learning System Startskript
echo "🧠 Starte Otto Learning System..."
echo "🎯 Kontinuierliches Lernen mit Jammeldateien und Kristallen"

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
# Otto Learning System - Umgebungsvariablen
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
python3 -c "import speech_recognition, pyaudio, yaml, dotenv, schedule" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installiere fehlende Abhängigkeiten..."
    pip3 install speechrecognition pyaudio pyyaml python-dotenv schedule
fi

# Prüfe Marker-Verzeichnis
if [ ! -d "../ALL_SEMANTIC_MARKER_TXT" ]; then
    echo "⚠️  Marker-Verzeichnis nicht gefunden"
    echo "📁 Erwartet: ../ALL_SEMANTIC_MARKER_TXT/ALL_NEWMARKER01/"
    echo "📝 Bitte stelle sicher, dass die Marker-Dateien verfügbar sind"
else
    echo "✅ Marker-Verzeichnis gefunden"
fi

# Prüfe ElevenLabs (optional)
if [ -z "$ELEVENLABS_API_KEY" ] || [ "$ELEVENLABS_API_KEY" = "your_elevenlabs_api_key_here" ]; then
    echo "⚠️  ElevenLabs API Key nicht gesetzt - Otto wird ohne Sprachausgabe laufen"
    echo "🎵 Optional: Setze ELEVENLABS_API_KEY in .env für Sprachausgabe"
else
    echo "✅ ElevenLabs API Key gefunden"
fi

echo ""
echo "🧠 Otto Learning System Features:"
echo "   • Kontinuierliches Lernen aus Interaktionen"
echo "   • Jammeldateien für Gedanken und Eindrücke"
echo "   • Mind-System für Erinnerungen"
echo "   • Strudel-Knoten-Kristalle für Erkenntnisse"
echo "   • Crunchjob alle 2 Stunden"
echo "   • Automatische Kristall-Triggerung"
echo ""

echo "📁 Erstelle Verzeichnisse..."
mkdir -p otto_jammel
mkdir -p otto_mind
echo "✅ Verzeichnisse erstellt"

echo "🎤 Starte Otto Learning System..."
echo "🔊 Sage 'Otto' um zu beginnen"
echo "⏹️  Drücke Ctrl+C zum Beenden"
echo ""

# Starte Otto
python3 otto_learning_system.py 