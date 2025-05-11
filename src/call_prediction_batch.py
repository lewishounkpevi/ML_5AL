import requests
import pandas as pd
import os

API_URL = "http://localhost:8000/predict_batch"

def predict_batch_from_csv(csv_path, output_dir="outputs", output_name="predictions_result.csv"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_name)

    df = pd.read_csv(csv_path)

    payload = []
    for _, row in df.iterrows():
        payload.append({
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
            "grade_software_engineering": float(row["Grade_Software_Engineering"])
        })

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        predictions = response.json()

        df["Prediction"] = [p["prediction"] for p in predictions]
        df["Probability"] = [p["probability"] for p in predictions]

        df.to_csv(output_path, index=False)
        print(f"✅ Prédictions sauvegardées dans : {output_path}")
    except Exception as e:
        print("❌ Erreur lors de l'appel batch à l'API :", e)

if __name__ == "__main__":
    predict_batch_from_csv("src/data/students_dataset.csv")
