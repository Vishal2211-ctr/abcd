import pandas as pd

class SimulationEngine:
    def __init__(self, model):
        self.model = model
        
    def run_scenario(self, base_data, lifestyle, months):
        """
        Combines base patient data with a lifestyle scenario and time horizon.
        """
        # Combine base data with lifestyle scenario
        scenario_data = base_data.copy()
        for key, value in lifestyle.items():
            scenario_data[key] = value
            
        scenario_data['months'] = months
        
        # Convert to DataFrame for model
        df = pd.DataFrame([scenario_data])
        
        # Run prediction
        prediction = self.model.predict(df)
        
        return prediction
