#!/bin/bash

echo "🧠 Starte ORDO - Semantischer Task-Begleiter"
echo "=================================================="

# Wechsle ins Ordo-Verzeichnis
cd "$(dirname "$0")"

# Prüfe Python-Umgebung
python3 check_python_env.py

# Starte Ordo
echo "🎤 Ordo startet..."
python3 ordo_voice_agent.py

