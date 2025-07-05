
import os
import sys

python_path = sys.executable

if "anaconda" in python_path.lower():
    print("\n❌ Du bist im falschen Terminal – ANACONDA erkannt.")
    print(f"Pfad: {python_path}")
    print("Bitte öffne ein neues Terminal über Spotlight oder Programme → Dienstprogramme → Terminal")
    print("Dann prüfe mit: which python3 → sollte NICHT 'anaconda' enthalten.")
else:
    print("\n✅ Du bist im richtigen Terminal.")
    print(f"Python-Interpreter: {python_path}")
