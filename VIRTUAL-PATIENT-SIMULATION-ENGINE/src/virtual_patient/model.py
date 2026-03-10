import joblib
import os
import pandas as pd
from utils.feature_engineering import preprocess_features, get_feature_names, get_target_names

class HealthModel:
    def __init__(self, model_path='models/patient_simulation_model.joblib'):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}. Please run training first.")
        
        self.model = joblib.load(model_path)
        self.feature_names = get_feature_names()
        self.target_names = get_target_names()
        
    def predict(self, patient_data):
        """
        Expects a DataFrame with all necessary features.
        Returns a dictionary of predictions with safety bounds applied.
        """
        # Ensure preprocessing
        X = preprocess_features(patient_data)
        X = X[self.feature_names]
        
        # Predict
        raw_preds = self.model.predict(X)[0]
        
        # Structure results and apply safety bounds
        predictions = {}
        for i, target in enumerate(self.target_names):
            val = raw_preds[i]
            
            # Apply Safety Bounds
            if target == 'predicted_systolic_bp':
                val = max(80, min(200, val))
            elif target == 'predicted_diastolic_bp':
                val = max(50, min(120, val))
            elif target == 'predicted_glucose_level':
                val = max(60, min(300, val))
            elif target == 'predicted_cholesterol_level':
                val = max(100, min(400, val))
            elif 'risk_score' in target:
                val = max(0.0, min(1.0, val))
                
            predictions[target] = round(float(val), 2)
            
        return predictions
