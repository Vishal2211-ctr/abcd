import joblib
import os

os.makedirs('models', exist_ok=True)
path = 'models/test_file.joblib'
joblib.dump({'status': 'ok'}, path)
if os.path.exists(path):
    print(f"SUCCESS: File created at {os.path.abspath(path)}")
else:
    print("FAILURE: File not found after saving")
