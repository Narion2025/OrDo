
import speech_recognition as sr
import time
import os
import threading
import json

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

def sprich(text):
    os.system(f'say -v "Markus" "{text}"')

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

        sprich("Ich habe es dem Kanban hinzugefügt.")
    except Exception as e:
        sprich("Fehler beim Schreiben ins Kanban.")
        print(e)

def projekt_anlegen(name):
    try:
        ordner_name = name.strip().replace(" ", "_")
        pfad = os.path.join(PROJEKTE_ROOT, ordner_name)
        os.makedirs(pfad, exist_ok=True)
        sprich(f"Projekt {name} wurde angelegt.")
    except Exception as e:
        sprich("Fehler beim Anlegen des Projekts.")
        print(e)

def analysiere_befehl(text):
    text = text.lower()

    if "download" in text and ("ordne" in text or "sortier" in text):
        sprich("Ich sortiere deine Downloads.")
        nietzsche_sort_downloads.sortiere_downloads()

    if "kanban" in text or "aufgabe" in text or "task" in text:
        aufgabe = text.split("hinzu")[-1].strip()
        if aufgabe:
            kanban_add(aufgabe)
        else:
            sprich("Was soll ich dem Kanban hinzufügen?")

    if "projekt" in text or "ordner" in text:
        name = text.split("projekt")[-1].strip()
        if name:
            projekt_anlegen(name)
        else:
            sprich("Wie soll das Projekt heißen?")

    if "tragödie" in text:
        sprich("Ich überwache deine Projektstruktur.")
        nietzsche_watch_tragoedie.main()

    if "code" in text or "skript" in text:
        sprich("Ich beginne, ein Skript zu schreiben.")
        nietzsche_code_writer.generate_code()

print("🎤 Nietzsche wartet auf Sprachbefehl... Sag 'Nietzsche', um ihn zu aktivieren.")

while True:
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
