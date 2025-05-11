import requests

API_URL = "http://localhost:8000/cluster"

sample = {
    "grade_math": 12.5,
    "grade_programming": 14.0,
    "grade_algorithms": 13.5,
    "grade_databases": 15.0,
    "grade_software_engineering": 16.0
}

def call_cluster_api(data):
    try:
        response = requests.post(API_URL, json=data)
        response.raise_for_status()
        result = response.json()
        return {"cluster": result.get("cluster")}
    except requests.exceptions.RequestException as e:
        print("❌ Erreur lors de l’appel API :", e)
        return {"cluster": None}

if __name__ == "__main__":
    print("🔍 Prédiction du cluster pour l'étudiant :")
    result = call_cluster_api(sample)
    print("🧠 Cluster prédit :", result["cluster"])
