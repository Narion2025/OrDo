
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class NietzscheHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            self.kommentieren(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.kommentieren(event.src_path)

    def kommentieren(self, pfad):
        sprueche = [
            "Etwas Neues ist geboren… im Dreck der Downloads.",
            "Noch eine Datei, noch ein Stein auf dem Grab der Ordnung.",
            "Ich hasse alles, was temporär ist. Und doch lebst du davon.",
            "Das ist kein Fortschritt – das ist ein Download."
        ]
        spruch = sprueche[hash(pfad) % len(sprueche)]
        subprocess.run(["say", "-v", "Markus", spruch])

downloads_path = os.path.expanduser("~/Downloads")

observer = Observer()
event_handler = NietzscheHandler()
observer.schedule(event_handler, downloads_path, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
