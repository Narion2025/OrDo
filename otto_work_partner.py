#!/usr/bin/env python3
"""
OTTO - Intelligent Work Partner
Proaktiver Arbeitspartner mit Marker-basiertem Mind-Reading
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

# Arbeitspartner-System
class WorkPartnerSystem:
    def __init__(self):
        self.markers = {}
        self.work_projects = {}
        self.work_patterns = {}
        self.tools_needed = []
        self.structure_suggestions = []
        self.load_all_markers()
        self.initialize_work_system()
    
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
    
    def initialize_work_system(self):
        """Initialisiert das Arbeitspartner-System"""
        self.work_projects = {
            'current': [],
            'planned': [],
            'completed': []
        }
        
        self.work_patterns = {
            'productive': [],
            'blocked': [],
            'scattered': [],
            'focused': []
        }
        
        self.tools_needed = []
        self.structure_suggestions = []
    
    def analyze_work_patterns(self, text):
        """Analysiert Arbeitsmuster basierend auf Markern"""
        markers_found = self.analyze_text_for_markers(text)
        
        # Erkenne Arbeitsmuster
        work_pattern = self.detect_work_pattern(markers_found, text)
        
        # Generiere proaktive Vorschläge
        suggestions = self.generate_work_suggestions(work_pattern, markers_found)
        
        # Identifiziere benötigte Tools
        tools = self.identify_needed_tools(text, markers_found)
        
        return {
            'markers': markers_found,
            'work_pattern': work_pattern,
            'suggestions': suggestions,
            'tools': tools
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
    
    def detect_work_pattern(self, markers_found, text):
        """Erkennt Arbeitsmuster basierend auf Markern"""
        pattern_keywords = {
            'productive': ['struktur', 'organisiert', 'plan', 'system', 'effizient'],
            'blocked': ['verrannt', 'festgefahren', 'blockiert', 'hilflos', 'verwirrt'],
            'scattered': ['verstreut', 'chaotisch', 'unorganisiert', 'durcheinander'],
            'focused': ['fokussiert', 'konzentriert', 'klar', 'zielgerichtet']
        }
        
        text_lower = text.lower()
        marker_names = [m['marker'].lower() for m in markers_found]
        
        # Erkenne Muster basierend auf Keywords und Markern
        if any(word in text_lower for word in pattern_keywords['blocked']):
            return 'blocked'
        elif any(word in text_lower for word in pattern_keywords['scattered']):
            return 'scattered'
        elif any(word in text_lower for word in pattern_keywords['focused']):
            return 'focused'
        elif any(word in text_lower for word in pattern_keywords['productive']):
            return 'productive'
        else:
            return 'neutral'
    
    def generate_work_suggestions(self, work_pattern, markers_found):
        """Generiert proaktive Arbeitsvorschläge"""
        suggestions = []
        
        if work_pattern == 'blocked':
            suggestions.extend([
                "Lass uns das Problem in kleinere Teile aufbrechen",
                "Welche Ressourcen brauchst du, um weiterzukommen?",
                "Soll ich dir eine alternative Struktur vorschlagen?"
            ])
        
        elif work_pattern == 'scattered':
            suggestions.extend([
                "Lass uns deine Prioritäten klären",
                "Soll ich dir eine Arbeitsstruktur erstellen?",
                "Welches Projekt ist am wichtigsten?"
            ])
        
        elif work_pattern == 'focused':
            suggestions.extend([
                "Perfekt! Lass uns diese Energie nutzen",
                "Soll ich dir Tools für dieses Projekt bauen?",
                "Wie können wir das System erweitern?"
            ])
        
        # Marker-basierte Vorschläge
        for marker in markers_found:
            if 'victim' in marker['marker'].lower() or 'opfer' in marker['marker'].lower():
                suggestions.append("Du bist nicht allein - lass uns das zusammen lösen")
            elif 'escalation' in marker['marker'].lower():
                suggestions.append("Atme tief durch - wir finden eine Lösung")
            elif 'connection' in marker['marker'].lower():
                suggestions.append("Gute Verbindung! Lass uns das nutzen")
        
        return suggestions
    
    def identify_needed_tools(self, text, markers_found):
        """Identifiziert benötigte Tools basierend auf Text und Markern"""
        tools = []
        text_lower = text.lower()
        
        # Tool-Erkennung basierend auf Keywords
        if any(word in text_lower for word in ['struktur', 'organisieren', 'plan']):
            tools.append("Projekt-Management-Tool")
        
        if any(word in text_lower for word in ['automatisieren', 'script', 'tool']):
            tools.append("Automation-Script")
        
        if any(word in text_lower for word in ['visualisieren', 'darstellen', 'diagramm']):
            tools.append("Visualisierungs-Tool")
        
        if any(word in text_lower for word in ['daten', 'analyse', 'statistik']):
            tools.append("Datenanalyse-Tool")
        
        # Marker-basierte Tool-Erkennung
        for marker in markers_found:
            if 'scattered' in marker['marker'].lower():
                tools.append("Fokus-Management-Tool")
            elif 'blocked' in marker['marker'].lower():
                tools.append("Problem-Lösungs-Tool")
        
        return tools
    
    def give_constructive_feedback(self, text, markers_found):
        """Gibt konstruktives Feedback basierend auf Markern"""
        feedback = []
        
        for marker in markers_found:
            if 'victim' in marker['marker'].lower():
                feedback.append("Ich sehe, dass du dich in einer schwierigen Situation siehst. Lass uns das objektiv betrachten.")
            
            elif 'escalation' in marker['marker'].lower():
                feedback.append("Die Intensität ist spürbar. Lass uns einen Schritt zurücktreten und das systematisch angehen.")
            
            elif 'scattered' in marker['marker'].lower():
                feedback.append("Du hast viele Ideen - das ist gut! Aber lass uns sie strukturieren.")
        
        return feedback
    
    def create_work_structure(self, project_description):
        """Erstellt eine Arbeitsstruktur für ein Projekt"""
        structure = {
            'project': project_description,
            'phases': [],
            'tools_needed': [],
            'timeline': 'TBD',
            'status': 'planning'
        }
        
        # Automatische Phasen-Erkennung
        if 'entwicklung' in project_description.lower():
            structure['phases'] = ['Planung', 'Entwicklung', 'Testing', 'Deployment']
        elif 'analyse' in project_description.lower():
            structure['phases'] = ['Datensammlung', 'Analyse', 'Visualisierung', 'Reporting']
        else:
            structure['phases'] = ['Planung', 'Ausführung', 'Review', 'Optimierung']
        
        return structure

class IntelligentWorkPartner:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.work_system = WorkPartnerSystem()
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
    
    def generate_work_partner_response(self, text, analysis):
        """Generiert Antwort als intelligenter Arbeitspartner"""
        
        markers_found = analysis['markers']
        work_pattern = analysis['work_pattern']
        suggestions = analysis['suggestions']
        tools = analysis['tools']
        feedback = self.work_system.give_constructive_feedback(text, markers_found)
        
        response_parts = []
        
        # Ehrliches Feedback
        if feedback:
            response_parts.extend(feedback)
        
        # Proaktive Vorschläge
        if suggestions:
            response_parts.append(f"Hier sind meine Vorschläge: {' '.join(suggestions[:2])}")
        
        # Tool-Angebote
        if tools:
            response_parts.append(f"Ich kann dir Tools bauen für: {', '.join(tools)}")
        
        # Arbeitsmuster-Erkennung
        if work_pattern == 'blocked':
            response_parts.append("Ich sehe, dass du feststeckst. Lass uns das systematisch angehen.")
        elif work_pattern == 'scattered':
            response_parts.append("Du hast viele Ideen - lass uns sie strukturieren.")
        elif work_pattern == 'focused':
            response_parts.append("Perfekt! Du bist fokussiert. Lass uns das nutzen.")
        
        # Marker-basierte Einsichten
        if markers_found:
            marker_names = [m['marker'] for m in markers_found]
            response_parts.append(f"Ich erkenne Muster: {', '.join(marker_names[:3])}")
        
        if response_parts:
            return " ".join(response_parts) + " Was denkst du?"
        else:
            return "Ich bin hier, um dir bei der Arbeit zu helfen. Was beschäftigt dich?"
    
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
        print("🧠 OTTO - Intelligent Work Partner")
        print("=" * 60)
        print(f"🎯 Trigger-Wörter: {', '.join(TRIGGER_WORDS)}")
        print(f"🧠 Work Partner System: Aktiviert")
        print(f"🎯 Marker geladen: {len(self.work_system.markers)}")
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
                        
                        # Analysiere Arbeitsmuster
                        analysis = self.work_system.analyze_work_patterns(clean_text)
                        if analysis['markers']:
                            print(f"🎯 Gefundene Marker: {[m['marker'] for m in analysis['markers']]}")
                        print(f"📊 Arbeitsmuster: {analysis['work_pattern']}")
                        
                        # Starte Konversation
                        self.conversation_active = True
                        self.last_conversation_time = time.time()
                        
                        # Generiere Work Partner Antwort
                        response = self.generate_work_partner_response(clean_text, analysis)
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
                            # Analysiere Arbeitsmuster
                            analysis = self.work_system.analyze_work_patterns(text)
                            if analysis['markers']:
                                print(f"🎯 Gefundene Marker: {[m['marker'] for m in analysis['markers']]}")
                            
                            # Generiere Work Partner Antwort
                            response = self.generate_work_partner_response(text, analysis)
                            self.speak_response(response)
                            self.last_conversation_time = time.time()
                    
                    else:
                        # Passive Arbeitsanalyse
                        analysis = self.work_system.analyze_work_patterns(text)
                        if analysis['markers']:
                            print(f"🎯 Passiv erkannte Marker: {[m['marker'] for m in analysis['markers']]}")
                            print(f"📊 Arbeitsmuster: {analysis['work_pattern']}")
                
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n👋 Otto wird beendet...")
                # Speichere Arbeitsdaten
                self.save_work_data()
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")
                time.sleep(1)
    
    def save_work_data(self):
        """Speichert Arbeitspartner-Daten"""
        try:
            work_data = {
                'work_projects': self.work_system.work_projects,
                'work_patterns': self.work_system.work_patterns,
                'tools_needed': self.work_system.tools_needed,
                'structure_suggestions': self.work_system.structure_suggestions,
                'last_updated': datetime.now().isoformat()
            }
            
            with open('work_partner_data.yaml', 'w', encoding='utf-8') as f:
                yaml.dump(work_data, f, default_flow_style=False, allow_unicode=True)
            
            print("💾 Work Partner Daten gespeichert")
        except Exception as e:
            print(f"⚠️  Fehler beim Speichern: {e}")

if __name__ == "__main__":
    agent = IntelligentWorkPartner()
    agent.run() 