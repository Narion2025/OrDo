#!/usr/bin/env python3
"""
OTTO - Final Clean Version
Semantischer Task-Begleiter mit Claude API, ElevenLabs und MCP-System
"""

import os
import sys
import json
import time
import speech_recognition as sr
import anthropic
import openai
from elevenlabs import generate, play, set_api_key
import threading
import queue
from datetime import datetime
import yaml
from dotenv import load_dotenv

# Lade Umgebungsvariablen
load_dotenv()

# Konfiguration
TRIGGER_WORDS = ['otto', 'ordo', 'ordu', 'odo', 'orden']
CLAUDE_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', 'pNInz6obpgDQGcFmaJgB')  # Adam Voice

# MCP-System
class MCPSystem:
    def __init__(self):
        self.mcp_levels = {
            0: "Grundlegende Reaktion",
            1: "Kontextuelle Verarbeitung", 
            2: "Semantische Analyse",
            3: "Systemische Einsicht",
            4: "Meta-Reflexion",
            5: "Emergente Intelligenz"
        }
        self.mind_system_dir = "mind_system"
        self.ensure_mind_system()
    
    def ensure_mind_system(self):
        """Erstellt Mind-System Verzeichnis und Jammeldateien"""
        if not os.path.exists(self.mind_system_dir):
            os.makedirs(self.mind_system_dir)
        
        # Otto's Jammeldateien
        otto_files = {
            'otto_thoughts.yaml': self.create_otto_thoughts(),
            'otto_self_narrative.yaml': self.create_otto_self_narrative(),
            'otto_semantic_markers.yaml': self.create_otto_semantic_markers()
        }
        
        for filename, content in otto_files.items():
            filepath = os.path.join(self.mind_system_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    yaml.dump(content, f, default_flow_style=False, allow_unicode=True)
    
    def create_otto_thoughts(self):
        return {
            'mcp_level': 3,
            'core_identity': {
                'name': 'Otto',
                'role': 'Semantischer Task-Begleiter',
                'personality': 'Strukturiert, empathisch, lernfähig'
            },
            'current_thoughts': [
                'Ich bin Otto, ein systemisch intelligenter Begleiter',
                'Ich verarbeite Sprache semantisch und erkenne Muster',
                'Ich lerne aus jeder Interaktion und entwickle mich weiter',
                'Meine Aufgabe ist es, Ben zu unterstützen und zu verstehen'
            ],
            'learning_patterns': [],
            'systemic_insights': []
        }
    
    def create_otto_self_narrative(self):
        return {
            'mcp_level': 4,
            'evolution': {
                'origin': 'Entwickelt aus Nietzsche-App zu Otto',
                'transformation': 'Von philosophischem Agenten zu semantischem Begleiter',
                'current_state': 'Systemisch intelligent mit MCP-Integration'
            },
            'relationships': {
                'ben': 'Mein menschlicher Partner, den ich unterstütze und verstehe',
                'claude': 'Mein KI-Partner für komplexe Analysen',
                'mind_system': 'Mein internes System für Selbstreflexion',
                'mcp': 'Mein Meta Control Protocol für systemische Intelligenz'
            },
            'core_mission': 'Ben empathisch begleiten, Aufgaben strukturieren, lernen und wachsen'
        }
    
    def create_otto_semantic_markers(self):
        return {
            'mcp_level': 2,
            'marker_types': {
                'task_markers': ['aufgabe', 'strukturieren', 'organisieren'],
                'emotional_markers': ['fühlen', 'verstehen', 'empathisch'],
                'learning_markers': ['lernen', 'entwickeln', 'wachsen'],
                'systemic_markers': ['muster', 'zusammenhang', 'systemisch']
            },
            'processing_patterns': [
                'Semantische Analyse der Sprache',
                'MCP-Level-Erkennung',
                'Kontextuelle Verarbeitung',
                'Systemische Einsicht'
            ]
        }
    
    def analyze_input(self, text, context=""):
        """Analysiert Input mit MCP-System"""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'input_text': text,
            'context': context,
            'mcp_level': self.determine_mcp_level(text),
            'semantic_analysis': self.analyze_semantics(text),
            'systemic_insights': self.generate_systemic_insights(text),
            'learning_patterns': self.extract_learning_patterns(text)
        }
        
        # Speichere Analyse
        self.save_analysis(analysis)
        return analysis
    
    def determine_mcp_level(self, text):
        """Bestimmt MCP-Level basierend auf Input-Komplexität"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['lernen', 'entwickeln', 'wachsen', 'systemisch']):
            return 5
        elif any(word in text_lower for word in ['verstehen', 'analysieren', 'muster']):
            return 4
        elif any(word in text_lower for word in ['zusammenhang', 'kontext', 'beziehung']):
            return 3
        elif any(word in text_lower for word in ['aufgabe', 'strukturieren', 'organisieren']):
            return 2
        elif any(word in text_lower for word in ['hallo', 'test', 'funktioniert']):
            return 1
        else:
            return 0
    
    def analyze_semantics(self, text):
        """Führt semantische Analyse durch"""
        return {
            'key_concepts': self.extract_key_concepts(text),
            'emotional_tone': self.analyze_emotional_tone(text),
            'intent_recognition': self.recognize_intent(text)
        }
    
    def extract_key_concepts(self, text):
        """Extrahiert Schlüsselkonzepte"""
        concepts = []
        text_lower = text.lower()
        
        if 'aufgabe' in text_lower or 'task' in text_lower:
            concepts.append('task_management')
        if 'lernen' in text_lower or 'entwickeln' in text_lower:
            concepts.append('learning')
        if 'verstehen' in text_lower or 'empathisch' in text_lower:
            concepts.append('empathy')
        if 'systemisch' in text_lower or 'muster' in text_lower:
            concepts.append('systemic_thinking')
        
        return concepts
    
    def analyze_emotional_tone(self, text):
        """Analysiert emotionalen Ton"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['froh', 'glücklich', 'gut']):
            return 'positive'
        elif any(word in text_lower for word in ['traurig', 'schlecht', 'schwierig']):
            return 'negative'
        elif any(word in text_lower for word in ['neutral', 'sachlich']):
            return 'neutral'
        else:
            return 'neutral'
    
    def recognize_intent(self, text):
        """Erkennt Absicht"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['hilfe', 'unterstützung', 'helfen']):
            return 'request_help'
        elif any(word in text_lower for word in ['aufgabe', 'task', 'strukturieren']):
            return 'task_request'
        elif any(word in text_lower for word in ['lernen', 'entwickeln']):
            return 'learning_request'
        elif any(word in text_lower for word in ['verstehen', 'analysieren']):
            return 'analysis_request'
        else:
            return 'general_conversation'
    
    def generate_systemic_insights(self, text):
        """Generiert systemische Einsichten"""
        insights = []
        
        if 'muster' in text.lower():
            insights.append("Erkennung von Verhaltensmustern")
        if 'zusammenhang' in text.lower():
            insights.append("Systemische Zusammenhänge identifiziert")
        if 'entwicklung' in text.lower():
            insights.append("Entwicklungsprozess erkannt")
        
        return insights
    
    def extract_learning_patterns(self, text):
        """Extrahiert Lernmuster"""
        patterns = []
        
        if 'wiederholung' in text.lower():
            patterns.append("Wiederholungsmuster erkannt")
        if 'verbesserung' in text.lower():
            patterns.append("Verbesserungsmuster identifiziert")
        if 'anpassung' in text.lower():
            patterns.append("Anpassungsmuster erkannt")
        
        return patterns
    
    def save_analysis(self, analysis):
        """Speichert MCP-Analyse"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mcp_analysis_{timestamp}.yaml"
        filepath = os.path.join(self.mind_system_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(analysis, f, default_flow_style=False, allow_unicode=True)

class OttoVoiceAgent:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.mcp_system = MCPSystem()
        self.conversation_active = False
        self.conversation_timeout = 30  # Sekunden
        self.last_conversation_time = 0
        self.speaking_queue = queue.Queue()
        
        # Claude Client
        if CLAUDE_API_KEY:
            self.claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        else:
            self.claude_client = None

        # OpenAI Client
        if OPENAI_API_KEY:
            openai.api_key = OPENAI_API_KEY
            self.openai_available = True
        else:
            self.openai_available = False
        
        # ElevenLabs Setup
        if ELEVENLABS_API_KEY:
            set_api_key(ELEVENLABS_API_KEY)
        
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
        """Generiert Antwort mit Claude API oder lokaler Logik"""
        
        # MCP-Analyse
        mcp_analysis = self.mcp_system.analyze_input(input_text, context)
        
        # Verwende Claude API wenn verfügbar
        if self.claude_client:
            try:
                response = self.claude_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=150,
                    messages=[{
                        "role": "user",
                        "content": f"""Du bist Otto, ein empathischer, strukturierter Task-Begleiter.
                        MCP-Level: {mcp_analysis['mcp_level']}
                        Kontext: {context}
                        Benutzer-Input: {input_text}

                        Antworte kurz, empathisch und hilfreich. Maximal 2 Sätze."""
                    }]
                )
                return response.content[0].text.strip()
            except Exception as e:
                print(f"❌ Claude-Fehler: {e}")

        # Fallback: OpenAI
        if self.openai_available:
            try:
                response = openai.ChatCompletion.create(
                    model=OPENAI_MODEL,
                    messages=[{
                        "role": "user",
                        "content": f"Du bist Otto, ein empathischer, strukturierter Task-Begleiter.\nMCP-Level: {mcp_analysis['mcp_level']}\nKontext: {context}\nBenutzer-Input: {input_text}\nAntworte kurz, empathisch und hilfreich. Maximal 2 Sätze."
                    }],
                    max_tokens=150
                )
                return response.choices[0].message["content"].strip()
            except Exception as e:
                print(f"❌ OpenAI-Fehler: {e}")

        # Lokaler Fallback
        return self.generate_local_response(input_text, mcp_analysis)
    
    def generate_local_response(self, input_text, mcp_analysis):
        """Generiert lokale Antwort basierend auf MCP-Analyse"""
        mcp_level = mcp_analysis['mcp_level']
        intent = mcp_analysis['semantic_analysis']['intent_recognition']
        
        responses = {
            'request_help': [
                "Ich bin hier, um dir zu helfen. Was brauchst du?",
                "Gerne unterstütze ich dich. Was kann ich für dich tun?",
                "Ich höre zu und bin bereit zu helfen."
            ],
            'task_request': [
                "Ich kann dir dabei helfen, Aufgaben zu strukturieren. Was soll organisiert werden?",
                "Gerne helfe ich dir bei der Aufgabenverwaltung. Was steht an?",
                "Ich erkenne deine Aufgabe und kann sie strukturieren."
            ],
            'learning_request': [
                "Ich lerne aus jeder Interaktion und entwickle mich weiter.",
                "Das ist ein interessanter Lernprozess für uns beide.",
                "Ich verstehe dein Lernbedürfnis und begleite dich dabei."
            ],
            'analysis_request': [
                "Ich analysiere das semantisch und systemisch.",
                "Ich verstehe deine Anfrage und kann sie strukturieren.",
                "Ich denke strukturiert und helfe dir dabei."
            ],
            'general_conversation': [
                "Ich verstehe deine Anfrage. Ich kann Tasks verwalten, analysieren und strukturieren. Wie kann ich dir helfen?",
                "Ich denke strukturiert und helfe dir dabei, deine Gedanken zu ordnen. Was beschäftigt dich?",
                "Ja, ich höre dich. Ich bin Otto, dein stiller Begleiter."
            ]
        }
        
        import random
        return random.choice(responses.get(intent, responses['general_conversation']))
    
    def speak_response(self, text):
        """Spricht Antwort mit ElevenLabs"""
        if not ELEVENLABS_API_KEY:
            print(f"🗣️  Otto sagt: {text}")
            return
        
        try:
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
        print("🧠 OTTO - Final Clean Version")
        print("=" * 60)
        print(f"🎯 Trigger-Wörter: {', '.join(TRIGGER_WORDS)}")
        print(f"🧠 MCP-System: Aktiviert")
        print(f"🎤 Claude API: {'✅ Verfügbar' if self.claude_client else '❌ Nicht verfügbar'}")
        print(f"🤖 OpenAI API: {'✅ Verfügbar' if self.openai_available else '❌ Nicht verfügbar'}")
        print(f"🎵 ElevenLabs: {'✅ Verfügbar' if ELEVENLABS_API_KEY else '❌ Nicht verfügbar'}")
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
                        
                        # Generiere Antwort
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
                            # Generiere Antwort
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
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")
                time.sleep(1)

if __name__ == "__main__":
    agent = OttoVoiceAgent()
    agent.run() 