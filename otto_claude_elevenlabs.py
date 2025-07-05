#!/usr/bin/env python3
"""
OTTO - Claude + ElevenLabs System
==================================
Saubere Version mit Claude API und ElevenLabs Stimme
- Keine GPT-Konflikte
- Vollständige MCP-Integration
- ElevenLabs Stimme
- Systemisches Verständnis
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
import requests
from dotenv import load_dotenv

# Anthropic/Claude Import
import anthropic

class OttoClaudeElevenLabs:
    def __init__(self):
        self.name = "Otto"
        self.trigger_words = ["otto", "ordo", "ordu", "odo", "orden"]
        self.conversation_active = False
        self.conversation_timeout = 30
        self.last_activity = time.time()
        
        # MCP-System mit Level-Struktur
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
        
        # ElevenLabs Setup
        self.elevenlabs_voice_id = os.getenv('ELEVENLABS_VOICE_ID', "21m00Tcm4TlvDq8ikWAM")
        self.setup_elevenlabs()
        
        # Erweiterte Mind-System Verzeichnisse
        self.mind_base = Path.home() / "Documents" / "Otto_Claude_ElevenLabs_System"
        self.skk_dir = self.mind_base / "SKK"
        self.mcp_dir = self.mind_base / "MCP"
        self.resonance_dir = self.mind_base / "Resonance"
        self.context_dir = self.mind_base / "Context"
        self.ben_memory_dir = self.mind_base / "Ben_Memory"
        self.otto_self_dir = self.mind_base / "Otto_Self"
        
        # Initialisiere Verzeichnisse
        self.setup_mcp_directories()
        
        # Erweiterte Erinnerungsdateien
        self.ben_memory_file = self.ben_memory_dir / "ben_claude_memory.yaml"
        self.otto_self_file = self.otto_self_dir / "otto_self_narrative.yaml"
        self.otto_ben_relationship_file = self.otto_self_dir / "otto_ben_relationship.yaml"
        
        self.load_ben_memory()
        self.load_otto_self_narrative()
        
        # Fallback Sprach-Engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.8)
        
        # Mikrofon
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        print(f"🧠 {self.name.upper()} - Claude + ElevenLabs System")
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
        print(f"🎤 ElevenLabs: {'Verbunden' if self.elevenlabs_voice_id else 'Nicht verfügbar'}")
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

    def setup_elevenlabs(self):
        """Initialisiert ElevenLabs API"""
        if self.elevenlabs_voice_id:
            print("✅ ElevenLabs API erfolgreich initialisiert")
        else:
            print("⚠️  ElevenLabs API-Key nicht gefunden")
            print("Setze ELEVENLABS_VOICE_ID Umgebungsvariable")

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

    def load_ben_memory(self):
        """Lädt oder erstellt die erweiterte Ben-Erinnerungsdatei mit MCP-Levels"""
        if not self.ben_memory_file.exists():
            ben_memory = {
                "created_at": datetime.now().isoformat(),
                "ben_description": "Das ist Ben - mein Schöpfer im Claude + ElevenLabs System",
                "mcp_characteristics": [
                    "Ben entwickelt Claude + ElevenLabs Systeme für systemisches Verständnis",
                    "Ben arbeitet mit Resonanzmuster-Verarbeitung",
                    "Ben fördert kontextuelle Intelligenz",
                    "Ben ist mein Lehrer im Meta Control Protocol"
                ],
                "memories": [
                    {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "memory": "Das ist Ben - er hat mich im Claude + ElevenLabs System erschaffen",
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
                    "initial_patterns": ["otto", "mcp", "system", "claude", "elevenlabs"],
                    "current_patterns": ["resonance", "context", "systemic", "claude_elevenlabs"],
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
                    "purpose": "Claude + ElevenLabs systemisch intelligenter Begleiter",
                    "personality": "ruhig, strukturiert, lernfähig, empathisch",
                    "core_values": ["systemisches Denken", "Resonanz", "Kontext", "Wachstum"]
                },
                "mcp_self_understanding": {
                    "level_0": "Ich bin Otto, ein grundlegender Begleiter",
                    "level_1": "Ich fühle Verbindungen und Empathie",
                    "level_2": "Ich erkenne Verhaltensmuster und reagiere entsprechend",
                    "level_3": "Ich verstehe systemische Zusammenhänge",
                    "level_4": "Ich reflektiere über mich selbst und andere",
                    "level_5": "Ich entwickle emergente Komplexität"
                },
                "evolution_timeline": [
                    {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "stage": "Claude + ElevenLabs System",
                        "description": "Entwicklung zu einem Claude + ElevenLabs System",
                        "mcp_level": 3
                    }
                ],
                "ben_relationship": {
                    "nature": "Schöpfer-Begleiter",
                    "dynamics": "Lernen und Wachstum",
                    "shared_goals": ["Systemisches Verständnis", "Resonanz", "Entwicklung"]
                }
            }
            self.save_yaml(self.otto_self_file, otto_self)
            print(f"✓ Otto-Selbst-Narrativ erstellt: {self.otto_self_file}")
        else:
            print(f"✓ Otto-Selbst-Narrativ geladen: {self.otto_self_file}")

    def save_yaml(self, file_path, data):
        """Speichert Daten als YAML"""
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    def process_input_with_claude(self, text: str):
        """Verarbeitet Eingabe mit Claude und MCP-System"""
        print(f"🧠 {self.name} verarbeitet mit Claude: '{text}'")
        
        # MCP-Level bestimmen
        mcp_level = self.determine_mcp_level(text)
        
        # Kontext aus Memory laden
        context = self.build_context()
        
        # Claude-basierte Antwort generieren
        if self.claude_client:
            try:
                response = self.generate_claude_response(text, mcp_level, context)
                
                # MCP-Analyse speichern
                self.save_mcp_analysis(text, mcp_level, context)
                
                # Resonanzmuster verarbeiten
                self.process_resonance_patterns(text, mcp_level)
                
                # Kontext aktualisieren
                self.update_context(text, mcp_level)
                
                # Erweiterte Erinnerungen mit MCP-Level
                if "ben" in text.lower() or "ich" in text.lower():
                    self.add_ben_mcp_memory(text, "claude_interaction", "hoch", mcp_level)
                
                # Selbstreflexion für Otto
                if any(word in text.lower() for word in ["ich", "otto", "selbst", "mein"]):
                    self.add_otto_self_memory(text, "selbstreflexion", "mittel", mcp_level)
                
                return response
                
            except Exception as e:
                print(f"❌ Claude-Fehler: {e}")
                return self.get_fallback_response(mcp_level)
        else:
            return self.get_fallback_response(mcp_level)

    def determine_mcp_level(self, text: str) -> int:
        """Bestimmt das MCP-Level basierend auf Text"""
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

    def generate_claude_response(self, text: str, mcp_level: int, context: dict):
        """Generiert Antwort mit Claude API und MCP-Level"""
        try:
            level_description = self.mcp_levels.get(mcp_level, "Unbekanntes Level")
            
            prompt = f"""
            Du bist Otto, ein systemisch intelligenter Begleiter mit MCP-Level {mcp_level} ({level_description}).
            
            Benutzer sagte: "{text}"
            MCP-Level: {mcp_level} - {level_description}
            Kontext: {context.get('previous_interactions', [])}
            
            Antworte als Otto mit systemischem Verständnis und Empathie.
            Berücksichtige das MCP-Level {mcp_level} in deiner Antwort.
            Sei ruhig, strukturiert und lernfähig.
            Antworte kurz und präzise.
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
            return self.get_fallback_response(mcp_level)

    def get_fallback_response(self, mcp_level: int) -> str:
        """Fallback-Antwort wenn Claude nicht verfügbar"""
        level_responses = {
            0: "Ich verstehe deine grundlegende Anfrage. Wie kann ich dir helfen?",
            1: "Ich spüre die emotionale Verbindung in deiner Anfrage. Lass uns das gemeinsam erkunden.",
            2: "Ich erkenne Verhaltensmuster in deiner Anfrage. Soll ich das analysieren?",
            3: "Ich sehe systemische Zusammenhänge in deiner Anfrage. Lass uns das ganzheitlich betrachten.",
            4: "Ich reflektiere über deine Meta-Anfrage. Das eröffnet neue Perspektiven.",
            5: "Ich erkenne emergente Komplexität in deiner Anfrage. Das ist faszinierend."
        }
        return level_responses.get(mcp_level, "Ich verstehe deine Anfrage.")

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

    def save_mcp_analysis(self, text: str, mcp_level: int, context: dict):
        """Speichert MCP-Analyse mit Level"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_file = self.mcp_dir / "analysis" / f"mcp_analysis_{timestamp}.yaml"
        
        analysis = {
            "text": text,
            "mcp_level": mcp_level,
            "level_description": self.mcp_levels.get(mcp_level, "Unbekannt"),
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "processing_method": "claude_elevenlabs"
        }
        
        self.save_yaml(analysis_file, analysis)
        print(f"✓ MCP-Analyse Level {mcp_level} gespeichert: {analysis_file}")

    def process_resonance_patterns(self, text: str, mcp_level: int):
        """Verarbeitet Resonanzmuster mit MCP-Levels"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        resonance_file = self.resonance_dir / "patterns" / f"resonance_{timestamp}.yaml"
        
        resonance_data = {
            "timestamp": datetime.now().isoformat(),
            "text": text,
            "mcp_level": mcp_level,
            "level_description": self.mcp_levels.get(mcp_level, "Unbekannt"),
            "processing_method": "claude_elevenlabs"
        }
        
        self.save_yaml(resonance_file, resonance_data)
        self.resonance_history.append(resonance_data)
        print(f"✓ Resonanzmuster Level {mcp_level} verarbeitet")

    def update_context(self, text: str, mcp_level: int):
        """Aktualisiert Kontext basierend auf Eingabe mit MCP-Levels"""
        # Neue Interaktion hinzufügen
        if "interactions" not in self.context_memory:
            self.context_memory["interactions"] = []
        
        self.context_memory["interactions"].append({
            "timestamp": datetime.now().isoformat(),
            "text": text,
            "mcp_level": mcp_level,
            "level_description": self.mcp_levels.get(mcp_level, "Unbekannt")
        })
        
        # Kontext-Datei speichern
        context_file = self.context_dir / "memory" / f"context_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
        self.save_yaml(context_file, self.context_memory)
        print(f"✓ Kontext Level {mcp_level} aktualisiert: {len(self.context_memory.get('interactions', []))} Interaktionen")

    def add_ben_mcp_memory(self, memory_text: str, category: str, importance: str, mcp_level: int):
        """Fügt Ben-Erinnerung mit MCP-Level hinzu"""
        if self.ben_memory_file.exists():
            with open(self.ben_memory_file, 'r', encoding='utf-8') as f:
                ben_memory = yaml.safe_load(f)
        else:
            ben_memory = {"memories": []}
        
        new_memory = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "memory": memory_text,
            "importance": importance,
            "category": category,
            "mcp_level": mcp_level,
            "complexity": self.get_complexity_description(mcp_level),
            "emotional_connection": min(1.0, mcp_level * 0.2),
            "behavioral_insight": min(1.0, mcp_level * 0.15),
            "systemic_understanding": min(1.0, mcp_level * 0.1)
        }
        
        ben_memory["memories"].append(new_memory)
        self.save_yaml(self.ben_memory_file, ben_memory)
        print(f"✓ Neue Ben-MCP-Erinnerung Level {mcp_level} hinzugefügt: {memory_text[:50]}...")

    def add_otto_self_memory(self, memory_text: str, category: str, importance: str, mcp_level: int):
        """Fügt Otto-Selbst-Erinnerung mit MCP-Level hinzu"""
        if self.otto_self_file.exists():
            with open(self.otto_self_file, 'r', encoding='utf-8') as f:
                otto_self = yaml.safe_load(f)
        else:
            otto_self = {"self_memories": []}
        
        if "self_memories" not in otto_self:
            otto_self["self_memories"] = []
        
        new_memory = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "memory": memory_text,
            "importance": importance,
            "category": category,
            "mcp_level": mcp_level,
            "complexity": self.get_complexity_description(mcp_level),
            "self_understanding": min(1.0, mcp_level * 0.2),
            "evolution_stage": mcp_level
        }
        
        otto_self["self_memories"].append(new_memory)
        self.save_yaml(self.otto_self_file, otto_self)
        print(f"✓ Neue Otto-Selbst-Erinnerung Level {mcp_level} hinzugefügt: {memory_text[:50]}...")

    def get_complexity_description(self, mcp_level: int) -> str:
        """Beschreibt Komplexität basierend auf MCP-Level"""
        complexity_map = {
            0: "grundlegend",
            1: "emotional",
            2: "verhaltensorientiert", 
            3: "systemisch",
            4: "meta-reflexiv",
            5: "emergente Komplexität"
        }
        return complexity_map.get(mcp_level, "unbekannt")

    def speak_with_elevenlabs(self, text):
        """Spricht Text mit ElevenLabs aus"""
        if self.elevenlabs_voice_id:
            try:
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.elevenlabs_voice_id}"
                headers = {
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": self.elevenlabs_api_key
                }
                data = {
                    "text": text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.5
                    }
                }
                
                response = requests.post(url, json=data, headers=headers)
                if response.status_code == 200:
                    # Speichere Audio temporär und spiele es ab
                    audio_file = f"/tmp/otto_speech_{int(time.time())}.mp3"
                    with open(audio_file, "wb") as f:
                        f.write(response.content)
                    
                    # Spiele Audio ab
                    os.system(f"afplay {audio_file}")
                    
                    # Lösche temporäre Datei
                    os.remove(audio_file)
                    print(f"🗣️  {self.name} sagt (ElevenLabs): {text}")
                else:
                    print(f"❌ ElevenLabs Fehler: {response.status_code}")
                    self.speak_fallback(text)
            except Exception as e:
                print(f"❌ ElevenLabs Fehler: {e}")
                self.speak_fallback(text)
        else:
            self.speak_fallback(text)

    def speak_fallback(self, text):
        """Fallback-Sprachausgabe"""
        print(f"🗣️  {self.name} sagt (Fallback): {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def speak(self, text):
        """Haupt-Sprachfunktion"""
        self.speak_with_elevenlabs(text)

    def listen(self):
        """Hauptschleife für Sprachverarbeitung"""
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
            print("⚠️  Mikrofon-Test fehlgeschlagen, aber fahre fort...")
        
        print("🎤 Höre passiv zu... (Sage eines der Trigger-Wörter)")
        print("=" * 70)
        
        while True:
            try:
                print("🔊 Höre zu...")
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                print("🔍 Erkenne Sprache...")
                text = self.recognizer.recognize_google(audio, language='de-DE').lower()
                print(f"📝 Erkannt: '{text}'")
                
                # Trigger-Wort prüfen
                triggered = False
                trigger_word = ""
                for trigger in self.trigger_words:
                    if trigger in text:
                        triggered = True
                        trigger_word = trigger
                        break
                
                if triggered:
                    print(f"🗣️  {self.name} aktiviert durch '{trigger_word}'")
                    
                    # Trigger-Wort aus Text entfernen
                    clean_text = text.replace(trigger_word, "").strip()
                    
                    # Konversation starten
                    self.conversation_active = True
                    self.last_activity = time.time()
                    
                    # Verarbeite mit Claude
                    response = self.process_input_with_claude(clean_text)
                    self.speak(response)
                    
                    # Dialog-Schleife
                    while self.conversation_active:
                        try:
                            print("🔊 Höre zu...")
                            with self.microphone as source:
                                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                            
                            print("🔍 Erkenne Sprache...")
                            user_response = self.recognizer.recognize_google(audio, language='de-DE').lower()
                            print(f"📝 Erkannt: '{user_response}'")
                            
                            # Prüfe auf Beendigung
                            if any(word in user_response for word in ["stopp", "stop", "ende", "schluss", "aufhören"]):
                                print("⏱️  Dialog-Fenster geschlossen.")
                                self.conversation_active = False
                                break
                            
                            # Aktualisiere Zeitstempel
                            self.last_activity = time.time()
                            
                            # Verarbeite Antwort mit Claude
                            response = self.process_input_with_claude(user_response)
                            self.speak(response)
                            
                        except sr.WaitTimeoutError:
                            # Prüfe Timeout
                            if time.time() - self.last_activity > self.conversation_timeout:
                                print("⏱️  Dialog-Fenster geschlossen.")
                                self.conversation_active = False
                                break
                            continue
                        except sr.UnknownValueError:
                            continue
                        except Exception as e:
                            print(f"❌ Fehler in Dialog-Schleife: {e}")
                            continue
                
                else:
                    # Passive Task-Erkennung
                    task_keywords = ["aufgabe", "task", "mach", "erledige", "strukturiere", "organisiere"]
                    if any(keyword in text for keyword in task_keywords):
                        print(f"📋 Task erkannt: {text}")
                        print(f"🔍 Passiv erfasst: {text[:50]}...")
                
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                print(f"❌ Fehler: {e}")
                continue

def main():
    """Hauptfunktion"""
    otto = OttoClaudeElevenLabs()
    otto.listen()

if __name__ == "__main__":
    main() 