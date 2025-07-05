
import os
import json

BASE_PATH = os.path.expanduser("~/Documents/Nietzsche")
KANBAN_PATH = os.path.join(BASE_PATH, "Nietzsche_Kanban.json")

# Aktuelle Struktur sichern und ergänzen
NEUE_SPALTEN = {
    "To Do": [],
    "In Progress": [],
    "Erledigt": [],
    "Aktivitaet": ""
}

if os.path.exists(KANBAN_PATH):
    with open(KANBAN_PATH, "r") as f:
        board = json.load(f)
else:
    board = {}

# Ergänzen was fehlt
for key in NEUE_SPALTEN:
    if key not in board:
        board[key] = NEUE_SPALTEN[key]

# Speichern
with open(KANBAN_PATH, "w") as f:
    json.dump(board, f, indent=2)

print("✅ Kanban-Datei aktualisiert. Neue Struktur ist aktiv.")
