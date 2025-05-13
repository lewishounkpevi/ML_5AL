# 🧠 ESGI Student ML Project

![CI](https://github.com/lewishounkpevi/ML_5AL/actions/workflows/ci.yml/badge.svg)


Un projet complet de Machine Learning déployé via **FastAPI** et **Streamlit**, permettant de :

- 🎯 Prédire la réussite ou l'échec d'un étudiant
- 🧩 Classer les étudiants dans des clusters selon leurs performances académiques
- 🐳 Déployer facilement en local ou avec Docker Compose

---

## 📁 Structure du projet

```
├── app/                        # Backend FastAPI
│   ├── main.py                # API principale
│   ├── model.joblib           # Modèle de classification
│   ├── cluster_model.joblib   # Modèle de clustering
│   ├── cluster_scaler.joblib  # Scaler pour clustering
│   └── ...
├── frontend/                  # Interface utilisateur Streamlit
│   ├── app.py                 # Point d'entrée
│   ├── app_streamlit_single.py
│   ├── app_streamlit_batch.py
│   ├── app_cluster_single.py
│   ├── app_cluster_batch.py
├── outputs/                   # Fichiers CSV enrichis (prédictions / clusters)
├── requirements.txt           # Dépendances Python
├── Dockerfile_api_full        # Image Docker pour FastAPI
├── Dockerfile_frontend        # Image Docker pour Streamlit
├── docker-compose.yml         # Orchestration multi-conteneur
├── .env                       # Variables d'environnement (API URLs)
└── orchestrator.sh            # Script interactif pour tout lancer
```

---

## ⚙️ Installation manuelle (mode local)

```bash
# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer FastAPI (backend)
uvicorn app.main:app --reload

# Lancer Streamlit (frontend)
cd frontend
streamlit run app.py
```

Assurez-vous d'avoir un fichier `.env` dans `frontend/` pour local :
```env
API_URL_PREDICT=http://localhost:8000/predict
API_URL_BATCH=http://localhost:8000/predict_batch
API_URL_CLUSTER=http://localhost:8000/cluster
API_URL_CLUSTER_BATCH=http://localhost:8000/cluster_batch
```

---

## 🐳 Déploiement Docker

```bash
# Lancer toute l'application avec Docker Compose
./run_compose.sh

# Ou redémarrer sans no-cache (avec cache)
./restart_compose_cached.sh
```

Accès :
- API docs 👉 http://localhost:8000/docs
- Interface Streamlit 👉 http://localhost:8501

---

## 🧪 Fonctionnalités principales

### 🔹 Prédiction individuelle (via Streamlit ou API)
- Formulaire complet : âge, revenu, région, notes, etc.
- Résultat : `Success` / `Failure` + probabilité

### 🔹 Prédiction batch (CSV → CSV)
- Upload CSV avec étudiants
- API retourne les colonnes : `Prediction`, `Probability`

### 🔹 Clustering individuel
- Entrée : 5 notes
- Sortie : numéro de cluster (KMeans, Silhouette, etc.)

### 🔹 Clustering batch (CSV → CSV)
- Upload CSV avec notes
- Retourne une colonne `Cluster`

---

## 📦 API (FastAPI)

- `/predict` : prédiction individuelle
- `/predict_batch` : prédiction CSV
- `/cluster` : clustering individuel
- `/cluster_batch` : clustering CSV

👉 Documentation auto : http://localhost:8000/docs

---

## 🔐 Bonnes pratiques MLOps

- 🔄 Pipeline `preprocess → predict` en production
- ✅ Validation Pydantic des entrées API
- 🔍 Tracking des erreurs et logs (`print`, `try/except`)
- 🐳 Conteneurisation complète + réseau isolé `ml_net`
- 📁 `.env` séparé pour Docker et local (frontend/.env)

---

## 🧰 Scripts utiles

```bash
./orchestrator.sh              # Menu interactif (local, docker, compose...)
./run_compose.sh               # Build & run complet
./restart_compose_cached.sh    # Restart rapide avec cache
./stop_compose.sh              # Stop tous les services
./status_compose.sh            # Affiche les conteneurs
```

---

## 🧑‍🏫 Auteurs

Projet pédagogique réalisé dans le cadre du Master 2 - ESGI 5AL1 - Machine Learning

---

## ✅ À faire / Améliorations possibles

- [ ] Ajout d’une base de données pour persister les prédictions
- [ ] Dashboard analytique en plus de Streamlit
- [ ] CI/CD avec GitHub Actions
- [ ] Monitoring (Prometheus / Grafana ?)

---

🚀 Let's deploy some ML!
