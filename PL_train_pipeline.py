import pickle
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from PL_data_pipeline import load_data, preprocess_data, get_train_test_split
from PL_mlflow_tracking import log_experiment
from config_loader import load_config, get_config_value

# Load configuration
config = load_config()

def train_model(X_train, y_train):
    """
    Train a simple MLP model using sklearn's MLPRegressor.
    """
    # Get model parameters from config
    hidden_layer_sizes = tuple(get_config_value(config, 'model.hidden_layer_sizes', [50]))
    max_iter = get_config_value(config, 'model.max_iter', 1000)
    random_state = get_config_value(config, 'model.random_state', 42)
    
    # Define the model
    model = MLPRegressor(hidden_layer_sizes=hidden_layer_sizes, max_iter=max_iter, random_state=random_state)
    
    # Train the model
    model.fit(X_train, y_train)
    
    return model

def save_model(model, filename=None):
    """
    Save the trained model to a file.
    """
    if filename is None:
        filename = get_config_value(config, 'data.model_save_path', 'model.pkl')
    
    with open(filename, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {filename}")

def load_model(filename=None):
    """
    Load a trained model from file.
    """
    if filename is None:
        filename = get_config_value(config, 'data.model_save_path', 'model.pkl')
    
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    return model

if __name__ == "__main__":
    # Load and preprocess data
    df = load_data()
    X, y, scaler = preprocess_data(df)
    X_train, X_test, y_train, y_test = get_train_test_split(X, y)
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Make predictions on test set for quick check
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Training completed. Test MSE: {mse:.4f}")
    
    # Save model
    save_model(model)
    
    # Log to MLflow
    params = {
        'hidden_layers': get_config_value(config, 'model.hidden_layer_sizes', [50]),
        'max_iter': get_config_value(config, 'model.max_iter', 1000)
    }
    log_experiment(model, params, {'mse': mse})