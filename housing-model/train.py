import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle
import os
import mlflow
import mlflow.sklearn

# Initialisation de MLflow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("housing_price_prediction")

# Chargement des données
data_path = 'housing.csv'
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Le fichier {data_path} est introuvable.")

data = pd.read_csv(data_path)

# Vérification des colonnes nécessaires
required_columns = ['median_house_value', 'ocean_proximity']
for col in required_columns:
    if col not in data.columns:
        raise ValueError(
            f"La colonne requise '{col}' est absente des données.")

X = data.drop('median_house_value', axis=1)
y = data['median_house_value']

# Encodage de la colonne 'ocean_proximity'
if 'ocean_proximity' in X.columns:
    encoder = OneHotEncoder()
    encoded_columns = encoder.fit_transform(
        X['ocean_proximity'].values.reshape(-1, 1))
    encoded_df = pd.DataFrame(encoded_columns.toarray(),
                              columns=encoder.get_feature_names_out(['ocean_proximity']))
    X = pd.concat([X.drop(columns=['ocean_proximity']), encoded_df], axis=1)

# Vérification des valeurs manquantes
if X.isnull().sum().sum() > 0:
    X = X.fillna(X.mean())

# Division des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Création et entraînement du modèle
with mlflow.start_run():
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Évaluation du modèle
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error (MSE) sur l'ensemble de test : {mse:.2f}")

    # Log des paramètres, métriques et modèle dans MLflow
    mlflow.log_param("random_state", 42)
    mlflow.log_metric("mse", mse)
    mlflow.sklearn.log_model(model, "model")

    # Sauvegarde locale du modèle
    model_path = 'model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Modèle sauvegardé dans {model_path}.")
