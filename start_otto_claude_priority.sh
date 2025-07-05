#!/bin/bash

echo "🧠 OTTO - Claude Priority System"
echo "================================="
echo "🎯 Claude bevorzugt für komplexe Aufgaben"
echo "🎤 Lokale Logik nur als Fallback"
echo "🔇 Keine doppelten Stimmen"
echo ""

# Prüfe API Keys
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY nicht gesetzt"
    echo "Setze die Umgebungsvariable: export ANTHROPIC_API_KEY='dein-api-key'"
    echo ""
fi

if [ -z "$ELEVENLABS_VOICE_ID" ]; then
    echo "⚠️  ELEVENLABS_VOICE_ID nicht gesetzt"
    echo "Setze die Umgebungsvariable: export ELEVENLABS_VOICE_ID='deine-voice-id'"
    echo ""
fi

# Wechsle ins richtige Verzeichnis
cd "$(dirname "$0")"

# Starte Otto Claude Priority
echo "🚀 Starte Otto Claude Priority..."
echo ""

python3 otto_claude_priority.py 