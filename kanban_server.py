
from flask import Flask, jsonify, request, send_from_directory
import json
import os

app = Flask(__name__)
KANBAN_PATH = os.path.expanduser("~/Documents/Nietzsche/Nietzsche_Kanban.json")

@app.route("/kanban")
def get_kanban():
    if not os.path.exists(KANBAN_PATH):
        return jsonify({"To Do": [], "Erledigt": []})
    with open(KANBAN_PATH) as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/update", methods=["POST"])
def update_kanban():
    data = request.json
    text = data["text"]
    column = data["column"]
    if not os.path.exists(KANBAN_PATH):
        board = {"To Do": [], "Erledigt": []}
    else:
        with open(KANBAN_PATH) as f:
            board = json.load(f)
    # Entferne aus allen Spalten
    for k in board:
        if text in board[k]:
            board[k].remove(text)
    # Füge in neue Spalte ein
    if column == "todo":
        board["To Do"].append(text)
    elif column == "erledigt":
        board["Erledigt"].append(text)
    with open(KANBAN_PATH, "w") as f:
        json.dump(board, f, indent=2)
    return jsonify({"status": "ok"})

@app.route("/")
def serve_html():
    return send_from_directory(".", "kanban.html")

if __name__ == "__main__":
    app.run(debug=True)
