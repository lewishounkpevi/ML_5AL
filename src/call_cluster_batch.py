import pandas as pd
import requests
import time

API_URL = "http://localhost:8000/cluster"

INPUT_PATH = "src/data/students_dataset.csv"
OUTPUT_PATH = "src/data/students_with_clusters.csv"

# Colonnes attendues pour le clustering
grade_cols = [
    "Grade_Math",
    "Grade_Programming",
    "Grade_Algorithms",
    "Grade_Databases",
    "Grade_Software_Engineering"
]

def call_cluster_api(payload):
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("cluster")
    except Exception as e:
        print("❌ Erreur d'appel API :", e)
        return None

def predict_clusters_from_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    results = []

    for i, row in df.iterrows():
        if row[grade_cols].isnull().any():
            results.append(None)
            continue

        payload = {
            "grade_math": row["Grade_Math"],
            "grade_programming": row["Grade_Programming"],
            "grade_algorithms": row["Grade_Algorithms"],
            "grade_databases": row["Grade_Databases"],
            "grade_software_engineering": row["Grade_Software_Engineering"]
        }

        cluster = call_cluster_api(payload)
        results.append(cluster)
        print(f"[{i+1}/{len(df)}] Cluster: {cluster}")
        time.sleep(0.1)  # éviter surcharge

    df["Cluster"] = results
    df.to_csv(output_csv, index=False)
    print(f"✅ Fichier exporté avec cluster : {output_csv}")


import pandas as pd
import requests
import os

def predict_cluster_batch_from_csv(csv_path, output_dir="outputs", output_name="cluster_results.csv"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_name)

    df = pd.read_csv(csv_path)

    grade_cols = [
        "Grade_Math", "Grade_Programming", "Grade_Algorithms",
        "Grade_Databases", "Grade_Software_Engineering"
    ]

    # Construction du payload
    payload = []
    valid_index = []

    for i, row in df.iterrows():
        if row[grade_cols].isnull().any():
            continue
        valid_index.append(i)
        payload.append({
            "grade_math": float(row["Grade_Math"]),
            "grade_programming": float(row["Grade_Programming"]),
            "grade_algorithms": float(row["Grade_Algorithms"]),
            "grade_databases": float(row["Grade_Databases"]),
            "grade_software_engineering": float(row["Grade_Software_Engineering"])
        })

    try:
        response = requests.post("http://localhost:8000/cluster_batch", json=payload)
        response.raise_for_status()
        clusters = response.json()

        # Initialiser la colonne
        df["Cluster"] = None
        for idx, cluster_id in zip(valid_index, clusters):
            df.at[idx, "Cluster"] = cluster_id

        df.to_csv(output_path, index=False)
        print(f"✅ Clusters sauvegardés dans : {output_path}")

    except Exception as e:
        print("❌ Erreur lors de l'appel batch clustering :", e)


import pandas as pd
import requests
import os

def predict_cluster_batch_from_csv(csv_path, output_dir="outputs", output_name="cluster_results.csv"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_name)

    df = pd.read_csv(csv_path)

    grade_cols = [
        "Grade_Math", "Grade_Programming", "Grade_Algorithms",
        "Grade_Databases", "Grade_Software_Engineering"
    ]

    # Filtrer les lignes valides (sans NaN)
    df_valid = df.dropna(subset=grade_cols).copy()

    # Préparer le payload complet d'un coup
    payload = df_valid[grade_cols].rename(columns={
        "Grade_Math": "grade_math",
        "Grade_Programming": "grade_programming",
        "Grade_Algorithms": "grade_algorithms",
        "Grade_Databases": "grade_databases",
        "Grade_Software_Engineering": "grade_software_engineering"
    }).to_dict(orient="records")

    try:
        response = requests.post("http://localhost:8000/cluster_batch", json=payload)
        response.raise_for_status()
        clusters = response.json()

        df_valid["Cluster"] = clusters

        # Fusionner avec les données initiales (pour garder les lignes avec NaN aussi)
        df = df.merge(df_valid[["Cluster"]], left_index=True, right_index=True, how="left")

        df.to_csv(output_path, index=False)
        print(f"✅ Clusters sauvegardés dans : {output_path}")

    except Exception as e:
        print("❌ Erreur lors de l'appel batch clustering :", e)


# Exécution manuelle
if __name__ == "__main__":
    predict_cluster_batch_from_csv("src/data/students_dataset.csv")

    # predict_clusters_from_csv(INPUT_PATH, OUTPUT_PATH)
