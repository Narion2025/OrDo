
#!/bin/bash

# Starte Sprachsteuerung
nohup python3 ~/Documents/Nietzsche/nietzsche_live.py > /dev/null 2>&1 &

# Starte Dateiüberwachung
nohup python3 ~/Documents/Nietzsche/nietzsche_watch_tragoedie.py > /dev/null 2>&1 &

# Starte Code-Bridge oder Task-Executor (wenn benötigt)
# nohup python3 ~/Documents/Nietzsche/nietzsche_code_writer.py > /dev/null 2>&1 &
echo "Nietzsche Autostart abgeschlossen."
