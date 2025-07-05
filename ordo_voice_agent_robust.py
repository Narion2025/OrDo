import voice_config
import speech_recognition as sr
import time
import os
import threading
import json
import sys
import uuid
from pathlib import Path
from elevenlabs import generate, save, set_api_key

# ElevenLabs Setup
set_api_key("sk_7f784c3c4dc74dde1d037474d515709047ad9b577fb48f28")

# Ordo-spezifische Konfiguration
KANBAN_PATH = os.path.expanduser("~/Documents/Ordo/Ordo_Kanban.json")
PROJEKTE_ROOT = os.path.expanduser("~/Projekte")
ORDO_IDENTITY_PATH = os.path.join(os.path.dirname(__file__), "ordo_identity.txt")

# Ordo-Verhalten
recognizer = sr.Recognizer()
mic = None
# Flexible Trigger für bessere Spracherkennung
triggers = ["ordo", "otto", "ordu", "odo", "orden"]
listening = False
last_input_time = 0
dialog_timeout = 10
is_speaking = False

def init_microphone():
    """Initialisiert das Mikrofon mit besserer Fehlerbehandlung"""
    global mic
    
    print("🎤 Initialisiere Mikrofon...")
    
    try:
        # Versuche Standard-Mikrofon
        mic = sr.Microphone()
        print(f"✅ Mikrofon initialisiert")
        
        # Test-Aufnahme
        print("🔍 Teste Mikrofon...")
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ Mikrofon-Test erfolgreich")
        
        return True
        
    except Exception as e:
        print(f"❌ Mikrofon-Fehler: {e}")
        return False

def sprich(text):
    """Ordo spricht mit ruhiger, strukturierter Stimme"""
    global is_speaking
    if is_speaking:
        return
    
    def run():
        global is_speaking
        is_speaking = True
        try:
            print(f"🗣️  Ordo sagt: {text}")
            # Verwende die neue Ordo-Voice-ID
            audio = generate(
                text=text, 
                voice=voice_config.VOICE_ID_ORDO, 
                model="eleven_multilingual_v2"
            )
            filename = f"/tmp/ordo_{uuid.uuid4()}.mp3"
            save(audio, filename)
            os.system(f'afplay "{filename}"')
            time.sleep(0.5)  # Kurze Pause nach dem Sprechen
        except Exception as e:
            print(f"❌ Fehler bei der Sprachausgabe: {e}")
        finally:
            is_speaking = False
    
    threading.Thread(target=run).start()

def kanban_add_simple(task):
    """Fügt Task einfach hinzu"""
    try:
        # Erstelle Ordo-Verzeichnis falls nicht vorhanden
        ordo_dir = os.path.dirname(KANBAN_PATH)
        os.makedirs(ordo_dir, exist_ok=True)
        
        if not os.path.exists(KANBAN_PATH):
            with open(KANBAN_PATH, "w") as f:
                json.dump({"To Do": [], "In Progress": [], "Erledigt": []}, f)

        with open(KANBAN_PATH, "r") as f:
            board = json.load(f)

        # Erstelle Task-Eintrag
        task_entry = {
            "id": f"#{len(board.get('To Do', [])) + 1:04d}",
            "text": task,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        board["To Do"].append(task_entry)

        with open(KANBAN_PATH, "w") as f:
            json.dump(board, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Task {task_entry['id']} hinzugefügt: {task}")
        return task_entry['id']

    except Exception as e:
        print(f"❌ Fehler beim Schreiben ins Kanban: {e}")
        return None

def check_trigger(text):
    """Prüft ob ein Trigger-Wort im Text enthalten ist"""
    text_lower = text.lower()
    for trigger in triggers:
        if trigger in text_lower:
            return trigger
    return None

def passive_task_recognition(text):
    """Erkennt Tasks passiv ohne Antwort"""
    # Muster für Task-Erkennung
    task_patterns = [
        "ich muss", "ich sollte", "ich müsste",
        "nicht vergessen", "todo", "aufgabe",
        "erledigen", "machen", "organisieren"
    ]
    
    text_lower = text.lower()
    for pattern in task_patterns:
        if pattern in text_lower:
            # Füge Task hinzu (passiv, ohne Sprachausgabe)
            task_id = kanban_add_simple(text)
            
            # Logge nur intern
            print(f"🔍 Passiv erkannter Task: {task_id}")
            return True
    
    return False

def analysiere_befehl(text, detected_trigger):
    """Analysiert Befehle für Ordo"""
    # Entferne den Trigger aus dem Text
    text_clean = text.lower().replace(detected_trigger, "").strip()
    print(f"🧠 Ordo verarbeitet: '{text_clean}'")

    if not text_clean:
        sprich("Wie kann ich dir helfen?")
        return

    if "kanban" in text_clean or "aufgabe" in text_clean or "task" in text_clean:
        if "hinzu" in text_clean:
            aufgabe = text_clean.split("hinzu")[-1].strip()
            if aufgabe:
                task_id = kanban_add_simple(aufgabe)
                sprich(f"Task {task_id} hinzugefügt.")
        elif "zeige" in text_clean or "liste" in text_clean or "status" in text_clean:
            zeige_kanban()

    elif "test" in text_clean:
        sprich("Ordo Test erfolgreich. Ich höre zu und kann sprechen.")

    elif "hilfe" in text_clean or "help" in text_clean:
        sprich("Ich bin Ordo. Ich erkenne Tasks und strukturiere sie. Sag einfach was du machen musst.")

    elif "hallo" in text_clean or "hörst du mich" in text_clean:
        sprich("Ja, ich höre dich. Ich bin Ordo, dein stiller Begleiter.")

    elif "weiter" in text_clean or "mehr" in text_clean:
        sprich("Ich höre weiter zu. Sage mir was du brauchst.")

    else:
        # Standardantwort für unbekannte Befehle
        sprich("Was genau soll ich strukturieren?")

def zeige_kanban():
    """Zeigt Kanban-Status"""
    try:
        with open(KANBAN_PATH, "r") as f:
            board = json.load(f)
        
        todo_count = len(board.get("To Do", []))
        progress_count = len(board.get("In Progress", []))
        done_count = len(board.get("Erledigt", []))
        
        sprich(f"Kanban-Status: {todo_count} offen, {progress_count} in Arbeit, {done_count} erledigt.")
        
    except Exception as e:
        sprich("Kanban-Daten nicht verfügbar.")

# Initialisierung
print("🧠 ORDO - Semantischer Task-Begleiter (Robust Version)")
print("=" * 60)
print(f"🎯 Trigger-Wörter: {', '.join(triggers)}")

# Initialisiere Mikrofon
if not init_microphone():
    print("❌ Mikrofon-Initialisierung fehlgeschlagen")
    sys.exit(1)

print("🎤 Höre passiv zu... (Sage eines der Trigger-Wörter)")
print("=" * 60)

# Hauptschleife
while True:
    try:
        print("🔊 Höre zu...")
        with mic as source:
            audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)

        print("🔍 Erkenne Sprache...")
        text = recognizer.recognize_google(audio, language="de-DE")
        current_time = time.time()
        
        print(f"📝 Erkannt: '{text}'")
        
        # Prüfe auf Trigger
        detected_trigger = check_trigger(text)
        
        if detected_trigger:
            listening = True
            last_input_time = current_time
            print(f"🗣️  Ordo aktiviert durch '{detected_trigger}'")
            
            # Sofortige Antwort
            analysiere_befehl(text, detected_trigger)
                
        elif listening:
            if current_time - last_input_time > dialog_timeout:
                listening = False
                print("⏱️  Dialog-Fenster geschlossen.")
            else:
                last_input_time = current_time
                print(f"🗣️  Fortsetzung: {text}")
                analysiere_befehl(text, "")
        
        else:
            # Passive Task-Erkennung (immer aktiv)
            task_recognized = passive_task_recognition(text)
            if task_recognized:
                print(f"🔍 Passiv erfasst: {text[:50]}...")

    except sr.WaitTimeoutError:
        continue
    except sr.UnknownValueError:
        continue
    except Exception as e:
        print(f"❌ Fehler: {e}")
        time.sleep(1)
        continue 