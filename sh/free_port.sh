#!/bin/bash

PORT=8000

echo "🔍 Recherche du processus utilisant le port $PORT..."
PID=$(sudo lsof -ti tcp:$PORT)

if [ -n "$PID" ]; then
  echo "⚙️ Processus détecté (PID=$PID). Tentative de kill..."
  kill -9 $PID
  echo "✅ Port $PORT libéré."
else
  echo "ℹ️ Aucun processus n'utilise le port $PORT (ou non détectable avec lsof)."
  echo "🔁 Tentative de libération avec fuser..."
  sudo fuser -k ${PORT}/tcp && echo "✅ Port $PORT libéré avec fuser."
fi
