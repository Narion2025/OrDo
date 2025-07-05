
import os
import json
from datetime import datetime

BASE_PATH = os.path.expanduser("~/Documents/Nietzsche")
KANBAN_PATH = os.path.join(BASE_PATH, "Nietzsche_Kanban.json")

# Initialstruktur erweitern
def init_kanban():
    if not os.path.exists(KANBAN_PATH):
        with open(KANBAN_PATH, "w") as f:
            json.dump({"To Do": [], "In Progress": [], "Erledigt": [], "Aktivitaet": ""}, f, indent=2)

def task_hinzufuegen(titel, status="To Do"):
    with open(KANBAN_PATH, "r") as f:
        board = json.load(f)
    board[status].append(titel)
    with open(KANBAN_PATH, "w") as f:
        json.dump(board, f, indent=2)

def task_starten(titel):
    with open(KANBAN_PATH, "r") as f:
        board = json.load(f)
    if titel in board["To Do"]:
        board["To Do"].remove(titel)
        board["In Progress"].append(titel)
        board["Aktivitaet"] = f"{datetime.now().strftime('%H:%M')} – '{titel}' wird bearbeitet"
    with open(KANBAN_PATH, "w") as f:
        json.dump(board, f, indent=2)

def task_abschliessen(titel):
    with open(KANBAN_PATH, "r") as f:
        board = json.load(f)
    if titel in board["In Progress"]:
        board["In Progress"].remove(titel)
        board["Erledigt"].append(titel)
        board["Aktivitaet"] = f"{datetime.now().strftime('%H:%M')} – '{titel}' abgeschlossen"
    with open(KANBAN_PATH, "w") as f:
        json.dump(board, f, indent=2)

def status_anzeigen():
    with open(KANBAN_PATH, "r") as f:
        board = json.load(f)
    print("\n📋 Nietzsche Kanban Board")
    for spalte in ["To Do", "In Progress", "Erledigt"]:
        print(f"\n{spalte}:")
        for task in board[spalte]:
            print(f"  - {task}")
    print(f"\n🧠 Aktivität: {board.get('Aktivitaet', '')}")

if __name__ == "__main__":
    init_kanban()
    status_anzeigen()
