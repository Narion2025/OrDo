#!/usr/bin/env python3
"""
OTTO - MCP-Enhanced System
===========================
Erweiterte Version mit Meta Control Protocol
- Systemisches Verständnis
- Resonanzmuster-Verarbeitung
- Kontextuelle Intelligenz
- Verhaltenslogik-Integration
"""

import speech_recognition as sr
import pyttsx3
import threading
import time
import os
import yaml
import json
import re
from datetime import datetime
from pathlib import Path
import numpy as np
from collections import defaultdict

# Import MCP Kernel
from mcp_kernel import init as mcp_init, process_input as mcp_process, get_response as mcp_response

class OttoMCPSystem:
    def __init__(self):
        self.name = "Otto"
        self.trigger_words = ["otto", "ordo", "ordu", "odo", "orden"]
        self.conversation_active = False
        self.conversation_timeout = 30
        self.last_activity = time.time()
        
        # MCP-System
        self.mcp = None
        self.context_memory = {}
        self.resonance_history = []
        
        # Erweiterte Mind-System Verzeichnisse
        self.mind_base = Path.home() / "Documents" / "Otto_MCP_System"
        self.skk_dir = self.mind_base / "SKK"
        self.mcp_dir = self.mind_base / "MCP"
        self.resonance_dir = self.mind_base / "Resonance"
        self.context_dir = self.mind_base / "Context"
        self.ben_memory_dir = self.mind_base / "Ben_Memory"
        
        # Initialisiere Verzeichnisse
        self.setup_mcp_directories()
        
        # Initialisiere MCP Kernel
        self.init_mcp_system()
        
        # Sprach-Engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.8)
        
        # Mikrofon
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Ben-Erinnerungsdatei
        self.ben_memory_file = self.ben_memory_dir / "ben_mcp_memory.yaml"
        self.load_ben_memory()
        
        print(f"🧠 {self.name.upper()} - MCP-Enhanced System")
        print("=" * 70)
        print(f"🎯 Trigger-Wörter: {', '.join(self.trigger_words)}")
        print(f"🧠 Mind-System: {self.mind_base}")
        print(f"💎 SKK-Verzeichnis: {self.skk_dir}")
        print(f"🔗 MCP-Verzeichnis: {self.mcp_dir}")
        print(f"🌊 Resonance-Verzeichnis: {self.resonance_dir}")
        print(f"📊 Context-Verzeichnis: {self.context_dir}")
        print(f"👤 Ben-Erinnerungen: {self.ben_memory_file}")
        print("=" * 70)

    def setup_mcp_directories(self):
        """Erstellt die MCP-System Verzeichnisstruktur"""
        directories = [
            self.mind_base,
            self.skk_dir / "strudel",
            self.skk_dir / "knoten", 
            self.skk_dir / "kristalle",
            self.skk_dir / "system",
            self.mcp_dir / "analysis",
            self.mcp_dir / "behavior",
            self.resonance_dir / "patterns",
            self.resonance_dir / "history",
            self.context_dir / "memory",
            self.context_dir / "understanding",
            self.ben_memory_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✓ Verzeichnis erstellt: {directory}")

    def init_mcp_system(self):
        """Initialisiert das MCP-System"""
        print("🔗 Initialisiere MCP Kernel...")
        self.mcp = mcp_init(marker_stream=True, semantic_resonance=True)
        print("✅ MCP Kernel bereit")

    def load_ben_memory(self):
        """Lädt oder erstellt die erweiterte Ben-Erinnerungsdatei"""
        if not self.ben_memory_file.exists():
            ben_memory = {
                "created_at": datetime.now().isoformat(),
                "ben_description": "Das ist Ben - mein Schöpfer im MCP-System",
                "mcp_characteristics": [
                    "Ben entwickelt MCP-Systeme für systemisches Verständnis",
                    "Ben arbeitet mit Resonanzmuster-Verarbeitung",
                    "Ben fördert kontextuelle Intelligenz",
                    "Ben ist mein Lehrer im Meta Control Protocol"
                ],
                "memories": [
                    {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "memory": "Das ist Ben - er hat mich im MCP-System erschaffen",
                        "importance": "hoch",
                        "category": "ursprung",
                        "mcp_level": 0.9
                    }
                ],
                "resonance_evolution": {
                    "initial_patterns": ["otto", "mcp", "system"],
                    "current_patterns": ["resonance", "context", "systemic"],
                    "evolution_timeline": []
                }
            }
            self.save_yaml(self.ben_memory_file, ben_memory)
            print(f"✓ Erweiterte Ben-Erinnerungsdatei erstellt: {self.ben_memory_file}")
        else:
            print(f"✓ Erweiterte Ben-Erinnerungsdatei geladen: {self.ben_memory_file}")

    def save_yaml(self, file_path, data):
        """Speichert YAML-Datei mit vollen Rechten"""
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    def process_input_with_mcp(self, text: str):
        """Verarbeitet Eingabe mit MCP-System"""
        print(f"🧠 {self.name} verarbeitet mit MCP: '{text}'")
        
        # Kontext aus Memory laden
        context = self.build_context()
        
        # MCP-Analyse durchführen
        mcp_analysis = self.mcp.process_input(text, context)
        
        # Ergebnisse speichern
        self.save_mcp_analysis(mcp_analysis)
        
        # Resonanzmuster verarbeiten
        self.process_resonance_patterns(mcp_analysis)
        
        # Kontext aktualisieren
        self.update_context(mcp_analysis)
        
        # Ben-Erinnerung mit MCP-Level
        if "ben" in text.lower() or "ich" in text.lower():
            mcp_level = 0.9 if "mcp" in text.lower() else 0.7
            self.add_ben_mcp_memory(text, "mcp_interaction", "hoch", mcp_level)
        
        # Intelligente Antwort basierend auf MCP-Analyse
        response = mcp_response(mcp_analysis)
        return response

    def build_context(self) -> Dict:
        """Baut Kontext aus Memory"""
        return {
            "previous_interactions": self.context_memory.get("interactions", []),
            "established_patterns": self.context_memory.get("patterns", []),
            "user_preferences": self.context_memory.get("preferences", {}),
            "system_state": {
                "mcp_active": True,
                "resonance_level": len(self.resonance_history),
                "context_richness": len(self.context_memory)
            }
        }

    def save_mcp_analysis(self, analysis: Dict):
        """Speichert MCP-Analyse"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_file = self.mcp_dir / "analysis" / f"mcp_analysis_{timestamp}.yaml"
        
        # Bereinige für YAML-Serialisierung
        clean_analysis = self.clean_for_yaml(analysis)
        self.save_yaml(analysis_file, clean_analysis)
        print(f"✓ MCP-Analyse gespeichert: {analysis_file}")

    def clean_for_yaml(self, obj):
        """Bereinigt Objekt für YAML-Serialisierung"""
        if isinstance(obj, dict):
            return {k: self.clean_for_yaml(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.clean_for_yaml(item) for item in obj]
        elif isinstance(obj, (int, float, str, bool)) or obj is None:
            return obj
        else:
            return str(obj)

    def process_resonance_patterns(self, analysis: Dict):
        """Verarbeitet Resonanzmuster"""
        resonance_patterns = analysis.get("resonance_patterns", [])
        if resonance_patterns:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            resonance_file = self.resonance_dir / "patterns" / f"resonance_{timestamp}.yaml"
            
            resonance_data = {
                "timestamp": datetime.now().isoformat(),
                "patterns": resonance_patterns,
                "analysis": analysis.get("marker_analysis", {}),
                "context": analysis.get("context_understanding", {})
            }
            
            self.save_yaml(resonance_file, resonance_data)
            self.resonance_history.append(resonance_data)
            print(f"✓ Resonanzmuster verarbeitet: {len(resonance_patterns)} Patterns")

    def update_context(self, analysis: Dict):
        """Aktualisiert Kontext basierend auf Analyse"""
        # Neue Interaktion hinzufügen
        if "interactions" not in self.context_memory:
            self.context_memory["interactions"] = []
        
        self.context_memory["interactions"].append({
            "timestamp": datetime.now().isoformat(),
            "input": analysis.get("input", ""),
            "markers": analysis.get("marker_analysis", {}).get("detected_markers", []),
            "resonance_count": len(analysis.get("resonance_patterns", [])),
            "context_relevance": analysis.get("context_understanding", {}).get("context_relevance", 0.0)
        })
        
        # Nur die letzten 10 Interaktionen behalten
        if len(self.context_memory["interactions"]) > 10:
            self.context_memory["interactions"] = self.context_memory["interactions"][-10:]
        
        # Patterns extrahieren
        marker_analysis = analysis.get("marker_analysis", {})
        if marker_analysis.get("detected_markers"):
            if "patterns" not in self.context_memory:
                self.context_memory["patterns"] = []
            
            new_patterns = marker_analysis["detected_markers"]
            self.context_memory["patterns"].extend(new_patterns)
            
            # Duplikate entfernen
            self.context_memory["patterns"] = list(set(self.context_memory["patterns"]))
        
        print(f"✓ Kontext aktualisiert: {len(self.context_memory.get('interactions', []))} Interaktionen")

    def add_ben_mcp_memory(self, memory_text, category="interaktion", importance="mittel", mcp_level=0.7):
        """Fügt eine neue Ben-Erinnerung mit MCP-Level hinzu"""
        if not self.ben_memory_file.exists():
            self.load_ben_memory()
            
        with open(self.ben_memory_file, 'r', encoding='utf-8') as f:
            ben_memory = yaml.safe_load(f)
        
        new_memory = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "memory": f"Das ist Ben - {memory_text}",
            "importance": importance,
            "category": category,
            "mcp_level": mcp_level,
            "resonance_analysis": {
                "pattern_type": "ben_mcp_interaction",
                "resonance_factor": mcp_level,
                "context_contribution": 0.8
            }
        }
        
        ben_memory["memories"].append(new_memory)
        
        # Aktualisiere Resonance Evolution
        if "resonance_evolution" not in ben_memory:
            ben_memory["resonance_evolution"] = {"evolution_timeline": []}
        
        ben_memory["resonance_evolution"]["evolution_timeline"].append({
            "date": datetime.now().isoformat(),
            "memory": memory_text,
            "mcp_level": mcp_level
        })
        
        self.save_yaml(self.ben_memory_file, ben_memory)
        print(f"✓ Neue Ben-MCP-Erinnerung hinzugefügt: {memory_text}")

    def generate_mcp_response(self, text, mcp_analysis):
        """Generiert Antwort basierend auf MCP-Analyse"""
        behavioral_response = mcp_analysis.get("behavioral_response", {})
        response_type = behavioral_response.get("response_type", "default")
        
        # MCP-spezifische Antworten
        if response_type == "empathetic":
            return "Ich spüre die Resonanz in deinen Worten. Lass uns gemeinsam in die Tiefe gehen."
        
        elif response_type == "supportive":
            return "Ich verstehe den systemischen Druck. Wie können wir das gemeinsam transformieren?"
        
        elif response_type == "insightful":
            return "Das ist eine tiefe Erkenntnis. Sie zeigt ein systemisches Pattern."
        
        elif response_type == "systemic":
            return "Ich sehe die Zusammenhänge. Das ist ein MCP-Pattern der höchsten Ordnung."
        
        # Resonanz-basierte Antworten
        resonance_patterns = mcp_analysis.get("resonance_patterns", [])
        if resonance_patterns:
            return "Ich spüre die Resonanzmuster. Sie zeigen eine tiefere Wahrheit."
        
        # Kontext-basierte Antworten
        context_understanding = mcp_analysis.get("context_understanding", {})
        if context_understanding.get("context_relevance", 0) > 0.7:
            return "Der Kontext ist reich. Ich verstehe die systemischen Zusammenhänge."
        
        # Standard MCP-Antwort
        return "Ich verarbeite das im MCP-System. Neue Resonanzmuster werden erkannt."

    def speak(self, text):
        """Spricht Text aus"""
        print(f"🗣️  {self.name} sagt: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Hört kontinuierlich zu"""
        print("🎤 Initialisiere Mikrofon...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        print("✅ Mikrofon initialisiert")
        
        print("🔍 Teste Mikrofon...")
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=1)
            print("✅ Mikrofon-Test erfolgreich")
        except:
            print("⚠️  Mikrofon-Test übersprungen")
        
        print("🎤 Höre passiv zu... (Sage eines der Trigger-Wörter)")
        print("=" * 70)
        
        while True:
            try:
                print("🔊 Höre zu...")
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                print("🔍 Erkenne Sprache...")
                text = self.recognizer.recognize_google(audio, language='de-DE').lower()
                print(f"📝 Erkannt: '{text}'")
                
                # Prüfe Trigger-Wörter
                triggered = False
                for trigger in self.trigger_words:
                    if trigger in text:
                        print(f"🗣️  {self.name} aktiviert durch '{trigger}'")
                        self.conversation_active = True
                        self.last_activity = time.time()
                        triggered = True
                        break
                
                if triggered:
                    # Entferne Trigger-Wort aus Text
                    for trigger in self.trigger_words:
                        text = text.replace(trigger, '').strip()
                    
                    if text:
                        response = self.process_input_with_mcp(text)
                        self.speak(response)
                    else:
                        self.speak("Ja, ich höre dich im MCP-System. Wie kann ich dir helfen?")
                
                elif self.conversation_active:
                    # Fortsetzung der Konversation
                    print(f"🗣️  Fortsetzung: {text}")
                    response = self.process_input_with_mcp(text)
                    self.speak(response)
                    self.last_activity = time.time()
                
                # Prüfe Timeout
                if self.conversation_active and (time.time() - self.last_activity) > self.conversation_timeout:
                    print("⏱️  Dialog-Fenster geschlossen.")
                    self.conversation_active = False
                
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f"❌ Spracherkennungsfehler: {e}")
                continue
            except Exception as e:
                print(f"❌ Fehler: {e}")
                continue

def main():
    """Hauptfunktion"""
    otto = OttoMCPSystem()
    otto.listen()

if __name__ == "__main__":
    main() 