#!/bin/bash

echo "🧠 ORDO - Semantischer Task-Begleiter (GPT-Enhanced)"
echo "=================================================="
echo ""

# Prüfe ob Python3 verfügbar ist
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 ist nicht installiert!"
    exit 1
fi

# Prüfe ob die notwendigen Module installiert sind
echo "🔍 Prüfe Abhängigkeiten..."
python3 -c "import speech_recognition, elevenlabs, openai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Fehlende Abhängigkeiten! Installiere sie mit:"
    echo "pip3 install SpeechRecognition elevenlabs openai pyaudio"
    exit 1
fi

echo "✅ Abhängigkeiten OK"
echo ""

# Wechsle ins richtige Verzeichnis
cd "$(dirname "$0")"

# Prüfe ob die Ordo-Dateien vorhanden sind
if [ ! -f "ordo_voice_agent_gpt.py" ]; then
    echo "❌ ordo_voice_agent_gpt.py nicht gefunden!"
    exit 1
fi

if [ ! -f "voice_config.py" ]; then
    echo "❌ voice_config.py nicht gefunden!"
    exit 1
fi

echo "🚀 Starte Ordo mit GPT-Integration..."
echo "🎯 Trigger-Wörter: ordo, otto, ordu, odo, orden"
echo "🧠 GPT-Fallback für komplexe Antworten aktiviert"
echo ""

# Starte Ordo
python3 ordo_voice_agent_gpt.py 