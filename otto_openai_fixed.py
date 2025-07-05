#!/usr/bin/env python3
"""
🧠 OTTO - Semantischer Task-Begleiter (OpenAI Fixed)
============================================================
🎯 Trigger-Wörter: otto, ordo, ordu, odo, orden
🧠 OpenAI-Integration mit korrekter API-Version
🎤 Sprachsteuerung mit ElevenLabs
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

# OpenAI Import (Version 0.28)
import openai

# Lade .env Datei
load_dotenv()

class OttoOpenAIFixed:
    def __init__(self):
        print("🧠 OTTO - Semantischer Task-Begleiter (OpenAI Fixed)")
        print("=" * 60)
        print("🎯 Trigger-Wörter: otto, ordo, ordu, odo, orden")
        print("🧠 OpenAI-Integration mit korrekter API-Version")
        print("🎤 Sprachsteuerung mit ElevenLabs")
        print("📋 Task-Management mit Kanban-System")
        
        # OpenAI Setup
        self.setup_openai()
        
        # Mikrofon und Spracherkennung
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Task-Management
        self.tasks = []
        self.task_counter = 0
        self.load_tasks()
        
        # Konversationsmodus
        self.conversation_active = False
        self.conversation_timeout = 30  # Sekunden
        self.last_interaction = time.time()
        
        # Stimme
        self.setup_voice()
        
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

    def setup_openai(self):
        """Initialisiert OpenAI mit korrekter Version"""
        try:
            # Lade API-Key aus .env oder verwende Standard
            api_key = os.getenv('OPENAI_API_KEY', 'sk-7f784c3c4dc74dde1d037474d515709047ad9b577fb48f28')
            openai.api_key = api_key
            self.openai_available = True
            print("✅ OpenAI erfolgreich initialisiert")
        except Exception as e:
            print(f"⚠️  OpenAI Setup Fehler: {e}")
            self.openai_available = False

    def setup_voice(self):
        """Initialisiert Sprachausgabe"""
        try:
            # Prüfe ElevenLabs
            elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
            if elevenlabs_key and elevenlabs_key != 'your_elevenlabs_api_key_here':
                self.use_elevenlabs = True
                self.elevenlabs_key = elevenlabs_key
                self.voice_id = os.getenv('ELEVENLABS_VOICE_ID', 'pNInz6obpgDQGcFmaJgB')
                print("✅ ElevenLabs verfügbar")
            else:
                self.use_elevenlabs = False
                # Fallback: pyttsx3
                self.engine = pyttsx3.init()
                voices = self.engine.getProperty('voices')
                if voices:
                    self.engine.setProperty('voice', voices[0].id)
                self.engine.setProperty('rate', 150)
                print("✅ pyttsx3 Sprachausgabe aktiviert")
        except Exception as e:
            print(f"⚠️  Sprachausgabe Setup Fehler: {e}")
            self.use_elevenlabs = False

    def speak(self, text):
        """Spricht Text aus"""
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
                    "model_id": "eleven_monolingual_v1",
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
            except Exception as e:
                print(f"⚠️  ElevenLabs Fehler: {e}")
                # Fallback zu pyttsx3
                if hasattr(self, 'engine'):
                    self.engine.say(text)
                    self.engine.runAndWait()
        else:
            # Verwende pyttsx3
            if hasattr(self, 'engine'):
                self.engine.say(text)
                self.engine.runAndWait()

    def load_tasks(self):
        """Lädt gespeicherte Tasks"""
        try:
            with open('Nietzsche_Kanban.json', 'r', encoding='utf-8') as f:
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
        with open('Nietzsche_Kanban.json', 'w', encoding='utf-8') as f:
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
        """Verarbeitet Eingabe und generiert Antwort"""
        text = text.lower().strip()
        
        # Trigger-Wörter entfernen
        triggers = ['otto', 'ordo', 'ordu', 'odo', 'orden']
        for trigger in triggers:
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
        
        # Wenn OpenAI verfügbar, erweitere die Antwort
        if self.openai_available:
            try:
                enhanced_response = self.enhance_with_openai(text)
                return enhanced_response
            except Exception as e:
                print(f"⚠️  OpenAI-Erweiterung fehlgeschlagen: {e}")
                return "Ich verstehe deine Anfrage. Wie kann ich dir helfen?"
        else:
            return "Ich verstehe deine Anfrage. Wie kann ich dir helfen?"

    def enhance_with_openai(self, text):
        """Erweitert Antwort mit OpenAI"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Du bist Otto, ein stiller, strukturierter und empathischer Begleiter. Du antwortest kurz, freundlich und hilfreich. Du bist ruhig, reflektiert und unterstützt bei der Organisation von Gedanken und Aufgaben."},
                    {"role": "user", "content": f"Antworte auf diese Anfrage: {text}"}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ OpenAI-Fehler: {e}")
            return "Ich verstehe deine Anfrage. Wie kann ich dir helfen?"

    def listen(self):
        """Hauptschleife für Spracherkennung"""
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
                triggers = ['otto', 'ordo', 'ordu', 'odo', 'orden']
                triggered = any(trigger in text_lower for trigger in triggers)
                
                if triggered:
                    print(f"🗣️  Otto aktiviert durch '{next(trigger for trigger in triggers if trigger in text_lower)}'")
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
    otto = OttoOpenAIFixed()
    otto.listen() 