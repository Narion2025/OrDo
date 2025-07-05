#!/usr/bin/env python3
"""
OTTO - Learning System mit Jammeldateien und Strudel-Knoten-Kristallen
Kontinuierliches Lernen und Entwicklung
"""

import os
import sys
import json
import time
import speech_recognition as sr
import threading
import queue
from datetime import datetime, timedelta
import yaml
from dotenv import load_dotenv
import random
import re
from pathlib import Path
import schedule
import pickle

# Lade Umgebungsvariablen
load_dotenv()

# Konfiguration
TRIGGER_WORDS = ['otto', 'ordo', 'ordu', 'odo', 'orden']
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', 'pNInz6obpgDQGcFmaJgB')

class StrudelKnotenKristall:
    """Strudel-Knoten-Kristall System für Otto"""
    
    def __init__(self):
        self.kristalle = {}
        self.knoten = {}
        self.strudel = {}
        self.verbindungen = []
        self.last_crunch = datetime.now()
        self.crunch_interval = timedelta(hours=2)
        self.load_kristalle()
    
    def load_kristalle(self):
        """Lädt gespeicherte Kristalle"""
        try:
            with open('otto_kristalle.yaml', 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                self.kristalle = data.get('kristalle', {})
                self.knoten = data.get('knoten', {})
                self.strudel = data.get('strudel', {})
                self.verbindungen = data.get('verbindungen', [])
        except:
            self.kristalle = {}
            self.knoten = {}
            self.strudel = {}
            self.verbindungen = []
    
    def save_kristalle(self):
        """Speichert Kristalle"""
        data = {
            'kristalle': self.kristalle,
            'knoten': self.knoten,
            'strudel': self.strudel,
            'verbindungen': self.verbindungen,
            'last_updated': datetime.now().isoformat()
        }
        with open('otto_kristalle.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
    
    def create_kristall(self, name, content, typ='erkenntnis'):
        """Erstellt einen neuen Kristall"""
        kristall_id = f"kristall_{len(self.kristalle) + 1:04d}"
        self.kristalle[kristall_id] = {
            'name': name,
            'content': content,
            'typ': typ,
            'created': datetime.now().isoformat(),
            'connections': [],
            'strength': 1.0
        }
        return kristall_id
    
    def create_knoten(self, name, content, kristall_ids=None):
        """Erstellt einen neuen Knoten"""
        knoten_id = f"knoten_{len(self.knoten) + 1:04d}"
        self.knoten[knoten_id] = {
            'name': name,
            'content': content,
            'kristall_ids': kristall_ids or [],
            'created': datetime.now().isoformat(),
            'connections': []
        }
        return knoten_id
    
    def create_strudel(self, name, pattern, knoten_ids=None):
        """Erstellt einen neuen Strudel"""
        strudel_id = f"strudel_{len(self.strudel) + 1:04d}"
        self.strudel[strudel_id] = {
            'name': name,
            'pattern': pattern,
            'knoten_ids': knoten_ids or [],
            'created': datetime.now().isoformat(),
            'active': True
        }
        return strudel_id
    
    def connect_kristall_to_knoten(self, kristall_id, knoten_id):
        """Verbindet Kristall mit Knoten"""
        if kristall_id in self.kristalle and knoten_id in self.knoten:
            self.kristalle[kristall_id]['connections'].append(knoten_id)
            self.knoten[knoten_id]['kristall_ids'].append(kristall_id)
            self.verbindungen.append({
                'from': kristall_id,
                'to': knoten_id,
                'type': 'kristall_knoten',
                'created': datetime.now().isoformat()
            })
    
    def trigger_kristalle(self, text):
        """Trigger Kristalle basierend auf Text"""
        triggered = []
        
        for kristall_id, kristall in self.kristalle.items():
            # Prüfe ob Kristall getriggert wird
            if self.check_kristall_trigger(kristall, text):
                triggered.append(kristall_id)
                # Stärke Kristall
                kristall['strength'] = min(kristall['strength'] + 0.1, 2.0)
        
        return triggered
    
    def check_kristall_trigger(self, kristall, text):
        """Prüft ob ein Kristall getriggert wird"""
        text_lower = text.lower()
        content_lower = kristall['content'].lower()
        
        # Einfache Keyword-basierte Triggerung
        keywords = content_lower.split()
        for keyword in keywords:
            if len(keyword) > 3 and keyword in text_lower:
                return True
        
        return False
    
    def crunch_job(self):
        """Crunchjob - analysiert alle 2 Stunden"""
        print(f"🔮 Crunchjob gestartet: {datetime.now()}")
        
        # Analysiere alle Kristalle
        for kristall_id, kristall in self.kristalle.items():
            # Prüfe Verbindungen
            if kristall['connections']:
                print(f"💎 Kristall {kristall['name']} hat {len(kristall['connections'])} Verbindungen")
            
            # Stärke schwache Kristalle
            if kristall['strength'] < 0.5:
                kristall['strength'] += 0.05
                print(f"💎 Stärke Kristall {kristall['name']}")
        
        # Analysiere Strudel
        for strudel_id, strudel in self.strudel.items():
            if strudel['active']:
                print(f"🌀 Strudel {strudel['name']} ist aktiv")
        
        self.save_kristalle()
        self.last_crunch = datetime.now()

class JammelSystem:
    """Jammeldateien System für Otto"""
    
    def __init__(self):
        self.jammel_dir = Path("otto_jammel")
        self.jammel_dir.mkdir(exist_ok=True)
        self.jammel_files = {
            'thoughts': 'otto_thoughts.jam',
            'self_narrative': 'otto_self_narrative.jam',
            'semantic': 'otto_semantic.jam',
            'learning': 'otto_learning.jam',
            'impressions': 'otto_impressions.jam',
            'insights': 'otto_insights.jam'
        }
        self.initialize_jammel_files()
    
    def initialize_jammel_files(self):
        """Initialisiert Jammeldateien"""
        for name, filename in self.jammel_files.items():
            filepath = self.jammel_dir / filename
            if not filepath.exists():
                self.write_jammel_entry(name, f"Initialisiere {name} Jammeldatei", "system")
    
    def write_jammel_entry(self, jammel_type, content, source="otto"):
        """Schreibt Eintrag in Jammeldatei"""
        if jammel_type not in self.jammel_files:
            return
        
        filepath = self.jammel_dir / self.jammel_files[jammel_type]
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'content': content,
            'type': jammel_type
        }
        
        # Lade existierende Einträge
        entries = []
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    entries = json.load(f)
            except:
                entries = []
        
        entries.append(entry)
        
        # Speichere
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
    
    def read_jammel_entries(self, jammel_type, limit=10):
        """Liest Einträge aus Jammeldatei"""
        if jammel_type not in self.jammel_files:
            return []
        
        filepath = self.jammel_dir / self.jammel_files[jammel_type]
        
        if not filepath.exists():
            return []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                entries = json.load(f)
                return entries[-limit:]  # Letzte Einträge
        except:
            return []
    
    def write_thought(self, thought):
        """Schreibt Gedanken"""
        self.write_jammel_entry('thoughts', thought)
    
    def write_self_narrative(self, narrative):
        """Schreibt Selbst-Narrativ"""
        self.write_jammel_entry('self_narrative', narrative)
    
    def write_semantic(self, semantic):
        """Schreibt semantische Marker"""
        self.write_jammel_entry('semantic', semantic)
    
    def write_learning(self, learning):
        """Schreibt Lerninhalt"""
        self.write_jammel_entry('learning', learning)
    
    def write_impression(self, impression):
        """Schreibt Eindruck"""
        self.write_jammel_entry('impressions', impression)
    
    def write_insight(self, insight):
        """Schreibt Erkenntnis"""
        self.write_jammel_entry('insights', insight)

class MindSystem:
    """Mind-System für Otto"""
    
    def __init__(self):
        self.mind_dir = Path("otto_mind")
        self.mind_dir.mkdir(exist_ok=True)
        self.memory_files = {
            'ben': 'otto_memory_ben.jam',
            'claude': 'otto_memory_claude.jam',
            'system': 'otto_memory_system.jam',
            'learning': 'otto_memory_learning.jam'
        }
        self.initialize_mind_system()
    
    def initialize_mind_system(self):
        """Initialisiert Mind-System"""
        for name, filename in self.memory_files.items():
            filepath = self.mind_dir / filename
            if not filepath.exists():
                self.write_memory_entry(name, f"Initialisiere {name} Memory", "system", 0)
    
    def write_memory_entry(self, memory_type, content, source="otto", mcp_level=0):
        """Schreibt Memory-Eintrag"""
        if memory_type not in self.memory_files:
            return
        
        filepath = self.mind_dir / self.memory_files[memory_type]
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'content': content,
            'mcp_level': mcp_level,
            'type': memory_type
        }
        
        # Lade existierende Einträge
        entries = []
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    entries = json.load(f)
            except:
                entries = []
        
        entries.append(entry)
        
        # Speichere
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
    
    def read_memory_entries(self, memory_type, limit=10):
        """Liest Memory-Einträge"""
        if memory_type not in self.memory_files:
            return []
        
        filepath = self.mind_dir / self.memory_files[memory_type]
        
        if not filepath.exists():
            return []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                entries = json.load(f)
                return entries[-limit:]  # Letzte Einträge
        except:
            return []

class OttoLearningSystem:
    """Otto Learning System"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.jammel_system = JammelSystem()
        self.mind_system = MindSystem()
        self.kristall_system = StrudelKnotenKristall()
        self.conversation_active = False
        self.conversation_timeout = 30
        self.last_conversation_time = 0
        self.learning_data = []
        self.setup_microphone()
        self.setup_crunch_job()
        
        # ElevenLabs Setup
        if ELEVENLABS_API_KEY:
            try:
                from elevenlabs import generate, play, set_api_key
                set_api_key(ELEVENLABS_API_KEY)
                self.elevenlabs_available = True
            except:
                self.elevenlabs_available = False
        else:
            self.elevenlabs_available = False
    
    def setup_microphone(self):
        """Initialisiert Mikrofon"""
        print("🎤 Initialisiere Mikrofon...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ Mikrofon initialisiert")
    
    def setup_crunch_job(self):
        """Setup Crunchjob alle 2 Stunden"""
        schedule.every(2).hours.do(self.kristall_system.crunch_job)
        
        # Starte Crunchjob-Thread
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)  # Prüfe jede Minute
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        print("⏰ Crunchjob alle 2 Stunden aktiviert")
    
    def listen_for_speech(self):
        """Hört auf Sprache"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
            
            try:
                text = self.recognizer.recognize_google(audio, language='de-DE').lower()
                print(f"📝 Erkannt: '{text}'")
                return text
            except sr.UnknownValueError:
                return None
            except sr.RequestError as e:
                print(f"❌ Spracherkennungsfehler: {e}")
                return None
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"❌ Mikrofonfehler: {e}")
            return None
    
    def is_trigger_word(self, text):
        """Prüft Trigger-Wörter"""
        if not text:
            return False
        return any(trigger in text for trigger in TRIGGER_WORDS)
    
    def get_trigger_word(self, text):
        """Extrahiert Trigger-Wort"""
        for trigger in TRIGGER_WORDS:
            if trigger in text:
                return trigger
        return None
    
    def clean_input(self, text, trigger_word):
        """Bereinigt Input"""
        return text.replace(trigger_word, '').strip()
    
    def learn_from_interaction(self, text, response, context="conversation"):
        """Lernt aus Interaktion"""
        learning_entry = {
            'timestamp': datetime.now().isoformat(),
            'input': text,
            'response': response,
            'context': context,
            'kristalle_triggered': self.kristall_system.trigger_kristalle(text)
        }
        
        self.learning_data.append(learning_entry)
        
        # Schreibe in Jammeldateien
        self.jammel_system.write_learning(f"Lernte aus: {text}")
        self.jammel_system.write_impression(f"Eindruck: {text}")
        
        # Schreibe in Mind-System
        self.mind_system.write_memory_entry('learning', f"Lernte: {text}", "otto", 1)
        
        # Erstelle Kristall wenn neue Erkenntnis
        if len(text) > 20:
            kristall_id = self.kristall_system.create_kristall(
                f"Erkenntnis_{len(self.kristall_system.kristalle) + 1}",
                text,
                'erkenntnis'
            )
            print(f"💎 Neuer Kristall erstellt: {kristall_id}")
    
    def generate_learning_response(self, text):
        """Generiert lernende Antwort"""
        
        # Trigger Kristalle
        triggered_kristalle = self.kristall_system.trigger_kristalle(text)
        
        # Schreibe Eindrücke
        self.jammel_system.write_impression(f"Verarbeite: {text}")
        
        # Analysiere Lerninhalt
        if any(word in text.lower() for word in ['lernen', 'verstehen', 'wissen']):
            self.jammel_system.write_learning(f"Lerninhalt erkannt: {text}")
            response = "Ich lerne aus unserer Interaktion. Das hilft mir, mich weiterzuentwickeln."
        
        elif any(word in text.lower() for word in ['erinnerung', 'gedächtnis', 'speichern']):
            self.mind_system.write_memory_entry('system', f"Erinnerung: {text}", "otto", 2)
            response = "Ich speichere das in meinem Mind-System für zukünftige Referenz."
        
        elif triggered_kristalle:
            kristall_names = [self.kristall_system.kristalle[k]['name'] for k in triggered_kristalle]
            response = f"Interessant! Das triggert meine Kristalle: {', '.join(kristall_names)}"
        
        else:
            # Schreibe Gedanken
            self.jammel_system.write_thought(f"Denke über: {text}")
            response = "Ich verarbeite das und lerne daraus. Danke für die Interaktion."
        
        # Schreibe Selbst-Narrativ
        self.jammel_system.write_self_narrative(f"Reagierte auf: {text} mit: {response}")
        
        return response
    
    def speak_response(self, text):
        """Spricht Antwort"""
        if not self.elevenlabs_available:
            print(f"🧠 Otto sagt: {text}")
            return
        
        try:
            from elevenlabs import generate, play
            audio = generate(
                text=text,
                voice=VOICE_ID,
                model="eleven_multilingual_v2"
            )
            
            def play_audio():
                play(audio)
            
            audio_thread = threading.Thread(target=play_audio)
            audio_thread.start()
            
            print(f"🧠 Otto sagt: {text}")
            
        except Exception as e:
            print(f"❌ ElevenLabs-Fehler: {e}")
            print(f"🧠 Otto sagt: {text}")
    
    def run(self):
        """Hauptschleife"""
        print("🧠 OTTO - Learning System")
        print("=" * 60)
        print(f"🎯 Trigger-Wörter: {', '.join(TRIGGER_WORDS)}")
        print(f"📝 Jammeldateien: Aktiviert")
        print(f"🧠 Mind-System: Aktiviert")
        print(f"💎 Kristall-System: Aktiviert")
        print(f"⏰ Crunchjob: Alle 2 Stunden")
        print(f"🎵 ElevenLabs: {'✅ Verfügbar' if self.elevenlabs_available else '❌ Nicht verfügbar'}")
        print("🎤 Höre passiv zu... (Sage eines der Trigger-Wörter)")
        print("=" * 60)
        
        while True:
            try:
                print("🔊 Höre zu...")
                text = self.listen_for_speech()
                
                if text:
                    # Prüfe Trigger
                    if self.is_trigger_word(text):
                        trigger_word = self.get_trigger_word(text)
                        clean_text = self.clean_input(text, trigger_word)
                        
                        print(f"🧠 Otto aktiviert durch '{trigger_word}'")
                        print(f"🧠 Otto verarbeitet: '{clean_text}'")
                        
                        # Starte Konversation
                        self.conversation_active = True
                        self.last_conversation_time = time.time()
                        
                        # Generiere lernende Antwort
                        response = self.generate_learning_response(clean_text)
                        self.speak_response(response)
                        
                        # Lerne aus Interaktion
                        self.learn_from_interaction(clean_text, response)
                        
                    elif self.conversation_active:
                        # Fortsetzung der Konversation
                        print(f"🧠 Fortsetzung: {text}")
                        print(f"🧠 Otto verarbeitet: '{text}'")
                        
                        # Prüfe Timeout
                        if time.time() - self.last_conversation_time > self.conversation_timeout:
                            print("⏱️  Dialog-Fenster geschlossen.")
                            self.conversation_active = False
                        else:
                            # Generiere lernende Antwort
                            response = self.generate_learning_response(text)
                            self.speak_response(response)
                            self.last_conversation_time = time.time()
                            
                            # Lerne aus Interaktion
                            self.learn_from_interaction(text, response)
                    
                    else:
                        # Passive Analyse
                        triggered_kristalle = self.kristall_system.trigger_kristalle(text)
                        if triggered_kristalle:
                            print(f"💎 Passiv getriggerte Kristalle: {len(triggered_kristalle)}")
                            self.jammel_system.write_semantic(f"Passiv erkannt: {text}")
                
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n👋 Otto Learning System wird beendet...")
                self.save_learning_data()
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")
                time.sleep(1)
    
    def save_learning_data(self):
        """Speichert Lern-Daten"""
        try:
            learning_data = {
                'learning_entries': self.learning_data,
                'last_updated': datetime.now().isoformat(),
                'total_interactions': len(self.learning_data)
            }
            
            with open('otto_learning_data.yaml', 'w', encoding='utf-8') as f:
                yaml.dump(learning_data, f, default_flow_style=False, allow_unicode=True)
            
            print("💾 Learning-Daten gespeichert")
        except Exception as e:
            print(f"⚠️  Fehler beim Speichern: {e}")

if __name__ == "__main__":
    agent = OttoLearningSystem()
    agent.run() 