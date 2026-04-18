"""Task 7: Trigger model training script"""
import subprocess
import logging

logger = logging.getLogger(__name__)


def trigger_training():
    logger.info("Triggering model training...")
    result = subprocess.run(
        ["python", "mlops/training/train.py",
         "--n_estimators", "200",
         "--max_depth", "6",
         "--learning_rate", "0.1"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        logger.error(f"Training failed:\n{result.stderr}")
        raise RuntimeError(f"Training script failed: {result.stderr}")

    logger.info("Training completed successfully")
    logger.info(result.stdout)
