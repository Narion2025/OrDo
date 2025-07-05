
import os
from dotenv import load_dotenv
from openai import OpenAI
from nietzsche_todo import add_todo, show_todos, delete_todo

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

assistant_id = "asst_xXtpaxefbJylYNnGa5iWdXqf"

def interpret_and_act(prompt):
    """Interpretiert deinen Text und führt die passende Aktion aus."""
    if "zeige" in prompt.lower() and "todo" in prompt.lower():
        show_todos()
    elif "lösche" in prompt.lower():
        try:
            index = int(''.join(filter(str.isdigit, prompt)))
            delete_todo(index)
        except ValueError:
            print("❗ Keine gültige Nummer erkannt.")
    elif "füge" in prompt.lower() or "hinzu" in prompt.lower():
        task = prompt.split("zur To-do-Liste hinzu")[-1].strip(" .")
        if task:
            add_todo(task)
        else:
            print("🧐 Konnte keine Aufgabe erkennen.")
    else:
        print("🤔 Ich weiß nicht, was ich tun soll. Sag z. B. 'Füge Backup machen zur To-do-Liste hinzu'.")

if __name__ == "__main__":
    while True:
        user_input = input("\n🎙️ Was soll Nietzsche tun? (Strg+C zum Beenden)\n> ")
        interpret_and_act(user_input)
