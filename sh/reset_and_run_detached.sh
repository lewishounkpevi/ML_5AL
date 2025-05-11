#!/bin/bash

echo "🔧 Arrêt et nettoyage des conteneurs..."
docker compose down --remove-orphans

echo ""
echo "🧱 Reconstruction complète sans cache..."
docker compose build --no-cache

echo ""
echo "🚀 Lancement en arrière-plan (mode détaché)..."
docker compose up -d

echo ""
echo "📡 Accès local :"
echo "  🧠 API       → http://localhost:8000/docs"
echo "  📊 Frontend  → http://localhost:8501"
