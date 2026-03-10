import numpy as np
import pandas as pd

def preprocess_features(df):
    """
    Convert raw patient data and lifestyle scenarios into features for the ML model.
    """
    # Encoding categorical variables
    diet_mapping = {
        'balanced': 0,
        'low_sodium': 1,
        'low_carb': 2,
        'high_fat': 3
    }
    stress_mapping = {
        'low': 0,
        'medium': 1,
        'high': 2
    }
    
    processed_df = df.copy()
    
    # Map categoricals if they exist (handling both single rows and dataframes)
    if 'diet_type' in processed_df.columns:
        processed_df['diet_type'] = processed_df['diet_type'].map(diet_mapping).fillna(0)
    
    if 'stress_level' in processed_df.columns:
        processed_df['stress_level'] = processed_df['stress_level'].map(stress_mapping).fillna(1)
        
    if 'smoking_status' in processed_df.columns:
        processed_df['smoking_status'] = processed_df['smoking_status'].astype(int)
        
    # Feature interactions (example: age * BMI)
    if 'age' in processed_df.columns and 'BMI' in processed_df.columns:
        processed_df['age_bmi_interaction'] = processed_df['age'] * processed_df['BMI']
        
    return processed_df

def get_feature_names():
    return [
        'age', 'systolic_bp', 'diastolic_bp', 'cholesterol_level', 'glucose_level',
        'exercise_minutes_per_day', 'diet_type', 'smoking_status', 
        'alcohol_units_per_week', 'sleep_hours_per_night', 'stress_level', 
        'BMI', 'months', 'age_bmi_interaction'
    ]

def get_target_names():
    return [
        'predicted_systolic_bp', 'predicted_diastolic_bp', 
        'predicted_glucose_level', 'predicted_cholesterol_level',
        'cardiovascular_risk_score', 'diabetes_risk_score'
    ]
