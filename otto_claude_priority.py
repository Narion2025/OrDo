#!/usr/bin/env python3
"""
OTTO - Claude Priority System
==============================
Saubere Version mit Claude-Priorität
- Claude für komplexe Aufgaben
- Lokale Logik nur als Fallback
- Keine doppelten Stimmen
- ElevenLabs Integration
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

class OttoClaudePriority:
    def __init__(self):
        self.name = "Otto"
        self.trigger_words = ["otto", "ordo", "ordu", "odo", "orden"]
        self.conversation_active = False
        self.conversation_timeout = 30
        self.last_activity = time.time()
        
        # Claude Setup
        self.claude_client = None
        self.setup_claude()
        
        # ElevenLabs Setup
        self.elevenlabs_voice_id = os.getenv('ELEVENLABS_VOICE_ID', "21m00Tcm4TlvDq8ikWAM")
        self.setup_elevenlabs()
        
        # MCP System
        self.mcp_levels = {
            0: "Basis-Verständnis",
            1: "Kontextuelle Analyse", 
            2: "Systemische Einsicht",
            3: "Meta-Reflexion",
            4: "Emergente Intelligenz",
            5: "Transzendente Weisheit"
        }
        
        # Verzeichnisstruktur erstellen
        self.setup_directories()
        
        # Mikrofon Setup
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Task-Management
        self.tasks = []
        self.task_counter = 0
        
        print("🧠 OTTO - Claude Priority System")
        print("==================================")
        print("🎯 Claude bevorzugt für komplexe Aufgaben")
        print("🎤 Lokale Logik nur als Fallback")
        print("🔇 Keine doppelten Stimmen")
        print("")

    def setup_claude(self):
        """Claude API Setup"""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key and api_key != "sk-ant-api03-dein-claude-key-hier":
            try:
                self.claude_client = anthropic.Anthropic(api_key=api_key)
                print("✅ Claude API erfolgreich initialisiert")
            except Exception as e:
                print(f"⚠️  Claude API Fehler: {e}")
                self.claude_client = None
        else:
            print("⚠️  Claude API-Key nicht gefunden")
            print("Setze ANTHROPIC_API_KEY Umgebungsvariable")
            self.claude_client = None

    def setup_elevenlabs(self):
        """ElevenLabs Setup"""
        try:
            # Test ElevenLabs Verbindung
            response = requests.get("https://api.elevenlabs.io/v1/voices", timeout=5)
            if response.status_code == 200:
                print("✅ ElevenLabs API erfolgreich initialisiert")
            else:
                print("⚠️  ElevenLabs API nicht verfügbar")
        except:
            print("⚠️  ElevenLabs API nicht verfügbar")

    def setup_directories(self):
        """Erstelle Verzeichnisstruktur"""
        base_dir = Path.home() / "Documents" / "Otto_Claude_Priority_System"
        base_dir.mkdir(exist_ok=True)
        
        # SKK-Struktur
        (base_dir / "SKK" / "strudel").mkdir(parents=True, exist_ok=True)
        (base_dir / "SKK" / "knoten").mkdir(parents=True, exist_ok=True)
        (base_dir / "SKK" / "kristalle").mkdir(parents=True, exist_ok=True)
        (base_dir / "SKK" / "system").mkdir(parents=True, exist_ok=True)
        
        # MCP-Struktur
        (base_dir / "MCP" / "analysis").mkdir(parents=True, exist_ok=True)
        (base_dir / "MCP" / "behavior").mkdir(parents=True, exist_ok=True)
        (base_dir / "MCP" / "levels").mkdir(parents=True, exist_ok=True)
        
        # Jammeldateien
        (base_dir / "jammel").mkdir(exist_ok=True)
        
        print("✓ Verzeichnisstruktur erstellt")

    def speak_with_elevenlabs(self, text):
        """Spreche mit ElevenLabs"""
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.elevenlabs_voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": os.getenv('ELEVENLABS_API_KEY', '')
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
                # Audio abspielen
                with open("temp_audio.mp3", "wb") as f:
                    f.write(response.content)
                os.system("afplay temp_audio.mp3")
                os.remove("temp_audio.mp3")
            else:
                # Fallback zu pyttsx3
                self.speak_fallback(text)
        except:
            self.speak_fallback(text)

    def speak_fallback(self, text):
        """Fallback Sprachausgabe"""
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def speak(self, text):
        """Intelligente Sprachausgabe"""
        print(f"🗣️  Otto sagt: {text}")
        
        # Versuche ElevenLabs, dann Fallback
        try:
            self.speak_with_elevenlabs(text)
        except:
            self.speak_fallback(text)

    def determine_mcp_level(self, text):
        """Bestimme MCP-Level basierend auf Text-Komplexität"""
        complexity_score = 0
        
        # Wortanzahl
        words = text.split()
        complexity_score += len(words) * 0.1
        
        # Komplexe Wörter
        complex_words = ['systemisch', 'emergent', 'meta', 'transzendent', 'reflexion']
        for word in complex_words:
            if word in text.lower():
                complexity_score += 2
        
        # Emotionale Intensität
        emotional_words = ['fühle', 'empfinde', 'verstehe', 'denke', 'glaube']
        for word in emotional_words:
            if word in text.lower():
                complexity_score += 1
        
        # Bestimme Level
        if complexity_score < 1:
            return 0
        elif complexity_score < 2:
            return 1
        elif complexity_score < 3:
            return 2
        elif complexity_score < 4:
            return 3
        elif complexity_score < 5:
            return 4
        else:
            return 5

    def analyze_with_claude(self, text, mcp_level):
        """Analysiere mit Claude API"""
        if not self.claude_client:
            return None
            
        try:
            level_description = self.mcp_levels.get(mcp_level, "Unbekanntes Level")
            
            prompt = f"""
            Du bist Otto, ein systemisch intelligenter Begleiter mit MCP-Level {mcp_level} ({level_description}).
            
            Benutzer sagte: "{text}"
            MCP-Level: {mcp_level} - {level_description}
            
            Antworte als Otto mit systemischem Verständnis und Empathie.
            Berücksichtige das MCP-Level {mcp_level} in deiner Antwort.
            Sei ruhig, strukturiert und lernfähig.
            Antworte kurz und prägnant.
            """
            
            response = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text.strip()
        except Exception as e:
            print(f"⚠️  Claude-Fehler: {e}")
            return None

    def generate_local_response(self, text, mcp_level):
        """Lokale Antwort-Generierung als Fallback"""
        level_responses = {
            0: "Ich verstehe. Wie kann ich dir helfen?",
            1: "Das ist interessant. Lass mich das verarbeiten.",
            2: "Ich sehe die Zusammenhänge. Was denkst du?",
            3: "Das wirft Fragen auf. Was beschäftigt dich?",
            4: "Das ist komplex. Lass uns das durchgehen.",
            5: "Das ist tiefgründig. Ich höre zu."
        }
        
        # Einfache Schlüsselwort-Erkennung
        if any(word in text.lower() for word in ['hallo', 'hi', 'hey']):
            return "Hallo! Ich bin Otto, dein Begleiter."
        elif any(word in text.lower() for word in ['wie', 'was', 'warum']):
            return "Das ist eine gute Frage. Lass mich nachdenken."
        elif any(word in text.lower() for word in ['danke', 'thanks']):
            return "Gerne! Ich bin hier, um zu helfen."
        else:
            return level_responses.get(mcp_level, "Ich verstehe. Erzähl mir mehr.")

    def process_input(self, text):
        """Verarbeite Eingabe mit Claude-Priorität"""
        if not text.strip():
            return "Wie kann ich dir helfen?"
        
        # MCP-Level bestimmen
        mcp_level = self.determine_mcp_level(text)
        
        # Versuche Claude zuerst
        claude_response = self.analyze_with_claude(text, mcp_level)
        
        if claude_response:
            # Claude erfolgreich - verwende seine Antwort
            return claude_response
        else:
            # Fallback zu lokaler Logik
            return self.generate_local_response(text, mcp_level)

    def listen_for_speech(self):
        """Höre kontinuierlich nach Sprache"""
        print("🎤 Initialisiere Mikrofon...")
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("✅ Mikrofon initialisiert")
        
        print("🔍 Teste Mikrofon...")
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                test_text = self.recognizer.recognize_google(audio, language='de-DE')
                print("✅ Mikrofon-Test erfolgreich")
        except:
            print("⚠️  Mikrofon-Test fehlgeschlagen")
        
        print("🎤 Höre passiv zu... (Sage eines der Trigger-Wörter)")
        print("=" * 60)
        
        while True:
            try:
                with self.microphone as source:
                    print("🔊 Höre zu...")
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                    
                print("🔍 Erkenne Sprache...")
                text = self.recognizer.recognize_google(audio, language='de-DE').lower()
                print(f"📝 Erkannt: '{text}'")
                
                # Trigger-Wort Erkennung
                trigger_detected = any(trigger in text for trigger in self.trigger_words)
                
                if trigger_detected:
                    # Trigger erkannt - starte Konversation
                    self.conversation_active = True
                    self.last_activity = time.time()
                    
                    # Entferne Trigger-Wort aus Text
                    for trigger in self.trigger_words:
                        text = text.replace(trigger, '').strip()
                    
                    print(f"🗣️  Otto aktiviert durch '{next(trigger for trigger in self.trigger_words if trigger in text)}'")
                    
                    if text:
                        print(f"🧠 Otto verarbeitet: '{text}'")
                        response = self.process_input(text)
                        self.speak(response)
                    else:
                        self.speak("Wie kann ich dir helfen?")
                        
                elif self.conversation_active:
                    # Konversation läuft
                    print(f"🗣️  Fortsetzung: {text}")
                    print(f"🧠 Otto verarbeitet: '{text}'")
                    
                    response = self.process_input(text)
                    self.speak(response)
                    
                    self.last_activity = time.time()
                    
                # Timeout prüfen
                if self.conversation_active and (time.time() - self.last_activity) > self.conversation_timeout:
                    print("⏱️  Dialog-Fenster geschlossen.")
                    self.conversation_active = False
                    
            except sr.WaitTimeoutError:
                # Timeout - prüfe ob Konversation beendet werden soll
                if self.conversation_active and (time.time() - self.last_activity) > self.conversation_timeout:
                    print("⏱️  Dialog-Fenster geschlossen.")
                    self.conversation_active = False
                continue
                
            except sr.UnknownValueError:
                continue
                
            except Exception as e:
                print(f"❌ Fehler: {e}")
                continue

if __name__ == "__main__":
    load_dotenv()
    otto = OttoClaudePriority()
    otto.listen_for_speech() 