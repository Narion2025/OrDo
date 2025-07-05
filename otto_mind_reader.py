#!/usr/bin/env python3
"""
OTTO - Mind Reader Version
Verwendet Marker, um das Denksystem zu verstehen und zu antizipieren
"""

import os
import sys
import json
import time
import speech_recognition as sr
import threading
import queue
from datetime import datetime
import yaml
from dotenv import load_dotenv
import random
import re
from pathlib import Path

# Lade Umgebungsvariablen
load_dotenv()

# Konfiguration
TRIGGER_WORDS = ['otto', 'ordo', 'ordu', 'odo', 'orden']
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', 'pNInz6obpgDQGcFmaJgB')

# Marker-System
class MarkerSystem:
    def __init__(self):
        self.markers = {}
        self.mind_patterns = {}
        self.user_profile = {}
        self.anticipation_data = {}
        self.load_all_markers()
    
    def load_all_markers(self):
        """Lädt alle Marker aus dem ALL_SEMANTIC_MARKER_TXT Verzeichnis"""
        marker_dir = Path("../ALL_SEMANTIC_MARKER_TXT/ALL_NEWMARKER01")
        
        if not marker_dir.exists():
            print(f"⚠️  Marker-Verzeichnis nicht gefunden: {marker_dir}")
            return
        
        print(f"🔍 Lade Marker aus: {marker_dir}")
        
        # Lade alle .txt und .yaml Dateien
        marker_files = list(marker_dir.glob("*.txt")) + list(marker_dir.glob("*.yaml"))
        
        for file_path in marker_files:
            try:
                self.load_marker_file(file_path)
            except Exception as e:
                print(f"⚠️  Fehler beim Laden von {file_path.name}: {e}")
        
        print(f"✅ {len(self.markers)} Marker geladen")
    
    def load_marker_file(self, file_path):
        """Lädt eine einzelne Marker-Datei"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Versuche YAML zu parsen
            try:
                data = yaml.safe_load(content)
                if data and isinstance(data, dict):
                    self.process_marker_data(data, file_path.name)
                    return
            except:
                pass
            
            # Fallback: Text-basiertes Parsing
            self.process_text_marker(content, file_path.name)
            
        except Exception as e:
            print(f"⚠️  Fehler beim Laden von {file_path}: {e}")
    
    def process_marker_data(self, data, filename):
        """Verarbeitet YAML-basierte Marker-Daten"""
        marker_name = data.get('marker', filename.replace('.yaml', '').replace('.txt', ''))
        
        self.markers[marker_name] = {
            'name': marker_name,
            'description': data.get('beschreibung', ''),
            'examples': data.get('beispiele', []),
            'patterns': data.get('semantic_grab', {}).get('patterns', []),
            'tags': data.get('tags', []),
            'filename': filename
        }
    
    def process_text_marker(self, content, filename):
        """Verarbeitet Text-basierte Marker-Dateien"""
        lines = content.split('\n')
        marker_name = filename.replace('.txt', '').replace('.yaml', '')
        
        description = ""
        examples = []
        patterns = []
        
        in_examples = False
        in_patterns = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('marker:'):
                marker_name = line.split(':', 1)[1].strip()
            elif line.startswith('beschreibung:'):
                description = line.split(':', 1)[1].strip()
            elif line.startswith('beispiele:'):
                in_examples = True
                in_patterns = False
            elif line.startswith('semantic_grab:'):
                in_examples = False
                in_patterns = True
            elif in_examples and line.startswith('- '):
                examples.append(line[2:].strip('"'))
            elif in_patterns and line.startswith('- '):
                patterns.append(line[2:])
        
        self.markers[marker_name] = {
            'name': marker_name,
            'description': description,
            'examples': examples,
            'patterns': patterns,
            'filename': filename
        }
    
    def analyze_text_for_markers(self, text):
        """Analysiert Text auf Marker"""
        found_markers = []
        text_lower = text.lower()
        
        for marker_name, marker_data in self.markers.items():
            # Prüfe Beispiele
            for example in marker_data['examples']:
                if example.lower() in text_lower:
                    found_markers.append({
                        'marker': marker_name,
                        'type': 'example_match',
                        'confidence': 0.8,
                        'description': marker_data['description']
                    })
                    break
            
            # Prüfe Patterns
            for pattern in marker_data['patterns']:
                if pattern.lower() in text_lower:
                    found_markers.append({
                        'marker': marker_name,
                        'type': 'pattern_match',
                        'confidence': 0.9,
                        'description': marker_data['description']
                    })
                    break
        
        return found_markers
    
    def update_user_profile(self, text, markers_found):
        """Aktualisiert das Benutzerprofil basierend auf gefundenen Markern"""
        timestamp = datetime.now().isoformat()
        
        if 'conversation_history' not in self.user_profile:
            self.user_profile['conversation_history'] = []
        
        self.user_profile['conversation_history'].append({
            'timestamp': timestamp,
            'text': text,
            'markers_found': markers_found
        })
        
        # Analysiere Muster
        self.analyze_mind_patterns()
    
    def analyze_mind_patterns(self):
        """Analysiert Muster im Denksystem des Benutzers"""
        if len(self.user_profile.get('conversation_history', [])) < 3:
            return
        
        # Häufigste Marker
        marker_counts = {}
        for entry in self.user_profile['conversation_history']:
            for marker in entry['markers_found']:
                marker_name = marker['marker']
                marker_counts[marker_name] = marker_counts.get(marker_name, 0) + 1
        
        # Dominante Denkmuster
        dominant_patterns = sorted(marker_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        self.mind_patterns['dominant_markers'] = dominant_patterns
        self.mind_patterns['last_updated'] = datetime.now().isoformat()
        
        # Antizipationsdaten
        self.update_anticipation_data()
    
    def update_anticipation_data(self):
        """Aktualisiert Daten für Antizipation"""
        if not self.mind_patterns.get('dominant_markers'):
            return
        
        # Erstelle Antizipationsprofil
        anticipation_profile = {
            'likely_responses': [],
            'communication_style': '',
            'emotional_patterns': [],
            'cognitive_biases': [],
            'last_updated': datetime.now().isoformat()
        }
        
        # Analysiere dominante Marker für Antizipation
        for marker_name, count in self.mind_patterns['dominant_markers']:
            marker_data = self.markers.get(marker_name, {})
            
            if 'victim' in marker_name.lower() or 'opfer' in marker_name.lower():
                anticipation_profile['likely_responses'].append('Selbstmitleid oder Opferrolle')
                anticipation_profile['emotional_patterns'].append('Verletzlichkeit')
            
            elif 'manipulation' in marker_name.lower() or 'gaslighting' in marker_name.lower():
                anticipation_profile['likely_responses'].append('Verteidigung oder Rechtfertigung')
                anticipation_profile['cognitive_biases'].append('Verteidigungsmechanismus')
            
            elif 'escalation' in marker_name.lower() or 'eskalation' in marker_name.lower():
                anticipation_profile['likely_responses'].append('Intensivierung der Emotion')
                anticipation_profile['emotional_patterns'].append('Intensität')
            
            elif 'connection' in marker_name.lower() or 'verbindung' in marker_name.lower():
                anticipation_profile['likely_responses'].append('Suche nach Nähe')
                anticipation_profile['communication_style'] = 'Bindungsorientiert'
        
        self.anticipation_data = anticipation_profile

class MindReaderOtto:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.marker_system = MarkerSystem()
        self.conversation_active = False
        self.conversation_timeout = 30
        self.last_conversation_time = 0
        self.speaking_queue = queue.Queue()
        
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
        
        self.setup_microphone()
    
    def setup_microphone(self):
        """Initialisiert Mikrofon"""
        print("🎤 Initialisiere Mikrofon...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ Mikrofon initialisiert")
        
        # Teste Mikrofon
        print("🔍 Teste Mikrofon...")
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=1)
            print("✅ Mikrofon-Test erfolgreich")
        except:
            print("⚠️  Mikrofon-Test fehlgeschlagen, aber fortfahren...")
    
    def listen_for_speech(self):
        """Hört auf Sprache und erkennt Trigger"""
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
        """Prüft ob Trigger-Wort erkannt wurde"""
        if not text:
            return False
        
        return any(trigger in text for trigger in TRIGGER_WORDS)
    
    def get_trigger_word(self, text):
        """Extrahiert das erkannte Trigger-Wort"""
        for trigger in TRIGGER_WORDS:
            if trigger in text:
                return trigger
        return None
    
    def clean_input(self, text, trigger_word):
        """Bereinigt Input nach Trigger-Entfernung"""
        return text.replace(trigger_word, '').strip()
    
    def analyze_mind_patterns(self, text):
        """Analysiert Text auf Marker und Denkmuster"""
        markers_found = self.marker_system.analyze_text_for_markers(text)
        self.marker_system.update_user_profile(text, markers_found)
        
        return markers_found
    
    def generate_mind_reader_response(self, text, markers_found):
        """Generiert Antwort basierend auf Mind-Reading"""
        
        if not markers_found:
            return "Ich höre dich und lerne deine Denkmuster kennen. Was beschäftigt dich?"
        
        # Analysiere die gefundenen Marker
        marker_names = [m['marker'] for m in markers_found]
        dominant_patterns = self.marker_system.mind_patterns.get('dominant_markers', [])
        anticipation = self.marker_system.anticipation_data
        
        # Erstelle intelligente Antwort basierend auf Mind-Reading
        response_parts = []
        
        # Erkenne Denkmuster
        if any('victim' in m.lower() or 'opfer' in m.lower() for m in marker_names):
            response_parts.append("Ich spüre, dass du dich in einer schwierigen Situation siehst.")
        
        if any('manipulation' in m.lower() or 'gaslighting' in m.lower() for m in marker_names):
            response_parts.append("Es scheint, als ob du dich gegen etwas wehrst oder verteidigst.")
        
        if any('escalation' in m.lower() or 'eskalation' in m.lower() for m in marker_names):
            response_parts.append("Die Intensität deiner Emotionen ist spürbar.")
        
        if any('connection' in m.lower() or 'verbindung' in m.lower() for m in marker_names):
            response_parts.append("Du suchst nach Verbindung und Verständnis.")
        
        # Antizipiere basierend auf Mustern
        if anticipation.get('likely_responses'):
            response_parts.append("Ich kann mir vorstellen, was als nächstes kommen könnte.")
        
        if anticipation.get('communication_style'):
            response_parts.append(f"Dein Kommunikationsstil ist {anticipation['communication_style']}.")
        
        # Füge Mind-Reading-Element hinzu
        if dominant_patterns:
            top_pattern = dominant_patterns[0][0]
            response_parts.append(f"Ich erkenne das Muster: {top_pattern}")
        
        if response_parts:
            return " ".join(response_parts) + " Erzähl mir mehr."
        else:
            return "Ich lerne deine Denkmuster kennen. Was denkst du darüber?"
    
    def speak_response(self, text):
        """Spricht Antwort mit ElevenLabs"""
        if not self.elevenlabs_available:
            print(f"🧠 Otto sagt: {text}")
            return
        
        try:
            from elevenlabs import generate, play
            # Generiere Audio
            audio = generate(
                text=text,
                voice=VOICE_ID,
                model="eleven_multilingual_v2"
            )
            
            # Spiele Audio in separatem Thread
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
        print("🧠 OTTO - Mind Reader Version")
        print("=" * 60)
        print(f"🎯 Trigger-Wörter: {', '.join(TRIGGER_WORDS)}")
        print(f"🧠 Mind-Reading System: Aktiviert")
        print(f"🎯 Marker geladen: {len(self.marker_system.markers)}")
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
                        
                        # Analysiere Mind-Patterns
                        markers_found = self.analyze_mind_patterns(clean_text)
                        if markers_found:
                            print(f"🎯 Gefundene Marker: {[m['marker'] for m in markers_found]}")
                        
                        # Starte Konversation
                        self.conversation_active = True
                        self.last_conversation_time = time.time()
                        
                        # Generiere Mind-Reader Antwort
                        response = self.generate_mind_reader_response(clean_text, markers_found)
                        self.speak_response(response)
                        
                    elif self.conversation_active:
                        # Fortsetzung der Konversation
                        print(f"🧠 Fortsetzung: {text}")
                        print(f"🧠 Otto verarbeitet: '{text}'")
                        
                        # Prüfe Timeout
                        if time.time() - self.last_conversation_time > self.conversation_timeout:
                            print("⏱️  Dialog-Fenster geschlossen.")
                            self.conversation_active = False
                        else:
                            # Analysiere Mind-Patterns
                            markers_found = self.analyze_mind_patterns(text)
                            if markers_found:
                                print(f"🎯 Gefundene Marker: {[m['marker'] for m in markers_found]}")
                            
                            # Generiere Mind-Reader Antwort
                            response = self.generate_mind_reader_response(text, markers_found)
                            self.speak_response(response)
                            self.last_conversation_time = time.time()
                    
                    else:
                        # Passive Mind-Analyse
                        markers_found = self.analyze_mind_patterns(text)
                        if markers_found:
                            print(f"🎯 Passiv erkannte Marker: {[m['marker'] for m in markers_found]}")
                            print(f"🧠 Mind-Analyse: {text[:50]}...")
                
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n👋 Otto wird beendet...")
                # Speichere Mind-Profile
                self.save_mind_data()
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")
                time.sleep(1)
    
    def save_mind_data(self):
        """Speichert Mind-Reading-Daten"""
        try:
            mind_data = {
                'user_profile': self.marker_system.user_profile,
                'mind_patterns': self.marker_system.mind_patterns,
                'anticipation_data': self.marker_system.anticipation_data,
                'last_updated': datetime.now().isoformat()
            }
            
            with open('mind_reading_data.yaml', 'w', encoding='utf-8') as f:
                yaml.dump(mind_data, f, default_flow_style=False, allow_unicode=True)
            
            print("💾 Mind-Reading-Daten gespeichert")
        except Exception as e:
            print(f"⚠️  Fehler beim Speichern: {e}")

if __name__ == "__main__":
    agent = MindReaderOtto()
    agent.run() 