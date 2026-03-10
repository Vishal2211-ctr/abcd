import pandas as pd
import joblib
import os
from sklearn.multioutput import MultiOutputRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from utils.feature_engineering import preprocess_features, get_feature_names, get_target_names

def train_health_model(data_path='data/synthetic_health_data.csv', model_dir='models'):
    # Load data
    if not os.path.exists(data_path):
        print(f"Data file {data_path} not found. Ensure synthetic data is generated.")
        return
        
    df = pd.read_csv(data_path)
    
    # Preprocess
    df_processed = preprocess_features(df)
    
    # Define features and targets
    features = get_feature_names()
    targets = get_target_names()
    
    X = df_processed[features]
    y = df_processed[targets]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Training MultiOutputRegressor with XGBoost on {len(X_train)} samples...")
    
    # Initialize XGBRegressor with reasonable defaults
    base_model = XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42,
        objective='reg:squarederror'
    )
    
    # MultiOutputRegressor to handle multiple health metrics
    model = MultiOutputRegressor(base_model)
    model.fit(X_train, y_train)
    
    # Evaluation
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions, multioutput='raw_values')
    r2 = r2_score(y_test, predictions, multioutput='raw_values')
    
    print("\nModel Evaluation:")
    for i, target in enumerate(targets):
        print(f"{target} - MAE: {mae[i]:.4f}, R2: {r2[i]:.4f}")
        
    # Save model
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'patient_simulation_model.joblib')
    joblib.dump(model, model_path)
    print(f"\nModel saved to {model_path}")

if __name__ == "__main__":
    train_health_model()
