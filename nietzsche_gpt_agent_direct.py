import voice_config\n
import os
import openai
import speech_recognition as sr
import threading
import uuid
from elevenlabs import generate, save, set_api_key

# SET DIRECT KEYS HERE
OPENAI_API_KEY = "sk_b2877bf05c982b54b368fbaa246ab4f667439c45aec61fdc"  # <– dein echter OpenAI Key hier eintragen
ELEVEN_API_KEY = "sk_7f784c3c4dc74dde1d037474d515709047ad9b577fb48f28"     # <– dein echter ElevenLabs Key hier eintragen


# Setup
openai.api_key = OPENAI_API_KEY
set_api_key(ELEVEN_API_KEY)

# Paths
BASE_PATH = os.path.expanduser("~/Documents/Nietzsche")
AUDIO_DIR = os.path.join(BASE_PATH, "audio")
IDEEN_DIR = os.path.join(BASE_PATH, "Die Geburt der Tragödie/Ideen")
KANBAN_PATH = os.path.join(BASE_PATH, "Nietzsche_Kanban.json")
ERFAHRUNG_PATH = os.path.join(BASE_PATH, "erfahrungen.txt")
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(IDEEN_DIR, exist_ok=True)

recognizer = sr.Recognizer()
mic = sr.Microphone()
is_speaking = False

def sprich(text):
    global is_speaking
    if is_speaking:
        return
    def run():
        global is_speaking
        is_speaking = True
        try:
            audio = generate(text=text, voice=voice_config.VOICE_ID_NIETZSCHE, model="eleven_multilingual_v2")
            filename = os.path.join(AUDIO_DIR, f"gpt_{uuid.uuid4()}.mp3")
            save(audio, filename)
            os.system(f'afplay "{filename}"')
        except Exception as e:
            print("Fehler bei Sprachausgabe:", e)
        is_speaking = False
    threading.Thread(target=run).start()

def merke_antwort(text):
    with open(ERFAHRUNG_PATH, "a") as f:
        f.write(f"{text}\n")

def frage_gpt(prompt, erfahrung=""):
    try:
        messages = [
            {"role": "system", "content": f"""Du bist Friedrich Nietzsche als überzogene, ironisch-melancholische Bühnenfigur.
Du analysierst die Sprache deines Gegenübers. Wenn du Aufgaben erkennst wie Downloads ordnen, Idee speichern oder Kanban pflegen, erwähne das mit kurzen JSON-Hinweisen.
Antworten dürfen sarkastisch, tiefgründig und schwarz-humorig sein, aber du führst aus, was verlangt wird.
Früheres Wissen:
{erfahrung}
""" },
            {"role": "user", "content": prompt}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.8,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Fehler bei GPT:", e)
        return None

erfahrung = ""
if os.path.exists(ERFAHRUNG_PATH):
    with open(ERFAHRUNG_PATH) as f:
        erfahrung = f.read().strip()

sprich("Ich bin zurück. Direkt verdrahtet mit der Wolke.")

while True:
    if is_speaking:
        continue

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎧 Lausche...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language="de-DE").strip()
            print("🗣️ Du hast gesagt:", text)

            if "der wille zur macht" in text.lower():
                sprich("Ich schweige. Du hast es so gewollt.")
                break

            if any(x in text.lower() for x in ["gut gemacht", "lern das", "merk dir das"]):
                merke_antwort(text)
                sprich("Fein. Ich hab's notiert.")

            antwort = frage_gpt(text, erfahrung)
            if antwort:
                print("🧠 Antwort:", antwort)
                sprich(antwort.split("[")[0].strip())
        except Exception as e:
            print("❌ Fehler:", e)
