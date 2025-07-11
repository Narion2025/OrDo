# LLM Growth Environment

Dieses Projekt stellt ein leichtgewichtiges Lernumfeld für ein Sprachmodell bereit. Das Skript `llm_growth_environment.py` speichert jede Interaktion in YAML-Dateien und baut daraus ein einfaches Profil auf.

## Start

```bash
python3 llm_growth_environment.py
```

## Dateien

- **user_profile.yaml** – enthält häufig genutzte Schlüsselwörter und die Anzahl der Interaktionen.
- **user_interactions.yaml** – protokolliert Eingaben und Antworten chronologisch.

Das System dient als Grundlage und kann mit echten LLM-Aufrufen oder weiteren Analysefunktionen erweitert werden, um die Bedürfnisse des Nutzers besser zu antizipieren.

## Erweiterung: Emotionserkennung

Das Skript `ben_emotion_learning.py` baut auf dieser Umgebung auf. Es analysiert die Lautstärke der Spracheingabe, leitet daraus eine einfache Emotion ab und aktualisiert ein Benutzerprofil. Dadurch entsteht eine kleine Rückkopplungsschleife, in der das System Annahmen über den Nutzer fortlaufend prüft.

Starten mit:

```bash
python3 ben_emotion_learning.py
```
