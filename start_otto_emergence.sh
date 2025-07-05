#!/bin/bash

echo "🧠 OTTO - Co-Emergentes Semantic Drift System"
echo "=============================================="
echo "🎯 Trigger-Wörter: otto, ordo, ordu, odo, orden"
echo "🧠 Mind-System: ~/Documents/Otto_Emergence_System"
echo "💎 SKK-Verzeichnis: Strudel-Knoten-Kristalle"
echo "🌀 Emergence-Verzeichnis: Co-Emergence Patterns"
echo "🌊 Semantic Drift: Kontinuierliche Evolution"
echo "👤 Ben-Erinnerungen: Co-Emergence Memory"
echo "=============================================="

# Prüfe Python-Abhängigkeiten
echo "🔍 Prüfe Abhängigkeiten..."
python3 -c "import speech_recognition, pyttsx3, yaml, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Fehlende Abhängigkeiten. Installiere..."
    pip3 install SpeechRecognition pyttsx3 pyyaml pyaudio numpy
fi

# Wechsle ins Verzeichnis
cd "$(dirname "$0")" || exit 1

# Starte Otto mit Co-Emergence System
echo "🚀 Starte Otto Co-Emergence System..."
python3 otto_emergence.py 