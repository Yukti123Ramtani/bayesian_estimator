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
OPTIMAL_THRESHOLD = 0.3622

@app.post("/predict")
def predict_reorder_probability(request: PredictionRequest):
    # Model probability output
    probabilities = model.predict_proba(X)[:, 1]
    
    # Classify based on optimal F1-score threshold
    recommended_items = [
        pid for pid, prob in zip(request.product_ids, probabilities) 
        if prob >= OPTIMAL_THRESHOLD
    ]
    
    return {
        "user_id": request.user_id,
        "recommended_product_ids": recommended_items,
        "threshold_used": OPTIMAL_THRESHOLD
    }
