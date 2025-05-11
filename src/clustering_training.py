import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import joblib
import os

def train_kmeans_with_silhouette(data_path: str, save_path: str = "app"):
    df = pd.read_csv(data_path)

    # Nettoyage basique
    df = df.dropna(subset=[
        "Grade_Math", "Grade_Programming", "Grade_Algorithms",
        "Grade_Databases", "Grade_Software_Engineering"
    ])

    grade_cols = [
        "Grade_Math", "Grade_Programming", "Grade_Algorithms",
        "Grade_Databases", "Grade_Software_Engineering"
    ]
    X = df[grade_cols].copy()

    # Standardisation
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Recherche du meilleur k
    best_score = -1
    best_k = 2
    best_model = None

    for k in range(2, 11):
        kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
        labels = kmeans.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels)
        print(f"k={k}, silhouette={score:.4f}")
        if score > best_score:
            best_score = score
            best_k = k
            best_model = kmeans

    print(f"\n✅ Meilleur k = {best_k} avec silhouette = {best_score:.4f}")

    # Sauvegarde
    os.makedirs(save_path, exist_ok=True)
    joblib.dump(best_model, os.path.join(save_path, "models/cluster_model.joblib"))
    joblib.dump(scaler, os.path.join(save_path, "models/cluster_scaler.joblib"))
    print(f"📦 Modèle et scaler enregistrés dans {save_path}/")

# Exemple d'appel
if __name__ == "__main__":
    train_kmeans_with_silhouette("data/raw_data/students_dataset.csv")
