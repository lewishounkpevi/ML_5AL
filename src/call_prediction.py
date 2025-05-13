import requests
import pandas as pd
import time
import os

API_URL = "http://localhost:8000/predict"


def call_prediction_api(data):
    try:
        print("\n📤 Données envoyées :", data)
        response = requests.post(API_URL, json=data)
        response.raise_for_status()
        result = response.json()
        print(
            f"✅ Prédiction : {result['prediction']} ({round(result['probability']* 100, 2)}%)"
        )
        return {
            "prediction": result["prediction"],
            "probability": round(result["probability"] * 100, 2),
        }
    except requests.exceptions.RequestException as e:
        print("❌ Erreur lors de l’appel API :", e)
        return {"prediction": None, "probability": None}


def predict_from_csv(csv_path, output_path="predictions.csv"):
    df = pd.read_csv(csv_path)
    results = []

    for index, row in df.iterrows():
        try:
            payload = {
                "age": int(row["Age"]),
                "student_income": float(row["Student_Income_EUR"]),
                "parent_income": float(row["Parent_Income_EUR"]),
                "academic_year": int(row["Academic_Year"]),
                "region": row["Region"],
                "residence_type": row["Residence_Type"],
                "gender": row["Gender"],
                "grade_math": float(row["Grade_Math"]),
                "grade_programming": float(row["Grade_Programming"]),
                "grade_algorithms": float(row["Grade_Algorithms"]),
                "grade_databases": float(row["Grade_Databases"]),
                "grade_software_engineering": float(row["Grade_Software_Engineering"]),
            }

            result = call_prediction_api(payload)
            results.append(result)
            print(
                f"[{index+1}/{len(df)}] ✅ {result['prediction']} ({round(result['probability']*100, 2)}%)"
            )
            time.sleep(0.1)  # Pour éviter de spammer l'API
        except Exception as row_error:
            print(f"⚠️ Erreur ligne {index+1} : {row_error}")
            results.append({"prediction": None, "probability": None})

    # Fusion des résultats
    results_df = pd.DataFrame(results)
    final_df = pd.concat([df, results_df], axis=1)
    final_df.to_csv(output_path, index=False)
    print(f"📄 Résultats enregistrés dans {output_path}")


def predict_and_save_csv(
    csv_path, output_dir="outputs", output_name="predictions_result.csv"
):
    # Créer le dossier si besoin
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_name)

    df = pd.read_csv(csv_path)
    results = []

    for index, row in df.iterrows():
        payload = {
            "age": int(row["Age"]),
            "student_income": float(row["Student_Income_EUR"]),
            "parent_income": float(row["Parent_Income_EUR"]),
            "academic_year": int(row["Academic_Year"]),
            "region": row["Region"],
            "residence_type": row["Residence_Type"],
            "gender": row["Gender"],
            "grade_math": float(row["Grade_Math"]),
            "grade_programming": float(row["Grade_Programming"]),
            "grade_algorithms": float(row["Grade_Algorithms"]),
            "grade_databases": float(row["Grade_Databases"]),
            "grade_software_engineering": float(row["Grade_Software_Engineering"]),
        }

        result = call_prediction_api(payload)
        results.append(result)
        print(
            f"[{index+1}/{len(df)}] ✅ {result['prediction']} ({result['probability']}%)"
        )
        time.sleep(0.05)

    df["Prediction"] = [r["prediction"] for r in results]
    df["Probability"] = [r["probability"] for r in results]

    df.to_csv(output_path, index=False)
    print(f"📁 Résultats sauvegardés dans : {output_path}")


if __name__ == "__main__":
    # Prédiction individuelle
    sample = {
        "age": 22,
        "student_income": 500,
        "parent_income": 2000,
        "academic_year": 2022,
        "region": "Île-de-France",
        "residence_type": "Urban",
        "gender": "Male",
        "grade_math": 9,
        "grade_programming": 1,
        "grade_algorithms": 13,
        "grade_databases": 2,
        "grade_software_engineering": 3,
    }

    print("🔍 Prédiction individuelle :")
    call_prediction_api(sample)

    # Prédictions batch (optionnel)
    # print("\n📊 Prédictions batch à partir du fichier CSV...")

    # Appel avec sauvegarde dans dossier outputs/
    # predict_and_save_csv("src/data/students_dataset.csv")

    # predict_from_csv("src/data/students_dataset.csv")
