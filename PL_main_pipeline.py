from PL_data_pipeline import load_data, preprocess_data, get_train_test_split
from PL_train_pipeline import train_model, save_model
from PL_evaluate_pipeline import evaluate_model
from PL_mlflow_tracking import log_experiment
from config_loader import load_config, get_config_value

# Load configuration
config = load_config()

def run_pipeline():
    """
    Run the full MLOps pipeline: data → train → evaluate → save model.
    """
    print("Starting MLOps Pipeline...")
    
    # Step 1: Data Pipeline
    print("1. Loading and preprocessing data...")
    df = load_data()
    X, y, scaler = preprocess_data(df)
    X_train, X_test, y_train, y_test = get_train_test_split(X, y)
    print("Data loaded and preprocessed.")
    
    # Step 2: Train Pipeline
    print("2. Training model...")
    model = train_model(X_train, y_train)
    print("Model trained.")
    
    # Step 3: Evaluate Pipeline
    print("3. Evaluating model...")
    metrics = evaluate_model(model, X_test, y_test)
    
    # Step 4: Save Model
    print("4. Saving model...")
    save_model(model)
    print("Model saved.")
    
    # Step 5: Log to MLflow
    print("5. Logging to MLflow...")
    params = {
        'hidden_layers': get_config_value(config, 'model.hidden_layer_sizes', [50]),
        'max_iter': get_config_value(config, 'model.max_iter', 1000)
    }
    log_experiment(model, params, metrics)
    print("Pipeline completed successfully!")
    
    return model, metrics

if __name__ == "__main__":
    # Run the full pipeline
    model, metrics = run_pipeline()