import voice_config\nimport os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ELEVEN_API_KEY")

text = "Hallo, ich bin Wagner. Ich spreche zu dir aus den Tiefen der KI."

output_path = Path("~/Documents/Nietzsche/audio/test_output.mp3").expanduser()
output_path.parent.mkdir(parents=True, exist_ok=True)

url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_config.VOICE_ID_NIETZSCHE}"
headers = {
    "xi-api-key": api_key,
    "Content-Type": "application/json"
}
json_data = {
    "text": text,
    "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
}

response = requests.post(url, headers=headers, json=json_data)

if response.status_code == 200:
    with open(output_path, 'wb') as f:
        f.write(response.content)
    print("✅ Audio gespeichert:", output_path)
else:
    print("🛑 Fehler bei ElevenLabs:", response.status_code)
    print(response.text)
