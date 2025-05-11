import streamlit as st
import requests
import os

from dotenv import load_dotenv

# Chargement dynamique des variables d'environnement
env_path = ".env" if os.path.exists(".env") else "../.env"
# env_path = ".env" if os.path.exists(".env") else "../.env"

load_dotenv(dotenv_path=env_path)

API_URL = os.getenv("API_URL_CLUSTER", "http://localhost:8000/cluster")

def run_single_cluster_app():
    st.title("🧩 Clustering d'un étudiant")
    st.sidebar.markdown(f"🌐 API utilisée : `{API_URL}`")
    st.markdown("""
    Entrez les notes ci-dessous pour prédire à quel **cluster** appartient cet étudiant.
    """)

    with st.form("cluster_form"):
        grade_math = st.number_input("Note en Mathématiques", 0.0, 20.0, step=0.1)
        grade_programming = st.number_input("Note en Programmation", 0.0, 20.0, step=0.1)
        grade_algorithms = st.number_input("Note en Algorithmes", 0.0, 20.0, step=0.1)
        grade_databases = st.number_input("Note en Bases de données", 0.0, 20.0, step=0.1)
        grade_software_engineering = st.number_input("Note en Génie logiciel", 0.0, 20.0, step=0.1)

        submitted = st.form_submit_button("🔎 Prédire le cluster")

    if submitted:
        payload = {
            "grade_math": grade_math,
            "grade_programming": grade_programming,
            "grade_algorithms": grade_algorithms,
            "grade_databases": grade_databases,
            "grade_software_engineering": grade_software_engineering
        }

        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            result = response.json()

            if result["cluster"] is not None:
                st.success(f"✅ L'étudiant appartient au cluster : {result['cluster']}")
            else:
                st.error("❌ Impossible de déterminer le cluster.")

        except Exception as e:
            st.error(f"❌ Erreur lors de l'appel à l'API : {e}")
