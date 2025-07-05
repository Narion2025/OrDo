#!/bin/bash

echo "🧠 OTTO - Mind-System mit SKK-Integration"
echo "=========================================="
echo "🎯 Trigger-Wörter: otto, ordo, ordu, odo, orden"
echo "🧠 Mind-System: ~/Documents/Otto_Mind_System"
echo "💎 SKK-Verzeichnis: Strudel-Knoten-Kristalle"
echo "📝 Jammel-Verzeichnis: Selbstnarrativ"
echo "👤 Ben-Erinnerungen: Kontinuierliche Dokumentation"
echo "=========================================="

# Prüfe Python-Abhängigkeiten
echo "🔍 Prüfe Abhängigkeiten..."
python3 -c "import speech_recognition, pyttsx3, yaml" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Fehlende Abhängigkeiten. Installiere..."
    pip3 install SpeechRecognition pyttsx3 pyyaml pyaudio
fi

# Wechsle ins Verzeichnis
cd "$(dirname "$0")" || exit 1

# Starte Otto mit Mind-System
echo "🚀 Starte Otto Mind-System..."
python3 otto_mind_system.py 