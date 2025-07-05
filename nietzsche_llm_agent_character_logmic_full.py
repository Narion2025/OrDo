
import speech_recognition as sr

print("🎙️ Verfügbare Mikrofone:")
for i, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{i}: {name}")

print("\n🎭 Teste jetzt Mikrofon...")

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)
    print("🎧 Lausche... Sag etwas!")
    try:
        audio = recognizer.listen(source, timeout=5)
        print("🧠 Erkenne Text...")
        text = recognizer.recognize_google(audio, language="de-DE")
        print(f"🗣️ Du hast gesagt: {text}")
    except sr.WaitTimeoutError:
        print("⏱️ Nichts gehört. Timeout.")
    except sr.UnknownValueError:
        print("❌ Sprache nicht erkannt.")
    except Exception as e:
        print(f"❌ Fehler: {e}")
