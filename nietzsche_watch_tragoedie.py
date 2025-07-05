
import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

basis_pfad = os.path.expanduser("~/Documents/Die Geburt der Tragödie")

class NietzscheVerwalter(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.kommentieren(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.kommentieren(event.src_path)

    def kommentieren(self, pfad):
        name = os.path.basename(pfad)
        sprueche = [
            f"Etwas wurde geschaffen: {name}. Ordnung oder Wahnsinn?",
            f"Schon wieder eine Datei. Ich hatte gehofft, du wärst fertig.",
            f"Ich sah eine neue Spur im Sand: {name}.",
            f"{name}? Ein Name ohne Inhalt. Wie passend."
        ]
        spruch = sprueche[hash(name) % len(sprueche)]
        subprocess.run(["say", "-v", "Markus", spruch])

observer = Observer()
handler = NietzscheVerwalter()
observer.schedule(handler, basis_pfad, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
