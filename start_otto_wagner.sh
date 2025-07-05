#!/bin/bash

# .env laden, falls vorhanden
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "🧠 OTTO - Fixed Otto-Stimme Version"
echo "==============================="
echo "🎤 Garantiert Otto-Stimme (Voice-ID aus .env oder Umgebungsvariable)"
echo "🧠 Intelligente Claude-Antworten"
echo "❌ Keine OpenAI-Fehler"
echo ""

# Prüfe API Keys
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY nicht gesetzt"
    echo "Setze die Umgebungsvariable oder trage ihn in die .env ein: ANTHROPIC_API_KEY=..."
    echo ""
fi

# Wechsle ins richtige Verzeichnis
cd "$(dirname "$0")"

# Starte Otto mit Otto-Stimme
echo "🚀 Starte Otto mit eigener Stimme..."
echo ""

python3 otto_fixed_wagner.py 