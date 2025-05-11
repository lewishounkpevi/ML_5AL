import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Chargement dynamique des variables d'environnement
env_path = ".env" if os.path.exists(".env") else "../.env"
# env_path = ".env" if os.path.exists(".env") else "../.env"

load_dotenv(dotenv_path=env_path)

API_URL = os.getenv("API_URL_CLUSTER_BATCH", "http://localhost:8000/cluster_batch")

def run_batch_cluster_app():
    st.title("🧩 Clustering batch d'étudiants")
    st.sidebar.markdown(f"🌐 API utilisée : `{API_URL}`")
    st.markdown("""
    Importez un fichier **CSV** contenant les colonnes de notes pour prédire les **clusters** de plusieurs étudiants.
    """)

    uploaded_file = st.file_uploader("📂 Choisir un fichier CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Aperçu des données importées :", df.head())

        grade_cols = [
            "Grade_Math", "Grade_Programming", "Grade_Algorithms",
            "Grade_Databases", "Grade_Software_Engineering"
        ]

        if not all(col in df.columns for col in grade_cols):
            st.error("❌ Fichier invalide. Il manque certaines colonnes de notes.")
            return

        df_valid = df.dropna(subset=grade_cols).copy()

        payload = df_valid[grade_cols].rename(columns={
            "Grade_Math": "grade_math",
            "Grade_Programming": "grade_programming",
            "Grade_Algorithms": "grade_algorithms",
            "Grade_Databases": "grade_databases",
            "Grade_Software_Engineering": "grade_software_engineering"
        }).to_dict(orient="records")

        if st.button("🔎 Lancer le clustering"):
            try:
                response = requests.post(API_URL, json=payload)
                response.raise_for_status()
                clusters = response.json()

                df_valid["Cluster"] = clusters
                df_final = df.merge(df_valid[["Cluster"]], left_index=True, right_index=True, how="left")

                st.success("✅ Clustering effectué avec succès !")
                st.write(df_final.head())

                csv_out = df_final.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Télécharger le fichier avec clusters", data=csv_out, file_name="cluster_results.csv", mime="text/csv")

            except Exception as e:
                st.error(f"❌ Erreur lors de l'appel à l'API : {e}")
