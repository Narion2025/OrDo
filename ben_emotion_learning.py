#!/usr/bin/env python3
"""Adaptive LLM environment with simple feedback loops and emotion detection.
This script extends ``llm_growth_environment.py`` by analysing the microphone
input for amplitude-based emotions and updating a persistent user model. It can
be used to experiment with small memory feedback loops.
"""

from pathlib import Path
import yaml
import numpy as np
import speech_recognition as sr
from llm_growth_environment import LLMGrowthEnvironment


class EmotionDetector:
    """Derives a basic emotional state from raw audio amplitude."""

    def detect(self, audio: sr.AudioData) -> str:
        raw = audio.get_raw_data()
        # Convert bytes to int16 numpy array for amplitude estimation
        samples = np.frombuffer(raw, dtype=np.int16)
        amplitude = float(np.abs(samples).mean())
        if amplitude > 4000:
            return "angry"
        if amplitude > 2000:
            return "excited"
        if amplitude > 500:
            return "neutral"
        return "calm"


class BenUserModel:
    """Stores simple assumptions about Ben and updates them over time."""

    def __init__(self, path: str = "ben_user_model.yaml"):
        self.path = Path(path)
        self.data = {"assumptions": {}}
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    loaded = yaml.safe_load(f)
                    if isinstance(loaded, dict):
                        self.data.update(loaded)
            except Exception:
                pass

    def _save(self) -> None:
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                yaml.dump(self.data, f, allow_unicode=True)
        except Exception:
            pass

    def update(self, tokens, emotion: str) -> None:
        assumptions = self.data.setdefault("assumptions", {})
        if any(t in {"struktur", "plan", "organisation"} for t in tokens):
            assumptions["needs_structure"] = (
                assumptions.get("needs_structure", 0.0) + 0.1
            )
        if emotion in {"angry", "excited"}:
            assumptions["stress_level"] = assumptions.get("stress_level", 0.0) + 0.05
        if emotion == "calm":
            assumptions["calm_pref"] = assumptions.get("calm_pref", 0.0) + 0.05
        for key in assumptions:
            assumptions[key] = max(0.0, min(1.0, assumptions[key]))
        self._save()

    def summary(self) -> str:
        return ", ".join(
            f"{k}={v:.2f}" for k, v in self.data.get("assumptions", {}).items()
        )


class FeedbackEnvironment(LLMGrowthEnvironment):
    """Adds a tiny feedback loop on top of ``LLMGrowthEnvironment``."""

    def generate_response(self, user_input: str) -> str:
        base = super().generate_response(user_input)
        if (
            self.profile.get("interactions", 0) % 5 == 0
            and self.profile["interactions"] > 0
        ):
            base += " | Erinnerung: Ich lerne weiterhin von dir."
        return base


def main() -> None:
    env = FeedbackEnvironment()
    user_model = BenUserModel()
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    emotion_detector = EmotionDetector()

    print("Adaptive Lernumgebung gestartet. Sage 'exit' zum Beenden.")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        with mic as source:
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="de-DE")
        except sr.UnknownValueError:
            continue
        emotion = emotion_detector.detect(audio)
        tokens = [t.lower() for t in text.split()]
        response = env.generate_response(text)
        print(f"LLM ({emotion}):", response)
        env.update_profile(text)
        env.record_interaction(text, response)
        user_model.update(tokens, emotion)
        print("Annahmen:", user_model.summary())
        if text.strip().lower() in {"exit", "quit"}:
            break

    print("Lernumgebung beendet.")


if __name__ == "__main__":
    main()
