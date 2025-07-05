#!/bin/bash

echo "🧠 OTTO - Claude-Enhanced System (Korrigiert)"
echo "=============================================="
echo "🎯 Starte Otto mit korrigierter MCP-Integration..."
echo ""

# Prüfe ob ANTHROPIC_API_KEY gesetzt ist
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY nicht gesetzt"
    echo "Setze die Umgebungsvariable: export ANTHROPIC_API_KEY='dein-api-key'"
    echo ""
fi

# Wechsle ins richtige Verzeichnis
cd "$(dirname "$0")"

# Starte Otto mit korrigierter MCP-Integration
echo "🚀 Starte Otto Claude Enhanced (Korrigiert)..."
echo ""

python3 otto_claude_enhanced.py 