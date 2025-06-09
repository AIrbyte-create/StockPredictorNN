import os
BASE_DIR = os.path.dirname(__file__)

import subprocess
import time

# 🔹 Pfad zum Hauptskript
hauptskript_path = os.path.join(BASE_DIR, r"Aktienai/Models/10_1/Diagramm/Main_10_1_Diagramm.py")

# 🔹 Pfad zur Eingabe-Datei
file_path = os.path.join(BASE_DIR, r"Aktien_Trainer/Vorhersage/Eingabe_Daten.txt")

# 📄 Datei öffnen und die ersten zwei Zeilen speichern
with open(file_path, "r", encoding="utf-8") as file:
    lines = [line.strip() for line in file if line.strip()][:2]  # Nur die ersten zwei nicht-leeren Zeilen nehmen

if len(lines) < 2:
    raise ValueError("Die Datei enthält weniger als zwei Zeilen.")

# 🟢 Nur die letzten 10 Zahlen aus der zweiten Zeile extrahieren
numbers = lines[1].split(",")
lines[1] = ",".join(numbers[-10:])  # Nimmt nur die letzten 10 Zahlen

# 🟢 Starte das Hauptskript mit den zwei Zeilen
process = subprocess.Popen(
    ["python", hauptskript_path],
    stdin=subprocess.PIPE,
    text=True
)

time.sleep(10)  # ⏳ Warte, damit das Skript bereit ist

# 🔄 Die zwei Zeilen eingeben
for line in lines:
    process.stdin.write(line + "\n")
    process.stdin.flush()
    time.sleep(5)

# 🛑 Beenden des Hauptskripts
process.stdin.write("exit\n")
process.stdin.flush()

# 🏁 Warte, bis das Hauptskript beendet ist
process.wait()
