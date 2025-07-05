
import os
import json
import time
import requests

kanban_pfad = os.path.expanduser("~/Documents/Die Geburt der Tragödie/Nietzsche_Kanban.json")
llm_url = "http://localhost:1234/v1/chat/completions"
headers = {"Content-Type": "application/json"}

def frage_llm(prompt):
    payload = {
        "model": "meta-llama-3.1-8b-instruct",
        "messages": [
            {"role": "system", "content": "Du bist Friedrich Nietzsche. Du antwortest mit präzisem, ausführbarem Python-Code, wenn du darum gebeten wirst. Ansonsten sprichst du in aphoristischer, düster-ironischer Sprache."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }
    try:
        response = requests.post(llm_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print("LLM antwortete mit Status:", response.status_code)
    except Exception as e:
        print("Fehler bei LLM:", e)
    return None

def ausführen():
    while True:
        try:
            with open(kanban_pfad, "r") as f:
                board = json.load(f)

            aufgaben = board.get("Nietzsche", [])
            erledigte = board.get("Erledigt", [])

            neue_aufgaben = []
            for aufgabe in aufgaben:
                print("Bearbeite:", aufgabe)
                antwort = frage_llm(aufgabe)
                if antwort:
                    print("Antwort:", antwort)
                    erledigte.append(f"{aufgabe} (ausgeführt)")
                else:
                    neue_aufgaben.append(aufgabe)

            board["Nietzsche"] = neue_aufgaben
            board["Erledigt"] = erledigte

            with open(kanban_pfad, "w") as f:
                json.dump(board, f, indent=4)

        except Exception as e:
            print("Fehler beim Lesen oder Schreiben des Boards:", e)

        time.sleep(10)

ausführen()
