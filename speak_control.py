
import os
import time
from pathlib import Path

LOCK_PATH = Path.home() / "Documents/Nietzsche/speaking.lock"

def begin_speaking(timeout=10):
    start = time.time()
    while LOCK_PATH.exists():
        if time.time() - start > timeout:
            return False
        time.sleep(0.1)
    LOCK_PATH.touch()
    return True

def end_speaking():
    if LOCK_PATH.exists():
        LOCK_PATH.unlink()
