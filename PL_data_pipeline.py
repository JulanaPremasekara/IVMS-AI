import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from config_loader import load_config, get_config_value

# Load configuration
config = load_config()

def load_data():
    """
    Load dataset. For this example, we'll create dummy data.
    In a real scenario, you could load from CSV files like inventory.csv or vendor.csv.
    """
    # Get random seed from config
    random_seed = get_config_value(config, 'data.random_seed', 42)
    np.random.seed(random_seed)
    
    # Create dummy data: features like price, quantity, category, and target (e.g., vendor score)
    data = {
        'price': np.random.uniform(10, 1000, 1000),
        'quantity': np.random.randint(1, 100, 1000),
        'category': np.random.choice(['A', 'B', 'C'], 1000),
        'vendor_score': np.random.uniform(0, 1, 1000)  # Target: continuous score
    }
    df = pd.DataFrame(data)
    return df
    data = {
        'price': np.random.uniform(10, 1000, 1000),
        'quantity': np.random.randint(1, 100, 1000),
        'category': np.random.choice(['A', 'B', 'C'], 1000),
        'vendor_score': np.random.uniform(0, 1, 1000)  # Target: continuous score
    }
    df = pd.DataFrame(data)
    return df

def preprocess_data(df):
    """
    Perform basic preprocessing: handle missing values, encode categories, scale features.
    """
    # Handle missing values (dummy data has none, but good practice)
    df = df.dropna()

    # Encode categorical features
    le = LabelEncoder()
    df['category'] = le.fit_transform(df['category'])

    # Split features and target
    X = df.drop('vendor_score', axis=1)
    y = df['vendor_score']

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler

def get_train_test_split(X, y, test_size=None):
    """
    Split data into train and test sets.
    """
    if test_size is None:
        test_size = get_config_value(config, 'training.test_size', 0.2)
    
    random_state = get_config_value(config, 'training.random_state', 42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    # Example usage
    df = load_data()
    print("Data loaded:", df.head())
    X, y, scaler = preprocess_data(df)
    X_train, X_test, y_train, y_test = get_train_test_split(X, y)
    print("Data preprocessed and split.")