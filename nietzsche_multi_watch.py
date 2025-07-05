
import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Ordner, die Nietzsche überwachen soll
ueberwachte_pfade = [
    os.path.expanduser("~/Documents/Die Geburt der Tragödie"),
    os.path.expanduser("~/Documents/Dionysos"),
    os.path.expanduser("~/Documents/Zarathustra"),
    os.path.expanduser("~/Documents/Aufräumen")
]

class MultiNietzsche(FileSystemEventHandler):
    def kommentieren(self, pfad):
        name = os.path.basename(pfad)
        sprueche = [
            f"Ich sehe: {name}. Ordnung wird gefordert.",
            f"Noch ein Artefakt im Wahnsinn: {name}.",
            f"{name}? Ein Schritt auf dem Pfad zur Klarheit.",
            f"Ein neuer Schatten in deinem Reich: {name}."
        ]
        spruch = sprueche[hash(name) % len(sprueche)]
        subprocess.run(["say", "-v", "Markus", spruch])

    def on_created(self, event):
        if not event.is_directory:
            self.kommentieren(event.src_path)

observer = Observer()
handler = MultiNietzsche()
for pfad in ueberwachte_pfade:
    os.makedirs(pfad, exist_ok=True)
    observer.schedule(handler, pfad, recursive=True)

observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
