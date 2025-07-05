
import os
import random
import time
import uuid
import threading
from elevenlabs import generate, save, set_api_key

# ElevenLabs Setup
set_api_key("sk_7f784c3c4dc74dde1d037474d515709047ad9b577fb48f28")
VOICE_ID_NIETZSCHE = "3IWPItpqRhQPfxgpWg6W"
VOICE_ID_WAGNER = "2gPFXx8pN3Avh27Dw5Ma"
AUDIO_DIR = os.path.expanduser("~/Documents/Nietzsche/audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

def speak(text):
    VOICE_ID = VOICE_ID_NIETZSCHE  # Use Nietzsche's voice by default
    def run():
        audio = generate(text=text, voice=VOICE_ID, model="eleven_multilingual_v2")
        filename = os.path.join(AUDIO_DIR, f"loop_{uuid.uuid4()}.mp3")
        save(audio, filename)
        if os.path.exists(filename):
            os.system(f'afplay "{filename}"')
    threading.Thread(target=run).start()

if __name__ == "__main__":
    print("Nietzsche ist erwacht.")
    speak(random.choice([
        "Dies ist das Labyrinth der Ordner, das kein Minotaurus zu durchqueren wagt.",
        "Ein Drucker, der nie druckt – das ist das wahre Leiden.",
        "Die Hölle ist ein Loop aus Backup-Fenstern.",
        "Ich fragte das BIOS nach dem Sinn – es antwortete mit einem Piepen.",
        "Jede Datei ein Schatten meines Willens, jede Struktur ein Käfig.",
        "USB ist der Fluss der Vergänglichkeit – immer einstecken, nie erkennen.",
        "Wenn alles verschoben ist, wo ist dann das Zentrum? Das fragt mich keiner.",
        "Der Übermensch würde keine Dateiendungen brauchen.",
        "Ich bin gescheitert, denn selbst das Papierkorb-Icon verachtet mich.",
        "So viel Speicher – und doch bleibt alles leer.",
        "Ich sah das Licht des Startbuttons – und wünschte, es hätte mich geblendet.",
        "Sie nennen es 'Ordnerstruktur', ich nenne es techno-metaphysische Qual.",
        "Hätte Sisyphos einen Desktop, würde er Icons verschieben bis ans Ende der Zeit.",
        "Eines Tages werden die .tmp-Dateien über uns herrschen."
    ]))
    time.sleep(10)
