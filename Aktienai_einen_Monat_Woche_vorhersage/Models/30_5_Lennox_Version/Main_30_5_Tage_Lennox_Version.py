import os
BASE_DIR = os.path.dirname(__file__)

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os
import matplotlib.pyplot as plt  # Matplotlib für das Diagramm
from datetime import datetime

# Modell definieren
model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=(30,)),
        layers.Dense(48, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(24, activation='relu'),
        layers.Dense(16, activation='relu'),
        layers.Dense(12, activation='relu'),
        layers.Dense(8, activation='relu'),
        layers.Dense(5)  # 5 Werte als Ausgabe
    ])

# Modell kompilieren mit explizitem Verlust 'mean_squared_error'
model.compile(optimizer='adam', loss='mean_squared_error')

# Pfad zum Speichern des Modells
model_save_path = os.path.join(BASE_DIR, r"Aktienai_einen_Monat_Woche_vorhersage/Models/30_5_Lennox_Version/trained_model.h5")


# Funktion, um das Modell zu speichern
def save_model():
    model.save(model_save_path)
    print("\nModell wurde gespeichert.")

# Funktion, um das Modell zu laden
def load_model():
    if os.path.exists(model_save_path):
        model = keras.models.load_model(model_save_path, compile=True)  
        model.compile(optimizer='adam', loss='mean_squared_error')  # Recompile nach Laden
        print("\nModell erfolgreich geladen und kompiliert.")
    else:
        print("\nKein gespeichertes Modell gefunden. Ein neues Modell wird erstellt.")
        model = keras.Sequential([
                layers.Dense(64, activation='relu', input_shape=(30,)),
                layers.Dense(48, activation='relu'),
                layers.Dense(32, activation='relu'),
                layers.Dense(24, activation='relu'),
                layers.Dense(16, activation='relu'),
                layers.Dense(12, activation='relu'),
                layers.Dense(8, activation='relu'),
                layers.Dense(5)  # 5 Werte als Ausgabe
            ])
        model.compile(optimizer='adam', loss='mean_squared_error')

    return model  # ✅ Jetzt wird 'model' immer zurückgegeben!


# Funktion, um Benutzereingaben zu sammeln und das Modell zu trainieren
def train_model_with_user_data():
    X = []
    y = []
    
    # Liste für die Differenzen (Vorhergesagte Werte - Tatsächliche Werte)
    differences = []
    
    while True:
        # Benutzereingaben
        print("\n")
        user_input = input("Gib 30 Zahlen für die Eingabedaten (durch Kommas getrennt) ein oder 'exit' zum Beenden: ")
        
        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'test':
            test_model()
            continue
        
        # Eingabe verarbeiten
        try:
            user_data = list(map(float, user_input.split(',')))
            if len(user_data) != 30:
                print("\n")
                print("Bitte genau 30 Zahlen eingeben.")
                continue
            print("\n")
            next_numbers = list(map(float, input("Gib 5 Zielwerte für die nächste Ausgabe ein (durch Kommas getrennt): ").split(',')))
            if len(next_numbers) != 5:
                print("Bitte genau 5 Zielwerte eingeben.")
                continue
            
            # Daten hinzufügen
            X.append(user_data)
            y.append(next_numbers)

            # Testen des Modells mit der zuletzt eingegebenen Zahl (ohne des Trainings)
            prediction_before = model.predict(np.array([user_data], dtype=np.float32))
            print("\n")
            print(f"Vorhergesagte nächste 5 Zahlen (ohne Training): {prediction_before[0]}")

            # Modell mit den bisherigen Daten trainieren
            print("Training...")

            X_np = np.array(X, dtype=np.float32)
            y_np = np.array(y, dtype=np.float32)
            
            model.fit(X_np, y_np, epochs=100, verbose=0)  # Training mit den neuen Daten

            # Testen des Modells mit der zuletzt eingegebenen Zahl
            prediction_after = model.predict(np.array([user_data], dtype=np.float32))
            print("\n")
            print(f"Vorhergesagte nächste 5 Zahlen (mit Training): {prediction_after[0]}")
        
            # Berechne die Differenz und speichere sie
            difference = np.abs(prediction_after[0] - next_numbers)
            differences.append(difference)

        except ValueError:
            print("\n")
            print("Ungültige Eingabe. Bitte sicherstellen, dass nur Zahlen eingegeben werden.")
    
    # Diagramm nach dem Training
    plot_differences(differences)

    save_model()  # Modell speichern nach dem Training


# Funktion, um das Modell zu testen (Vorhersage der nächsten 5 Zahlen)
def test_model():
    print("\n")
    test_input = input("Gib 30 Zahlen ein, um die nächsten 5 Zahlen vorherzusagen (durch Kommas getrennt): ")
    
    try:
        user_data = list(map(float, test_input.split(',')))
        if len(user_data) != 30:
            print("\n")
            print("Bitte genau 30 Zahlen eingeben.")
            return
        
        # Vorhersage der nächsten 5 Zahlen
        prediction = model.predict(np.array([user_data], dtype=np.float32))
        print("\n")
        print(f"Vorhergesagte nächsten 5 Zahlen: {prediction[0]}")
        
        # Korrigierte Ausgabe mit float-Wert statt Array
        if np.all(prediction[0] > user_data[-5:]):
            print(f"INVEST: Vorhersage = {prediction[0]}, Letzte 5 Zahlen = {user_data[-5:]}")
        else:
            print(f"DON'T INVEST: Vorhersage = {prediction[0]}, Letzte 5 Zahlen = {user_data[-5:]}")

    except ValueError:
        print("\n")
        print("Ungültige Eingabe. Bitte sicherstellen, dass nur Zahlen eingegeben werden.")

# Funktion, um die Differenzen zu plotten

def plot_differences(differences):
    # Verzeichnis überprüfen und gegebenenfalls erstellen
    directory = os.path.join(BASE_DIR, r"Aktien_Trainer/Lern-Fortschritt/30_5_Lennox_Edition")
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Differenzen in ein NumPy-Array umwandeln für einfachere Verarbeitung
    differences = np.array(differences)

    # Mittelwert der Differenzen berechnen
    avg_difference = np.mean(differences, axis=0)

    # Diagramm plotten
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    plt.figure(figsize=(10, 5))

    # Jede Linie einzeln zeichnen und beschriften
    for i in range(differences.shape[1]):
        plt.plot(differences[:, i], label=f'Differenz Wert {i+1}')

    # Durchschnittslinie zeichnen
    plt.axhline(y=np.mean(avg_difference), color='r', linestyle='--', label="Durchschnitt")

    # Titel und Achsenbeschriftungen
    plt.title("Differenz zwischen Vorhersage und tatsächlichem Wert während des Trainings")
    plt.xlabel("Trainings-Iterationen")
    plt.ylabel("Differenz (Vorhergesagt - Tatsächlich)")

    # Raster für bessere Lesbarkeit
    plt.grid(True, linestyle="--", alpha=0.6)

    # Legende hinzufügen
    plt.legend()

    # Diagramm als PNG-Datei speichern und überschreiben
    plt.savefig(os.path.join(directory, f"training_differences_{timestamp}.png"))
    plt.close()  # Schließt das Diagramm nach dem Speichern
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Diagramm plotten
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    plt.plot(differences)
    plt.title("Differenz zwischen Vorhersage und tatsächlichem Wert während des Trainings")
    plt.xlabel("Training Iterationen")
    plt.ylabel("Differenz (Vorhergesagt - Tatsächlich)")
    
    # Diagramm als PNG-Datei speichern und überschreiben
    plt.savefig(os.path.join(directory, f"training_differences_2_{timestamp}.png"))
    plt.close()  # Schließt das Diagramm nach dem Speichern
# Modell laden (falls vorhanden) oder neues Modell erstellen
model = load_model()

# Modell mit Benutzereingaben trainieren
train_model_with_user_data()
