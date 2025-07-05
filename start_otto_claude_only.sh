#!/bin/bash

echo "🧠 OTTO - Claude-Only System"
echo "============================"
echo "🎯 Starte Otto mit nur Claude API (keine GPT-Konflikte)..."
echo ""

# Prüfe ob ANTHROPIC_API_KEY gesetzt ist
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY nicht gesetzt"
    echo "Setze die Umgebungsvariable: export ANTHROPIC_API_KEY='dein-api-key'"
    echo ""
fi

# Wechsle ins richtige Verzeichnis
cd "$(dirname "$0")"

# Starte Otto Claude-Only
echo "🚀 Starte Otto Claude-Only..."
echo ""

python3 otto_claude_only.py 