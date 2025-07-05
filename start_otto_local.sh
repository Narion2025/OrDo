#!/bin/bash

echo "🧠 OTTO - Semantischer Task-Begleiter (Lokale Version)"
echo "=================================================="
echo ""

# Prüfe ob Python3 verfügbar ist
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 ist nicht installiert!"
    exit 1
fi

# Prüfe ob die notwendigen Module installiert sind
echo "🔍 Prüfe Abhängigkeiten..."
python3 -c "import speech_recognition, elevenlabs" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Fehlende Abhängigkeiten! Installiere sie mit:"
    echo "pip3 install SpeechRecognition elevenlabs pyaudio"
    exit 1
fi

echo "✅ Abhängigkeiten OK"
echo ""

# Wechsle ins richtige Verzeichnis
cd "$(dirname "$0")"

# Prüfe ob die Otto-Dateien vorhanden sind
if [ ! -f "ordo_voice_agent_local.py" ]; then
    echo "❌ ordo_voice_agent_local.py nicht gefunden!"
    exit 1
fi

if [ ! -f "voice_config.py" ]; then
    echo "❌ voice_config.py nicht gefunden!"
    exit 1
fi

echo "🚀 Starte Otto (Lokale Version)..."
echo "🎯 Haupttrigger: 'Otto' (einfacher zu erkennen)"
echo "🎯 Backup-Trigger: ordo, ordu, odo, orden"
echo "🧠 Lokale Intelligenz ohne API-Abhängigkeiten"
echo ""

# Starte Otto
python3 ordo_voice_agent_local.py 