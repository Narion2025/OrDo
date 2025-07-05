
import os
import shutil
import datetime

# Downloads-Pfad
downloads_path = os.path.expanduser("~/Downloads")

# Zielpfade
kategorien = {
    "Bilder": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Dokumente": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Archive": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Audio": [".mp3", ".wav", ".m4a", ".flac", ".aac"],
    "Video": [".mp4", ".mov", ".avi", ".mkv", ".wmv"],
    "Programme": [".dmg", ".pkg", ".exe", ".app", ".sh", ".bat"]
}

def sag(text):
    print(f"(Nietzsche flüstert still: {text})")

def sortiere_downloads():
    dateien = [f for f in os.listdir(downloads_path) if os.path.isfile(os.path.join(downloads_path, f))]

    for datei in dateien:
        dateipfad = os.path.join(downloads_path, datei)
        _, ext = os.path.splitext(datei.lower())

        for kategorie, endungen in kategorien.items():
            if ext in endungen:
                zielordner = os.path.join(downloads_path, kategorie)
                os.makedirs(zielordner, exist_ok=True)
                zielpfad = os.path.join(zielordner, datei)
                shutil.move(dateipfad, zielpfad)
                sag(f"{kategorie} erkannt. Datei verschoben: {datei}")
                break
