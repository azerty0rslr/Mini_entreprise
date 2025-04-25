import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib

import envoie_de_mail as em

# 1. Simulation d'un jeu de données
np.random.seed(42)
n_samples = 300
temp = np.random.uniform(0, 40, n_samples)  # Température en °C
humidity = np.random.uniform(10, 100, n_samples)  # Humidité en %
zone_quality = np.random.choice([0, 1, 2], n_samples)  # 0 = mauvaise, 1 = moyenne, 2 = bonne


# Fonction de durée théorique simplifiée
def estimate_life(temp, humidity, quality):
    base = 30
    temp_effect = -0.3 * temp
    humidity_effect = -0.1 * humidity
    quality_bonus = [0, 5, 10][quality]
    noise = np.random.normal(0, 2)
    return base + temp_effect + humidity_effect + quality_bonus + noise

conservation_days = [estimate_life(t, h, q) for t, h, q in zip(temp, humidity, zone_quality)]

# Création du DataFrame
data = pd.DataFrame({
    'temp': temp,
    'humidity': humidity,
    'zone_quality': zone_quality,
    'conservation_days': conservation_days
})

# 2. Préparation des données
X = data[['temp', 'humidity', 'zone_quality']]
y = data['conservation_days']

# 3. Entraînement du modèle
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# 4. Fonction de prédiction

def predict_conservation(temp, humidity, zone_quality):
    input_data = pd.DataFrame([[temp, humidity, zone_quality]], columns=['temp', 'humidity', 'zone_quality'])
    prediction = model.predict(input_data)[0]
    return round(prediction, 2)

# 5. Exemple d'utilisation
import random
temperature = random.randint(10, 20)
humidity = random.randint(50, 70)
zone_quality = random.randint(0, 2)
ex_pred = predict_conservation(temperature, humidity, zone_quality)
print(f"Durée estimée de conservation : {ex_pred} jours")

# 6. Sauvegarde du modèle si besoin
joblib.dump(model, "conservation_model.pkl")

sender_email = input("Entrez votre adresse e-mail : ")
sender_password = input("Entrez votre mot de passe : ")
receiver_email = input("Entrez l'adresse e-mail du destinataire : ")
em.envoie_mail(ex_pred, sender_email, sender_password, receiver_email)