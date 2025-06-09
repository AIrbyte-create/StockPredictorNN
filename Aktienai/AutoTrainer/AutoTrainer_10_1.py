import os
BASE_DIR = os.path.dirname(__file__)

import time
import subprocess
from pynput.keyboard import Controller, Key

keyboard = Controller()

# 🔹 Pfad zum Hauptskript
hauptskript_path = os.path.join(BASE_DIR, r"Aktienai/Models/10_1/Main_10_1_Tage.py")

# 🔹 Pfad zur Eingabe-Datei
file_path = os.path.join(BASE_DIR, r"Aktienai/AktienInformationDownloader/10_1/PUM.DE_prices_only_11.txt")

# 📄 Datei öffnen und Zeilen speichern
with open(file_path, "r", encoding="utf-8") as file:
    lines = [line.strip() for line in file if line.strip()]  # Leere Zeilen entfernen

index = 0  # Start bei der ersten Zeile

while index < len(lines):  
    # 🟢 Starte das Hauptskript
    process = subprocess.Popen(["python", hauptskript_path])
    time.sleep(3)  # ⏳ Warte, damit das Skript bereit ist

    # 🔄 20 Zeilen eingeben (falls noch genug übrig sind)
    for _ in range(20):
        if index >= len(lines):  # Falls wir am Ende der Datei sind
            break
        time.sleep(5)
        keyboard.type(lines[index])  # Zeile eintippen
        keyboard.press(Key.enter)  # Enter drücken
        keyboard.release(Key.enter)
        index += 1  # Zur nächsten Zeile springen
        time.sleep(1)  # ⏳ Kurze Pause zwischen den Eingaben

    # 🛑 Nach 20 Zeilen "exit" eingeben
    time.sleep(5)
    keyboard.type("exit")
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    

    # 🏁 Warte, bis das Hauptskript beendet ist
    process.wait()

    # ⏳ 10 Sekunden warten, bevor es weitergeht
    print("Warte 10 Sekunden, bevor das Hauptskript neu gestartet wird...")
    time.sleep(10)
