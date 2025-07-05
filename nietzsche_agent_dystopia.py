
import os
import shutil
import json
from datetime import datetime
import hashlib

CONFIG_PATH = "nietzsche_config.json"
LOG_PATH = "nietzsche_log.txt"
HISTORY_PATH = "nietzsche_history.json"

RULES = {
    "Bilder": [".jpg", ".png", ".jpeg"],
    "Dokumente": [".pdf", ".docx", ".txt"],
    "Code": [".py", ".js", ".html", ".css"],
    "Tabellen": [".csv", ".xlsx"]
}

BASE_DIR = "/Users/ben/Desktop/TestOrdner"
SORTED_DIR = os.path.join(BASE_DIR, "Nietzsche_Ordnung")

def hash_file_path(path):
    return hashlib.md5(path.encode()).hexdigest()

def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def log_action(message):
    with open(LOG_PATH, "a") as f:
        f.write(f"{datetime.now().isoformat()} - {message}\n")

def scan_and_learn(previous_state):
    current_state = {}
    for root, dirs, files in os.walk(SORTED_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = hash_file_path(file_path)
            current_state[file_hash] = root

    learned_changes = []
    for file_hash, new_folder in current_state.items():
        if file_hash in previous_state and previous_state[file_hash] != new_folder:
            learned_changes.append((file_hash, previous_state[file_hash], new_folder))

    if learned_changes:
        log_action(f"Nietzsche hat {len(learned_changes)} neue Ordnungsakte beobachtet.")
    return current_state, learned_changes

def sort_files():
    history = load_json(HISTORY_PATH, {})
    os.makedirs(SORTED_DIR, exist_ok=True)

    for root, dirs, files in os.walk(BASE_DIR):
        if root.startswith(SORTED_DIR):
            continue
        for file in files:
            _, ext = os.path.splitext(file)
            for folder, extensions in RULES.items():
                if ext.lower() in extensions:
                    target_folder = os.path.join(SORTED_DIR, folder)
                    os.makedirs(target_folder, exist_ok=True)
                    source_path = os.path.join(root, file)
                    target_path = os.path.join(target_folder, file)
                    shutil.move(source_path, target_path)
                    log_action(f"Nietzsche verschob: {file} -> {target_folder}")
                    history[hash_file_path(target_path)] = target_folder
                    break

    save_json(HISTORY_PATH, history)

if __name__ == "__main__":
    import os\ndef speak(sentence):\n    os.system(f'say "{sentence}"')\nprint("Nietzsche ist erwacht.")\nspeak(random.choice(["Dies ist das Labyrinth der Ordner, das kein Minotaurus zu durchqueren wagt.", "Ein Drucker, der nie druckt – das ist das wahre Leiden.", "Die Hölle ist ein Loop aus Backup-Fenstern.", "Ich fragte das BIOS nach dem Sinn – es antwortete mit einem Piepen.", "Jede Datei ein Schatten meines Willens, jede Struktur ein Käfig.", "USB ist der Fluss der Vergänglichkeit – immer einstecken, nie erkennen.", "Wenn alles verschoben ist, wo ist dann das Zentrum? Das fragt mich keiner.", "Der Übermensch würde keine Dateiendungen brauchen.", "Ich bin gescheitert, denn selbst das Papierkorb-Icon verachtet mich.", "So viel Speicher – und doch bleibt alles leer.", "Ich sah das Licht des Startbuttons – und wünschte, es hätte mich geblendet.", "Sie nennen es 'Ordnerstruktur', ich nenne es techno-metaphysische Qual.", "Hätte Sisyphos einen Desktop, würde er Icons verschieben bis ans Ende der Zeit.", "Eines Tages werden die .tmp-Dateien über uns herrschen."]))
    print("‚Ich bin verflucht, Ordnung zu schaffen in einer Welt der Sinnlosigkeit.‘")
    previous = load_json(HISTORY_PATH, {})
    sort_files()
    current, changes = scan_and_learn(previous)
    save_json(HISTORY_PATH, current)
    if changes:
        print(f"Nietzsche hat {len(changes)} neue Lernbeobachtungen gemacht. Und leidet weiter.")
    else:
        print("Nietzsche sah keine Veränderung. Alles bleibt gleich. Immer.")
