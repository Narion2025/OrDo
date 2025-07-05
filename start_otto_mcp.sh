#!/bin/bash

echo "🧠 OTTO - MCP-Enhanced System"
echo "=============================="
echo "🎯 Trigger-Wörter: otto, ordo, ordu, odo, orden"
echo "🧠 Mind-System: ~/Documents/Otto_MCP_System"
echo "💎 SKK-Verzeichnis: Strudel-Knoten-Kristalle"
echo "🔗 MCP-Verzeichnis: Meta Control Protocol"
echo "🌊 Resonance-Verzeichnis: Resonanzmuster"
echo "📊 Context-Verzeichnis: Kontextuelle Intelligenz"
echo "👤 Ben-Erinnerungen: MCP-Enhanced Memory"
echo "=============================="

# Prüfe Python-Abhängigkeiten
echo "🔍 Prüfe Abhängigkeiten..."
python3 -c "import speech_recognition, pyttsx3, yaml, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Fehlende Abhängigkeiten. Installiere..."
    pip3 install SpeechRecognition pyttsx3 pyyaml pyaudio numpy
fi

# Wechsle ins Verzeichnis
cd "$(dirname "$0")" || exit 1

# Starte Otto mit MCP-System
echo "🚀 Starte Otto MCP-System..."
python3 otto_mcp_system.py 