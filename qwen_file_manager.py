import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BASE_DIRS = {
    "Downloads": Path.home() / "Downloads",
    "Dokumente": Path.home() / "Dokumente",
    "Projekte": Path.home() / "Projekte",
    "Schreibtisch": Path.home() / "Schreibtisch",
}
OTTO_TRASH = Path.home() / "Otto_trash"

class ActivityHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_activity = time.time()

    def on_any_event(self, event):
        self.last_activity = time.time()

handler = ActivityHandler()
observer = Observer()

for name, path in BASE_DIRS.items():
    os.makedirs(path, exist_ok=True)
    observer.schedule(handler, str(path), recursive=True)

os.makedirs(OTTO_TRASH, exist_ok=True)
observer.start()

try:
    while True:
        time.sleep(5)
        if time.time() - handler.last_activity > 600:
            print("Ben, hast du mal kurz einen Moment?")
            handler.last_activity = time.time()
except KeyboardInterrupt:
    pass
finally:
    observer.stop()
    observer.join()
