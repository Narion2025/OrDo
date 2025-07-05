#!/bin/bash

echo "🚀 Starte Otto Claude-Enhanced System..."
echo "=========================================="

# Prüfe ob wir im richtigen Verzeichnis sind
if [ ! -f "otto_claude_enhanced.py" ]; then
    echo "❌ Fehler: otto_claude_enhanced.py nicht gefunden!"
    echo "Bitte führe das Skript aus dem OrDo/Nietzsche Verzeichnis aus."
    exit 1
fi

# Prüfe Python-Abhängigkeiten
echo "🔍 Prüfe Abhängigkeiten..."

# Prüfe Anthropic/Claude
python3 -c "import anthropic; print('Anthropic Version:', anthropic.__version__)" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Anthropic nicht installiert!"
    echo "Führe aus: pip install anthropic"
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

# Prüfe Claude API Key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY nicht gesetzt!"
    echo "Setze die Umgebungsvariable: export ANTHROPIC_API_KEY='dein-api-key'"
    echo "Du kannst den Key von https://console.anthropic.com/ bekommen"
    echo ""
    echo "Möchtest du trotzdem fortfahren? (j/n)"
    read -r response
    if [[ ! "$response" =~ ^[Jj]$ ]]; then
        exit 1
    fi
else
    echo "✅ Claude API Key gefunden"
fi

echo ""
echo "🧠 Starte Otto Claude-Enhanced System..."
echo "=========================================="
python3 otto_claude_enhanced.py 