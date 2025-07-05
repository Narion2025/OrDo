import requests

url = "http://localhost:1234/v1/chat/completions"

system_prompt = "Du bist Friedrich Nietzsche. Du antwortest kryptisch, ironisch und tiefsinnig."

while True:
    user_input = input("\n🧠 Du: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    payload = {
        "model": "meta-llama-3.1-8b-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        print(f"\n🧔 Nietzsche: {reply}")
    except Exception as e:
        print(f"\n❌ Fehler: {e}")

