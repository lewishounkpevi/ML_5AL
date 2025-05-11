#!/bin/bash

# Activer l'environnement virtuel si besoin
# source venv/bin/activate

# Aller dans le dossier frontend
cd frontend || exit

# Lancer l'application Streamlit
streamlit run app.py
