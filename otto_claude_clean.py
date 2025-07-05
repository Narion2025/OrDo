#!/usr/bin/env python3
"""
OTTO - Claude-Only Clean System
================================
Saubere Version ohne OpenAI-Konflikte
- Nur Claude API
- ElevenLabs Stimme
- MCP-System Integration
- Keine doppelten Stimmen
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

class OttoClaudeClean:
    def __init__(self):
        self.name = "Otto"
        self.trigger_words = ["otto", "ordo", "ordu", "odo", "orden"]
        self.conversation_active = False
        self.conversation_timeout = 30
        self.last_activity = time.time()
        
        # Claude API Setup
        self.claude_client = None
        self.setup_claude()
        
        # ElevenLabs Setup
        self.elevenlabs_voice_id = os.getenv('ELEVENLABS_VOICE_ID', "21m00Tcm4TlvDq8ikWAM")
        self.setup_elevenlabs()
        
        # Mind-System Verzeichnisse
        self.mind_base = Path.home() / "Documents" / "Otto_Claude_Clean_System"
        self.skk_dir = self.mind_base / "SKK"
        self.mcp_dir = self.mind_base / "MCP"
        self.resonance_dir = self.mind_base / "Resonance"
        self.context_dir = self.mind_base / "Context"
        self.ben_memory_dir = self.mind_base / "Ben_Memory"
        self.otto_self_dir = self.mind_base / "Otto_Self"
        
        # Initialisiere Verzeichnisse
        self.setup_directories()
        
        # Mikrofon Setup
        self.setup_microphone()
        
        # Task-Management
        self.tasks = []
        self.task_counter = 0
        
        print(f"🧠 {self.name.upper()} - Claude-Only Clean System")
        print("=" * 60)
        print(f"🎯 Trigger-Wörter: {', '.join(self.trigger_words)}")
        print(f"🧠 Claude API: {'Verbunden' if self.claude_client else 'Nicht verfügbar'}")
        print(f"🎤 ElevenLabs: {'Verbunden' if self.elevenlabs_voice_id else 'Nicht verfügbar'}")
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
        """Initialisiert ElevenLabs API"""
        if self.elevenlabs_voice_id:
            print("✅ ElevenLabs API erfolgreich initialisiert")
        else:
            print("⚠️  ElevenLabs Voice-ID nicht gefunden")
            print("Setze ELEVENLABS_VOICE_ID Umgebungsvariable")

    def setup_directories(self):
        """Erstellt die Mind-System Verzeichnisstruktur"""
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

    def speak(self, text):
        """Spricht Text über ElevenLabs oder lokale Engine"""
        if not text:
            return
            
        def speak_thread():
            try:
                if self.elevenlabs_voice_id:
                    # ElevenLabs API
                    url = "https://api.elevenlabs.io/v1/text-to-speech/" + self.elevenlabs_voice_id
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
                        # Speichere Audio
                        audio_file = self.mind_base / f"otto_response_{int(time.time())}.mp3"
                        with open(audio_file, "wb") as f:
                            f.write(response.content)
                        
                        # Spiele Audio ab
                        os.system(f'afplay "{audio_file}"')
                    else:
                        print(f"❌ ElevenLabs Fehler: {response.status_code}")
                        self.speak_local(text)
                else:
                    self.speak_local(text)
                    
            except Exception as e:
                print(f"❌ Sprachausgabe Fehler: {e}")
                self.speak_local(text)
        
        threading.Thread(target=speak_thread).start()

    def speak_local(self, text):
        """Lokale Sprachausgabe als Fallback"""
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.8)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"❌ Lokale Sprachausgabe Fehler: {e}")

    def process_input(self, text):
        """Verarbeitet Eingabe mit Claude API oder lokaler Logik"""
        if not text:
            return "Ich verstehe deine Anfrage nicht."
            
        # Entferne Trigger-Wörter
        clean_text = text.lower()
        for trigger in self.trigger_words:
            clean_text = clean_text.replace(trigger, "").strip()
        
        if not clean_text:
            return "Ja, ich höre dich. Ich bin Otto, dein stiller Begleiter."
        
        # Claude API für komplexe Antworten
        if self.claude_client:
            try:
                response = self.claude_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1000,
                    messages=[
                        {
                            "role": "user",
                            "content": f"""Du bist Otto, ein empathischer, strukturierter KI-Assistent. 
                            Antworte auf Deutsch, sei hilfsbereit und strukturiert.
                            Benutzer: {clean_text}"""
                        }
                    ]
                )
                return response.content[0].text
            except Exception as e:
                print(f"❌ Claude API Fehler: {e}")
                return self.local_response(clean_text)
        else:
            return self.local_response(clean_text)

    def local_response(self, text):
        """Lokale Antwortlogik als Fallback"""
        text_lower = text.lower()
        
        # Einfache Befehle
        if any(word in text_lower for word in ["hallo", "hi", "hey"]):
            return "Hallo! Ich bin Otto, dein stiller Begleiter. Wie kann ich dir helfen?"
        
        elif any(word in text_lower for word in ["hilfe", "help", "was kannst du"]):
            return "Ich kann dir bei der Strukturierung von Aufgaben helfen, Fragen beantworten und dich unterstützen. Was beschäftigt dich?"
        
        elif any(word in text_lower for word in ["test", "funktioniert"]):
            return "Otto Test erfolgreich. Ich höre zu und kann sprechen."
        
        elif any(word in text_lower for word in ["aufgabe", "task", "strukturieren"]):
            return "Ich verstehe, dass du etwas strukturieren möchtest. Was genau soll ich für dich organisieren?"
        
        else:
            return "Ich verstehe deine Anfrage. Ich kann Tasks verwalten, analysieren und strukturieren. Wie kann ich dir helfen?"

    def listen(self):
        """Hauptschleife für Spracherkennung"""
        print("🎤 Höre passiv zu... (Sage eines der Trigger-Wörter)")
        print("=" * 60)
        
        while True:
            try:
                with self.microphone as source:
                    print("🔊 Höre zu...")
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                try:
                    text = self.recognizer.recognize_google(audio, language="de-DE")
                    print(f"📝 Erkannt: '{text}'")
                    
                    # Prüfe Trigger-Wörter
                    text_lower = text.lower()
                    triggered = any(trigger in text_lower for trigger in self.trigger_words)
                    
                    if triggered:
                        print(f"🗣️  {self.name} aktiviert durch '{next(trigger for trigger in self.trigger_words if trigger in text_lower)}'")
                        
                        # Verarbeite Eingabe
                        response = self.process_input(text)
                        print(f"🧠 {self.name} verarbeitet: '{text}'")
                        print(f"🗣️  {self.name} sagt: {response}")
                        
                        # Spricht Antwort
                        self.speak(response)
                        
                        # Starte Konversation
                        self.conversation_active = True
                        self.last_activity = time.time()
                        
                    elif self.conversation_active:
                        # Fortsetzung der Konversation
                        print(f"🗣️  Fortsetzung: {text}")
                        
                        # Prüfe Timeout
                        if time.time() - self.last_activity > self.conversation_timeout:
                            print("⏱️  Dialog-Fenster geschlossen.")
                            self.conversation_active = False
                        else:
                            # Verarbeite Fortsetzung
                            response = self.process_input(text)
                            print(f"🧠 {self.name} verarbeitet: '{text}'")
                            print(f"🗣️  {self.name} sagt: {response}")
                            self.speak(response)
                            self.last_activity = time.time()
                    
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"❌ Spracherkennung Fehler: {e}")
                    
            except KeyboardInterrupt:
                print("\n👋 Otto wird beendet...")
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")

if __name__ == "__main__":
    load_dotenv()
    otto = OttoClaudeClean()
    otto.listen() 