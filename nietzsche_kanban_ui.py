
import streamlit as st
import os
import json
from datetime import datetime

# Pfad zur Kanban-Datei
BASE_PATH = os.path.expanduser("~/Documents/Nietzsche")
KANBAN_PATH = os.path.join(BASE_PATH, "Nietzsche_Kanban.json")

# Laden oder Initialisieren
def lade_board():
    if not os.path.exists(KANBAN_PATH):
        board = {"To Do": [], "In Progress": [], "Erledigt": [], "Aktivitaet": ""}
        with open(KANBAN_PATH, "w") as f:
            json.dump(board, f, indent=2)
    with open(KANBAN_PATH, "r") as f:
        return json.load(f)

def speichere_board(board):
    with open(KANBAN_PATH, "w") as f:
        json.dump(board, f, indent=2)

# UI Start
st.set_page_config(page_title="Nietzsche Kanban", layout="wide")
st.title("📋 Nietzsche Kanban Board")

board = lade_board()

cols = st.columns(3)
spalten = ["To Do", "In Progress", "Erledigt"]

for i, spalte in enumerate(spalten):
    with cols[i]:
        st.subheader(spalte)
        for idx, task in enumerate(board[spalte]):
            st.markdown(f"- {task}")

# Aktivität
st.markdown("---")
st.subheader("🧠 Aktuelle Aktivität:")
st.write(board.get("Aktivitaet", "Noch nichts passiert."))

# Neue Aufgabe hinzufügen
st.markdown("---")
with st.form("add_task"):
    neuer_task = st.text_input("Neue Aufgabe:")
    zielspalte = st.selectbox("Spalte", spalten)
    submitted = st.form_submit_button("Hinzufügen")
    if submitted and neuer_task.strip():
        board[zielspalte].append(neuer_task.strip())
        board["Aktivitaet"] = f"{datetime.now().strftime('%H:%M')} – '{neuer_task.strip()}' hinzugefügt in {zielspalte}"
        speichere_board(board)
        st.experimental_rerun()
