import os
import yaml
import joblib
import pandas as pd
import numpy as np
from lightgbm import LGBMClassifier
from sklearn.metrics import roc_auc_score
from feature_engineering import FeaturePipeline

def train_pipeline(config_path: str = "config/config.yaml"):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # 1. Load data & run feature engineering
    pipeline = FeaturePipeline()
    feature_matrix = pipeline.fit_transform(raw_df)
    
    feature_cols = [
        'user_total_orders', 'user_reorder_rate', 'user_avg_basket_size',
        'prod_reorder_prior', 'prod_avg_cart_position', 'prod_total_purchases',
        'up_total_purchases', 'up_avg_cart_position', 'up_purchase_ratio', 'up_orders_since_last'
    ]

    X = feature_matrix[feature_cols]
    y = feature_matrix['reordered']

    # 2. Train LightGBM
    clf = LGBMClassifier(**config['model']['params'])
    clf.fit(X, y)

    # 3. Save Model
    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, "models/lgbm_reorder_model.pkl")
    print("Model serialized to models/lgbm_reorder_model.pkl")

if __name__ == "__main__":
    train_pipeline()
