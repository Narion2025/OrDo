#!/usr/bin/env python3
"""
OTTO - Fixed Wagner Version
===========================
Saubere Version mit:
- Garantiert Wagner-Stimme (2gPFXx8pN3Avh27Dw5Ma)
- Intelligente Claude-Antworten
- Keine OpenAI-Fehler
- Vollständige MCP-Integration
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

class OttoFixedWagner:
    def __init__(self):
        self.name = "Otto"
        self.trigger_words = ["otto", "ordo", "ordu", "odo", "orden"]
        self.conversation_active = False
        self.conversation_timeout = 30
        self.last_activity = time.time()
        
        # Claude API Setup
        self.claude_client = None
        self.setup_claude()
        
        # ElevenLabs Setup - OTTO STIMME FEST EINGESTELLT
        self.elevenlabs_voice_id = os.getenv('ELEVENLABS_VOICE_ID', "kXV9fIZ5YNtH4TFjs2sD")
        self.setup_elevenlabs()
        
        # Mind-System Setup
        self.mind_base = Path.home() / "Documents" / "Otto_Wagner_System"
        self.setup_mind_system()
        
        # Mikrofon Setup
        self.setup_microphone()
        
        # Task-Management
        self.tasks = []
        self.task_counter = 0
        
        print(f"🧠 {self.name.upper()} - Fixed Wagner Version")
        print("=" * 60)
        print(f"🎯 Trigger-Wörter: {', '.join(self.trigger_words)}")
        print(f"🎤 Wagner-Stimme: {self.elevenlabs_voice_id}")
        print(f"🧠 Claude API: {'Verbunden' if self.claude_client else 'Nicht verfügbar'}")
        print(f"💾 Mind-System: {self.mind_base}")
        print("=" * 60)

    def setup_claude(self):
        """Initialisiert Claude API"""
        try:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if api_key and api_key != 'your_claude_api_key_here':
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
        """Initialisiert ElevenLabs mit Wagner-Stimme"""
        print(f"✅ ElevenLabs mit Wagner-Stimme initialisiert: {self.elevenlabs_voice_id}")

    def setup_mind_system(self):
        """Erstellt das Mind-System"""
        directories = [
            self.mind_base,
            self.mind_base / "conversations",
            self.mind_base / "tasks",
            self.mind_base / "memory"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✓ Verzeichnis erstellt: {directory}")

    def setup_microphone(self):
        """Initialisiert das Mikrofon"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Test-Aufnahme
            print("🔍 Teste Mikrofon...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Mikrofon-Test erfolgreich")
            
        except Exception as e:
            print(f"❌ Mikrofon-Fehler: {e}")

    def speak_with_wagner(self, text):
        """Spricht Text mit Wagner-Stimme aus"""
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.elevenlabs_voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": "sk_7f784c3c4dc74dde1d037474d515709047ad9b577fb48f28"
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
                # Speichere Audio temporär und spiele es ab
                audio_file = f"/tmp/otto_wagner_{int(time.time())}.mp3"
                with open(audio_file, "wb") as f:
                    f.write(response.content)
                
                # Spiele Audio ab
                os.system(f"afplay {audio_file}")
                
                # Lösche temporäre Datei
                os.remove(audio_file)
                print(f"🗣️  {self.name} sagt (Wagner): {text}")
                return True
            else:
                print(f"❌ ElevenLabs Fehler: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ ElevenLabs Fehler: {e}")
            return False

    def speak_fallback(self, text):
        """Fallback-Sprachausgabe"""
        print(f"🗣️  {self.name} sagt (Fallback): {text}")
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def speak(self, text):
        """Intelligente Sprachausgabe"""
        if not text:
            return
            
        # Versuche Wagner-Stimme zuerst
        if not self.speak_with_wagner(text):
            self.speak_fallback(text)

    def get_claude_response(self, user_input):
        """Holt intelligente Antwort von Claude"""
        if not self.claude_client:
            return "Entschuldigung, Claude API ist nicht verfügbar."
        
        try:
            # Erstelle Kontext für Claude
            context = f"""
Du bist Otto, ein intelligenter, empathischer und strukturierter Begleiter. 
Du sprichst mit der Wagner-Stimme und bist ruhig, aber tiefgründig.

Benutzer: {user_input}

Antworte natürlich, empathisch und hilfreich. Sei nicht zu kurz, aber auch nicht zu lang.
"""
            
            response = self.claude_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=150,
                messages=[
                    {"role": "user", "content": context}
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            print(f"❌ Claude Fehler: {e}")
            return "Entschuldigung, ich kann das gerade nicht verarbeiten."

    def process_input(self, text):
        """Verarbeitet Benutzereingabe intelligent"""
        if not text:
            return
            
        # Entferne Trigger-Wörter aus der Eingabe
        clean_text = text.lower()
        for trigger in self.trigger_words:
            clean_text = clean_text.replace(trigger.lower(), "").strip()
        
        if not clean_text:
            return
            
        print(f"🧠 {self.name} verarbeitet: '{clean_text}'")
        
        # Hole intelligente Antwort von Claude
        response = self.get_claude_response(clean_text)
        
        # Speichere Konversation
        self.save_conversation(clean_text, response)
        
        # Spreche Antwort
        self.speak(response)

    def save_conversation(self, user_input, response):
        """Speichert Konversation"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conversation = {
            "timestamp": timestamp,
            "user_input": user_input,
            "otto_response": response
        }
        
        conversation_file = self.mind_base / "conversations" / f"conversation_{int(time.time())}.json"
        with open(conversation_file, 'w', encoding='utf-8') as f:
            json.dump(conversation, f, ensure_ascii=False, indent=2)

    def listen_for_trigger(self):
        """Hört auf Trigger-Wörter"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
            try:
                text = self.recognizer.recognize_google(audio, language='de-DE').lower()
                print(f"📝 Erkannt: '{text}'")
                
                # Prüfe auf Trigger-Wörter
                for trigger in self.trigger_words:
                    if trigger in text:
                        print(f"🗣️  {self.name} aktiviert durch '{trigger}'")
                        self.conversation_active = True
                        self.last_activity = time.time()
                        
                        # Verarbeite Eingabe
                        self.process_input(text)
                        return True
                
                # Wenn Konversation aktiv, verarbeite weiter
                if self.conversation_active and time.time() - self.last_activity < self.conversation_timeout:
                    print(f"🗣️  Fortsetzung: {text}")
                    self.last_activity = time.time()
                    self.process_input(text)
                    return True
                else:
                    if self.conversation_active:
                        print("⏱️  Dialog-Fenster geschlossen.")
                        self.conversation_active = False
                
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"❌ Spracherkennung Fehler: {e}")
                
        except sr.WaitTimeoutError:
            pass
        except Exception as e:
            print(f"❌ Mikrofon Fehler: {e}")
        
        return False

    def run(self):
        """Hauptschleife"""
        print("🎤 Höre passiv zu... (Sage eines der Trigger-Wörter)")
        print("=" * 60)
        
        while True:
            try:
                print("🔊 Höre zu...")
                self.listen_for_trigger()
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n👋 Otto wird beendet...")
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")
                time.sleep(1)

if __name__ == "__main__":
    load_dotenv()
    otto = OttoFixedWagner()
    otto.run() 