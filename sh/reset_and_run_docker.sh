#!/bin/bash

echo "🧹 Nettoyage des conteneurs existants..."
docker compose down --remove-orphans

echo "🔨 Reconstruction complète sans cache..."
docker compose build --no-cache

echo "🚀 Lancement de l'application (API + Frontend)..."
docker compose up
