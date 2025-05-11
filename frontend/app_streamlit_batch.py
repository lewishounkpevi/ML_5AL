import streamlit as st
import pandas as pd
import requests
import os

from dotenv import load_dotenv

# ✅ Chargement dynamique du bon fichier .env
env_path = ".env" if os.path.exists(".env") else "../.env"
load_dotenv(dotenv_path=env_path)

API_URL = os.getenv("API_URL_BATCH", "http://localhost:8000/predict_batch")

def run_batch_predict_app():
    # st.set_page_config(page_title="Prédiction étudiante en batch", layout="centered")
    st.title("🎓 Prédictions de réussite étudiante (batch)")
    st.sidebar.markdown(f"🔗 API utilisée (batch) : `{API_URL}`")



    
    # API_URL = "http://localhost:8000/predict_batch"

    uploaded_file = st.file_uploader("📂 Importez un fichier CSV contenant les étudiants :", type="csv")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("Fichier chargé avec succès !")

            if st.button("🔢 Lancer la prédiction"):
                with st.spinner("Appel à l'API en cours..."):
                    payload = [
                        {
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
                        }
                        for _, row in df.iterrows()
                    ]

                    try:
                        response = requests.post(API_URL, json=payload)
                        response.raise_for_status()
                        results = response.json()

                        df["Prediction"] = [r["prediction"] for r in results]
                        df["Probability"] = [r["probability"] for r in results]

                        st.success("Prédiction réussie !")
                        st.dataframe(df.head())

                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button("📁 Télécharger les résultats", csv, "predictions_result.csv", "text/csv")

                    except Exception as e:
                        st.error(f"Erreur lors de l'appel API : {e}")

        except Exception as file_error:
            st.error(f"Erreur de lecture du fichier : {file_error}")
