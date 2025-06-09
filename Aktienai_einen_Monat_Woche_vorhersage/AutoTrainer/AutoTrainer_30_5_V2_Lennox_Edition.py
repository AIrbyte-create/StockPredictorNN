import os
BASE_DIR = os.path.dirname(__file__)

import time
import subprocess

# 🔹 Pfad zum Hauptskript
hauptskript_path = os.path.join(BASE_DIR, r"Aktienai_einen_Monat_Woche_vorhersage/Models/30_5_Lennox_Version/Main_30_5_Tage_Lennox_Version.py")

# 🔹 Pfad zur Eingabe-Datei
file_path = os.path.join(BASE_DIR, r"Aktienai_einen_Monat_Woche_vorhersage/AktienInformationDownloader/30_5/PUM.DE_prices_only_35.txt")

# 📄 Datei öffnen und Zeilen speichern
with open(file_path, "r", encoding="utf-8") as file:
    lines = [line.strip() for line in file if line.strip()]  # Leere Zeilen entfernen

index = 0  # Start bei der ersten Zeile

while index < len(lines):  
    # 🟢 Starte das Hauptskript mit Piped Input
    process = subprocess.Popen(["python", hauptskript_path], stdin=subprocess.PIPE, text=True)

    time.sleep(3)  # ⏳ Warte, damit das Skript bereit ist

    # 🔄 50 Zeilen eingeben (falls noch genug übrig sind)
    for _ in range(20):
        if index >= len(lines):  # Falls wir am Ende der Datei sind
            break
        process.stdin.write(lines[index] + "\n")  # Direkt in das Skript schreiben
        process.stdin.flush()  # Sofort absenden
        index += 1  # Zur nächsten Zeile springen
        time.sleep(1)  # ⏳ Kurze Pause zwischen den Eingaben

    # 🛑 Nach 50 Zeilen "exit" senden
    time.sleep(70)
    process.stdin.write("exit\n")
    process.stdin.flush()

    # 🏁 Warte, bis das Hauptskript beendet ist
    process.wait()

    # ⏳ 10 Sekunden warten, bevor es weitergeht
    print("Warte 10 Sekunden, bevor das Hauptskript neu gestartet wird...")
    time.sleep(10)
