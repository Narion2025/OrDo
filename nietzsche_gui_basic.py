
import sys
import os
import json
import uuid
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt, QTimer
import threading
import time

BASE_PATH = os.path.expanduser("~/Documents/Nietzsche")
KANBAN_PATH = os.path.join(BASE_PATH, "Nietzsche_Kanban.json")

def lade_aktivitaet():
    try:
        with open(KANBAN_PATH) as f:
            board = json.load(f)
        return board.get("Aktivitaet", "Keine Information.")
    except:
        return "Keine Verbindung zum Kanban-Board."

class NietzscheGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nietzsche Dialog & Aktivität")
        self.setFixedSize(500, 700)

        self.layout = QVBoxLayout()

        # Nietzsche Bild
        self.bild_label = QLabel(self)
        pixmap = QPixmap(os.path.join(BASE_PATH, "nietzsche.png"))
        self.bild_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        self.bild_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.bild_label)

        # Aktivitätslampe
        self.lampe = QFrame()
        self.lampe.setFixedSize(20, 20)
        self.lampe.setStyleSheet("background-color: gray; border-radius: 10px;")
        self.layout.addWidget(self.lampe, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Aktivitätstext
        self.aktivitaet_label = QLabel("🧠 Aktivität: Wird geladen...")
        self.aktivitaet_label.setWordWrap(True)
        self.layout.addWidget(self.aktivitaet_label)

        # Dialogbereich
        self.dialog = QTextEdit()
        self.dialog.setReadOnly(True)
        self.layout.addWidget(self.dialog)

        # Button zum Simulieren einer Idee
        self.idea_button = QPushButton("💡 Nietzsche hat eine Idee")
        self.idea_button.clicked.connect(self.simuliere_idee)
        self.layout.addWidget(self.idea_button)

        self.setLayout(self.layout)

        # Timer zum Aktualisieren
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(3000)

    def simuliere_idee(self):
        self.dialog.append("🧠 Nietzsche: Ich habe eine Eingebung über Ordnung und Wahnsinn...")
        self.lampe.setStyleSheet("background-color: green; border-radius: 10px;")

        def reset():
            time.sleep(4)
            self.lampe.setStyleSheet("background-color: gray; border-radius: 10px;")
        threading.Thread(target=reset, daemon=True).start()

    def update_status(self):
        akt = lade_aktivitaet()
        self.aktivitaet_label.setText(f"🧠 Aktivität: {akt}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenster = NietzscheGUI()
    fenster.show()
    sys.exit(app.exec())
