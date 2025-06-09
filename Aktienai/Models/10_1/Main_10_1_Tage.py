import os
BASE_DIR = os.path.dirname(__file__)

import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os



# Modell definieren
model = keras.Sequential([
    layers.Dense(32, activation='relu', input_shape=(10,)),
    layers.Dense(16, activation='relu'),
    layers.Dense(1)  # Eine Zahl als Ausgabe
])

# Modell kompilieren mit explizitem Verlust 'mean_squared_error'
model.compile(optimizer='adam', loss='mean_squared_error')

# Pfad zum Speichern des Modells
model_save_path = os.path.join(BASE_DIR, r"Aktienai/Models/10_1/trained_model.h5")


# Funktion, um das Modell zu speichern
def save_model():
    model.save(model_save_path)
    print("\n")
    print("Modell wurde gespeichert.")

# Funktion, um das Modell zu laden
def load_model():
    if os.path.exists(model_save_path):
        model = keras.models.load_model(model_save_path, compile=True)  
        model.compile(optimizer='adam', loss='mean_squared_error')  # Recompile nach Laden
        print("\nModell erfolgreich geladen und kompiliert.")
    else:
        print("\nKein gespeichertes Modell gefunden. Ein neues Modell wird erstellt.")
        model = keras.Sequential([
            layers.Dense(32, activation='relu', input_shape=(10,)),
            layers.Dense(16, activation='relu'),
            layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')

    return model  # ✅ Jetzt wird 'model' immer zurückgegeben!


# Funktion, um Benutzereingaben zu sammeln und das Modell zu trainieren
def train_model_with_user_data():
    X = []
    y = []
    
    while True:
        # Benutzereingaben
        print("\n")
        user_input = input("Gib 10 Zahlen für die Eingabedaten (durch Kommas getrennt) ein oder 'exit' zum Beenden: ")
        
        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'test':
            test_model()
            continue
        
        # Eingabe verarbeiten
        try:
            user_data = list(map(float, user_input.split(',')))
            if len(user_data) != 10:
                print("\n")
                print("Bitte genau 10 Zahlen eingeben.")
                continue
            print("\n")
            next_number = float(input("Gib die nächste Zahl als Ziel (Ausgabe) ein: "))
            
            # Daten hinzufügen
            X.append(user_data)
            y.append(next_number)

            # Testen des Modells mit der zuletzt eingegebenen Zahl (ohne des Trainings)
            prediction = model.predict(np.array([user_data], dtype=np.float32))
            print("\n")
            print(f"Vorhergesagte nächste Zahl (ohne Training): {prediction[0][0]:.2f}")
            print("\n")
 
            # Modell mit den bisherigen Daten trainieren
            print("Training...")
            print("\n")
            X_np = np.array(X, dtype=np.float32)
            y_np = np.array(y, dtype=np.float32)
            
            model.fit(X_np, y_np, epochs=100, verbose=0)  # Training mit den neuen Daten

            # Testen des Modells mit der zuletzt eingegebenen Zahl
            prediction = model.predict(np.array([user_data], dtype=np.float32))
            print("\n")
            print(f"Vorhergesagte nächste Zahl (mit Training): {prediction[0][0]:.2f}")
        
        except ValueError:
            print("\n")
            print("Ungültige Eingabe. Bitte sicherstellen, dass nur Zahlen eingegeben werden.")
        
    save_model()  # Modell speichern nach dem Training

# Funktion, um das Modell zu testen (11. Zahl vorhersagen)
def test_model():
    print("\n")
    test_input = input("Gib 10 Zahlen ein, um die nächste Zahl (11. Zahl) vorherzusagen (durch Kommas getrennt): ")
    
    try:
        user_data = list(map(float, test_input.split(',')))
        if len(user_data) != 10:
            print("\n")
            print("Bitte genau 10 Zahlen eingeben.")
            return
        
        # Vorhersage der 11. Zahl
        prediction = model.predict(np.array([user_data], dtype=np.float32))
        print("\n")
        print(f"Vorhergesagte 11. Zahl: {prediction[0][0]:.2f}")
        
        # Korrigierte Ausgabe mit float-Wert statt Array
        if prediction[0][0] > user_data[-1]:
            print(f"INVEST: Vorhersage = {prediction[0][0]:.2f}, Letzte Zahl = {user_data[-1]:.2f}")
        else:
            print(f"DON'T INVEST: Vorhersage = {prediction[0][0]:.2f}, Letzte Zahl = {user_data[-1]:.2f}")

            
    
    except ValueError:
        print("\n")
        print("Ungültige Eingabe. Bitte sicherstellen, dass nur Zahlen eingegeben werden.")

# Modell laden (falls vorhanden) oder neues Modell erstellen
model = load_model()

# Modell mit Benutzereingaben trainieren
train_model_with_user_data()
