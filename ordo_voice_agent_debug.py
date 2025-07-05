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
trigger = "ordo"
listening = False
last_input_time = 0
dialog_timeout = 10
is_speaking = False

def init_microphone():
    """Initialisiert das Mikrofon mit besserer Fehlerbehandlung"""
    global mic
    
    print("🎤 Initialisiere Mikrofon...")
    
    try:
        # Liste verfügbare Mikrofone auf
        mic_list = sr.Microphone.list_microphone_names()
        print(f"📋 Verfügbare Mikrofone: {len(mic_list)}")
        for i, name in enumerate(mic_list):
            print(f"   {i}: {name}")
        
        # Versuche Standard-Mikrofon
        mic = sr.Microphone()
        print(f"✅ Standard-Mikrofon initialisiert (Index: {mic.device_index})")
        
        # Test-Aufnahme
        print("🔍 Teste Mikrofon...")
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ Mikrofon-Test erfolgreich")
        
        return True
        
    except Exception as e:
        print(f"❌ Mikrofon-Fehler: {e}")
        print("💡 Mögliche Lösungen:")
        print("   1. Mikrofon-Berechtigung in Systemeinstellungen prüfen")
        print("   2. Terminal Mikrofon-Zugriff erlauben")
        print("   3. Anderes Mikrofon verwenden")
        return False

def load_ordo_identity():
    """Lädt die Ordo-Identität"""
    try:
        with open(ORDO_IDENTITY_PATH, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Du bist Ordo. Du hörst zu und strukturierst."

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

def analysiere_befehl(text):
    """Analysiert Befehle für Ordo"""
    text_lower = text.lower()
    print(f"🧠 Ordo verarbeitet: {text}")

    if "kanban" in text_lower or "aufgabe" in text_lower or "task" in text_lower:
        if "hinzu" in text_lower:
            aufgabe = text.split("hinzu")[-1].strip()
            if aufgabe:
                task_id = kanban_add_simple(aufgabe)
                sprich(f"Task {task_id} hinzugefügt.")
        elif "zeige" in text_lower or "liste" in text_lower:
            zeige_kanban()

    elif "test" in text_lower:
        sprich("Ordo Test erfolgreich. Ich höre zu.")

    elif "hilfe" in text_lower or "help" in text_lower:
        sprich("Ich bin Ordo. Ich erkenne Tasks und strukturiere sie. Sag einfach was du machen musst.")

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
print("🧠 ORDO - Semantischer Task-Begleiter (Debug-Version)")
print("=" * 60)

# Lade Ordo-Identität
ordo_identity = load_ordo_identity()
print("🎭 Ordo-Identität geladen")

# Initialisiere Mikrofon
if not init_microphone():
    print("❌ Mikrofon-Initialisierung fehlgeschlagen")
    print("🔄 Starte im Text-Modus...")
    
    # Text-Modus für Testing
    print("💬 Text-Modus aktiv. Geben Sie Befehle ein:")
    while True:
        try:
            text_input = input("Sie: ").strip()
            if not text_input:
                continue
            if text_input.lower() == "exit":
                break
                
            # Passive Task-Erkennung
            task_recognized = passive_task_recognition(text_input)
            
            # Aktive Kommunikation bei Trigger
            if trigger in text_input.lower():
                befehl = text_input.lower().replace(trigger, "").strip()
                print(f"🗣️  Ordo aktiviert: {befehl}")
                if befehl:
                    analysiere_befehl(befehl)
                else:
                    sprich("Wie kann ich dir helfen?")
            elif task_recognized:
                print(f"🔍 Passiv erfasst: {text_input[:50]}...")
                
        except KeyboardInterrupt:
            print("\n👋 Ordo beendet.")
            break
    
    sys.exit(0)

print("🎤 Höre passiv zu... (Trigger: 'Ordo')")
print("=" * 60)

# Hauptschleife
while True:
    if is_speaking:
        continue

    try:
        print("🔊 Höre zu...")
        with mic as source:
            audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)

        print("🔍 Erkenne Sprache...")
        text = recognizer.recognize_google(audio, language="de-DE")
        current_time = time.time()
        
        print(f"📝 Erkannt: {text}")
        
        # Passive Task-Erkennung (immer aktiv)
        task_recognized = passive_task_recognition(text)
        
        # Aktive Kommunikation nur bei Trigger
        if trigger in text.lower():
            listening = True
            last_input_time = current_time
            befehl = text.lower().replace(trigger, "").strip()
            
            print(f"🗣️  Ordo aktiviert: {befehl}")
            
            if befehl:
                threading.Thread(target=analysiere_befehl, args=(befehl,)).start()
            else:
                sprich("Wie kann ich dir helfen?")
                
        elif listening:
            if current_time - last_input_time > dialog_timeout:
                listening = False
                print("⏱️  Dialog-Fenster geschlossen.")
            else:
                last_input_time = current_time
                print(f"🗣️  Fortsetzung: {text}")
                threading.Thread(target=analysiere_befehl, args=(text,)).start()
        
        # Stille Bestätigung bei passiver Task-Erkennung
        elif task_recognized:
            print(f"🔍 Passiv erfasst: {text[:50]}...")

    except sr.WaitTimeoutError:
        continue
    except sr.UnknownValueError:
        continue
    except Exception as e:
        print(f"❌ Fehler: {e}")
        time.sleep(1) 