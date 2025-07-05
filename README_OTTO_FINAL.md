# OTTO - Final Clean Version

## Übersicht
Otto ist ein semantischer Task-Begleiter mit systemischer Intelligenz, der Sprache erkennt, Aufgaben verwaltet und empathisch begleitet.

## Features
- 🎤 **Spracherkennung**: Erkennt Trigger-Wörter (Otto, Ordo, etc.)
- 🧠 **Claude API Integration**: Intelligente Antworten mit Anthropic Claude
- 🎵 **ElevenLabs Voice**: Natürliche Sprachausgabe
- 🔬 **MCP-System**: Meta Control Protocol für systemische Intelligenz
- 📝 **Mind-System**: Automatische Jammeldateien für Selbstreflexion
- 💬 **Konversationsmodus**: Natürliche Dialoge mit Timeout

## Installation

### 1. Abhängigkeiten installieren
```bash
pip3 install speechrecognition pyaudio anthropic elevenlabs python-dotenv pyyaml
```

### 2. API Keys konfigurieren
Erstelle eine `.env` Datei:
```bash
ANTHROPIC_API_KEY=your_claude_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=pNInz6obpgDQGcFmaJgB
```

### 3. Starten
```bash
chmod +x start_otto_final.sh
./start_otto_final.sh
```

## Verwendung

### Trigger-Wörter
- "Otto" (Haupttrigger)
- "Ordo", "Ordu", "Odo", "Orden" (Alternative)

### Konversationsmodus
1. Sage "Otto" + deine Nachricht
2. Otto antwortet
3. Du kannst direkt weiterreden
4. Konversation bleibt 30 Sekunden aktiv
5. Danach wird das Dialog-Fenster geschlossen

### Passive Task-Erkennung
Otto erkennt automatisch Aufgaben in deiner Sprache und speichert sie.

## MCP-System (Meta Control Protocol)

### MCP-Level
- **Level 0**: Grundlegende Reaktion
- **Level 1**: Kontextuelle Verarbeitung
- **Level 2**: Semantische Analyse
- **Level 3**: Systemische Einsicht
- **Level 4**: Meta-Reflexion
- **Level 5**: Emergente Intelligenz

### Mind-System
Otto erstellt automatisch Jammeldateien:
- `otto_thoughts.yaml`: Aktuelle Gedanken und Lernmuster
- `otto_self_narrative.yaml`: Selbst-Narrativ und Entwicklung
- `otto_semantic_markers.yaml`: Semantische Marker und Verarbeitung

## Konfiguration

### Claude API
- Gehe zu: https://console.anthropic.com/
- Erstelle einen API Key
- Trage ihn in die `.env` Datei ein

### ElevenLabs Voice
- Gehe zu: https://elevenlabs.io/
- Erstelle einen API Key
- Wähle eine Voice ID (Standard: Adam)
- Trage beides in die `.env` Datei ein

## Fehlerbehebung

### Mikrofon-Probleme
```bash
# Prüfe Mikrofon
python3 -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

### API-Fehler
- Prüfe API Keys in `.env`
- Stelle sicher, dass die Keys korrekt sind
- Otto läuft auch ohne APIs im lokalen Modus

### PyAudio-Fehler (macOS)
```bash
brew install portaudio
pip3 install pyaudio
```

## Entwicklung

### Neue Features hinzufügen
1. Erweitere `MCPSystem` für neue Analysen
2. Füge neue Trigger-Wörter hinzu
3. Erweitere lokale Antworten in `generate_local_response`

### Debugging
```bash
# Debug-Modus
python3 -u otto_final_clean.py
```

## Lizenz
Dieses Projekt ist für persönliche Nutzung bestimmt.

## Support
Bei Problemen:
1. Prüfe die `.env` Konfiguration
2. Stelle sicher, dass alle Abhängigkeiten installiert sind
3. Prüfe Mikrofon-Berechtigungen
4. Starte Otto neu mit `./start_otto_final.sh` 