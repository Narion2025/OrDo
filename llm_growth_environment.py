#!/usr/bin/env python3
"""LLM Growth Environment

Dieses Skript bietet eine einfache Umgebung, in der ein Sprachmodell aus Interaktionen lernen kann.\nBenutzereingaben und Antworten werden dauerhaft in YAML-Dateien gespeichert, um ein grundlegendes Profil aufzubauen.\n"""

from collections import Counter
from datetime import datetime
from pathlib import Path
import yaml

class LLMGrowthEnvironment:
    def __init__(self, profile_path: str = "user_profile.yaml", log_path: str = "user_interactions.yaml"):
        self.profile_path = Path(profile_path)
        self.log_path = Path(log_path)
        self.profile = {"keywords": {}, "interactions": 0}
        self.interactions = []
        self._load_profile()
        self._load_log()

    def _load_profile(self):
        if self.profile_path.exists():
            try:
                with open(self.profile_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, dict):
                        self.profile.update(data)
            except Exception:
                pass

    def _load_log(self):
        if self.log_path.exists():
            try:
                with open(self.log_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, list):
                        self.interactions = data
            except Exception:
                pass

    def _save_profile(self):
        try:
            with open(self.profile_path, "w", encoding="utf-8") as f:
                yaml.dump(self.profile, f, allow_unicode=True)
        except Exception:
            pass

    def _save_log(self):
        try:
            with open(self.log_path, "w", encoding="utf-8") as f:
                yaml.dump(self.interactions, f, allow_unicode=True)
        except Exception:
            pass

    def update_profile(self, user_input: str) -> None:
        tokens = [t.lower() for t in user_input.split()]
        counts = Counter(tokens)
        for token, count in counts.items():
            self.profile["keywords"][token] = self.profile["keywords"].get(token, 0) + count
        self.profile["interactions"] += 1

    def record_interaction(self, user_input: str, response: str) -> None:
        self.interactions.append({
            "timestamp": datetime.now().isoformat(),
            "input": user_input,
            "response": response,
        })
        self._save_log()
        self._save_profile()

    def generate_response(self, user_input: str) -> str:
        # Platzhalter für echte LLM-Integration
        keywords = ", ".join(sorted(set(user_input.split())))
        return f"Ich habe deine Eingabe verstanden. Schlüsselwörter: {keywords}"

    def interactive_loop(self) -> None:
        print("LLM Lernumgebung gestartet. Tippe 'exit' zum Beenden.")
        try:
            while True:
                user_input = input("Du: ").strip()
                if user_input.lower() in {"exit", "quit"}:
                    break
                response = self.generate_response(user_input)
                print("LLM:", response)
                self.update_profile(user_input)
                self.record_interaction(user_input, response)
        finally:
            self._save_log()
            self._save_profile()
            print("Lernumgebung beendet.")

if __name__ == "__main__":
    env = LLMGrowthEnvironment()
    env.interactive_loop()
