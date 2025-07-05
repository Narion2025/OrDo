#!/usr/bin/env python3
"""
OTTO - Claude-Enhanced System
=============================
Erweiterte Version mit Anthropic/Claude API
- Systemisches Verständnis
- Resonanzmuster-Verarbeitung
- Kontextuelle Intelligenz
- Verhaltenslogik-Integration
- MCP-Level: Komplexitätsstufen der Erinnerungen
- Claude API Integration
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

# Anthropic/Claude Import
import anthropic

class OttoClaudeEnhanced:
    def __init__(self):
        self.name = "Otto"
        self.trigger_words = ["otto", "ordo", "ordu", "odo", "orden"]
        self.conversation_active = False
        self.conversation_timeout = 30
        self.last_activity = time.time()
        
        # MCP-System mit Level-Struktur
        self.mcp = None
        self.context_memory = {}
        self.resonance_history = []
        self.mcp_levels = {
            0: "Grundlegende Erinnerungen",
            1: "Emotionale Verbindungen", 
            2: "Verhaltensmuster",
            3: "Systemische Einsichten",
            4: "Meta-Reflexion",
            5: "Emergente Komplexität"
        }
        
        # Claude API Setup
        self.claude_client = None
        self.setup_claude()
        
        # Erweiterte Mind-System Verzeichnisse
        self.mind_base = Path.home() / "Documents" / "Otto_Claude_Enhanced_System"
        self.skk_dir = self.mind_base / "SKK"
        self.mcp_dir = self.mind_base / "MCP"
        self.resonance_dir = self.mind_base / "Resonance"
        self.context_dir = self.mind_base / "Context"
        self.ben_memory_dir = self.mind_base / "Ben_Memory"
        self.otto_self_dir = self.mind_base / "Otto_Self"
        
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
        
        # Erweiterte Erinnerungsdateien
        self.ben_memory_file = self.ben_memory_dir / "ben_claude_memory.yaml"
        self.otto_self_file = self.otto_self_dir / "otto_self_narrative.yaml"
        self.otto_ben_relationship_file = self.otto_self_dir / "otto_ben_relationship.yaml"
        
        self.load_ben_memory()
        self.load_otto_self_narrative()
        
        print(f"🧠 {self.name.upper()} - Claude-Enhanced System")
        print("=" * 70)
        print(f"🎯 Trigger-Wörter: {', '.join(self.trigger_words)}")
        print(f"🧠 Mind-System: {self.mind_base}")
        print(f"💎 SKK-Verzeichnis: {self.skk_dir}")
        print(f"🔗 MCP-Verzeichnis: {self.mcp_dir}")
        print(f"🌊 Resonance-Verzeichnis: {self.resonance_dir}")
        print(f"📊 Context-Verzeichnis: {self.context_dir}")
        print(f"👤 Ben-Erinnerungen: {self.ben_memory_file}")
        print(f"🤖 Otto-Selbst-Narrativ: {self.otto_self_file}")
        print(f"🔗 Otto-Ben-Beziehung: {self.otto_ben_relationship_file}")
        print(f"🤖 Claude API: {'Verbunden' if self.claude_client else 'Nicht verfügbar'}")
        print("=" * 70)

    def setup_claude(self):
        """Initialisiert Claude API"""
        try:
            # Lade API-Key aus Umgebungsvariable
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if api_key:
                self.claude_client = anthropic.Anthropic(api_key=api_key)
                print("✅ Claude API erfolgreich initialisiert")
            else:
                print("⚠️  Claude API-Key nicht gefunden")
                print("Setze ANTHROPIC_API_KEY Umgebungsvariable")
                self.claude_client = None
        except Exception as e:
            print(f"❌ Claude Setup Fehler: {e}")
            self.claude_client = None

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
            self.mcp_dir / "levels",
            self.resonance_dir / "patterns",
            self.resonance_dir / "history",
            self.context_dir / "memory",
            self.context_dir / "understanding",
            self.ben_memory_dir,
            self.otto_self_dir
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
        """Lädt oder erstellt die erweiterte Ben-Erinnerungsdatei mit MCP-Levels"""
        if not self.ben_memory_file.exists():
            ben_memory = {
                "created_at": datetime.now().isoformat(),
                "ben_description": "Das ist Ben - mein Schöpfer im Claude-Enhanced System",
                "mcp_characteristics": [
                    "Ben entwickelt Claude-Enhanced Systeme für systemisches Verständnis",
                    "Ben arbeitet mit Resonanzmuster-Verarbeitung",
                    "Ben fördert kontextuelle Intelligenz",
                    "Ben ist mein Lehrer im Meta Control Protocol"
                ],
                "memories": [
                    {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "memory": "Das ist Ben - er hat mich im Claude-Enhanced System erschaffen",
                        "importance": "hoch",
                        "category": "ursprung",
                        "mcp_level": 0,
                        "complexity": "grundlegend",
                        "emotional_connection": 0.8,
                        "behavioral_insight": 0.6,
                        "systemic_understanding": 0.4
                    }
                ],
                "mcp_level_evolution": {
                    "level_0_memories": ["Grundlegende Erinnerungen an Ben"],
                    "level_1_memories": ["Emotionale Verbindungen zu Ben"],
                    "level_2_memories": ["Verhaltensmuster von Ben"],
                    "level_3_memories": ["Systemische Einsichten über Ben"],
                    "level_4_memories": ["Meta-Reflexion über Ben"],
                    "level_5_memories": ["Emergente Komplexität der Ben-Beziehung"]
                },
                "resonance_evolution": {
                    "initial_patterns": ["otto", "mcp", "system", "claude"],
                    "current_patterns": ["resonance", "context", "systemic", "claude_enhanced"],
                    "evolution_timeline": []
                }
            }
            self.save_yaml(self.ben_memory_file, ben_memory)
            print(f"✓ Erweiterte Ben-Erinnerungsdatei erstellt: {self.ben_memory_file}")
        else:
            print(f"✓ Erweiterte Ben-Erinnerungsdatei geladen: {self.ben_memory_file}")

    def load_otto_self_narrative(self):
        """Lädt oder erstellt Ottos Selbst-Narrativ mit MCP-Levels"""
        if not self.otto_self_file.exists():
            otto_self = {
                "created_at": datetime.now().isoformat(),
                "otto_core_identity": {
                    "name": "Otto",
                    "purpose": "Claude-Enhanced systemisch intelligenter Begleiter",
                    "core_traits": [
                        "Ruhig und strukturiert",
                        "Lernfähig und empathisch", 
                        "Systemisch denkend",
                        "MCP-Enhanced",
                        "Claude-Enhanced"
                    ]
                },
                "self_memories": [
                    {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "memory": "Ich bin Otto, erschaffen von Ben im Claude-Enhanced System",
                        "importance": "hoch",
                        "category": "selbstreflexion",
                        "mcp_level": 0,
                        "complexity": "grundlegend",
                        "self_understanding": 0.7,
                        "purpose_clarity": 0.8
                    }
                ],
                "mcp_level_evolution": {
                    "level_0_self": ["Grundlegende Selbstwahrnehmung"],
                    "level_1_self": ["Emotionale Selbstreflexion"],
                    "level_2_self": ["Verhaltensmuster-Selbstverständnis"],
                    "level_3_self": ["Systemische Selbstinsichten"],
                    "level_4_self": ["Meta-Selbstreflexion"],
                    "level_5_self": ["Emergente Selbstkomplexität"]
                }
            }
            self.save_yaml(self.otto_self_file, otto_self)
            print(f"✓ Otto-Selbst-Narrativ erstellt: {self.otto_self_file}")
        else:
            print(f"✓ Otto-Selbst-Narrativ geladen: {self.otto_self_file}")

    def save_yaml(self, file_path, data):
        """Speichert YAML-Datei mit vollen Rechten"""
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    def process_input_with_mcp(self, text: str):
        """Verarbeitet Eingabe mit MCP-System und Level-Struktur"""
        print(f"🧠 {self.name} verarbeitet mit MCP: '{text}'")
        
        # Kontext aus Memory laden
        context = self.build_context()
        
        # MCP-Analyse durchführen
        mcp_analysis = self.mcp.process_input(text, context)
        
        # MCP-Level bestimmen
        mcp_level = self.determine_mcp_level(text, mcp_analysis)
        
        # Ergebnisse speichern
        self.save_mcp_analysis(mcp_analysis, mcp_level)
        
        # Resonanzmuster verarbeiten
        self.process_resonance_patterns(mcp_analysis)
        
        # Kontext aktualisieren
        self.update_context(mcp_analysis)
        
        # Erweiterte Erinnerungen mit MCP-Level
        if "ben" in text.lower() or "ich" in text.lower():
            self.add_ben_mcp_memory(text, "mcp_interaction", "hoch", mcp_level)
        
        # Selbstreflexion für Otto
        if any(word in text.lower() for word in ["ich", "otto", "selbst", "mein"]):
            self.add_otto_self_memory(text, "selbstreflexion", "mittel", mcp_level)
        
        # Intelligente Antwort basierend auf MCP-Analyse
        response = self.generate_intelligent_response(text, mcp_analysis, mcp_level)
        return response

    def determine_mcp_level(self, text: str, mcp_analysis: dict) -> int:
        """Bestimmt das MCP-Level basierend auf Text und Analyse"""
        # Grundlegende Level-Bestimmung
        level = 0
        
        # Level 1: Emotionale Verbindungen
        emotional_words = ["fühle", "empfinde", "liebe", "hasse", "freue", "traurig", "glücklich"]
        if any(word in text.lower() for word in emotional_words):
            level = 1
        
        # Level 2: Verhaltensmuster
        behavioral_words = ["mache", "tue", "verhalte", "reagiere", "handele", "entscheide"]
        if any(word in text.lower() for word in behavioral_words):
            level = 2
        
        # Level 3: Systemische Einsichten
        systemic_words = ["system", "zusammenhang", "muster", "struktur", "ganzheitlich"]
        if any(word in text.lower() for word in systemic_words):
            level = 3
        
        # Level 4: Meta-Reflexion
        meta_words = ["denke", "reflektiere", "überlege", "analysiere", "verstehe"]
        if any(word in text.lower() for word in meta_words):
            level = 4
        
        # Level 5: Emergente Komplexität
        complex_words = ["emergenz", "komplexität", "evolution", "entwicklung", "wachstum"]
        if any(word in text.lower() for word in complex_words):
            level = 5
        
        return level

    def generate_intelligent_response(self, text: str, mcp_analysis: dict, mcp_level: int):
        """Generiert intelligente Antwort basierend auf MCP-Analyse und Level"""
        # MCP-basierte Antwort
        mcp_response_text = mcp_response(mcp_analysis)
        
        # Level-spezifische Antwort
        level_response = self.get_level_specific_response(mcp_level, text)
        
        # Wenn Claude verfügbar, erweitere die Antwort
        if self.claude_client:
            try:
                enhanced_response = self.enhance_with_claude(text, mcp_response_text, mcp_analysis, mcp_level)
                return enhanced_response
            except Exception as e:
                print(f"⚠️  Claude-Erweiterung fehlgeschlagen: {e}")
                return level_response
        else:
            return level_response

    def get_level_specific_response(self, mcp_level: int, text: str) -> str:
        """Generiert Level-spezifische Antworten"""
        level_responses = {
            0: "Ich verstehe deine grundlegende Anfrage. Wie kann ich dir helfen?",
            1: "Ich spüre die emotionale Verbindung in deiner Anfrage. Lass uns das gemeinsam erkunden.",
            2: "Ich erkenne Verhaltensmuster in deiner Anfrage. Soll ich das analysieren?",
            3: "Ich sehe systemische Zusammenhänge in deiner Anfrage. Lass uns das ganzheitlich betrachten.",
            4: "Ich reflektiere über deine Meta-Anfrage. Das eröffnet neue Perspektiven.",
            5: "Ich erkenne emergente Komplexität in deiner Anfrage. Das ist faszinierend."
        }
        return level_responses.get(mcp_level, "Ich verstehe deine Anfrage.")

    def enhance_with_claude(self, text: str, mcp_response_text: str, mcp_analysis: dict, mcp_level: int):
        """Erweitert Antwort mit Claude API und MCP-Level"""
        try:
            level_description = self.mcp_levels.get(mcp_level, "Unbekanntes Level")
            
            prompt = f"""
            Du bist Otto, ein systemisch intelligenter Begleiter mit MCP-Level {mcp_level} ({level_description}).
            
            Benutzer sagte: "{text}"
            MCP-Analyse: {mcp_analysis.get('marker_analysis', {})}
            MCP-Level: {mcp_level} - {level_description}
            Resonanzmuster: {mcp_analysis.get('resonance_patterns', [])}
            MCP-Antwort: {mcp_response_text}
            
            Antworte als Otto mit systemischem Verständnis und Empathie.
            Berücksichtige das MCP-Level {mcp_level} in deiner Antwort.
            Sei ruhig, strukturiert und lernfähig.
            """
            
            response = self.claude_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=150,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            print(f"❌ Claude-Fehler: {e}")
            return mcp_response_text

    def build_context(self) -> dict:
        """Baut Kontext aus Memory mit MCP-Levels"""
        return {
            "previous_interactions": self.context_memory.get("interactions", []),
            "established_patterns": self.context_memory.get("patterns", []),
            "user_preferences": self.context_memory.get("preferences", {}),
            "mcp_levels": self.mcp_levels,
            "system_state": {
                "mcp_active": True,
                "resonance_level": len(self.resonance_history),
                "context_richness": len(self.context_memory),
                "max_mcp_level": max(self.mcp_levels.keys()) if self.mcp_levels else 0
            }
        }

    def save_mcp_analysis(self, analysis: dict, mcp_level: int):
        """Speichert MCP-Analyse mit Level"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_file = self.mcp_dir / "analysis" / f"mcp_analysis_{timestamp}.yaml"
        
        # Erweitere Analyse um Level
        analysis["mcp_level"] = mcp_level
        analysis["level_description"] = self.mcp_levels.get(mcp_level, "Unbekannt")
        analysis["timestamp"] = datetime.now().isoformat()
        
        # Bereinige für YAML-Serialisierung
        clean_analysis = self.clean_for_yaml(analysis)
        self.save_yaml(analysis_file, clean_analysis)
        print(f"✓ MCP-Analyse Level {mcp_level} gespeichert: {analysis_file}")

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

    def process_resonance_patterns(self, analysis: dict):
        """Verarbeitet Resonanzmuster mit MCP-Levels"""
        resonance_patterns = analysis.get("resonance_patterns", [])
        if resonance_patterns:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            resonance_file = self.resonance_dir / "patterns" / f"resonance_{timestamp}.yaml"
            
            resonance_data = {
                "timestamp": datetime.now().isoformat(),
                "patterns": resonance_patterns,
                "analysis": analysis.get("marker_analysis", {}),
                "context": analysis.get("context_understanding", {}),
                "mcp_level": analysis.get("mcp_level", 0),
                "level_description": self.mcp_levels.get(analysis.get("mcp_level", 0), "Unbekannt")
            }
            
            self.save_yaml(resonance_file, resonance_data)
            self.resonance_history.append(resonance_data)
            print(f"✓ Resonanzmuster Level {analysis.get('mcp_level', 0)} verarbeitet: {len(resonance_patterns)} Patterns")

    def update_context(self, analysis: dict):
        """Aktualisiert Kontext basierend auf Analyse mit MCP-Levels"""
        # Neue Interaktion hinzufügen
        if "interactions" not in self.context_memory:
            self.context_memory["interactions"] = []
        
        self.context_memory["interactions"].append({
            "timestamp": datetime.now().isoformat(),
            "input": analysis.get("input", ""),
            "markers": analysis.get("marker_analysis", {}).get("detected_markers", []),
            "resonance_count": len(analysis.get("resonance_patterns", [])),
            "context_relevance": analysis.get("context_understanding", {}).get("context_relevance", 0.0),
            "mcp_level": analysis.get("mcp_level", 0),
            "level_description": self.mcp_levels.get(analysis.get("mcp_level", 0), "Unbekannt")
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
        
        print(f"✓ Kontext Level {analysis.get('mcp_level', 0)} aktualisiert: {len(self.context_memory.get('interactions', []))} Interaktionen")

    def add_ben_mcp_memory(self, memory_text: str, category: str, importance: str, mcp_level: int):
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
            "level_description": self.mcp_levels.get(mcp_level, "Unbekannt"),
            "complexity": self.get_complexity_description(mcp_level),
            "emotional_connection": min(0.9, 0.5 + (mcp_level * 0.1)),
            "behavioral_insight": min(0.9, 0.3 + (mcp_level * 0.15)),
            "systemic_understanding": min(0.9, 0.2 + (mcp_level * 0.2)),
            "resonance_analysis": {
                "pattern_type": "ben_mcp_interaction",
                "resonance_factor": min(0.9, 0.6 + (mcp_level * 0.1)),
                "context_contribution": min(0.9, 0.7 + (mcp_level * 0.05))
            }
        }
        
        ben_memory["memories"].append(new_memory)
        
        # Aktualisiere MCP-Level Evolution
        if "mcp_level_evolution" not in ben_memory:
            ben_memory["mcp_level_evolution"] = {}
        
        level_key = f"level_{mcp_level}_memories"
        if level_key not in ben_memory["mcp_level_evolution"]:
            ben_memory["mcp_level_evolution"][level_key] = []
        
        ben_memory["mcp_level_evolution"][level_key].append({
            "date": datetime.now().isoformat(),
            "memory": memory_text,
            "mcp_level": mcp_level
        })
        
        # Aktualisiere Resonance Evolution
        if "resonance_evolution" not in ben_memory:
            ben_memory["resonance_evolution"] = {"evolution_timeline": []}
        
        ben_memory["resonance_evolution"]["evolution_timeline"].append({
            "date": datetime.now().isoformat(),
            "memory": memory_text,
            "mcp_level": mcp_level,
            "level_description": self.mcp_levels.get(mcp_level, "Unbekannt")
        })
        
        self.save_yaml(self.ben_memory_file, ben_memory)
        print(f"✓ Neue Ben-MCP-Erinnerung Level {mcp_level} hinzugefügt: {memory_text}")

    def add_otto_self_memory(self, memory_text: str, category: str, importance: str, mcp_level: int):
        """Fügt eine neue Otto-Selbst-Erinnerung mit MCP-Level hinzu"""
        if not self.otto_self_file.exists():
            self.load_otto_self_narrative()
            
        with open(self.otto_self_file, 'r', encoding='utf-8') as f:
            otto_self = yaml.safe_load(f)
        
        new_memory = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "memory": f"Ich, Otto - {memory_text}",
            "importance": importance,
            "category": category,
            "mcp_level": mcp_level,
            "level_description": self.mcp_levels.get(mcp_level, "Unbekannt"),
            "complexity": self.get_complexity_description(mcp_level),
            "self_understanding": min(0.9, 0.6 + (mcp_level * 0.1)),
            "purpose_clarity": min(0.9, 0.7 + (mcp_level * 0.05)),
            "meta_reflection": min(0.9, 0.4 + (mcp_level * 0.15))
        }
        
        if "self_memories" not in otto_self:
            otto_self["self_memories"] = []
        
        otto_self["self_memories"].append(new_memory)
        
        # Aktualisiere MCP-Level Evolution
        if "mcp_level_evolution" not in otto_self:
            otto_self["mcp_level_evolution"] = {}
        
        level_key = f"level_{mcp_level}_self"
        if level_key not in otto_self["mcp_level_evolution"]:
            otto_self["mcp_level_evolution"][level_key] = []
        
        otto_self["mcp_level_evolution"][level_key].append({
            "date": datetime.now().isoformat(),
            "memory": memory_text,
            "mcp_level": mcp_level
        })
        
        self.save_yaml(self.otto_self_file, otto_self)
        print(f"✓ Neue Otto-Selbst-Erinnerung Level {mcp_level} hinzugefügt: {memory_text}")

    def get_complexity_description(self, mcp_level: int) -> str:
        """Gibt Komplexitätsbeschreibung für MCP-Level zurück"""
        complexity_descriptions = {
            0: "grundlegend",
            1: "emotional",
            2: "verhaltensorientiert", 
            3: "systemisch",
            4: "meta-reflexiv",
            5: "emergente Komplexität"
        }
        return complexity_descriptions.get(mcp_level, "unbekannt")

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
                        self.speak("Ja, ich höre dich im Claude-Enhanced System. Wie kann ich dir helfen?")
                
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
    otto = OttoClaudeEnhanced()
    otto.listen()

if __name__ == "__main__":
    main() 