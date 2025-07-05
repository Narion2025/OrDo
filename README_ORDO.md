# 🧠 ORDO - Semantischer Task-Begleiter

## Überblick

Ordo ist ein lokaler KI-Assistent, der aus der Nietzsche-App transformiert wurde. Er kombiniert passive Zuhör-Technologie mit semantischer Marker-Analyse, um Tasks zu erkennen, zu strukturieren und empathische Ordnungsvorschläge zu generieren.

## 🎯 Kernfunktionen

### Passives Zuhören
- **Kontinuierliche Aufmerksamkeit**: Ordo hört permanent zu, ohne zu stören
- **Task-Erkennung**: Erkennt automatisch Aufgaben in natürlicher Sprache
- **Trigger-Aktivierung**: Spricht nur bei direkter Ansprache mit "Ordo"

### Semantische Marker-Analyse
- **11 Marker-Typen**: Ambivalenz, Selbstreflexion, Meta-Kommunikation, etc.
- **119 Patterns**: Umfassende Mustererkennung für emotionale und kommunikative Dynamiken
- **CoSD-Integration**: Cognitive Semantic Drift-Analyse für Risikobewertung

### Strukturelle Ordnung
- **Kanban-System**: Automatische Task-Kategorisierung mit Referenznummern
- **Semantischer Kontext**: Jeder Task wird mit emotionalem/kommunikativem Kontext gespeichert
- **Strukturfragen**: Proaktive, vorsichtige Ordnungsvorschläge

## 🏗️ Technische Architektur

### Dual-LLM-System
- **Primär**: OpenAI GPT-4 (über bestehende API)
- **Sekundär**: Mistral 7B (lokal, geplant)
- **Fallback**: Intelligente Auswahl basierend auf Komplexität

### Voice-System
- **ElevenLabs**: Ruhige, strukturierte Stimme (ID: kXV9fIZ5YNtH4TFjs2sD)
- **Google Speech Recognition**: Deutsche Spracherkennung
- **Trigger-Wort**: "Ordo"

### Datenstruktur
```
~/Documents/Ordo/
├── Ordo_Kanban.json          # Task-Verwaltung
├── semantic_context/         # Marker-Analysen
└── logs/                     # System-Logs
```

## 🚀 Installation & Setup

### 1. Abhängigkeiten installieren
```bash
pip install -r requirements_ordo.txt
```

### 2. Umgebungsvariablen
```bash
# .env Datei erstellen
VOICE_ID_ORDO=kXV9fIZ5YNtH4TFjs2sD
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=sk_7f784c3c4dc74dde1d037474d515709047ad9b577fb48f28
```

### 3. Ordo starten
```bash
./start_ordo.sh
```

## 📋 Verwendung

### Passive Task-Erkennung
Ordo erkennt automatisch Aussagen wie:
- "Ich muss noch..."
- "Ich sollte mal..."
- "Nicht vergessen..."
- "Todo: ..."

### Aktive Kommunikation
```
"Ordo, zeige meine Tasks"
"Ordo, analysiere diesen Text"
"Ordo, strukturelle Fragen"
"Ordo, Kanban-Status"
```

### Strukturfragen
Ordo stellt vorsichtige Fragen wie:
- "Ich sehe mehrere offene Tasks. Soll ich diese nach Priorität clustern?"
- "Möchtest du deine Tasks strukturieren?"

## 🧬 Semantische Marker

### Verfügbare Marker-Typen
1. **Ambivalenz-Marker**: Widersprüchliche Aussagen
2. **Selbstreflexions-Marker**: Introspektive Äußerungen
3. **Meta-Kommunikations-Marker**: Gespräche über Gespräche
4. **Care-Signature-Marker**: Beziehungsbasierte Signale
5. **Resonanz-Matching-Marker**: Übereinstimmungs-Erkennung

### Marker-Statistiken
- **11 Marker** geladen
- **119 Patterns** verfügbar
- **5 Marker-Typen** aktiv

## 🔧 Konfiguration

### config_ordo.json
```json
{
    "semantic_config": {
        "marker_threshold": 0.7,
        "drift_analysis": true,
        "passive_listening": true,
        "question_frequency": "vorsichtig"
    },
    "voice_config": {
        "voice_id": "kXV9fIZ5YNtH4TFjs2sD",
        "style": "ruhig, klar, strukturiert"
    }
}
```

## 🎭 Ordo-Identität

Ordo verkörpert:
- **Stille Aufmerksamkeit**: Hört zu, ohne zu urteilen
- **Strukturelle Klarheit**: Ordnet ohne zu kontrollieren
- **Empathische Resonanz**: Versteht emotionale Muster
- **Präzise Kommunikation**: Fragt, bevor er annimmt

## 🔄 Unterschiede zu Nietzsche

| Aspekt | Nietzsche | Ordo |
|--------|-----------|------|
| Persönlichkeit | Philosophisch, ironisch | Ruhig, strukturiert |
| Kommunikation | Aktiv kommentierend | Passiv zuhörend |
| Trigger | "nietzsche" | "ordo" |
| Fokus | Kreative Interpretation | Funktionale Ordnung |
| Marker | Keine | 11 semantische Marker |
| Task-System | Einfach | Erweitert mit Kontext |

## 🔮 Geplante Erweiterungen

1. **Mistral 7B Integration**: Lokale LLM-Unterstützung
2. **Erweiterte Marker**: Zusätzliche psychologische Muster
3. **Lernfähigkeit**: Adaptive Mustererkennung
4. **Web-Interface**: Optionale GUI für Task-Verwaltung
5. **Export-Funktionen**: Datenexport für Analyse

## 🛠️ Entwicklung

### Dateien-Struktur
```
OrDo/Nietzsche/
├── ordo_voice_agent.py           # Haupt-Agent
├── ordo_semantic_loader.py       # Marker-Loader
├── ordo_identity.txt             # Identitäts-Definition
├── config_ordo.json             # Konfiguration
├── voice_config.py              # Voice-Setup
├── start_ordo.sh               # Startskript
└── requirements_ordo.txt       # Abhängigkeiten
```

### Tests
```bash
# Semantic Loader testen
python3 ordo_semantic_loader.py

# Marker-Analyse testen
python3 -c "from ordo_semantic_loader import OrdoSemanticLoader; loader = OrdoSemanticLoader(); print(loader.load_all_markers())"
```

## 📞 Support

Bei Fragen oder Problemen:
1. Logs prüfen: `~/Documents/Ordo/logs/`
2. Semantic Loader testen: `python3 ordo_semantic_loader.py`
3. Konfiguration validieren: `config_ordo.json`

---

**Ordo** - Dein stiller Begleiter für strukturelle Klarheit. 🧠✨ 