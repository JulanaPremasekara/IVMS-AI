from sklearn.metrics import mean_squared_error, r2_score
from PL_data_pipeline import load_data, preprocess_data, get_train_test_split
from PL_train_pipeline import load_model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model using test data.
    Returns metrics like MSE and R2 score.
    """
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Model Evaluation:")
    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"R2 Score: {r2:.4f}")
    
    return {'mse': mse, 'r2': r2}

if __name__ == "__main__":
    # Load data and model
    df = load_data()
    X, y, scaler = preprocess_data(df)
    X_train, X_test, y_train, y_test = get_train_test_split(X, y)
    
    model = load_model()
    
    # Evaluate
    metrics = evaluate_model(model, X_test, y_test)