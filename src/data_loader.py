import pandas as pd
from typing import Tuple

class DataLoader:
    """Handles loading and temporal train-validation partitioning of order logs."""
    
    def __init__(self, raw_path: str = "data/raw/"):
        self.raw_path = raw_path

    def load_raw_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        orders = pd.read_csv(f"{self.raw_path}orders.csv")
        order_products = pd.read_csv(f"{self.raw_path}order_products.csv")
        return orders, order_products

    def create_temporal_split(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Splits dataset on user max order sequence to prevent target leakage."""
        max_orders = df.groupby('user_id')['order_number'].transform('max')
        train_mask = df['order_number'] < max_orders
        val_mask = df['order_number'] == max_orders
        return df[train_mask].copy(), df[val_mask].copy()
