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
# Otto als Haupttrigger (einfacher zu erkennen)
triggers = ["otto", "ordo", "ordu", "odo", "orden"]
listening = False
last_input_time = 0
dialog_timeout = 30  # Erhöht auf 30 Sekunden
is_speaking = False
conversation_active = False
conversation_history = []

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
    """Otto spricht mit ruhiger, strukturierter Stimme"""
    global is_speaking
    if is_speaking:
        print(f"⏳ Otto spricht bereits: {text}")
        return
    
    def run():
        global is_speaking
        is_speaking = True
        try:
            print(f"🗣️  Otto sagt: {text}")
            # Verwende die neue Ordo-Voice-ID
            audio = generate(
                text=text, 
                voice=voice_config.VOICE_ID_ORDO, 
                model="eleven_multilingual_v2"
            )
            filename = f"/tmp/otto_{uuid.uuid4()}.mp3"
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

def load_ordo_identity():
    """Lädt die Ordo-Identität"""
    try:
        with open(ORDO_IDENTITY_PATH, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Du bist Otto. Du hörst zu und strukturierst."

def intelligente_antwort(text_clean, conversation_context=""):
    """Gibt intelligente lokale Antworten mit Konversations-Kontext"""
    
    # Task-Management
    if any(word in text_clean for word in ["aufgabe", "task", "kanban"]):
        if "hinzu" in text_clean or "hinzufügen" in text_clean:
            aufgabe = text_clean.split("hinzu")[-1].strip()
            if aufgabe:
                task_id = kanban_add_simple(aufgabe)
                return f"Task {task_id} hinzugefügt. Was kann ich noch für dich tun?"
        elif any(word in text_clean for word in ["zeige", "liste", "status"]):
            return zeige_kanban_status() + " Möchtest du weitere Aufgaben hinzufügen?"
        else:
            return "Ich kann Tasks hinzufügen, anzeigen und verwalten. Sage 'Otto, kanban hinzu [Aufgabe]'. Was soll ich für dich organisieren?"
    
    # Analyse und Strukturierung
    elif any(word in text_clean for word in ["analysiere", "strukturiere", "organisiere"]):
        if conversation_context:
            return f"Basierend auf unserem Gespräch über {conversation_context}, analysiere ich deine Anfrage. Was genau soll ich organisieren?"
        else:
            return "Ich analysiere deine Anfrage und strukturiere sie. Erzähl mir mehr darüber, was du organisieren möchtest."
    
    # Erklärung und Hilfe
    elif any(word in text_clean for word in ["erkläre", "verstehe", "hilfe"]):
        return "Ich bin Otto, dein stiller Begleiter. Ich erkenne Tasks, strukturiere sie und helfe dir bei der Organisation. Was beschäftigt dich gerade?"
    
    # Meinung und Denken
    elif any(word in text_clean for word in ["denke", "meinung", "glaube"]):
        return "Ich denke strukturiert und helfe dir dabei, deine Gedanken zu ordnen. Was beschäftigt dich? Lass uns das gemeinsam durchgehen."
    
    # Plan und Strategie
    elif any(word in text_clean for word in ["plan", "strategie", "priorität"]):
        return "Ich helfe dir bei der Planung und Priorisierung. Lass uns das strukturiert angehen. Was ist dein wichtigstes Ziel?"
    
    # Ja/Nein Antworten
    elif any(word in text_clean for word in ["ja", "nein", "okay", "gut", "stimmt"]):
        if conversation_context:
            return f"Verstanden. {conversation_context} ist wichtig. Was ist der nächste Schritt?"
        else:
            return "Gut. Was können wir als nächstes angehen?"
    
    # Unbekannte Befehle
    else:
        if conversation_context:
            return f"Interessant. {conversation_context} ist ein wichtiger Punkt. Wie können wir das am besten angehen?"
        else:
            return "Ich verstehe deine Anfrage. Ich kann Tasks verwalten, analysieren und strukturieren. Erzähl mir mehr darüber."

def zeige_kanban_status():
    """Zeigt Kanban-Status"""
    try:
        with open(KANBAN_PATH, "r") as f:
            board = json.load(f)
        
        todo_count = len(board.get("To Do", []))
        progress_count = len(board.get("In Progress", []))
        done_count = len(board.get("Erledigt", []))
        
        return f"Kanban-Status: {todo_count} offen, {progress_count} in Arbeit, {done_count} erledigt."
        
    except Exception as e:
        return "Kanban-Daten nicht verfügbar."

def start_conversation():
    """Startet eine neue Konversation"""
    global conversation_active, conversation_history
    conversation_active = True
    conversation_history = []
    sprich("Hallo! Ich bin Otto, dein stiller Begleiter. Wie kann ich dir heute helfen?")

def continue_conversation(text_clean):
    """Führt die Konversation fort"""
    global conversation_history, last_input_time
    
    # Aktualisiere Zeit
    last_input_time = time.time()
    
    # Füge zur Konversations-Historie hinzu
    conversation_history.append(text_clean)
    
    # Bestimme Kontext aus der letzten Konversation
    context = ""
    if len(conversation_history) > 1:
        context = conversation_history[-2]  # Vorherige Nachricht als Kontext
    
    # Einfache Befehle
    if "test" in text_clean:
        sprich("Otto Test erfolgreich. Ich höre zu und kann sprechen. Was beschäftigt dich?")
        return

    elif "hallo" in text_clean or "hörst du mich" in text_clean:
        sprich("Ja, ich höre dich. Ich bin Otto, dein stiller Begleiter. Was kann ich für dich tun?")
        return

    elif "weiter" in text_clean or "mehr" in text_clean:
        sprich("Ich höre weiter zu. Erzähl mir mehr darüber.")
        return

    # Intelligente Antworten mit Kontext
    antwort = intelligente_antwort(text_clean, context)
    sprich(antwort)

def end_conversation():
    """Beendet die Konversation"""
    global conversation_active, conversation_history
    conversation_active = False
    conversation_history = []
    print("⏱️  Konversation beendet.")

def analysiere_befehl(text, detected_trigger):
    """Analysiert Befehle für Otto mit verbessertem Dialog"""
    # Entferne den Trigger aus dem Text
    text_clean = text.lower().replace(detected_trigger, "").strip()
    print(f"🧠 Otto verarbeitet: '{text_clean}'")

    if not text_clean:
        start_conversation()
        return

    # Starte oder setze Konversation fort
    if not conversation_active:
        start_conversation()
        # Warte kurz, dann verarbeite den ersten Befehl
        time.sleep(2)
        continue_conversation(text_clean)
    else:
        continue_conversation(text_clean)

# Initialisierung
print("🧠 OTTO - Semantischer Task-Begleiter (Konversations-Version)")
print("=" * 60)
print(f"🎯 Trigger-Wörter: {', '.join(triggers)} (Otto als Haupttrigger)")
print("🧠 Verbessertes Dialog-System mit Konversations-Kette")
print("⏱️  Dialog-Timeout: {dialog_timeout} Sekunden")

# Initialisiere Mikrofon
if not init_microphone():
    print("❌ Mikrofon-Initialisierung fehlgeschlagen")
    sys.exit(1)

print("🎤 Höre passiv zu... (Sage 'Otto' um mich zu aktivieren)")
print("=" * 60)

# Hauptschleife
while True:
    try:
        print("🔊 Höre zu...")
        with mic as source:
            audio = recognizer.listen(source, timeout=1, phrase_time_limit=10)

        print("🔍 Erkenne Sprache...")
        text = recognizer.recognize_google(audio, language="de-DE")
        current_time = time.time()
        
        print(f"📝 Erkannt: '{text}'")
        
        # Prüfe auf Trigger
        detected_trigger = check_trigger(text)
        
        if detected_trigger:
            listening = True
            last_input_time = current_time
            print(f"🗣️  Otto aktiviert durch '{detected_trigger}'")
            
            # Starte Konversation
            analysiere_befehl(text, detected_trigger)
                
        elif conversation_active:
            # Konversation läuft - prüfe Timeout
            if current_time - last_input_time > dialog_timeout:
                end_conversation()
                print("⏱️  Dialog-Fenster geschlossen.")
            else:
                # Setze Konversation fort
                print(f"🗣️  Konversation: {text}")
                continue_conversation(text)
        
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