#!/bin/bash

echo "♻️ Redémarrage de Docker Compose (avec cache)..."

echo ""
echo "🚀 Redémarrage avec build en cache..."
docker compose up --build -d

echo ""
echo "📡 Services accessibles :"
echo "  🧠 API       → http://localhost:8000/docs"
echo "  📊 Frontend  → http://localhost:8501"
