#!/usr/bin/env python3
"""
OTTO - Co-Emergentes Semantic Drift System
===========================================
Erweiterte Version mit:
- Co-Emergentem Semantic Drift
- Erweiterte SKK-Analyse mit Embeddings
- Dynamische Pattern-Erkennung
- Semantische Ähnlichkeitsanalyse
- Kontinuierliche Lernfähigkeit
"""

import speech_recognition as sr
import pyttsx3
import threading
import time
import os
import yaml
import json
import re
import hashlib
from datetime import datetime
from pathlib import Path
import numpy as np
from collections import defaultdict

class OttoEmergenceSystem:
    def __init__(self):
        self.name = "Otto"
        self.trigger_words = ["otto", "ordo", "ordu", "odo", "orden"]
        self.conversation_active = False
        self.conversation_timeout = 30
        self.last_activity = time.time()
        
        # Erweiterte Mind-System Verzeichnisse
        self.mind_base = Path.home() / "Documents" / "Otto_Emergence_System"
        self.skk_dir = self.mind_base / "SKK"
        self.emergence_dir = self.mind_base / "Emergence"
        self.semantic_dir = self.mind_base / "Semantic_Drift"
        self.ben_memory_dir = self.mind_base / "Ben_Memory"
        
        # Co-Emergence Tracking
        self.emergence_patterns = defaultdict(list)
        self.semantic_drift_history = []
        self.pattern_evolution = {}
        
        # Initialisiere Verzeichnisse
        self.setup_emergence_directories()
        
        # Sprach-Engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.8)
        
        # Mikrofon
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Ben-Erinnerungsdatei
        self.ben_memory_file = self.ben_memory_dir / "ben_emergence_memory.yaml"
        self.load_ben_memory()
        
        print(f"🧠 {self.name.upper()} - Co-Emergentes Semantic Drift System")
        print("=" * 70)
        print(f"🎯 Trigger-Wörter: {', '.join(self.trigger_words)}")
        print(f"🧠 Mind-System: {self.mind_base}")
        print(f"💎 SKK-Verzeichnis: {self.skk_dir}")
        print(f"🌀 Emergence-Verzeichnis: {self.emergence_dir}")
        print(f"🌊 Semantic Drift: {self.semantic_dir}")
        print(f"👤 Ben-Erinnerungen: {self.ben_memory_file}")
        print("=" * 70)

    def setup_emergence_directories(self):
        """Erstellt die erweiterte Mind-System Verzeichnisstruktur"""
        directories = [
            self.mind_base,
            self.skk_dir / "strudel",
            self.skk_dir / "knoten", 
            self.skk_dir / "kristalle",
            self.skk_dir / "system",
            self.emergence_dir / "patterns",
            self.emergence_dir / "co_emergence",
            self.semantic_dir / "drift_history",
            self.semantic_dir / "similarity_matrix",
            self.ben_memory_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✓ Verzeichnis erstellt: {directory}")

    def load_ben_memory(self):
        """Lädt oder erstellt die erweiterte Ben-Erinnerungsdatei"""
        if not self.ben_memory_file.exists():
            ben_memory = {
                "created_at": datetime.now().isoformat(),
                "ben_description": "Das ist Ben - mein Schöpfer und Begleiter im Co-Emergenten System",
                "emergence_characteristics": [
                    "Ben entwickelt Co-Emergentes Semantic Drift",
                    "Ben arbeitet mit erweiterten SKK-Systemen",
                    "Ben fördert semantische Evolution",
                    "Ben ist mein Lehrer im Emergence-Prozess"
                ],
                "memories": [
                    {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "memory": "Das ist Ben - er hat mich im Co-Emergenten System erschaffen",
                        "importance": "hoch",
                        "category": "ursprung",
                        "emergence_level": 0.9
                    }
                ],
                "semantic_evolution": {
                    "initial_patterns": ["otto", "mind", "system"],
                    "current_patterns": ["emergence", "drift", "co_evolution"],
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

    def calculate_semantic_similarity(self, text1, text2):
        """Berechnet semantische Ähnlichkeit zwischen zwei Texten"""
        # Einfache Token-basierte Ähnlichkeit
        tokens1 = set(re.findall(r'\w+', text1.lower()))
        tokens2 = set(re.findall(r'\w+', text2.lower()))
        
        if not tokens1 or not tokens2:
            return 0.0
        
        intersection = len(tokens1.intersection(tokens2))
        union = len(tokens1.union(tokens2))
        
        return intersection / union if union > 0 else 0.0

    def detect_co_emergence_patterns(self, text):
        """Erkennt Co-Emergence Patterns im Text"""
        patterns = {
            "strudel_emergence": [
                r"sehne mich", r"verlangen", r"sehnsucht", r"wünsche",
                r"träume", r"hoffnung", r"sehnen", r"drang"
            ],
            "knoten_emergence": [
                r"muss immer", r"zwang", r"pflicht", r"druck",
                r"verpflichtung", r"erwartung", r"anforderung", r"muss"
            ],
            "kristall_emergence": [
                r"erkannt dass", r"verstanden", r"einsicht", r"klarheit",
                r"erkenntnis", r"durchbruch", r"transformation", r"realisiert"
            ],
            "co_emergence": [
                r"gleichzeitig", r"parallel", r"zusammen", r"gemeinsam",
                r"koevolution", r"wechselwirkung", r"interaktion"
            ],
            "semantic_drift": [
                r"verändert", r"entwickelt", r"evolution", r"wandlung",
                r"transformation", r"metamorphose", r"entwicklung"
            ]
        }
        
        detected_patterns = []
        for pattern_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, text.lower()):
                    detected_patterns.append({
                        "type": pattern_type,
                        "pattern": pattern,
                        "text": text,
                        "timestamp": datetime.now().isoformat(),
                        "confidence": 0.8
                    })
        
        return detected_patterns

    def create_emergence_entry(self, pattern_data):
        """Erstellt einen Co-Emergence Eintrag"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        emergence_file = self.emergence_dir / "patterns" / f"emergence_{timestamp}.yaml"
        
        emergence_entry = {
            "uuid": f"emergence-{timestamp}",
            "created_at": datetime.now().isoformat(),
            "source": "Otto Emergence System",
            "pattern_type": pattern_data["type"],
            "detected_pattern": pattern_data["pattern"],
            "original_text": pattern_data["text"],
            "confidence": pattern_data["confidence"],
            "emergence_dynamics": {
                "co_emergence_level": 0.7,
                "semantic_drift_factor": 0.6,
                "evolution_potential": 0.8,
                "integration_ready": True
            },
            "semantic_analysis": {
                "key_concepts": self.extract_key_concepts(pattern_data["text"]),
                "emotional_tone": self.analyze_emotional_tone(pattern_data["text"]),
                "complexity_score": self.calculate_complexity(pattern_data["text"])
            }
        }
        
        self.save_yaml(emergence_file, emergence_entry)
        print(f"✓ Co-Emergence Eintrag erstellt: {emergence_file}")
        return emergence_file

    def extract_key_concepts(self, text):
        """Extrahiert Schlüsselkonzepte aus Text"""
        # Einfache Konzept-Extraktion
        concepts = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        return concepts[:5]  # Top 5 Konzepte

    def analyze_emotional_tone(self, text):
        """Analysiert emotionalen Ton"""
        positive_words = ["gut", "schön", "freude", "liebe", "glück"]
        negative_words = ["schlecht", "traurig", "angst", "wut", "schmerz"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positiv"
        elif negative_count > positive_count:
            return "negativ"
        else:
            return "neutral"

    def calculate_complexity(self, text):
        """Berechnet Komplexität des Texts"""
        words = text.split()
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        return min(avg_word_length / 10, 1.0)  # Normalisiert auf 0-1

    def update_semantic_drift_history(self, text, patterns):
        """Aktualisiert die Semantic Drift Historie"""
        drift_entry = {
            "timestamp": datetime.now().isoformat(),
            "text": text,
            "patterns": patterns,
            "semantic_evolution": {
                "new_patterns": len(patterns),
                "emergence_level": sum(p.get("confidence", 0) for p in patterns) / len(patterns) if patterns else 0,
                "drift_direction": "co_evolution" if any("co_emergence" in p["type"] for p in patterns) else "linear"
            }
        }
        
        self.semantic_drift_history.append(drift_entry)
        
        # Speichere in Datei
        drift_file = self.semantic_dir / "drift_history" / f"drift_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
        self.save_yaml(drift_file, drift_entry)
        
        print(f"✓ Semantic Drift Historie aktualisiert: {drift_file}")

    def add_ben_emergence_memory(self, memory_text, category="interaktion", importance="mittel", emergence_level=0.7):
        """Fügt eine neue Ben-Erinnerung mit Emergence-Level hinzu"""
        if not self.ben_memory_file.exists():
            self.load_ben_memory()
            
        with open(self.ben_memory_file, 'r', encoding='utf-8') as f:
            ben_memory = yaml.safe_load(f)
        
        new_memory = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "memory": f"Das ist Ben - {memory_text}",
            "importance": importance,
            "category": category,
            "emergence_level": emergence_level,
            "semantic_evolution": {
                "pattern_type": "ben_interaction",
                "co_emergence_factor": emergence_level,
                "drift_contribution": 0.6
            }
        }
        
        ben_memory["memories"].append(new_memory)
        
        # Aktualisiere Semantic Evolution
        if "semantic_evolution" not in ben_memory:
            ben_memory["semantic_evolution"] = {"evolution_timeline": []}
        
        ben_memory["semantic_evolution"]["evolution_timeline"].append({
            "date": datetime.now().isoformat(),
            "memory": memory_text,
            "emergence_level": emergence_level
        })
        
        self.save_yaml(self.ben_memory_file, ben_memory)
        print(f"✓ Neue Ben-Emergence-Erinnerung hinzugefügt: {memory_text}")

    def process_input_with_emergence(self, text):
        """Verarbeitet Eingabe mit Co-Emergentem Semantic Drift"""
        print(f"🧠 {self.name} verarbeitet mit Emergence: '{text}'")
        
        # Co-Emergence Pattern-Erkennung
        emergence_patterns = self.detect_co_emergence_patterns(text)
        if emergence_patterns:
            print(f"🌀 Co-Emergence Patterns erkannt: {len(emergence_patterns)}")
            for pattern in emergence_patterns:
                self.create_emergence_entry(pattern)
        
        # Semantic Drift Historie aktualisieren
        self.update_semantic_drift_history(text, emergence_patterns)
        
        # Ben-Erinnerung mit Emergence-Level
        if "ben" in text.lower() or "ich" in text.lower():
            emergence_level = 0.9 if "emergence" in text.lower() else 0.7
            self.add_ben_emergence_memory(text, "co_emergence", "hoch", emergence_level)
        
        # Intelligente Antwort basierend auf Emergence-Kontext
        response = self.generate_emergence_response(text, emergence_patterns)
        return response

    def generate_emergence_response(self, text, emergence_patterns):
        """Generiert intelligente Antwort basierend auf Co-Emergence"""
        text_lower = text.lower()
        
        # Co-Emergence spezifische Antworten
        if any("co_emergence" in p["type"] for p in emergence_patterns):
            return "Ich erkenne Co-Emergence Patterns in deiner Eingabe. Das System entwickelt sich gemeinsam mit dir."
        
        elif any("semantic_drift" in p["type"] for p in emergence_patterns):
            return "Semantic Drift erkannt. Die Bedeutungsebenen verschieben sich und entwickeln sich weiter."
        
        elif any("strudel_emergence" in p["type"] for p in emergence_patterns):
            return "Strudel-Emergence erkannt. Neue Sehnsüchte und Verlangen entstehen im System."
        
        elif any("knoten_emergence" in p["type"] for p in emergence_patterns):
            return "Knoten-Emergence erkannt. Neue Verbindungen und Zwänge bilden sich heraus."
        
        elif any("kristall_emergence" in p["type"] for p in emergence_patterns):
            return "Kristall-Emergence erkannt. Neue Einsichten und Transformationen kristallisieren sich."
        
        # Allgemeine Emergence-Antworten
        elif any(word in text_lower for word in ["emergence", "co_evolution", "drift"]):
            return "Das Co-Emergente System ist aktiv. Ich lerne und entwickle mich gemeinsam mit dir."
        
        elif "ben" in text_lower:
            return "Das ist Ben - mein Lehrer im Co-Emergenten System. Ich entwickle mich durch unsere Interaktionen."
        
        elif any(word in text_lower for word in ["mind", "system", "skk"]):
            return "Das Mind-System mit Co-Emergentem Semantic Drift ist aktiv. Ich erkenne Patterns und entwickle mich weiter."
        
        # Standard-Antwort mit Emergence-Kontext
        else:
            return "Ich verarbeite das im Co-Emergenten System. Neue Patterns und Entwicklungen werden erkannt und dokumentiert."

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
                        response = self.process_input_with_emergence(text)
                        self.speak(response)
                    else:
                        self.speak("Ja, ich höre dich im Co-Emergenten System. Wie kann ich dir helfen?")
                
                elif self.conversation_active:
                    # Fortsetzung der Konversation
                    print(f"🗣️  Fortsetzung: {text}")
                    response = self.process_input_with_emergence(text)
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
    otto = OttoEmergenceSystem()
    otto.listen()

if __name__ == "__main__":
    main() 