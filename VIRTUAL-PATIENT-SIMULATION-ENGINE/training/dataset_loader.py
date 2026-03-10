import pandas as pd
import numpy as np
import os
from utils.feature_engineering import preprocess_features

def generate_synthetic_data(num_samples=1000, output_path='data/synthetic_health_data.csv'):
    np.random.seed(42)
    
    # Baseline Features
    age = np.random.randint(20, 80, num_samples)
    bmi = np.random.uniform(18, 40, num_samples)
    base_sbp = np.random.randint(100, 160, num_samples)
    base_dbp = np.random.randint(60, 100, num_samples)
    base_chol = np.random.uniform(150, 300, num_samples)
    base_gluc = np.random.uniform(70, 150, num_samples)
    
    # Lifestyle Variables
    exercise = np.random.randint(0, 90, num_samples)
    diet = np.random.choice(['balanced', 'low_sodium', 'low_carb', 'high_fat'], num_samples)
    smoking = np.random.choice([False, True], num_samples, p=[0.7, 0.3])
    alcohol = np.random.randint(0, 20, num_samples)
    sleep = np.random.randint(4, 10, num_samples)
    stress = np.random.choice(['low', 'medium', 'high'], num_samples)
    months = np.random.choice([1, 3, 6, 12], num_samples)
    
    data = pd.DataFrame({
        'age': age,
        'systolic_bp': base_sbp,
        'diastolic_bp': base_dbp,
        'cholesterol_level': base_chol,
        'glucose_level': base_gluc,
        'BMI': bmi,
        'exercise_minutes_per_day': exercise,
        'diet_type': diet,
        'smoking_status': smoking,
        'alcohol_units_per_week': alcohol,
        'sleep_hours_per_night': sleep,
        'stress_level': stress,
        'months': months
    })
    
    # Simulate Results (Simple heuristics for realistic-ish behavior)
    # Exercise reduces BP, cholesterol, glucose
    # Smoking increases BP and risk
    # Poor diet (high fat) increases cholesterol
    # BMI increases risk and sugar levels
    
    t_sbp = base_sbp - (exercise * 0.1) + (smoking * 10) + (bmi * 0.5) - (sleep * 1)
    t_dbp = base_dbp - (exercise * 0.05) + (smoking * 5) + (bmi * 0.2)
    t_gluc = base_gluc - (exercise * 0.2) + (bmi * 1.5) + (diet == 'high_fat') * 10
    t_chol = base_chol - (exercise * 0.3) + (diet == 'high_fat') * 30 + (bmi * 0.8)
    
    # Normalize to time horizon (months) - change is cumulative
    decay = months / 12.0
    data['predicted_systolic_bp'] = base_sbp + (t_sbp - base_sbp) * decay
    data['predicted_diastolic_bp'] = base_dbp + (t_dbp - base_dbp) * decay
    data['predicted_glucose_level'] = base_gluc + (t_gluc - base_gluc) * decay
    data['predicted_cholesterol_level'] = base_chol + (t_chol - base_chol) * decay
    
    # Simple Risk Scores
    data['cardiovascular_risk_score'] = (data['age'] / 100) * 0.2 + (data['smoking_status'] * 0.1) + \
                                       (data['predicted_systolic_bp'] / 200) * 0.3 + \
                                       (data['predicted_cholesterol_level'] / 400) * 0.4
    
    data['diabetes_risk_score'] = (data['BMI'] / 40) * 0.4 + (data['predicted_glucose_level'] / 300) * 0.6
    
    # Clip to realistic ranges (Safety Layer mimic)
    data['predicted_systolic_bp'] = data['predicted_systolic_bp'].clip(80, 200)
    data['predicted_diastolic_bp'] = data['predicted_diastolic_bp'].clip(50, 120)
    data['predicted_glucose_level'] = data['predicted_glucose_level'].clip(60, 300)
    data['predicted_cholesterol_level'] = data['predicted_cholesterol_level'].clip(100, 400)
    data['cardiovascular_risk_score'] = data['cardiovascular_risk_score'].clip(0, 1)
    data['diabetes_risk_score'] = data['diabetes_risk_score'].clip(0, 1)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data.to_csv(output_path, index=False)
    print(f"Generated {num_samples} records at {output_path}")

if __name__ == "__main__":
    generate_synthetic_data()
