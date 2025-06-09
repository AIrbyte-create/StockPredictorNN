import yfinance as yf
import random
import datetime
import os

# Wähle eine Aktie (z.B. Puma)
TICKER = "PUM.DE"

# Definiere den Speicherpfad
SAVE_PATH = "C:\\Users\\Gabriel Schwarzbauer\\Desktop\\Aktienai\\AktienInformationDownloader\\10_1"  # Passe den Pfad nach Bedarf an
os.makedirs(SAVE_PATH, exist_ok=True)  # Erstelle den Ordner, falls er nicht existiert

# Hole die letzten 5 Jahre als möglichen Zeitraum
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=5 * 365)

# Erstelle eine Liste mit möglichen Daten
date_range = [start_date + datetime.timedelta(days=i) for i in range(((end_date - start_date).days) - 11)]

# Anzahl der Wiederholungen
num_loops = 5000

# Schleife für die gewünschten Durchläufe
for _ in range(num_loops):
    random_start_date = random.choice(date_range)
    stock_data = yf.download(TICKER, start=random_start_date, end=end_date)

    if stock_data.empty:
        print("Keine Daten gefunden. Versuche es erneut!")
    else:
        filtered_data = stock_data["Close"].head(11)
        
        filename1 = os.path.join(SAVE_PATH, f"{TICKER}_random_11_trading_days.txt")
        with open(filename1, "a") as file:
            file.write(f"Aktienkurs für {TICKER} von {filtered_data.index[0].date()} bis {filtered_data.index[-1].date()}:\n")
            file.write(filtered_data.to_string())
            file.write("\n\n")

        filename2 = os.path.join(SAVE_PATH, f"{TICKER}_prices_only_11.txt")
        prices = [f"{float(price):.8f}" for price in filtered_data.values]
        prices_first_10 = ",".join(prices[:10])
        prices_11th = prices[10]

        file_mode = "a" if os.path.exists(filename2) else "w"
        with open(filename2, file_mode) as file:
            file.write(prices_first_10 + "\n")
            file.write(prices_11th + "\n")

    print(f"Durchlauf abgeschlossen. Dateien gespeichert in {SAVE_PATH}:")
