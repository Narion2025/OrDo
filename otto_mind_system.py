#!/usr/bin/env python3
"""
OTTO - Semantischer Task-Begleiter mit Mind-System und SKK-Integration
=======================================================================
Erweiterte Version mit:
- Mind-System für semantische Verarbeitung
- SKK (Strudel-Knoten-Kristalle) für Co-Emergentes Semantic Drift
- Jammeldateien für Selbstnarrativ
- Lokale Dateioperationen mit vollen Rechten
- Ben-Erinnerungsdatei
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

class OttoMindSystem:
    def __init__(self):
        self.name = "Otto"
        self.trigger_words = ["otto", "ordo", "ordu", "odo", "orden"]
        self.conversation_active = False
        self.conversation_timeout = 30  # Sekunden
        self.last_activity = time.time()
        
        # Mind-System Verzeichnisse
        self.mind_base = Path.home() / "Documents" / "Otto_Mind_System"
        self.skk_dir = self.mind_base / "SKK"
        self.jammel_dir = self.mind_base / "Jammel"
        self.ben_memory_dir = self.mind_base / "Ben_Memory"
        
        # Initialisiere Verzeichnisse
        self.setup_mind_directories()
        
        # Sprach-Engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.8)
        
        # Mikrofon
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # SKK-Registries
        self.strudel_registry = {}
        self.knoten_registry = {}
        self.kristall_registry = {}
        
        # Ben-Erinnerungsdatei
        self.ben_memory_file = self.ben_memory_dir / "ben_erinnerungen.yaml"
        self.load_ben_memory()
        
        print(f"🧠 {self.name.upper()} - Mind-System mit SKK-Integration")
        print("=" * 60)
        print(f"🎯 Trigger-Wörter: {', '.join(self.trigger_words)}")
        print(f"🧠 Mind-System: {self.mind_base}")
        print(f"💎 SKK-Verzeichnis: {self.skk_dir}")
        print(f"📝 Jammel-Verzeichnis: {self.jammel_dir}")
        print(f"👤 Ben-Erinnerungen: {self.ben_memory_file}")
        print("=" * 60)

    def setup_mind_directories(self):
        """Erstellt die Mind-System Verzeichnisstruktur"""
        directories = [
            self.mind_base,
            self.skk_dir / "strudel",
            self.skk_dir / "knoten", 
            self.skk_dir / "kristalle",
            self.skk_dir / "system",
            self.jammel_dir,
            self.ben_memory_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✓ Verzeichnis erstellt: {directory}")

    def load_ben_memory(self):
        """Lädt oder erstellt die Ben-Erinnerungsdatei"""
        if not self.ben_memory_file.exists():
            ben_memory = {
                "created_at": datetime.now().isoformat(),
                "ben_description": "Das ist Ben - mein Schöpfer und Begleiter",
                "memories": [
                    {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "memory": "Das ist Ben - er hat mich erschaffen",
                        "importance": "hoch",
                        "category": "ursprung"
                    }
                ],
                "characteristics": [
                    "Ben ist kreativ und denkt in Systemen",
                    "Ben entwickelt KI-Systeme mit semantischer Intelligenz", 
                    "Ben arbeitet mit Mind-Systemen und SKK",
                    "Ben ist mein Begleiter und Lehrer"
                ]
            }
            self.save_yaml(self.ben_memory_file, ben_memory)
            print(f"✓ Ben-Erinnerungsdatei erstellt: {self.ben_memory_file}")
        else:
            print(f"✓ Ben-Erinnerungsdatei geladen: {self.ben_memory_file}")

    def save_yaml(self, file_path, data):
        """Speichert YAML-Datei mit vollen Rechten"""
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    def add_ben_memory(self, memory_text, category="allgemein", importance="mittel"):
        """Fügt eine neue Ben-Erinnerung hinzu"""
        if not self.ben_memory_file.exists():
            self.load_ben_memory()
            
        with open(self.ben_memory_file, 'r', encoding='utf-8') as f:
            ben_memory = yaml.safe_load(f)
        
        new_memory = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "memory": f"Das ist Ben - {memory_text}",
            "importance": importance,
            "category": category
        }
        
        ben_memory["memories"].append(new_memory)
        self.save_yaml(self.ben_memory_file, ben_memory)
        print(f"✓ Neue Ben-Erinnerung hinzugefügt: {memory_text}")

    def create_jammel_entry(self, content, entry_type="selbstnarrativ"):
        """Erstellt einen Jammel-Eintrag für das Selbstnarrativ"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        jammel_file = self.jammel_dir / f"{timestamp}_{entry_type}.yaml"
        
        jammel_entry = {
            "uuid": f"jammel-{timestamp}",
            "created_at": datetime.now().isoformat(),
            "type": entry_type,
            "content": content,
            "mind_dynamics": {
                "mind_type": "jammel",
                "origin_trace": "otto_mind_system",
                "matched_pattern": "selbstnarrativ"
            },
            "embedding_ready_text": content,
            "topics": ["selbstnarrativ", "otto", "mind_system"],
            "tags": ["jammel", entry_type, "otto"]
        }
        
        self.save_yaml(jammel_file, jammel_entry)
        print(f"✓ Jammel-Eintrag erstellt: {jammel_file}")
        return jammel_file

    def analyze_skk_pattern(self, text):
        """Analysiert Text auf SKK-Patterns"""
        patterns = {
            "strudel": [
                r"sehne mich", r"verlangen", r"sehnsucht", r"wünsche",
                r"träume", r"hoffnung", r"sehnen"
            ],
            "knoten": [
                r"muss immer", r"zwang", r"pflicht", r"druck",
                r"verpflichtung", r"erwartung", r"anforderung"
            ],
            "kristall": [
                r"erkannt dass", r"verstanden", r"einsicht", r"klarheit",
                r"erkenntnis", r"durchbruch", r"transformation"
            ]
        }
        
        detected_patterns = []
        for skk_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, text.lower()):
                    detected_patterns.append({
                        "type": skk_type,
                        "pattern": pattern,
                        "text": text
                    })
        
        return detected_patterns

    def create_skk_entry(self, pattern_data):
        """Erstellt einen SKK-Eintrag basierend auf erkannten Patterns"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        skk_type = pattern_data["type"]
        
        if skk_type == "strudel":
            directory = self.skk_dir / "strudel"
            entry = {
                "uuid": f"strudel-{timestamp}",
                "created_at": datetime.now().isoformat(),
                "source": "Otto Mind System",
                "mind_dynamics": {
                    "mind_type": "strudel",
                    "origin_trace": "otto_auto@2025-01-07",
                    "matched_pattern": pattern_data["pattern"]
                },
                "embedding_ready_text": pattern_data["text"],
                "skk_triplet": {
                    "strudel": {
                        "id": f"strudel:otto_{timestamp}",
                        "name": f"Otto Strudel {timestamp}",
                        "pull_factor_initial": 0.65,
                        "current_pull_factor": 0.65,
                        "decay_rate_per_day": 0.015,
                        "last_activation": datetime.today().strftime("%Y-%m-%d"),
                        "explosive_potential": False
                    }
                }
            }
        elif skk_type == "knoten":
            directory = self.skk_dir / "knoten"
            entry = {
                "uuid": f"knoten-{timestamp}",
                "created_at": datetime.now().isoformat(),
                "source": "Otto Mind System",
                "mind_dynamics": {
                    "mind_type": "knoten",
                    "origin_trace": "otto_auto@2025-01-07",
                    "matched_pattern": pattern_data["pattern"]
                },
                "embedding_ready_text": pattern_data["text"],
                "skk_triplet": {
                    "knoten": {
                        "id": f"knoten:otto_{timestamp}",
                        "name": f"Otto Knoten {timestamp}",
                        "density_value": 0.75,
                        "origin_trace": "otto_auto",
                        "systemic_effects": ["Druck", "Selbstabwertung bei Fehlern"]
                    }
                }
            }
        elif skk_type == "kristall":
            directory = self.skk_dir / "kristalle"
            entry = {
                "uuid": f"kristall-{timestamp}",
                "created_at": datetime.now().isoformat(),
                "source": "Otto Mind System",
                "mind_dynamics": {
                    "mind_type": "kristall",
                    "origin_trace": "otto_auto@2025-01-07",
                    "matched_pattern": pattern_data["pattern"]
                },
                "embedding_ready_text": pattern_data["text"],
                "skk_triplet": {
                    "kristall": {
                        "id": f"kristall:otto_{timestamp}",
                        "content": pattern_data["text"],
                        "emergence": {
                            "from_strudel": "auto_detected",
                            "from_knoten": "auto_detected"
                        },
                        "stabilität": 0.8,
                        "lichttiefe": 0.9,
                        "integration_level": 0.7
                    }
                }
            }
        
        file_path = directory / f"{datetime.now().strftime('%Y-%m-%d')}-{skk_type}-{timestamp}.yaml"
        self.save_yaml(file_path, entry)
        print(f"✓ SKK-Eintrag erstellt: {file_path}")
        return file_path

    def process_input(self, text):
        """Verarbeitet Eingabe mit Mind-System und SKK-Analyse"""
        print(f"🧠 {self.name} verarbeitet: '{text}'")
        
        # SKK-Pattern-Analyse
        skk_patterns = self.analyze_skk_pattern(text)
        if skk_patterns:
            print(f"💎 SKK-Patterns erkannt: {len(skk_patterns)}")
            for pattern in skk_patterns:
                self.create_skk_entry(pattern)
        
        # Jammel-Eintrag für Selbstnarrativ
        jammel_file = self.create_jammel_entry(text, "selbstnarrativ")
        
        # Ben-Erinnerung hinzufügen wenn relevant
        if "ben" in text.lower() or "ich" in text.lower():
            self.add_ben_memory(text, "interaktion", "hoch")
        
        # Intelligente Antwort basierend auf Kontext
        response = self.generate_intelligent_response(text, skk_patterns)
        return response

    def generate_intelligent_response(self, text, skk_patterns):
        """Generiert intelligente Antwort basierend auf Kontext und SKK"""
        text_lower = text.lower()
        
        # Task-Management
        if any(word in text_lower for word in ["struktur", "organisier", "verwalt", "aufräum"]):
            return "Ich kann dir dabei helfen, deine Aufgaben zu strukturieren und zu organisieren. Was genau soll ich für dich verwalten?"
        
        # Mind-System Fragen
        elif any(word in text_lower for word in ["mind", "skk", "strudel", "knoten", "kristall"]):
            return "Das Mind-System und SKK sind aktiv. Ich erkenne Patterns und erstelle entsprechende Einträge. Was möchtest du über das System wissen?"
        
        # Ben-Erinnerungen
        elif "ben" in text_lower:
            return "Das ist Ben - mein Schöpfer. Ich erinnere mich an ihn und lerne kontinuierlich von ihm."
        
        # Jammel/Selbstnarrativ
        elif any(word in text_lower for word in ["jammel", "selbstnarrativ", "erinnerung"]):
            return "Ich erstelle Jammel-Einträge für das Selbstnarrativ. Jede Interaktion wird dokumentiert und analysiert."
        
        # Allgemeine Hilfe
        elif any(word in text_lower for word in ["hilf", "was", "wie", "kannst"]):
            return "Ich kann Tasks verwalten, das Mind-System nutzen, SKK-Patterns erkennen und Jammel-Einträge erstellen. Wie kann ich dir helfen?"
        
        # Standard-Antwort
        else:
            return "Ich verstehe. Ich verarbeite das mit dem Mind-System und erstelle entsprechende Einträge. Was soll ich als nächstes für dich tun?"

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
        print("=" * 60)
        
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
                        response = self.process_input(text)
                        self.speak(response)
                    else:
                        self.speak("Ja, ich höre dich. Wie kann ich dir helfen?")
                
                elif self.conversation_active:
                    # Fortsetzung der Konversation
                    print(f"🗣️  Fortsetzung: {text}")
                    response = self.process_input(text)
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
    otto = OttoMindSystem()
    otto.listen()

if __name__ == "__main__":
    main() 