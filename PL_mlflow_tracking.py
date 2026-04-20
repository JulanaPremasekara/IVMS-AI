import mlflow
import mlflow.sklearn
from config_loader import load_config, get_config_value

# Load configuration
config = load_config()

# Set MLflow tracking URI and experiment
mlflow.set_tracking_uri(get_config_value(config, 'mlflow.tracking_uri', 'http://localhost:5000'))
mlflow.set_experiment(get_config_value(config, 'mlflow.experiment_name', 'Default'))

def log_experiment(model, params, metrics):
    """
    Log parameters, metrics, and model to MLflow.
    """
    # Start MLflow run
    with mlflow.start_run():
        # Log parameters
        for key, value in params.items():
            mlflow.log_param(key, value)
        
        # Log metrics
        for key, value in metrics.items():
            mlflow.log_metric(key, value)
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        print("Experiment logged to MLflow.")

def start_mlflow_ui():
    """
    Start MLflow UI for viewing experiments.
    Run 'mlflow ui' in terminal to view at http://localhost:5000
    """
    print("To view experiments, run 'mlflow ui' in terminal.")

if __name__ == "__main__":
    # Example: This would be called from other scripts
    print("MLflow tracking module. Use log_experiment() to log runs.")