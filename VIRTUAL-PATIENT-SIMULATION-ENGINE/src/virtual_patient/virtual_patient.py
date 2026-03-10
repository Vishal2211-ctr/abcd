import json
from src.virtual_patient.model import HealthModel
from src.virtual_patient.simulation import SimulationEngine

class VirtualPatient:
    """
    Virtual Patient class to simulate health outcomes based on lifestyle changes.
    """
    def __init__(self, patient_data):
        if isinstance(patient_data, str):
            self.patient_data = json.loads(patient_data)
        else:
            self.patient_data = patient_data
            
        # Initialize internal state and engine
        try:
            self.model = HealthModel()
        except FileNotFoundError:
            # Fallback for relative paths or different execution contexts
            import os
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            model_path = os.path.join(base_dir, 'models', 'patient_simulation_model.joblib')
            self.model = HealthModel(model_path=model_path)
            
        self.engine = SimulationEngine(self.model)
        
    def simulate(self, lifestyle, months=3):
        """
        Simulate health metrics for a given lifestyle scenario and time horizon.
        
        :param lifestyle: Dict containing lifestyle variables:
                          exercise_minutes_per_day, diet_type, smoking_status,
                          alcohol_units_per_week, sleep_hours_per_night, stress_level, BMI
        :param months: Simulation horizon (1, 3, 6, 12)
        :return: JSON result with predicted vitals and risk scores
        """
        # Use default BMI from patient data if not provided in lifestyle
        if 'BMI' not in lifestyle and 'BMI' in self.patient_data:
            lifestyle['BMI'] = self.patient_data['BMI']
        elif 'BMI' not in lifestyle:
            # Simple BMI estimation if not provided
            lifestyle['BMI'] = 25.0 
            
        prediction = self.engine.run_scenario(self.patient_data, lifestyle, months)
        return prediction

    def get_current_state(self):
        return self.patient_data
