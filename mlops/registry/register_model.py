"""Register the best performing model to MLflow Model Registry as Production"""
import mlflow
from mlflow.tracking import MlflowClient

MLFLOW_URI = "http://localhost:5000"
MODEL_NAME = "FinPredict_XGBoost"


def register_best_model():
    mlflow.set_tracking_uri(MLFLOW_URI)
    client = MlflowClient()

    experiment = mlflow.get_experiment_by_name("FinPredict_LoanApproval")
    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.f1_score DESC"]
    )

    if runs.empty:
        raise RuntimeError("No runs found. Run experiments first.")

    best_run = runs.iloc[0]
    print(f"Best run: {best_run.run_id} | F1: {best_run['metrics.f1_score']:.4f}")

    model_uri = f"runs:/{best_run.run_id}/loan_approval_model"
    mv = mlflow.register_model(model_uri, MODEL_NAME)

    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=mv.version,
        stage="Production"
    )
    print(f"Model version {mv.version} promoted to Production")


if __name__ == "__main__":
    register_best_model()
