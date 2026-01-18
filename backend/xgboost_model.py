import xgboost as xgb
import pandas as pd
import numpy as np
import os

class FailurePredictor:
    def __init__(self):
        self.model = None
        self.model_path = "xgboost_model.json"
        
    def train_dummy_model(self):
        # Create some dummy data for training if no model exists
        # Features: temp, vibration, pressure
        X = np.array([
            [60, 10, 100], [65, 12, 101], [70, 15, 99], # Normal
            [95, 45, 90], [98, 50, 88], [100, 55, 85]   # Failure
        ])
        y = np.array([0, 0, 0, 1, 1, 1])
        
        self.model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
        self.model.fit(X, y)
        self.model.save_model(self.model_path)
        print("Dummy model trained and saved.")

    def load_model(self):
        if os.path.exists(self.model_path):
            self.model = xgb.XGBClassifier()
            self.model.load_model(self.model_path)
        else:
            print("Model not found. Training dummy model...")
            self.train_dummy_model()

    def predict(self, temp, vibration, pressure):
        if not self.model:
            self.load_model()
            
        data = np.array([[temp, vibration, pressure]])
        prediction = self.model.predict(data)
        return int(prediction[0])

predictor = FailurePredictor()
