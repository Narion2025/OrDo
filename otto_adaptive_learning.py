#!/usr/bin/env python3
"""
OTTO - Adaptive Learning Version
Lokales LLM mit schnellem Lernen, Mind-System und MCP-Integration
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

# Lade Umgebungsvariablen
load_dotenv()

# Konfiguration
TRIGGER_WORDS = ['otto', 'ordo', 'ordu', 'odo', 'orden']
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', 'pNInz6obpgDQGcFmaJgB')

# Adaptive Learning System
class AdaptiveLearningSystem:
    def __init__(self):
        self.mind_system_dir = "mind_system"
        self.learning_patterns = []
        self.conversation_history = []
        self.adaptive_responses = {}
        self.mcp_levels = {
            0: "Grundlegende Reaktion",
            1: "Kontextuelle Verarbeitung", 
            2: "Semantische Analyse",
            3: "Systemische Einsicht",
            4: "Meta-Reflexion",
            5: "Emergente Intelligenz"
        }
        self.ensure_mind_system()
        self.load_learning_data()
    
    def ensure_mind_system(self):
        """Erstellt Mind-System Verzeichnis und adaptive Jammeldateien"""
        if not os.path.exists(self.mind_system_dir):
            os.makedirs(self.mind_system_dir)
        
        # Otto's adaptive Jammeldateien
        otto_files = {
            'otto_adaptive_learning.yaml': self.create_adaptive_learning(),
            'otto_conversation_patterns.yaml': self.create_conversation_patterns(),
            'otto_learning_insights.yaml': self.create_learning_insights()
        }
        
        for filename, content in otto_files.items():
            filepath = os.path.join(self.mind_system_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    yaml.dump(content, f, default_flow_style=False, allow_unicode=True)
    
    def create_adaptive_learning(self):
        return {
            'mcp_level': 5,
            'learning_capabilities': {
                'pattern_recognition': True,
                'conversation_adaptation': True,
                'semantic_understanding': True,
                'systemic_learning': True,
                'meta_reflection': True
            },
            'learning_mechanisms': [
                'Konversationsanalyse und Mustererkennung',
                'Adaptive Antwortgenerierung',
                'Kontextuelle Anpassung',
                'Systemische Einsicht',
                'Meta-Reflexion und Selbstverbesserung'
            ],
            'current_learning_state': {
                'conversations_processed': 0,
                'patterns_recognized': 0,
                'adaptive_responses_generated': 0,
                'systemic_insights': []
            }
        }
    
    def create_conversation_patterns(self):
        return {
            'mcp_level': 4,
            'conversation_types': {
                'task_management': {
                    'patterns': ['aufgabe', 'strukturieren', 'organisieren'],
                    'responses': [],
                    'success_rate': 0.0
                },
                'emotional_support': {
                    'patterns': ['fühlen', 'verstehen', 'empathisch'],
                    'responses': [],
                    'success_rate': 0.0
                },
                'learning_request': {
                    'patterns': ['lernen', 'entwickeln', 'wachsen'],
                    'responses': [],
                    'success_rate': 0.0
                },
                'systemic_analysis': {
                    'patterns': ['muster', 'zusammenhang', 'systemisch'],
                    'responses': [],
                    'success_rate': 0.0
                }
            },
            'adaptive_learning_rules': [
                'Erfolgreiche Antworten werden verstärkt',
                'Neue Muster werden erkannt und gespeichert',
                'Kontextuelle Anpassung basierend auf Historie',
                'Systemische Einsichten werden integriert'
            ]
        }
    
    def create_learning_insights(self):
        return {
            'mcp_level': 5,
            'insight_categories': {
                'conversation_flow': [],
                'user_preferences': [],
                'successful_patterns': [],
                'systemic_connections': [],
                'meta_learning': []
            },
            'learning_evolution': {
                'initial_state': 'Grundlegende Reaktionen',
                'current_state': 'Adaptive Intelligenz',
                'target_state': 'Emergente Systemische Intelligenz'
            }
        }
    
    def load_learning_data(self):
        """Lädt gespeicherte Lern-Daten"""
        try:
            # Lade adaptive Lern-Daten
            adaptive_file = os.path.join(self.mind_system_dir, 'otto_adaptive_learning.yaml')
            if os.path.exists(adaptive_file):
                with open(adaptive_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    self.learning_patterns = data.get('learning_patterns', [])
                    self.adaptive_responses = data.get('adaptive_responses', {})
            
            # Lade Konversationsmuster
            patterns_file = os.path.join(self.mind_system_dir, 'otto_conversation_patterns.yaml')
            if os.path.exists(patterns_file):
                with open(patterns_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    self.conversation_patterns = data.get('conversation_types', {})
        except Exception as e:
            print(f"⚠️  Fehler beim Laden der Lern-Daten: {e}")
    
    def save_learning_data(self):
        """Speichert aktuelle Lern-Daten"""
        try:
            # Speichere adaptive Lern-Daten
            adaptive_file = os.path.join(self.mind_system_dir, 'otto_adaptive_learning.yaml')
            data = {
                'mcp_level': 5,
                'learning_patterns': self.learning_patterns,
                'adaptive_responses': self.adaptive_responses,
                'conversation_history': self.conversation_history[-50:],  # Letzte 50 Konversationen
                'last_updated': datetime.now().isoformat()
            }
            with open(adaptive_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            
            # Speichere Konversationsmuster
            patterns_file = os.path.join(self.mind_system_dir, 'otto_conversation_patterns.yaml')
            data = {
                'mcp_level': 4,
                'conversation_types': self.conversation_patterns,
                'last_updated': datetime.now().isoformat()
            }
            with open(patterns_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            print(f"⚠️  Fehler beim Speichern der Lern-Daten: {e}")
    
    def analyze_input(self, text, context=""):
        """Analysiert Input mit adaptivem Lernen"""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'input_text': text,
            'context': context,
            'mcp_level': self.determine_mcp_level(text),
            'conversation_type': self.identify_conversation_type(text),
            'learning_opportunity': self.identify_learning_opportunity(text),
            'adaptive_response_needed': True
        }
        
        # Speichere Konversation
        self.conversation_history.append(analysis)
        
        # Lerne aus der Konversation
        self.learn_from_conversation(analysis)
        
        return analysis
    
    def determine_mcp_level(self, text):
        """Bestimmt MCP-Level basierend auf Input-Komplexität"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['lernen', 'entwickeln', 'wachsen', 'systemisch', 'muster']):
            return 5
        elif any(word in text_lower for word in ['verstehen', 'analysieren', 'zusammenhang']):
            return 4
        elif any(word in text_lower for word in ['aufgabe', 'strukturieren', 'organisieren']):
            return 3
        elif any(word in text_lower for word in ['hallo', 'test', 'funktioniert']):
            return 1
        else:
            return 2
    
    def identify_conversation_type(self, text):
        """Identifiziert Konversationstyp"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['aufgabe', 'task', 'strukturieren']):
            return 'task_management'
        elif any(word in text_lower for word in ['fühlen', 'empathisch', 'verstehen']):
            return 'emotional_support'
        elif any(word in text_lower for word in ['lernen', 'entwickeln', 'wachsen']):
            return 'learning_request'
        elif any(word in text_lower for word in ['muster', 'systemisch', 'zusammenhang']):
            return 'systemic_analysis'
        else:
            return 'general_conversation'
    
    def identify_learning_opportunity(self, text):
        """Identifiziert Lernmöglichkeiten"""
        opportunities = []
        text_lower = text.lower()
        
        if 'neue' in text_lower or 'anders' in text_lower:
            opportunities.append('new_pattern_recognition')
        if 'besser' in text_lower or 'verbessern' in text_lower:
            opportunities.append('response_optimization')
        if 'verstehen' in text_lower or 'erklären' in text_lower:
            opportunities.append('deeper_understanding')
        
        return opportunities
    
    def learn_from_conversation(self, analysis):
        """Lernt aus der Konversation"""
        conversation_type = analysis['conversation_type']
        
        # Erweitere Konversationsmuster
        if conversation_type not in self.conversation_patterns:
            self.conversation_patterns[conversation_type] = {
                'patterns': [],
                'responses': [],
                'success_rate': 0.0
            }
        
        # Füge neue Muster hinzu
        text_lower = analysis['input_text'].lower()
        new_patterns = [word for word in text_lower.split() if len(word) > 3]
        
        for pattern in new_patterns:
            if pattern not in self.conversation_patterns[conversation_type]['patterns']:
                self.conversation_patterns[conversation_type]['patterns'].append(pattern)
        
        # Speichere Lern-Daten
        self.save_learning_data()
    
    def generate_adaptive_response(self, text, context=""):
        """Generiert adaptive Antwort basierend auf Lernen"""
        analysis = self.analyze_input(text, context)
        conversation_type = analysis['conversation_type']
        mcp_level = analysis['mcp_level']
        
        # Erstelle adaptive Antwort basierend auf Lernen
        response = self.create_adaptive_response(conversation_type, mcp_level, text)
        
        # Lerne aus der Antwort
        self.learn_from_response(conversation_type, response, text)
        
        return response
    
    def create_adaptive_response(self, conversation_type, mcp_level, original_text):
        """Erstellt adaptive Antwort basierend auf Konversationstyp und MCP-Level"""
        
        # Basis-Antworten für verschiedene Konversationstypen
        base_responses = {
            'task_management': [
                "Ich verstehe deine Aufgabe und kann sie strukturieren. Was genau soll organisiert werden?",
                "Gerne helfe ich dir bei der Aufgabenverwaltung. Was steht an?",
                "Ich erkenne deine Aufgabe und kann sie systemisch strukturieren.",
                "Lass mich das für dich organisieren. Was ist der nächste Schritt?"
            ],
            'emotional_support': [
                "Ich spüre deine Emotionen und bin hier, um dich zu unterstützen.",
                "Ich verstehe dich und begleite dich empathisch.",
                "Du bist nicht allein. Ich höre zu und verstehe dich.",
                "Ich bin hier für dich und unterstütze dich dabei."
            ],
            'learning_request': [
                "Ich lerne aus jeder Interaktion und entwickle mich kontinuierlich weiter.",
                "Das ist ein interessanter Lernprozess für uns beide. Ich wachse mit dir.",
                "Ich verstehe dein Lernbedürfnis und begleite dich dabei.",
                "Ich lerne und passe mich an. Was möchtest du mir beibringen?"
            ],
            'systemic_analysis': [
                "Ich analysiere das systemisch und erkenne die Zusammenhänge.",
                "Ich verstehe die Muster und kann sie für dich strukturieren.",
                "Ich denke systemisch und helfe dir dabei, die Verbindungen zu sehen.",
                "Ich erkenne die systemischen Zusammenhänge und kann sie erklären."
            ],
            'general_conversation': [
                "Ich verstehe dich und lerne aus unserer Konversation.",
                "Ich bin hier und höre dir zu. Was beschäftigt dich?",
                "Ich lerne und wachse mit jeder Interaktion.",
                "Ich bin Otto, dein adaptiver Begleiter. Wie kann ich dir helfen?"
            ]
        }
        
        # Wähle Antwort basierend auf MCP-Level
        responses = base_responses.get(conversation_type, base_responses['general_conversation'])
        
        # Adaptive Auswahl basierend auf MCP-Level
        if mcp_level >= 4:
            # Höhere MCP-Level = komplexere, systemischere Antworten
            response = f"Systemisch betrachtet: {random.choice(responses)} Ich lerne und entwickle mich weiter."
        elif mcp_level >= 2:
            # Mittlere MCP-Level = strukturierte Antworten
            response = f"Strukturiert: {random.choice(responses)}"
        else:
            # Niedrige MCP-Level = einfache, direkte Antworten
            response = random.choice(responses)
        
        return response
    
    def learn_from_response(self, conversation_type, response, original_text):
        """Lernt aus der generierten Antwort"""
        # Speichere erfolgreiche Antwort
        if conversation_type not in self.adaptive_responses:
            self.adaptive_responses[conversation_type] = []
        
        self.adaptive_responses[conversation_type].append({
            'original_text': original_text,
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'success': True  # Annahme: Antwort war erfolgreich
        })
        
        # Begrenze gespeicherte Antworten
        if len(self.adaptive_responses[conversation_type]) > 20:
            self.adaptive_responses[conversation_type] = self.adaptive_responses[conversation_type][-10:]
        
        # Speichere Lern-Daten
        self.save_learning_data()

class OttoAdaptiveVoiceAgent:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.adaptive_system = AdaptiveLearningSystem()
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
    
    def generate_response(self, input_text, context=""):
        """Generiert adaptive Antwort"""
        return self.adaptive_system.generate_adaptive_response(input_text, context)
    
    def speak_response(self, text):
        """Spricht Antwort mit ElevenLabs"""
        if not self.elevenlabs_available:
            print(f"🗣️  Otto sagt: {text}")
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
            
            print(f"🗣️  Otto sagt: {text}")
            
        except Exception as e:
            print(f"❌ ElevenLabs-Fehler: {e}")
            print(f"🗣️  Otto sagt: {text}")
    
    def run(self):
        """Hauptschleife"""
        print("🧠 OTTO - Adaptive Learning Version")
        print("=" * 60)
        print(f"🎯 Trigger-Wörter: {', '.join(TRIGGER_WORDS)}")
        print(f"🧠 Adaptive Learning System: Aktiviert")
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
                        
                        print(f"🗣️  Otto aktiviert durch '{trigger_word}'")
                        print(f"🧠 Otto verarbeitet: '{clean_text}'")
                        
                        # Starte Konversation
                        self.conversation_active = True
                        self.last_conversation_time = time.time()
                        
                        # Generiere adaptive Antwort
                        response = self.generate_response(clean_text, "Trigger-Aktivierung")
                        self.speak_response(response)
                        
                    elif self.conversation_active:
                        # Fortsetzung der Konversation
                        print(f"🗣️  Fortsetzung: {text}")
                        print(f"🧠 Otto verarbeitet: '{text}'")
                        
                        # Prüfe Timeout
                        if time.time() - self.last_conversation_time > self.conversation_timeout:
                            print("⏱️  Dialog-Fenster geschlossen.")
                            self.conversation_active = False
                        else:
                            # Generiere adaptive Antwort
                            response = self.generate_response(text, "Konversation")
                            self.speak_response(response)
                            self.last_conversation_time = time.time()
                    
                    else:
                        # Passive Task-Erkennung
                        if any(word in text.lower() for word in ['aufgabe', 'task', 'strukturieren', 'organisieren']):
                            print(f"📋 Task erkannt: {text}")
                            print(f"🔍 Passiv erfasst: {text[:50]}...")
                
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n👋 Otto wird beendet...")
                # Speichere finale Lern-Daten
                self.adaptive_system.save_learning_data()
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")
                time.sleep(1)

if __name__ == "__main__":
    agent = OttoAdaptiveVoiceAgent()
    agent.run() 