
import sys
import os
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QLineEdit, QFileDialog
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer
import uuid
import datetime

BASE_PATH = os.path.expanduser("~/Documents/Nietzsche")
KANBAN_PATH = os.path.join(BASE_PATH, "Nietzsche_Kanban.json")
UPLOAD_PATH = os.path.join(BASE_PATH, "uploads")
os.makedirs(UPLOAD_PATH, exist_ok=True)

class NietzscheAgent(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nietzsche Agent – Dialog & Kontrolle")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        header = QLabel("🧠 Nietzsche Agent Control")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        self.activity_label = QLabel("Aktuelle Aktivität: (wird geladen)")
        layout.addWidget(self.activity_label)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)

        chat_input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.send_button = QPushButton("Senden")
        self.send_button.clicked.connect(self.handle_send)
        chat_input_layout.addWidget(self.chat_input)
        chat_input_layout.addWidget(self.send_button)
        layout.addLayout(chat_input_layout)

        file_layout = QHBoxLayout()
        self.upload_button = QPushButton("📂 Datei hochladen")
        self.upload_button.clicked.connect(self.upload_file)
        file_layout.addWidget(self.upload_button)

        self.code_view = QTextEdit()
        self.code_view.setReadOnly(True)
        self.code_view.setPlaceholderText("👁 Hier erscheint Code, den Nietzsche generiert.")
        file_layout.addWidget(self.code_view)
        layout.addLayout(file_layout)

        self.setLayout(layout)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_activity)
        self.update_timer.start(3000)

    def handle_send(self):
        text = self.chat_input.text().strip()
        if text:
            self.chat_history.append(f"👤 Du: {text}")
            self.chat_history.append(f"🧠 Nietzsche: Das Chaos nimmt Form an... ({text})")
            self.chat_input.clear()

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Datei auswählen")
        if file_path:
            filename = os.path.basename(file_path)
            dest = os.path.join(UPLOAD_PATH, f"{uuid.uuid4()}_{filename}")
            with open(file_path, "rb") as src, open(dest, "wb") as dst:
                dst.write(src.read())
            self.chat_history.append(f"📎 Datei hochgeladen: {filename}")
            self.chat_history.append("🧠 Nietzsche: Ich werde prüfen, ob sich darin Sinn verbirgt...")

    def update_activity(self):
        try:
            with open(KANBAN_PATH) as f:
                board = json.load(f)
            self.activity_label.setText("Aktuelle Aktivität: " + board.get("Aktivitaet", "keine"))
        except:
            self.activity_label.setText("Aktuelle Aktivität: (nicht verfügbar)")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = NietzscheAgent()
    win.show()
    sys.exit(app.exec())
