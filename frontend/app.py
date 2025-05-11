
import streamlit as st
from app_streamlit_single import run_single_predict_app
from app_streamlit_batch import run_batch_predict_app
from app_cluster_single import run_single_cluster_app
from app_cluster_batch import run_batch_cluster_app

st.set_page_config(page_title="ML App - Prédictions étudiantes", layout="centered")

st.sidebar.title("🏠 Menu")
page = st.sidebar.radio("Choisir une page :", [
    "Accueil",
    "Prédiction individuelle",
    "Prédiction batch",
    "Clustering individuel",
    "Clustering batch"
])

if page == "Accueil":
    st.title("🚀 Application de prédiction de réussite étudiante")
    st.markdown("""
    Bienvenue sur cette application développée avec **Streamlit**, **FastAPI** et **Machine Learning** 🤖

    ### Fonctionnalités disponibles
    - 📊 Prédiction individuelle via formulaire interactif
    - 📂 Prédiction batch avec import de fichier CSV
    - 🧩 Clustering des étudiants
    - 🔗 Appels à une API FastAPI en local
    """)

elif page == "Prédiction individuelle":
    run_single_predict_app()

elif page == "Prédiction batch":
    run_batch_predict_app()

elif page == "Clustering individuel":
    run_single_cluster_app()

elif page == "Clustering batch":
    run_batch_cluster_app()
