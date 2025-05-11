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
echo "1️⃣  Lancer l'API FastAPI en local (uvicorn)"
echo "2️⃣  Lancer uniquement l'API avec Docker"
echo "3️⃣  Lancer l'ensemble (API + Streamlit) avec Docker Compose"
echo "4️⃣  Arrêter tous les services Docker Compose"
echo "5️⃣  Redémarrer tous les services avec cache (mode détaché)"
echo ""

read -p "➡️  Entrez 1, 2, 3, 4 ou 5 : " choice

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
    echo "🔄 Lancement avec Docker Compose (API + Frontend)..."
    $COMPOSE_CMD up --build

elif [ "$choice" == "4" ]; then
    echo ""
    echo "🛑 Arrêt de Docker Compose et nettoyage..."
    $COMPOSE_CMD down --remove-orphans

elif [ "$choice" == "5" ]; then
    echo ""
    echo "♻️ Redémarrage complet avec cache (mode détaché)..."
    $COMPOSE_CMD down --remove-orphans
    $COMPOSE_CMD up --build -d
    echo ""
    echo "📡 Accès rapide :"
    echo "  🧠 API       → http://localhost:8000/docs"
    echo "  📊 Frontend  → http://localhost:8501"

else
    echo "❌ Option invalide. Choisissez 1 à 5."
    exit 1
fi
