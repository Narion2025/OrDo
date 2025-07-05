import voice_config\n
import speech_recognition as sr
import time
import os
import threading
import json
from elevenlabs import generate, save, set_api_key
import uuid

# ElevenLabs Setup
set_api_key("sk_7f784c3c4dc74dde1d037474d515709047ad9b577fb48f28")


# Aktionen
import nietzsche_sort_downloads
import nietzsche_kanban_executor_corrected
import nietzsche_watch_tragoedie
import nietzsche_code_writer

KANBAN_PATH = os.path.expanduser("~/Documents/Nietzsche/Nietzsche_Kanban.json")
PROJEKTE_ROOT = os.path.expanduser("~/Projekte")

recognizer = sr.Recognizer()
mic = sr.Microphone()
trigger = "nietzsche"
listening = False
last_input_time = 0
dialog_timeout = 10
is_speaking = False

def sprich(text):
    global is_speaking
    if is_speaking:
        return
    def run():
        global is_speaking
        is_speaking = True
        audio = generate(text=text, voice=voice_config.VOICE_ID_NIETZSCHE, model="eleven_multilingual_v2")
        filename = f"/tmp/nietzsche_{uuid.uuid4()}.mp3"
        save(audio, filename)
        os.system(f'afplay "{filename}"')
        is_speaking = False
    threading.Thread(target=run).start()

def kanban_add(task):
    try:
        if not os.path.exists(KANBAN_PATH):
            with open(KANBAN_PATH, "w") as f:
                json.dump({"To Do": [], "Erledigt": []}, f)

        with open(KANBAN_PATH, "r") as f:
            board = json.load(f)

        board["To Do"].append(task)

        with open(KANBAN_PATH, "w") as f:
            json.dump(board, f, indent=2)

    except Exception as e:
        print("Fehler beim Schreiben ins Kanban:", e)

def projekt_anlegen(name):
    try:
        ordner_name = name.strip().replace(" ", "_")
        pfad = os.path.join(PROJEKTE_ROOT, ordner_name)
        os.makedirs(pfad, exist_ok=True)
    except Exception as e:
        print("Fehler beim Anlegen des Projekts:", e)

def analysiere_befehl(text):
    text = text.lower()

    if "download" in text and ("ordne" in text or "sortier" in text):
        nietzsche_sort_downloads.sortiere_downloads()

    if "kanban" in text or "aufgabe" in text or "task" in text:
        aufgabe = text.split("hinzu")[-1].strip()
        if aufgabe:
            kanban_add(aufgabe)

    if "projekt" in text or "ordner" in text:
        name = text.split("projekt")[-1].strip()
        if name:
            projekt_anlegen(name)

    if "tragödie" in text:
        nietzsche_watch_tragoedie.main()

    if "code" in text or "skript" in text:
        nietzsche_code_writer.generate_code()

print("🧪 ELEVENLABS-AKTIV MIT afplay – echte Stimme via gespeicherter MP3")

while True:
    if is_speaking:
        continue

    with mic as source:
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="de-DE").lower()
        print("🗣️ Du hast gesagt:", text)
        current_time = time.time()

        if trigger in text:
            listening = True
            last_input_time = current_time
            befehl = text.replace(trigger, "").strip()
            if befehl:
                threading.Thread(target=analysiere_befehl, args=(befehl,)).start()
            else:
                sprich("Was genau soll ich tun?")
        elif listening:
            if current_time - last_input_time > dialog_timeout:
                listening = False
                print("⏱ Trigger-Fenster abgelaufen.")
            else:
                last_input_time = current_time
                threading.Thread(target=analysiere_befehl, args=(text,)).start()

    except sr.UnknownValueError:
        continue
    except Exception as e:
        print("❌ Fehler:", e)
