#!/bin/bash

# Récupérer l'adresse IP de WSL
WSL_IP=$(hostname -I | awk '{print $1}')

echo "�� Adresse IP de WSL détectée : $WSL_IP"

# Vérifier l'accès à l'API FastAPI
echo "\n🔍 Vérification de l'API (FastAPI) : http://$WSL_IP:8000/docs"
curl --silent --head http://$WSL_IP:8000/docs | grep HTTP || echo "❌ API FastAPI inaccessible"

# Vérifier l'accès à Streamlit
echo "\n🔍 Vérification du frontend (Streamlit) : http://$WSL_IP:8501"
curl --silent --head http://$WSL_IP:8501 | grep HTTP || echo "❌ Frontend Streamlit inaccessible"

# Conseils si erreur
echo "\n💡 Si vous voyez des erreurs ci-dessus :"
echo "- Assurez-vous que docker compose est bien lancé : docker compose up"
echo "- Vérifiez que les ports 8000 et 8501 sont exposés dans docker-compose.yml"
echo "- Si vous êtes sous WSL, utilisez l'IP WSL dans votre navigateur : http://$WSL_IP:8501"

