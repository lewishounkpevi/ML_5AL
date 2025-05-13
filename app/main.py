from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import os
from typing import List
from datetime import datetime
from app.schema import StudentInput, PredictionOutput
from app.schema import ClusteringInput, ClusteringOutput


from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Request
from fastapi.responses import Response
import time

app = FastAPI()

BASE_DIR = os.path.dirname(__file__)

model = joblib.load(os.path.join(BASE_DIR, "models/model.joblib"))
preprocessor = joblib.load(os.path.join(BASE_DIR, "models/preprocessor.joblib"))
label_encoder = joblib.load(os.path.join(BASE_DIR, "models/label_encoder.joblib"))


@app.get("/")
def read_root():
    return {"message": "API prédictive - Réussite Étudiante 🎓"}


@app.post("/predict", response_model=PredictionOutput)
def predict(data: StudentInput):
    try:
        input_df = pd.DataFrame([data.dict()])
        print("📥 Données reçues :", input_df.to_dict(orient="records")[0])

        # 1. Renommage
        column_mapping = {
            "age": "Age",
            "student_income": "Student_Income_EUR",
            "parent_income": "Parent_Income_EUR",
            "academic_year": "Academic_Year",
            "region": "Region",
            "residence_type": "Residence_Type",
            "gender": "Gender",
            "grade_math": "Grade_Math",
            "grade_programming": "Grade_Programming",
            "grade_algorithms": "Grade_Algorithms",
            "grade_databases": "Grade_Databases",
            "grade_software_engineering": "Grade_Software_Engineering",
        }
        input_df = input_df.rename(columns=column_mapping)

        # 2. Calcul de la moyenne si nécessaire
        if "Average_Grade" in preprocessor.feature_names_in_:
            input_df["Average_Grade"] = input_df[
                [
                    "Grade_Math",
                    "Grade_Programming",
                    "Grade_Algorithms",
                    "Grade_Databases",
                    "Grade_Software_Engineering",
                ]
            ].mean(axis=1)

        # 3. Transformation + prédiction
        X = preprocessor.transform(input_df)
        print("✅ Données transformées :", X.shape)

        prediction_encoded = model.predict(X)[0]
        probability = model.predict_proba(X)[0].max()
        prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]

        return PredictionOutput(
            prediction=prediction_label, probability=round(probability, 4)
        )

    except Exception as e:
        print("❌ ERREUR INTERNE :", e)
        return PredictionOutput(prediction=None, probability=None)


from typing import List


@app.post("/predict_batch")
def predict_batch(data: List[StudentInput]):
    try:
        input_df = pd.DataFrame([d.dict() for d in data])

        # Mapping des colonnes vers noms attendus
        column_mapping = {
            "age": "Age",
            "student_income": "Student_Income_EUR",
            "parent_income": "Parent_Income_EUR",
            "academic_year": "Academic_Year",
            "region": "Region",
            "residence_type": "Residence_Type",
            "gender": "Gender",
            "grade_math": "Grade_Math",
            "grade_programming": "Grade_Programming",
            "grade_algorithms": "Grade_Algorithms",
            "grade_databases": "Grade_Databases",
            "grade_software_engineering": "Grade_Software_Engineering",
        }
        input_df = input_df.rename(columns=column_mapping)

        # Recalcul de la moyenne si nécessaire
        if "Average_Grade" in preprocessor.feature_names_in_:
            input_df["Average_Grade"] = input_df[
                [
                    "Grade_Math",
                    "Grade_Programming",
                    "Grade_Algorithms",
                    "Grade_Databases",
                    "Grade_Software_Engineering",
                ]
            ].mean(axis=1)

        # Transformation
        X = preprocessor.transform(input_df)
        predictions = model.predict(X)
        probabilities = model.predict_proba(X).max(axis=1)
        decoded = label_encoder.inverse_transform(predictions)

        return [
            {"prediction": pred, "probability": round(prob, 4)}
            for pred, prob in zip(decoded, probabilities)
        ]

    except Exception as e:
        print("❌ ERREUR BATCH :", e)
        return []


print("✅ Modèles chargés depuis :", BASE_DIR)

# Chargement du modèle de clustering
# BASE_DIR = os.path.dirname(__file__)
CLUSTER_MODEL_PATH = os.path.join(BASE_DIR, "models/cluster_model.joblib")
CLUSTER_SCALER_PATH = os.path.join(BASE_DIR, "models/cluster_scaler.joblib")

if os.path.exists(CLUSTER_MODEL_PATH) and os.path.exists(CLUSTER_SCALER_PATH):
    cluster_model = joblib.load(CLUSTER_MODEL_PATH)
    cluster_scaler = joblib.load(CLUSTER_SCALER_PATH)
else:
    cluster_model = None
    cluster_scaler = None

# Colonnes normalisées utilisées pendant l'entraînement
GRADE_COLUMNS = [
    "Grade_Math",
    "Grade_Programming",
    "Grade_Algorithms",
    "Grade_Databases",
    "Grade_Software_Engineering",
]


@app.post("/cluster", response_model=ClusteringOutput)
def predict_cluster(data: ClusteringInput):
    try:
        input_df = pd.DataFrame([data.dict()])
        print("📥 Données reçues :", input_df.to_dict(orient="records")[0])

        # Renommage des colonnes
        input_df.columns = GRADE_COLUMNS

        features_scaled = cluster_scaler.transform(input_df)
        cluster_id = int(cluster_model.predict(features_scaled)[0])

        return ClusteringOutput(cluster=cluster_id)

    except Exception as e:
        print("❌ ERREUR CLUSTERING :", e)
        return ClusteringOutput(cluster=None)


@app.post("/cluster_batch", response_model=List[int])
def predict_cluster_batch(data: List[ClusteringInput]):
    try:
        df = pd.DataFrame([d.dict() for d in data])
        print(f"📥 Batch reçu : {len(df)} entrées")

        # Renommage des colonnes
        df.columns = GRADE_COLUMNS

        features_scaled = cluster_scaler.transform(df)
        clusters = cluster_model.predict(features_scaled)

        return clusters.tolist()

    except Exception as e:
        print("❌ ERREUR CLUSTERING BATCH :", e)
        return []


# 🔢 Métriques Prometheus
REQUEST_COUNT = Counter(
    "app_requests_total", "Total API Requests", ["method", "endpoint"]
)
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", "Latency of requests in seconds", ["endpoint"]
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    endpoint = request.url.path
    REQUEST_COUNT.labels(method=request.method, endpoint=endpoint).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(process_time)

    return response


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type="text/plain")
