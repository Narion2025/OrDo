import speech_recognition as sr

recognizer = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    print("🎤 Sprich jetzt…")
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio, language="de-DE")
    print("🗣️ Du hast gesagt:", text)
except sr.UnknownValueError:
    print("❌ Nicht verstanden.")
except sr.RequestError as e:
    print("❌ API-Fehler:", e)

