# 💰 FinPredict — Intelligent Loan Approval System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![React](https://img.shields.io/badge/React-18.2-blue)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0.1-orange)
![MLflow](https://img.shields.io/badge/MLflow-2.19.0-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![DVC](https://img.shields.io/badge/DVC-Data%20Versioning-purple)
![Airflow](https://img.shields.io/badge/Airflow-2.7.0-red)

> An AI-powered loan approval prediction system built with full MLOps best practices.
> Predicts loan approval or rejection based on 24 applicant features using XGBoost,
> served via FastAPI, monitored with Prometheus + Grafana, and orchestrated with Airflow.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Services and Ports](#-services-and-ports)
- [Quick Start](#-quick-start)
- [Data Versioning with DVC](#-data-versioning-with-dvc)
- [ML Experiments with MLflow](#-ml-experiments-with-mlflow)
- [Airflow Pipeline](#-airflow-pipeline)
- [Monitoring and Alerting](#-monitoring-and-alerting)
- [API Endpoints](#-api-endpoints)
- [Running Tests](#-running-tests)
- [Documentation](#-documentation)

---

## 🎯 Project Overview

FinPredict addresses the problem of **manual and inefficient loan approval processes**
in financial institutions which often lead to delays and inconsistent decisions.

The system uses an XGBoost classifier trained on **52,000 loan records** to predict
whether a loan should be approved or rejected based on applicant data such as income,
credit history, loan amount, and 21 other features.

| ML Metric   | Value  |
|-------------|--------|
| Accuracy    | 85.02% |
| F1-Score    | 88.84% |
| ROC-AUC     | 81.88% |
| Latency     | < 50ms |

---

## 🛠 Tech Stack

| Component              | Technology                        |
|------------------------|-----------------------------------|
| Frontend               | React.js 18.2                     |
| Backend API            | FastAPI 0.104.1 + Uvicorn         |
| ML Model               | XGBoost 2.0.1                     |
| Experiment Tracking    | MLflow 2.19.0                     |
| Pipeline Orchestration | Apache Airflow 2.7.0              |
| Data Versioning        | DVC                               |
| Containerization       | Docker + Docker Compose           |
| Monitoring             | Prometheus + Grafana              |
| Alerting               | Alertmanager → Gmail              |
| Source Control         | Git + DVC                         |
| Environment Parity     | MLproject + conda.yaml            |

---

## 📁 Project Structure

```
FinPredict/
│
├── 📁 .dvc/                          # DVC configuration
│   └── config                        # DVC remote settings
│
├── 📁 airflow/
│   └── Dockerfile                    # Custom Airflow image with ML dependencies
│
├── 📁 backend/                       # FastAPI inference backend
│   ├── 📁 api/
│   │   ├── 📁 middleware/
│   │   │   ├── __init__.py
│   │   │   └── cors.py               # CORS configuration
│   │   ├── 📁 routes/
│   │   │   ├── __init__.py
│   │   │   ├── health.py             # GET /health, GET /ready
│   │   │   ├── pipeline.py           # GET /api/v1/pipeline/status
│   │   │   └── predict.py            # POST /api/v1/predict + drift detection
│   │   ├── 📁 schemas/
│   │   │   ├── __init__.py
│   │   │   ├── request.py            # LoanApplication Pydantic schema (24 fields)
│   │   │   └── response.py           # PredictionResponse schema (6 fields)
│   │   ├── __init__.py
│   │   └── main.py                   # FastAPI app entry point
│   ├── 📁 model/
│   │   ├── __init__.py
│   │   ├── loader.py                 # Load model from MLflow registry
│   │   ├── predictor.py              # LoanPredictor class (singleton)
│   │   └── preprocessor.py          # Feature encoding + engineering pipeline
│   ├── 📁 monitoring/
│   │   ├── __init__.py
│   │   └── metrics.py               # Prometheus metrics (Counter, Histogram, Gauge)
│   ├── 📁 tests/
│   │   ├── __init__.py
│   │   ├── test_health.py            # TC01, TC02 — health endpoint tests
│   │   ├── test_predict.py           # TC03–TC06 — prediction endpoint tests
│   │   └── test_preprocessor.py     # TC07–TC10 — preprocessor unit tests
│   ├── 📁 logs/
│   │   └── app.log                   # Application logs
│   ├── .env                          # Environment variables
│   ├── config.py                     # Configuration loader
│   ├── Dockerfile                    # Backend Docker image
│   └── requirements.txt             # Python dependencies (pydantic v2)
│
├── 📁 data/
│   ├── 📁 raw/
│   │   ├── .gitignore                # DVC-managed — Git ignores the actual CSV
│   │   ├── Loan_Dataset.csv.dvc      # DVC pointer to raw dataset (VERSION 1)
│   │   └── Loan_Dataset.csv          # Original dataset — 52,000 rows, 27 columns
│   ├── 📁 processed/
│   │   ├── .gitignore                # DVC-managed processed files
│   │   ├── train.csv                 # Preprocessed training set — 41,600 rows (VERSION 2)
│   │   └── test.csv                  # Preprocessed test set — 10,400 rows (VERSION 2)
│   └── 📁 features/
│       ├── scaler.pkl                # Fitted StandardScaler
│       └── feature_baseline.json    # Baseline statistics for drift detection
│
├── 📁 dvc/
│   ├── 📁 .dvc/
│   │   └── config                    # DVC config (nested — original location)
│   ├── dvc.yaml                      # DVC pipeline definition (7 stages)
│   └── README.md                     # DVC two-version data explanation
│
├── 📁 frontend/                      # React.js web application
│   ├── 📁 public/
│   │   └── index.html
│   ├── 📁 src/
│   │   ├── 📁 api/
│   │   │   └── apiClient.js          # Axios API client (configurable base URL)
│   │   ├── 📁 components/
│   │   │   ├── LoanForm.jsx          # Main 24-field loan application form
│   │   │   ├── Loader.jsx            # Loading spinner
│   │   │   ├── Navbar.jsx            # Navigation bar
│   │   │   ├── PipelineView.jsx      # Pipeline task status display
│   │   │   └── ResultCard.jsx        # Approved/Rejected result card
│   │   ├── 📁 pages/
│   │   │   ├── Home.jsx              # Landing page
│   │   │   ├── Pipeline.jsx          # Pipeline monitor page
│   │   │   ├── Predict.jsx           # Loan eligibility check page
│   │   │   └── UserManual.jsx        # User manual page
│   │   ├── 📁 styles/
│   │   │   └── main.css              # Global CSS styles
│   │   ├── App.jsx                   # Root component with routing
│   │   └── index.jsx                 # React entry point
│   ├── .env                          # REACT_APP_API_URL=http://localhost:8000
│   ├── Dockerfile                    # Frontend Docker image
│   └── package.json                  # Node dependencies
│
├── 📁 mlflow_data/                   # MLflow persistent storage (Docker volume)
│   └── ...                           # Experiment runs, artifacts, model registry
│
├── 📁 mlops/
│   ├── 📁 data_pipeline/             # Airflow DAG tasks
│   │   ├── __init__.py
│   │   ├── airflow_dag.py            # 7-task DAG definition
│   │   ├── data_ingestion.py         # Task 1 — Load raw CSV
│   │   ├── data_validation.py        # Task 2 — Schema + quality checks
│   │   ├── data_cleaning.py          # Task 3 — Rename, drop, clip outliers
│   │   ├── encode_and_scale.py       # Task 5 — Encoding + StandardScaler
│   │   ├── feature_engineering.py   # Task 4 — Derive ratio features + baselines
│   │   ├── requirements_airflow.txt  # Airflow-specific pip deps (pydantic v1)
│   │   ├── split_data.py             # Task 6 — 80/20 stratified split
│   │   └── trigger_training.py       # Task 7 — Train XGBoost inside Airflow
│   ├── 📁 experiments/
│   │   ├── __init__.py
│   │   ├── logistic_regression.py    # Experiment 1 — Baseline model
│   │   ├── random_forest.py          # Experiment 2 — Ensemble model
│   │   └── xgboost_model.py          # Experiment 3 — Production model + autolog
│   ├── 📁 registry/
│   │   ├── __init__.py
│   │   └── register_model.py         # Promote best model to Production stage
│   ├── 📁 training/
│   │   ├── __init__.py
│   │   ├── evaluate.py               # Evaluate production model, save metrics.json
│   │   ├── preprocess.py             # Standalone preprocessing (no Airflow needed)
│   │   └── train.py                  # XGBoost training script with MLflow logging
│   └── __init__.py
│
├── 📁 mlruns/                        # Local MLflow tracking (auto-generated)
│   └── ...
│
├── 📁 monitoring/
│   ├── 📁 grafana/
│   │   ├── 📁 dashboards/
│   │   │   └── finpredict_dashboard.json   # 6-panel Grafana dashboard
│   │   └── 📁 provisioning/
│   │       ├── 📁 dashboards/
│   │       │   └── dashboards.yml          # Auto-load dashboard config
│   │       └── 📁 datasources/
│   │           └── prometheus.yml          # Auto-connect Prometheus datasource
│   ├── alert_rules.yml               # 4 Prometheus alert rules
│   └── prometheus.yml                # Prometheus scrape config
│
├── .dvcignore                        # DVC ignore rules
├── .gitignore                        # Git ignore rules
├── conda_airflow.yaml                # Conda env for Airflow (pydantic v1)
├── conda.yaml                        # Conda env for backend (pydantic v2)
├── docker-compose.yml                # Orchestrates all 6 services
├── dvc.lock                          # DVC pipeline lock file
├── dvc.yaml                          # DVC pipeline stages (root level)
├── dvc_setup.sh                      # One-time DVC initialization script
├── FinPredict_Project_Report.pdf     # Full project report
├── MLproject                         # MLflow project entry points
├── README.md                         # This file
└── SETUP.md                          # Step-by-step setup guide
```

---

## 🚀 Services and Ports

| Service    | Container Name         | URL                        | Description                    |
|------------|------------------------|----------------------------|--------------------------------|
| Frontend   | finpredict_frontend    | http://localhost:3002       | React.js loan application UI   |
| Backend    | finpredict_backend     | http://localhost:8000       | FastAPI inference engine        |
| MLflow     | finpredict_mlflow      | http://localhost:5000       | Experiment tracking + registry |
| Airflow    | finpredict_airflow     | http://localhost:8080       | Pipeline orchestration UI       |
| Prometheus | finpredict_prometheus  | http://localhost:9090       | Metrics scraping + alerts       |
| Grafana    | finpredict_grafana     | http://localhost:3001       | Real-time monitoring dashboard  |

---

## ⚡ Quick Start

### Prerequisites
- Docker Desktop installed and running
- Python 3.10+ with pip
- Node.js 18+ (only if running frontend locally)
- Git and DVC installed

### Step 1 — Clone and Place Dataset
```bash
git clone https://github.com/aminulrony2024/DA5402-MLOPS-End-to-End-Project
cd FinPredict

# Place dataset
cp /path/to/Loan_Dataset.csv data/raw/Loan_Dataset.csv
```

### Step 2 — Run Preprocessing (First Time Only)
```bash
pip install -r backend/requirements.txt
python mlops/training/preprocess.py
```

### Step 3 — Start All Services
```bash
docker compose up --build
```

### Step 4 — Run ML Experiments
```bash
export MLFLOW_TRACKING_URI=http://localhost:5000

python mlops/experiments/logistic_regression.py
python mlops/experiments/random_forest.py
python mlops/experiments/xgboost_model.py
python mlops/registry/register_model.py
```

### Step 5 — Restart Backend to Load Model
```bash
docker compose restart backend
```

### Step 6 — Open the Application
```
Frontend:  http://localhost:3002
Backend:   http://localhost:8000/docs
MLflow:    http://localhost:5000
Airflow:   http://localhost:8080  (admin / admin)
Grafana:   http://localhost:3001  (admin / admin)
```

---

## 📦 Data Versioning with DVC

Two versions of the dataset are tracked with DVC alongside Git:

| Version | File | Git Tag | Description |
|---------|------|---------|-------------|
| Version 1 (Raw) | `data/raw/Loan_Dataset.csv` | `data-v1-raw` | Original — 52,000 rows, 27 columns |
| Version 2 (Processed) | `data/processed/train.csv` + `test.csv` | `data-v2-processed` | Encoded, scaled, feature engineered |

```bash
# Initialize DVC (first time)
./dvc_setup.sh

# Reproduce full pipeline
dvc repro

# View pipeline DAG
dvc dag

# Switch to raw data version
git checkout data-v1-raw && dvc checkout

# Switch to processed data version
git checkout data-v2-processed && dvc checkout
```

---

## 🔬 ML Experiments with MLflow

Three models were compared. XGBoost was selected as the production model.

| Model               | Accuracy | F1-Score | ROC-AUC |
|---------------------|----------|----------|---------|
| Logistic Regression | ~78%     | ~80%     | ~82%    |
| Random Forest       | ~87%     | ~88%     | ~85%    |
| **XGBoost** ⭐      | **85%**  | **89%**  | **82%** |

```bash
# Run experiments
export MLFLOW_TRACKING_URI=http://localhost:5000
python mlops/experiments/xgboost_model.py

# Register best model to Production
python mlops/registry/register_model.py

# Run via MLproject
mlflow run . -e train
mlflow run . -e train -P n_estimators=300 -P max_depth=8
```

---

## 🔄 Airflow Pipeline

The data engineering pipeline runs as a 7-task Airflow DAG:

```
data_ingestion → data_validation → data_cleaning →
feature_engineering → encode_and_scale →
train_test_split → trigger_training
```

| Task | Description | Output |
|------|-------------|--------|
| data_ingestion | Load raw CSV, check row count | staged.csv |
| data_validation | Schema checks, null detection | Validation log |
| data_cleaning | Rename columns, clip outliers | cleaned.csv |
| feature_engineering | Derive 3 ratio features + baselines | featured.csv |
| encode_and_scale | Encode categoricals + StandardScaler | encoded.csv |
| train_test_split | 80/20 stratified split | train.csv + test.csv |
| trigger_training | Train XGBoost, log to MLflow | Registered model |

**Pipeline Performance:** ~13.4 seconds total for 52,000 records (~3,900 records/second)

---

## 📊 Monitoring and Alerting

### Prometheus Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `finpredict_prediction_latency_seconds` | Histogram | End-to-end prediction latency |
| `finpredict_predictions_total` | Counter | Total predictions (success/error) |
| `finpredict_http_requests_total` | Counter | Total HTTP requests |
| `finpredict_data_drift_score` | Gauge | Real-time data drift score |

### Alert Rules (monitoring/alert_rules.yml)

| Alert | Condition | Severity |
|-------|-----------|----------|
| HighErrorRate | Error rate > 5% for 1 minute | Critical |
| HighLatency | P95 latency > 200ms for 1 minute | Warning |
| NoPredictions | Zero predictions for 5 minutes | Warning |
| DataDriftDetected | Drift score > 0.1 | Warning |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Liveness probe |
| GET | `/ready` | Readiness probe (model loaded) |
| POST | `/api/v1/predict` | Loan approval prediction |
| POST | `/api/v1/feedback` | Submit ground truth feedback |
| GET | `/api/v1/pipeline/status` | Pipeline task statuses |
| GET | `/metrics` | Prometheus metrics |

### Example Prediction Request
```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Male", "age": 35, "marital_status": "Married",
    "dependents": 1, "education": "Graduate",
    "employment_status": "Employed", "occupation_type": "Salaried",
    "residential_status": "Own", "city_town": "Urban",
    "annual_income": 85000, "monthly_expenses": 2500,
    "credit_score": 720, "existing_loans": 1,
    "total_existing_loan_amount": 15000, "outstanding_debt": 8000,
    "loan_history": 0, "loan_amount_requested": 20000,
    "loan_term": 120, "loan_purpose": "Home",
    "interest_rate": 8.5, "loan_type": "Secured",
    "co_applicant": "Yes", "bank_account_history": 5,
    "transaction_frequency": 15
  }'
```

### Example Response
```json
{
  "loan_approved": true,
  "approval_probability": 0.8732,
  "risk_level": "Low",
  "message": "Loan Approved",
  "credit_score_impact": "Strong positive factor",
  "recommendation": "Your application meets our approval criteria."
}
```

---

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v
```

**Results: 10/10 tests passing**

```
tests/test_health.py::test_health_returns_200              PASSED
tests/test_health.py::test_ready_returns_200               PASSED
tests/test_predict.py::test_predict_returns_200            PASSED
tests/test_predict.py::test_predict_response_has_fields    PASSED
tests/test_predict.py::test_predict_probability_range      PASSED
tests/test_predict.py::test_predict_invalid_returns_422    PASSED
tests/test_preprocessor.py::test_returns_dataframe         PASSED
tests/test_preprocessor.py::test_has_one_row               PASSED
tests/test_preprocessor.py::test_debt_to_income_ratio      PASSED
tests/test_preprocessor.py::test_gender_encoded_correctly  PASSED
10 passed in 3.03s
```

---


## 🏗 Architecture

```
[React Frontend :3002]
        │  REST API (JSON only)
[FastAPI Backend :8000]
        │                    │
[MLflow Registry :5000]  [Prometheus :9090]
[XGBoost Production]         │
                        [Grafana :3001]

[Airflow DAG :8080] → 7-task pipeline → training
[Git + DVC] → code + data versioning
[Docker Compose] → all services on finpredict-net
```

---

## 📝 License

This project was developed as part of an MLOps course assignment.

---

*Built with ❤️ using Python, React, XGBoost, MLflow, Airflow, DVC, Docker, Prometheus and Grafana*
