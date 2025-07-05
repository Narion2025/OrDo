
import speech_recognition as sr
import time
import os
import threading

# Importiere Funktionsmodule
import nietzsche_sort_downloads
import nietzsche_kanban_executor_corrected
import nietzsche_watch_tragoedie
import nietzsche_code_writer

recognizer = sr.Recognizer()
mic = sr.Microphone()
trigger = "nietzsche"
listening = False
last_input_time = 0
dialog_timeout = 10

def sprich(text):
    os.system(f'say -v "Markus" "{text}"')

def analysiere_befehl(text):
    text = text.lower()
    if "download" in text or "ordne" in text:
        sprich("Ich sortiere deine Downloads.")
        nietzsche_sort_downloads.sortiere_downloads()
    elif "kanban" in text or "task" in text or "aufgabe" in text:
        sprich("Ich pflege das Kanban-Board.")
        nietzsche_kanban_executor_corrected.run_executor()
    elif "projekt" in text or "tragödie" in text:
        sprich("Ich überwache deine Projekte.")
        nietzsche_watch_tragoedie.main()
    elif "code" in text or "skript" in text:
        sprich("Ich beginne, ein Skript zu schreiben.")
        nietzsche_code_writer.generate_code()
    else:
        sprich("Das habe ich nicht verstanden. Bitte versuch es klarer.")

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
