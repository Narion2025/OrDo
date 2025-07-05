
import subprocess
import sys

try:
    import watchdog
    print("watchdog ist bereits installiert.")
except ImportError:
    print("Installiere watchdog...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "watchdog"])
