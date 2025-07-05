#!/bin/bash

echo "🧠 OTTO - Claude + ElevenLabs System"
echo "====================================="
echo "🎯 Starte Otto mit Claude API und ElevenLabs Stimme..."
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

# Starte Otto Claude + ElevenLabs
echo "🚀 Starte Otto Claude + ElevenLabs..."
echo ""

python3 otto_claude_elevenlabs.py 