#!/bin/bash

echo "🚀 Starte Otto MCP Working System..."
echo "======================================"

# Prüfe ob wir im richtigen Verzeichnis sind
if [ ! -f "otto_mcp_working.py" ]; then
    echo "❌ Fehler: otto_mcp_working.py nicht gefunden!"
    echo "Bitte führe das Skript aus dem OrDo/Nietzsche Verzeichnis aus."
    exit 1
fi

# Prüfe Python-Abhängigkeiten
echo "🔍 Prüfe Abhängigkeiten..."

# Prüfe OpenAI Version
python3 -c "import openai; print(f'OpenAI Version: {openai.__version__}')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ OpenAI nicht installiert!"
    echo "Führe aus: pip install openai==0.28"
    exit 1
fi

# Prüfe andere Abhängigkeiten
python3 -c "import speech_recognition, pyttsx3, yaml" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Fehlende Abhängigkeiten!"
    echo "Führe aus: pip install SpeechRecognition pyttsx3 PyYAML"
    exit 1
fi

echo "✅ Alle Abhängigkeiten verfügbar"
echo ""

# Starte Otto
echo "🧠 Starte Otto MCP Working System..."
echo "======================================"
python3 otto_mcp_working.py 