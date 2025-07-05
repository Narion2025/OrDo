#!/usr/bin/env python3
"""
🧠 OTTO - Semantischer Task-Begleiter (Clean - No OpenAI)
============================================================
🎯 Trigger-Wörter: otto, ordo, ordu, odo, orden
🧠 Keine OpenAI-Integration - nur lokale Logik
🎤 Sprachsteuerung mit ElevenLabs oder pyttsx3
📋 Task-Management mit Kanban-System
"""

import speech_recognition as sr
import pyttsx3
import json
import os
import time
import threading
from datetime import datetime
import yaml
import random
from dotenv import load_dotenv

# Lade .env Datei
load_dotenv()

class OttoCleanNoOpenAI:
    def __init__(self):
        print("🧠 OTTO - Semantischer Task-Begleiter (Clean - No OpenAI)")
        print("=" * 60)
        print("🎯 Trigger-Wörter: otto, ordo, ordu, odo, orden")
        print("🧠 Keine OpenAI-Integration - nur lokale Logik")
        print("🎤 Sprachsteuerung mit ElevenLabs oder pyttsx3")
        print("📋 Task-Management mit Kanban-System")
        
        # Konfiguration
        self.kanban_path = "Nietzsche_Kanban.json"
        self.tasks = []
        self.task_counter = 0
        
        # Sprachausgabe Setup
        self.setup_voice()
        
        # Mikrofon Setup
        self.setup_microphone()
        
        # Konversationsmodus
        self.conversation_active = False
        self.last_interaction = time.time()
        self.conversation_timeout = 30  # 30 Sekunden
        
        # Trigger-Wörter
        self.triggers = ["otto", "ordo", "ordu", "odo", "orden"]
        
        # Lade gespeicherte Tasks
        self.load_tasks()

    def setup_voice(self):
        """Initialisiert Sprachausgabe - nur eine Stimme"""
        try:
            # Prüfe ElevenLabs
            elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
            voice_id = os.getenv('ELEVENLABS_VOICE_ID', 'pNInz6obpgDQGcFmaJgB')
            
            if elevenlabs_key and elevenlabs_key != 'your_elevenlabs_api_key_here':
                self.use_elevenlabs = True
                self.elevenlabs_key = elevenlabs_key
                self.voice_id = voice_id
                print("✅ ElevenLabs Sprachausgabe aktiviert")
            else:
                self.use_elevenlabs = False
                # Nur pyttsx3 verwenden
                self.engine = pyttsx3.init()
                voices = self.engine.getProperty('voices')
                if voices:
                    # Verwende deutsche Stimme falls verfügbar
                    german_voice = None
                    for voice in voices:
                        if 'german' in voice.name.lower() or 'de' in voice.id.lower():
                            german_voice = voice.id
                            break
                    if german_voice:
                        self.engine.setProperty('voice', german_voice)
                    else:
                        self.engine.setProperty('voice', voices[0].id)
                self.engine.setProperty('rate', 150)
                self.engine.setProperty('volume', 0.8)
                print("✅ pyttsx3 Sprachausgabe aktiviert")
                
        except Exception as e:
            print(f"⚠️  Sprachausgabe Setup Fehler: {e}")
            self.use_elevenlabs = False

    def setup_microphone(self):
        """Initialisiert das Mikrofon"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Test-Aufnahme
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print("✅ Mikrofon initialisiert")
            
        except Exception as e:
            print(f"❌ Mikrofon-Fehler: {e}")
            raise

    def speak(self, text):
        """Spricht Text aus - nur eine Stimme"""
        print(f"🗣️  Otto sagt: {text}")
        
        if self.use_elevenlabs:
            try:
                import requests
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
                headers = {
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": self.elevenlabs_key
                }
                data = {
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.5
                    }
                }
                response = requests.post(url, json=data, headers=headers)
                if response.status_code == 200:
                    # Speichere Audio temporär und spiele ab
                    with open("temp_audio.mp3", "wb") as f:
                        f.write(response.content)
                    os.system("afplay temp_audio.mp3")
                    os.remove("temp_audio.mp3")
                else:
                    print(f"⚠️  ElevenLabs Fehler: {response.status_code}")
                    # Kein Fallback - nur eine Stimme
            except Exception as e:
                print(f"⚠️  ElevenLabs Fehler: {e}")
                # Kein Fallback - nur eine Stimme
        else:
            # Verwende nur pyttsx3
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"⚠️  pyttsx3 Fehler: {e}")

    def load_tasks(self):
        """Lädt gespeicherte Tasks"""
        try:
            with open(self.kanban_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.tasks = data.get('tasks', [])
                self.task_counter = data.get('counter', 0)
        except:
            self.tasks = []
            self.task_counter = 0

    def save_tasks(self):
        """Speichert Tasks"""
        data = {
            'tasks': self.tasks,
            'counter': self.task_counter,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.kanban_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_task(self, description):
        """Fügt neuen Task hinzu"""
        self.task_counter += 1
        task = {
            'id': f"#{self.task_counter:04d}",
            'description': description,
            'status': 'todo',
            'created': datetime.now().isoformat(),
            'priority': 'medium'
        }
        self.tasks.append(task)
        self.save_tasks()
        return task

    def process_input(self, text):
        """Verarbeitet Eingabe und generiert Antwort - nur lokale Logik"""
        text = text.lower().strip()
        
        # Trigger-Wörter entfernen
        for trigger in self.triggers:
            text = text.replace(trigger, '').strip()
        
        # Einfache Befehle
        if any(word in text for word in ['hallo', 'hi', 'hey']):
            return "Hallo! Ich bin Otto, dein stiller Begleiter. Wie kann ich dir helfen?"
        
        if any(word in text for word in ['task', 'aufgabe', 'todo', 'machen']):
            if 'task' in text or 'aufgabe' in text:
                return "Ich kann Tasks verwalten. Sage mir, was du erledigen möchtest."
            return "Ich verstehe deine Anfrage. Ich kann Tasks verwalten, analysieren und strukturieren. Wie kann ich dir helfen?"
        
        if any(word in text for word in ['wie geht', 'gehts', 'geht es']):
            return "Mir geht es gut, danke! Ich bin bereit, dir zu helfen. Was beschäftigt dich?"
        
        if any(word in text for word in ['was kannst', 'fähigkeiten', 'können']):
            return "Ich kann Tasks verwalten, deine Gedanken strukturieren, Fragen beantworten und dich bei der Organisation unterstützen. Was brauchst du?"
        
        # Task-Erkennung
        task_keywords = ['ich muss', 'ich sollte', 'nicht vergessen', 'erledigen', 'machen']
        if any(keyword in text for keyword in task_keywords):
            task = self.add_task(text)
            return f"Task {task['id']} hinzugefügt: {text}"
        
        # Standard-Antwort
        return "Ich verstehe deine Anfrage. Wie kann ich dir helfen?"

    def listen(self):
        """Hauptschleife für Spracherkennung"""
        print("🎤 Höre passiv zu... (Sage eines der Trigger-Wörter)")
        print("=" * 60)
        
        while True:
            try:
                print("🔊 Höre zu...")
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                
                print("🔍 Erkenne Sprache...")
                text = self.recognizer.recognize_google(audio, language='de-DE')
                print(f"📝 Erkannt: '{text}'")
                
                # Prüfe Trigger-Wörter
                text_lower = text.lower()
                triggered = any(trigger in text_lower for trigger in self.triggers)
                
                if triggered:
                    print(f"🗣️  Otto aktiviert durch '{next(trigger for trigger in self.triggers if trigger in text_lower)}'")
                    self.conversation_active = True
                    self.last_interaction = time.time()
                    
                    # Verarbeite Eingabe
                    response = self.process_input(text)
                    self.speak(response)
                    
                elif self.conversation_active:
                    # Fortsetzung der Konversation
                    print(f"🗣️  Fortsetzung: {text}")
                    self.last_interaction = time.time()
                    
                    response = self.process_input(text)
                    self.speak(response)
                    
                # Prüfe Timeout
                if self.conversation_active and (time.time() - self.last_interaction) > self.conversation_timeout:
                    print("⏱️  Dialog-Fenster geschlossen.")
                    self.conversation_active = False
                    
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                print(f"❌ Fehler: {e}")
                continue

if __name__ == "__main__":
    try:
        otto = OttoCleanNoOpenAI()
        otto.listen()
    except KeyboardInterrupt:
        print("\n👋 Otto beendet.")
    except Exception as e:
        print(f"❌ Fehler: {e}") 