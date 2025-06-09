import yfinance as yf
import datetime

def get_stock_prices(ticker, days):
    # Heutiges Datum und Startdatum berechnen
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=days+4)
    
    # Holen der historischen Aktienkurse
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

    # Nur Wochentage (Montag bis Freitag) berücksichtigen
    hist = hist[hist.index.weekday < 5]
    
    # Die letzten 'days' Kurse der Wochentage extrahieren
    prices = hist['Close'].tail(days).tolist()
    
    # Die Preise formatieren
    formatted_prices = ",".join(f"{price:.2f}" for price in prices)
    
    # Abrufen des derzeitigen Kurses
    current_price = stock.history(period="1d")['Close'].iloc[-1]

    # Ausgabe der Preise
    print(f"Preise der letzten {days} Tage: {formatted_prices}")
    print(f"Derzeitiger Preis: {current_price:.2f}")

if __name__ == "__main__":
    while True:
        ticker = input("Geben Sie das Ticker-Symbol der Aktie ein (oder 'exit' zum Beenden): ").strip().upper()
        if ticker == "EXIT":
            break
        try:
            days = int(input("Geben Sie die Anzahl der Tage ein, die zurückgeblickt werden sollen: ").strip())
            get_stock_prices(ticker, days)
        except Exception as e:
            print("Fehler beim Abrufen der Daten:", e)
