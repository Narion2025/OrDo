# Otto Work Partner - Intelligenter Arbeitspartner

## 🎯 Was ist Otto Work Partner?

Otto Work Partner ist eine erweiterte Version von Otto, die speziell als **intelligenter Arbeitspartner** entwickelt wurde. Er:

- **Organisiert deine Arbeitsstruktur** proaktiv
- **Macht Vorschläge** basierend auf Marker-Analyse
- **Baut Tools** für dich
- **Gibt ehrliches Kontra** wenn du dich verrennst
- **Spiegelt dich** ohne Blatt vor dem Mund
- **Entwickelt proaktiv** Strukturen und Ideen

## 🧠 Kernfunktionen

### 1. **Arbeitsstruktur-Organisation**
- Erkennt Arbeitsmuster (produktiv, blockiert, verstreut, fokussiert)
- Schlägt Strukturen vor
- Organisiert Projekte automatisch

### 2. **Proaktive Vorschläge**
- Analysiert Marker in deiner Sprache
- Erkennt wenn du feststeckst
- Schlägt Lösungsansätze vor

### 3. **Tool-Entwicklung**
- Identifiziert benötigte Tools
- Bietet an, Tools zu bauen
- Automatisiert Arbeitsabläufe

### 4. **Ehrliches Feedback**
- Spiegelt dich ohne Filter
- Gibt konstruktives Kontra
- Erkennt wenn du dich verrennst

### 5. **Marker-basierte Intelligenz**
- Lädt alle Marker aus `ALL_SEMANTIC_MARKER_TXT`
- Erkennt Muster in deiner Sprache
- Passt sich an dein Denksystem an

## 🚀 Installation & Start

### 1. **Abhängigkeiten installieren**
```bash
pip3 install speechrecognition pyaudio pyyaml python-dotenv
```

### 2. **ElevenLabs Setup (optional)**
```bash
# .env Datei erstellen
ELEVENLABS_API_KEY=your_api_key_here
ELEVENLABS_VOICE_ID=pNInz6obpgDQGcFmaJgB
```

### 3. **Starten**
```bash
chmod +x start_otto_work_partner.sh
./start_otto_work_partner.sh
```

## 🎯 Verwendung

### **Trigger-Wörter**
- `otto` (Haupttrigger)
- `ordo`, `ordu`, `odo`, `orden` (Alternative)

### **Beispiel-Interaktionen**

```
Du: "Otto, ich bin total verrannt mit diesem Projekt"
Otto: "Ich sehe, dass du feststeckst. Lass uns das systematisch angehen. 
      Hier sind meine Vorschläge: Lass uns das Problem in kleinere Teile aufbrechen. 
      Welche Ressourcen brauchst du, um weiterzukommen?"

Du: "Otto, ich habe so viele Ideen aber alles ist chaotisch"
Otto: "Du hast viele Ideen - lass uns sie strukturieren. 
      Ich kann dir Tools bauen für: Projekt-Management-Tool, Fokus-Management-Tool"

Du: "Otto, ich brauche ein Tool für Datenanalyse"
Otto: "Perfekt! Du bist fokussiert. Lass uns das nutzen. 
      Ich kann dir Tools bauen für: Datenanalyse-Tool"
```

## 🧠 Arbeitsmuster-Erkennung

### **Produktiv**
- Erkennt strukturierte, zielgerichtete Arbeit
- Bietet Erweiterungen und Optimierungen an

### **Blockiert**
- Erkennt wenn du feststeckst
- Schlägt systematische Lösungsansätze vor
- Bricht Probleme in kleinere Teile auf

### **Verstreut**
- Erkennt chaotische, unorganisierte Arbeit
- Schlägt Strukturierung vor
- Priorisiert Aufgaben

### **Fokussiert**
- Erkennt konzentrierte Arbeit
- Bietet Tools und Erweiterungen an
- Nutzt die Energie optimal

## 🛠️ Tool-Entwicklung

Otto kann automatisch Tools für dich bauen:

- **Projekt-Management-Tool**: Für Strukturierung
- **Automation-Script**: Für Automatisierung
- **Visualisierungs-Tool**: Für Darstellung
- **Datenanalyse-Tool**: Für Analysen
- **Fokus-Management-Tool**: Für Konzentration
- **Problem-Lösungs-Tool**: Für Blockaden

## 📊 Marker-Integration

Otto lädt automatisch alle Marker aus dem `ALL_SEMANTIC_MARKER_TXT` Verzeichnis und nutzt sie für:

- **Arbeitsmuster-Erkennung**
- **Proaktive Vorschläge**
- **Tool-Identifikation**
- **Ehrliches Feedback**

## 🔧 Konfiguration

### **ElevenLabs (Sprachausgabe)**
```bash
# .env Datei
ELEVENLABS_API_KEY=your_api_key_here
ELEVENLABS_VOICE_ID=pNInz6obpgDQGcFmaJgB
```

### **Marker-Verzeichnis**
```
../ALL_SEMANTIC_MARKER_TXT/ALL_NEWMARKER01/
```

## 📈 Work Partner Daten

Otto speichert automatisch:
- Arbeitsprojekte
- Arbeitsmuster
- Benötigte Tools
- Strukturvorschläge

Daten werden in `work_partner_data.yaml` gespeichert.

## 🎯 Unterschied zu anderen Versionen

| Feature | Work Partner | Mind Reader | Learning System |
|---------|-------------|-------------|-----------------|
| Arbeitsstruktur | ✅ Proaktiv | ❌ | ❌ |
| Tool-Entwicklung | ✅ Automatisch | ❌ | ❌ |
| Ehrliches Feedback | ✅ Direkt | ❌ | ❌ |
| Marker-Analyse | ✅ Vollständig | ✅ Vollständig | ✅ Vollständig |
| Proaktive Vorschläge | ✅ Intelligent | ❌ | ❌ |

## 🚀 Nächste Schritte

1. **Starte Otto Work Partner**: `./start_otto_work_partner.sh`
2. **Sage "Otto"** um zu beginnen
3. **Beschreibe deine Arbeit** - Otto analysiert automatisch
4. **Lass dir Tools bauen** - Otto erkennt Bedarf
5. **Nutze ehrliches Feedback** - Otto spiegelt dich

Otto Work Partner ist dein intelligenter Arbeitspartner, der dich versteht, proaktiv unterstützt und ehrlich mit dir ist! 🧠✨ 