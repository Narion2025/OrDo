import voice_config
import speech_recognition as sr
import time
import os
import threading
import json
import sys
import uuid
from pathlib import Path
from elevenlabs import generate, save, set_api_key

# ElevenLabs Setup
set_api_key("sk_7f784c3c4dc74dde1d037474d515709047ad9b577fb48f28")

# Füge MARSAP-Pfad hinzu für CoSD-Integration
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "MARSAP"))

# Importiere CoSD und Marker-System
try:
    from cosd import CoSDAnalyzer
    from marker_matcher import MarkerMatcher
    COSD_AVAILABLE = True
    print("✅ CoSD und Marker-System geladen")
except ImportError as e:
    print(f"⚠️  CoSD nicht verfügbar: {e}")
    COSD_AVAILABLE = False

# Aktionen (bestehende Module)
import nietzsche_sort_downloads
import nietzsche_kanban_executor_corrected
import nietzsche_watch_tragoedie

# Ordo-spezifische Konfiguration
KANBAN_PATH = os.path.expanduser("~/Documents/Ordo/Ordo_Kanban.json")
PROJEKTE_ROOT = os.path.expanduser("~/Projekte")
ORDO_IDENTITY_PATH = os.path.join(os.path.dirname(__file__), "ordo_identity.txt")

# Ordo-Verhalten
recognizer = sr.Recognizer()
mic = sr.Microphone()
trigger = "ordo"  # Geändert von "nietzsche" zu "ordo"
listening = False
last_input_time = 0
dialog_timeout = 10
is_speaking = False

# Semantische Analyse-Komponenten
cosd_analyzer = None
marker_matcher = None

def init_semantic_systems():
    """Initialisiert die semantischen Analysesysteme"""
    global cosd_analyzer, marker_matcher
    
    if COSD_AVAILABLE:
        try:
            cosd_analyzer = CoSDAnalyzer()
            marker_matcher = MarkerMatcher()
            
            # Lade Marker aus dem bereitgestellten Ordner
            marker_path = os.path.join(os.path.dirname(__file__), "..", "..", "ALL_SEMANTIC_MARKER_TXT", "ALL_NEWMARKER01")
            if os.path.exists(marker_path):
                print(f"📚 Lade Marker aus: {marker_path}")
                # Hier würde die Marker-Ladung implementiert werden
            
            print("✅ Semantische Systeme initialisiert")
        except Exception as e:
            print(f"⚠️  Fehler beim Initialisieren der semantischen Systeme: {e}")

def load_ordo_identity():
    """Lädt die Ordo-Identität"""
    try:
        with open(ORDO_IDENTITY_PATH, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Du bist Ordo. Du hörst zu und strukturierst."

def sprich(text):
    """Ordo spricht mit ruhiger, strukturierter Stimme"""
    global is_speaking
    if is_speaking:
        return
    
    def run():
        global is_speaking
        is_speaking = True
        try:
            # Verwende die neue Ordo-Voice-ID
            audio = generate(
                text=text, 
                voice=voice_config.VOICE_ID_ORDO, 
                model="eleven_multilingual_v2"
            )
            filename = f"/tmp/ordo_{uuid.uuid4()}.mp3"
            save(audio, filename)
            os.system(f'afplay "{filename}"')
        except Exception as e:
            print(f"Fehler bei der Sprachausgabe: {e}")
        finally:
            is_speaking = False
    
    threading.Thread(target=run).start()

def analyze_semantic_markers(text):
    """Analysiert Text auf semantische Marker"""
    if not COSD_AVAILABLE or not cosd_analyzer:
        return None
    
    try:
        # CoSD-Analyse für Drift-Erkennung
        result = cosd_analyzer.analyze_drift([text])
        
        # Marker-Analyse
        if marker_matcher:
            markers = marker_matcher.analyze_text(text)
            return {
                'drift_analysis': result,
                'markers': markers,
                'risk_level': result.risk_assessment.get('risk_level', 'unknown') if hasattr(result, 'risk_assessment') else 'unknown'
            }
    except Exception as e:
        print(f"Fehler bei der semantischen Analyse: {e}")
        return None

def kanban_add_with_context(task, semantic_context=None):
    """Fügt Task mit semantischem Kontext hinzu"""
    try:
        # Erstelle Ordo-Verzeichnis falls nicht vorhanden
        ordo_dir = os.path.dirname(KANBAN_PATH)
        os.makedirs(ordo_dir, exist_ok=True)
        
        if not os.path.exists(KANBAN_PATH):
            with open(KANBAN_PATH, "w") as f:
                json.dump({"To Do": [], "In Progress": [], "Erledigt": []}, f)

        with open(KANBAN_PATH, "r") as f:
            board = json.load(f)

        # Erstelle erweiterten Task-Eintrag
        task_entry = {
            "id": f"#{len(board.get('To Do', [])) + 1:04d}",
            "text": task,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "semantic_context": semantic_context
        }
        
        board["To Do"].append(task_entry)

        with open(KANBAN_PATH, "w") as f:
            json.dump(board, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Task {task_entry['id']} hinzugefügt: {task}")
        return task_entry['id']

    except Exception as e:
        print("Fehler beim Schreiben ins Kanban:", e)
        return None

def passive_task_recognition(text):
    """Erkennt Tasks passiv ohne Antwort"""
    # Muster für Task-Erkennung
    task_patterns = [
        "ich muss", "ich sollte", "ich müsste",
        "nicht vergessen", "todo", "aufgabe",
        "erledigen", "machen", "organisieren"
    ]
    
    text_lower = text.lower()
    for pattern in task_patterns:
        if pattern in text_lower:
            # Analysiere semantischen Kontext
            semantic_context = analyze_semantic_markers(text)
            
            # Füge Task hinzu (passiv, ohne Sprachausgabe)
            task_id = kanban_add_with_context(text, semantic_context)
            
            # Logge nur intern
            print(f"🔍 Passiv erkannter Task: {task_id}")
            return True
    
    return False

def analysiere_befehl(text):
    """Analysiert Befehle für Ordo"""
    text_lower = text.lower()

    # Bestehende Funktionen
    if "download" in text_lower and ("ordne" in text_lower or "sortier" in text_lower):
        nietzsche_sort_downloads.sortiere_downloads()
        sprich("Downloads sortiert.")

    elif "kanban" in text_lower or "aufgabe" in text_lower or "task" in text_lower:
        if "hinzu" in text_lower:
            aufgabe = text.split("hinzu")[-1].strip()
            if aufgabe:
                semantic_context = analyze_semantic_markers(aufgabe)
                task_id = kanban_add_with_context(aufgabe, semantic_context)
                sprich(f"Task {task_id} hinzugefügt.")
        elif "zeige" in text_lower or "liste" in text_lower:
            zeige_kanban()

    elif "projekt" in text_lower or "ordner" in text_lower:
        name = text.split("projekt")[-1].strip()
        if name:
            projekt_anlegen(name)
            sprich(f"Projekt {name} erstellt.")

    elif "tragödie" in text_lower:
        nietzsche_watch_tragoedie.main()

    elif "marker" in text_lower or "analyse" in text_lower:
        if "analysiere" in text_lower:
            text_to_analyze = text.replace("analysiere", "").strip()
            if text_to_analyze:
                semantic_result = analyze_semantic_markers(text_to_analyze)
                if semantic_result:
                    sprich(f"Analyse abgeschlossen. Risk-Level: {semantic_result['risk_level']}")
                else:
                    sprich("Analyse nicht möglich.")

    elif "frage" in text_lower and "strukturell" in text_lower:
        # Ordo-spezifische Strukturfragen
        generate_structural_questions()

    else:
        # Standardantwort für unbekannte Befehle
        sprich("Was genau soll ich strukturieren?")

def zeige_kanban():
    """Zeigt Kanban-Status"""
    try:
        with open(KANBAN_PATH, "r") as f:
            board = json.load(f)
        
        todo_count = len(board.get("To Do", []))
        progress_count = len(board.get("In Progress", []))
        done_count = len(board.get("Erledigt", []))
        
        sprich(f"Kanban-Status: {todo_count} offen, {progress_count} in Arbeit, {done_count} erledigt.")
        
    except Exception as e:
        sprich("Kanban-Daten nicht verfügbar.")

def generate_structural_questions():
    """Generiert strukturelle Fragen basierend auf aktuellen Tasks"""
    try:
        with open(KANBAN_PATH, "r") as f:
            board = json.load(f)
        
        todo_tasks = board.get("To Do", [])
        if len(todo_tasks) > 3:
            sprich("Ich sehe mehrere offene Tasks. Soll ich diese nach Priorität clustern?")
        elif len(todo_tasks) > 0:
            sprich("Möchtest du deine offenen Tasks strukturieren?")
        else:
            sprich("Keine offenen Tasks. Wie kann ich dir helfen?")
            
    except Exception as e:
        sprich("Strukturanalyse nicht möglich.")

def projekt_anlegen(name):
    """Erstellt neuen Projektordner"""
    try:
        ordner_name = name.strip().replace(" ", "_")
        pfad = os.path.join(PROJEKTE_ROOT, ordner_name)
        os.makedirs(pfad, exist_ok=True)
        print(f"📁 Projekt erstellt: {pfad}")
    except Exception as e:
        print("Fehler beim Anlegen des Projekts:", e)

# Initialisierung
print("🧠 ORDO - Semantischer Task-Begleiter")
print("=" * 50)

# Lade Ordo-Identität
ordo_identity = load_ordo_identity()
print("🎭 Ordo-Identität geladen")

# Initialisiere semantische Systeme
init_semantic_systems()

print("🎤 Höre passiv zu... (Trigger: 'Ordo')")
print("=" * 50)

# Hauptschleife
while True:
    if is_speaking:
        continue

    with mic as source:
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="de-DE")
        current_time = time.time()
        
        # Passive Task-Erkennung (immer aktiv)
        task_recognized = passive_task_recognition(text)
        
        # Aktive Kommunikation nur bei Trigger
        if trigger in text.lower():
            listening = True
            last_input_time = current_time
            befehl = text.lower().replace(trigger, "").strip()
            
            print(f"🗣️  Ordo aktiviert: {befehl}")
            
            if befehl:
                threading.Thread(target=analysiere_befehl, args=(befehl,)).start()
            else:
                sprich("Wie kann ich dir helfen?")
                
        elif listening:
            if current_time - last_input_time > dialog_timeout:
                listening = False
                print("⏱️  Dialog-Fenster geschlossen.")
            else:
                last_input_time = current_time
                print(f"🗣️  Fortsetzung: {text}")
                threading.Thread(target=analysiere_befehl, args=(text,)).start()
        
        # Stille Bestätigung bei passiver Task-Erkennung
        elif task_recognized:
            print(f"🔍 Passiv erfasst: {text[:50]}...")

    except sr.UnknownValueError:
        continue
    except Exception as e:
        print("❌ Fehler:", e) 