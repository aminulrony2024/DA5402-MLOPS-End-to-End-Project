"""Register the best performing model to MLflow Model Registry as Production"""
import mlflow
from mlflow.tracking import MlflowClient

MLFLOW_URI = "http://localhost:5000"
MODEL_NAME = "FinPredict_XGBoost"


def register_best_model():
    mlflow.set_tracking_uri(MLFLOW_URI)
    client = MlflowClient()

    experiment = mlflow.get_experiment_by_name("FinPredict_LoanApproval")
    if experiment is None:
        raise RuntimeError("Experiment 'FinPredict_LoanApproval' not found.")

    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string="params.model = 'XGBoost'",  # only XGBoost runs
        order_by=["metrics.f1_score DESC"]
    )

    if runs.empty:
        raise RuntimeError("No runs found. Run experiments first.")

    best_run = runs.iloc[0]
    best_run_id = best_run.run_id  # ✅ fix: define best_run_id
    print(f"Best run: {best_run_id} | F1: {best_run['metrics.f1_score']:.4f}")

    model_uri = f"runs:/{best_run_id}/xgboost_model"  # ✅ now resolves correctly
    mv = mlflow.register_model(model_uri, MODEL_NAME)

    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=mv.version,
        stage="Production"
    )
    print(f"Model version {mv.version} promoted to Production")


if __name__ == "__main__":
    register_best_model()