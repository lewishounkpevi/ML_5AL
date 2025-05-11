#!/bin/bash

echo ""
echo "🔍 Détection de la version de Docker Compose..."
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
elif docker-compose version &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    echo "❌ Docker Compose n'est pas installé."
    exit 1
fi

echo "✅ Commande détectée : $COMPOSE_CMD"

echo ""
echo "🔧 Choisissez le mode de lancement :"
echo "1️⃣  Lancer l'API en local (uvicorn)"
echo "2️⃣  Lancer uniquement l'API avec Docker"
echo "3️⃣  Lancer l'ensemble (API + Streamlit) avec Docker Compose"
echo ""

read -p "➡️  Entrez 1, 2 ou 3 : " choice

if [ "$choice" == "1" ]; then
    echo ""
    echo "🚀 Lancement de FastAPI en local..."
    uvicorn app.main:app --reload

elif [ "$choice" == "2" ]; then
    echo ""
    echo "🐳 Construction de l'image Docker pour l'API..."
    docker build -f Dockerfile_api_full -t ml-fastapi-api .

    echo "🚀 Lancement de l'API sur le port 8000..."
    docker run -p 8000:8000 ml-fastapi-api

elif [ "$choice" == "3" ]; then
    echo ""
    echo "🔄 Lancement avec Docker Compose..."
    $COMPOSE_CMD up --build

else
    echo "❌ Option invalide. Choisissez 1, 2 ou 3."
    exit 1
fi
