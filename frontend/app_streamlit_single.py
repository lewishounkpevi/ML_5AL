import streamlit as st
import requests
import os
from dotenv import load_dotenv

# ✅ Chargement dynamique du bon fichier .env
env_path = ".env" if os.path.exists(".env") else "../.env"
load_dotenv(dotenv_path=env_path)


API_URL = os.getenv("API_URL_PREDICT", "http://localhost:8000/predict")
print(f"🔍 API_URL_PREDICT utilisé : {API_URL}")

def run_single_predict_app():
    st.title("👩‍🏫 Prédiction de réussite d'un étudiant")
    st.sidebar.markdown(f"🌐 API utilisée : `{API_URL}`")

    with st.form("student_form"):
        age = st.slider("👶 Âge", 17, 30, 22)
        academic_year = st.number_input("📅 Année Académique", 2000, 2050, 2024)
        gender = st.selectbox("♂️ Genre", ["Male", "Female"])
        region = st.selectbox("📍 Région", ["Île-de-France", "Provence-Alpes-Côte d’Azur", "Bretagne", "Normandie"])
        residence_type = st.selectbox("Type de résidence", ["Urban", "Rural"])
        student_income = st.number_input("💰 Revenu étudiant (€)", min_value=0.0, value=400.0)
        parent_income = st.number_input("🏠 Revenu parental (€)", min_value=0.0, value=2500.0)

        st.markdown("### 📚 Notes")
        grade_math = st.slider("Maths", 0.0, 20.0, 12.0)
        grade_programming = st.slider("Programmation", 0.0, 20.0, 14.0)
        grade_algorithms = st.slider("Algorithmes", 0.0, 20.0, 13.0)
        grade_databases = st.slider("Bases de données", 0.0, 20.0, 11.0)
        grade_se = st.slider("Génie logiciel", 0.0, 20.0, 15.0)

        submitted = st.form_submit_button("🔢 Prédire")

    if submitted:
        payload = {
            "age": age,
            "student_income": student_income,
            "parent_income": parent_income,
            "academic_year": academic_year,
            "region": region,
            "residence_type": residence_type,
            "gender": gender,
            "grade_math": grade_math,
            "grade_programming": grade_programming,
            "grade_algorithms": grade_algorithms,
            "grade_databases": grade_databases,
            "grade_software_engineering": grade_se
        }

        with st.spinner("Appel à l'API..."):
            try:
                response = requests.post(API_URL, json=payload)
                response.raise_for_status()
                result = response.json()

                pred = result["prediction"]
                proba = result["probability"] * 100

                if pred == "Success":
                    st.success(f"✅ Réussite prévue ({proba:.2f}%)")
                else:
                    st.error(f"❌ Échec prévu ({proba:.2f}%)")

            except Exception as e:
                st.error(f"Erreur lors de l'appel API : {e}")
