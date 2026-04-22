FROM apache/airflow:2.9.0

# Install DAG dependencies once at build time
RUN pip install --no-cache-dir \
    scikit-learn==1.3.2 \
    pandas==2.1.2 \
    numpy==1.26.1 \
    xgboost==2.0.1 \
    mlflow==2.19.0