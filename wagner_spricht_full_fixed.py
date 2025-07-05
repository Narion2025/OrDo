
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import subprocess
import voice_config

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
assistant_id = "asst_xXtpaxefbJylYNnGa5iWdXqf"
eleven_key = os.getenv("ELEVEN_API_KEY")
voice_id = voice_config.VOICE_ID_WAGNER

def run_wagner(prompt):
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value

def speak(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": eleven_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        output_path = Path("~/Documents/Nietzsche/audio/wagner_output.mp3").expanduser()
        with open(output_path, "wb") as f:
            f.write(response.content)
        subprocess.run(["afplay", str(output_path)])
    else:
        print("Fehler bei ElevenLabs:", response.status_code, response.text)

if __name__ == "__main__":
    antwort = run_wagner("Wagner, was ist der Sinn eines guten Projekts?")
    speak(antwort)
