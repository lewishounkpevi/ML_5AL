#!/bin/bash

echo "🛑 Arrêt des services Docker Compose..."
docker compose down --remove-orphans

echo "✅ Tous les conteneurs ont été arrêtés proprement."
