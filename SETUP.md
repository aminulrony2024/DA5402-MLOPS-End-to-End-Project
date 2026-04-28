# FinPredict — Setup & Run Guide

## Prerequisites
- Docker Desktop installed and running
- Git installed
- At least 4GB RAM available

---

## Step 1 — Place Your Dataset
Copy your dataset into the project:
```
FinPredict/data/raw/Loan_Dataset.csv
```

---

## Step 2 — Initialize Git + DVC
```bash
cd FinPredict
git init
git add .
git commit -m "Initial commit"

pip install dvc
dvc init
dvc add data/raw/Loan_Dataset.csv
git add data/raw/Loan_Dataset.csv.dvc .gitignore
git commit -m "Track dataset with DVC"
```

---

## Step 3 — Run Preprocessing (First Time)
Before starting Docker, preprocess your data locally:
```bash
pip install -r backend/requirements.txt
python mlops/training/preprocess.py
```

---

## Step 4 — Start All Services
```bash
docker-compose up --build
```

This starts:
| Service    | URL                   |
|------------|-----------------------|
| Frontend   | http://localhost:3002 |
| Backend    | http://localhost:8000 |
| MLflow     | http://localhost:5000 |
| Airflow    | http://localhost:8080 |
| Prometheus | http://localhost:9090 |
| Grafana    | http://localhost:3001 |

---

## Step 5 — Run Experiments and Register Model
```bash
# Run all 3 experiments
python mlops/experiments/logistic_regression.py
python mlops/experiments/random_forest.py
python mlops/experiments/xgboost_model.py

# Register best model to Production
python mlops/registry/register_model.py
```

---

## Step 6 — Run Unit Tests
```bash
cd backend
pytest tests/ -v
```

---

## Step 7 — Run Airflow Pipeline
1. Open http://localhost:8080
2. Default credentials: admin / admin
3. Enable the `finpredict_data_pipeline` DAG
4. Trigger it manually or wait for the daily schedule

---

## Step 8 — View Monitoring
- **Prometheus**: http://localhost:9090 → query `finpredict_predictions_total`
- **Grafana**: http://localhost:3001 → import `monitoring/grafana/dashboard.json`

---

## DVC Pipeline (CI)
Run the full pipeline reproducibly:
```bash
cd dvc
dvc repro
```

View the DAG:
```bash
dvc dag
```

---

## Stopping Services
```bash
docker-compose down
```
