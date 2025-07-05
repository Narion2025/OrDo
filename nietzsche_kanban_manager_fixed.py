
import json
import os

kanban_path = os.path.expanduser("~/Documents/Die_Geburt_der_tragödie/Nietzsche_Kanban.json")

def lade_board():
    with open(kanban_path, "r") as f:
        return json.load(f)

def speichere_board(board):
    with open(kanban_path, "w") as f:
        json.dump(board, f, indent=4)

def zeige_board(board):
    print("\n--- Nietzsche Kanban Board ---")
    for spalte, einträge in board.items():
        print(f"\n[{spalte}]")
        for i, eintrag in enumerate(einträge, 1):
            print(f"{i}. {eintrag}")

def füge_hinzu(board):
    titel = input("Was soll hinzugefügt werden? ")
    spalte = input("In welche Spalte? (Idee / Geplant / In Arbeit / Warten / Erledigt): ")
    if spalte in board:
        board[spalte].append(titel)
        speichere_board(board)
        print("✅ Hinzugefügt.")
    else:
        print("❌ Ungültige Spalte.")

def verschiebe(board):
    zeige_board(board)
    quelle = input("Aus welcher Spalte verschieben? ")
    ziel = input("In welche Spalte? ")
    if quelle in board and ziel in board:
        try:
            index = int(input("Welche Nummer verschieben? ")) - 1
            eintrag = board[quelle].pop(index)
            board[ziel].append(eintrag)
            speichere_board(board)
            print("🔁 Verschoben.")
        except (IndexError, ValueError):
            print("❌ Ungültige Nummer.")
    else:
        print("❌ Ungültige Spalten.")

def dashboard():
    board = lade_board()
    while True:
        print("\n1. Zeige Board")
        print("2. Hinzufügen")
        print("3. Verschieben")
        print("0. Beenden")
        wahl = input("Auswahl: ")
        if wahl == "1":
            zeige_board(board)
        elif wahl == "2":
            füge_hinzu(board)
        elif wahl == "3":
            verschiebe(board)
        elif wahl == "0":
            break

dashboard()
