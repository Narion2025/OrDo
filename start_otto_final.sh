#!/bin/bash

# Otto Final Clean Version Startskript
echo "🚀 Starte Otto Final Clean Version..."

# Prüfe Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nicht gefunden"
    exit 1
fi

# Prüfe .env Datei
if [ ! -f ".env" ]; then
    echo "⚠️  .env Datei nicht gefunden"
    echo "📝 Erstelle .env Template..."
    cat > .env << EOF
# Otto Final Clean Version - Umgebungsvariablen
ANTHROPIC_API_KEY=your_claude_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=pNInz6obpgDQGcFmaJgB
EOF
    echo "✅ .env Template erstellt"
    echo "📝 Bitte trage deine API-Keys in die .env Datei ein"
    echo "🔑 Claude API Key: https://console.anthropic.com/"
    echo "🎵 ElevenLabs API Key: https://elevenlabs.io/"
fi

# Lade .env
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Prüfe API Keys
if [ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" = "your_claude_api_key_here" ]; then
    echo "⚠️  Claude API Key nicht gesetzt"
    echo "📝 Otto läuft im lokalen Modus ohne Claude API"
fi

if [ -z "$ELEVENLABS_API_KEY" ] || [ "$ELEVENLABS_API_KEY" = "your_elevenlabs_api_key_here" ]; then
    echo "⚠️  ElevenLabs API Key nicht gesetzt"
    echo "📝 Otto spricht nur Text ohne Audio"
fi

# Installiere Abhängigkeiten
echo "📦 Installiere Abhängigkeiten..."
pip3 install speechrecognition pyaudio anthropic elevenlabs python-dotenv pyyaml

# Starte Otto
echo "🧠 Starte Otto Final Clean Version..."
python3 otto_final_clean.py 