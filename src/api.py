import joblib
from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="Reorder Prediction Engine API")

# Load trained model binary on startup
model = None

@app.on_event("startup")
def load_model():
    global model
    model_path = "models/lgbm_reorder_model.pkl"
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        print("Loaded LightGBM model binary successfully.")
