import pandas as pd
import numpy as np

class FeaturePipeline:
    """Computes hierarchical aggregations across user, product, and interaction levels."""
    
    def compute_user_features(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.groupby('user_id').agg(
            user_total_orders=('order_number', 'max'),
            user_reorder_rate=('reordered', 'mean'),
            user_avg_basket_size=('add_to_cart_order', 'max')
        ).reset_index()

    def compute_product_features(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.groupby('product_id').agg(
            prod_reorder_prior=('reordered', 'mean'),
            prod_avg_cart_position=('add_to_cart_order', 'mean'),
            prod_total_purchases=('order_id', 'count')
        ).reset_index()

    def compute_user_product_features(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.groupby(['user_id', 'product_id']).agg(
            up_total_purchases=('order_id', 'count'),
            up_avg_cart_position=('add_to_cart_order', 'mean'),
            up_last_order_number=('order_number', 'max')
        ).reset_index()

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        u_df = self.compute_user_features(df)
        p_df = self.compute_product_features(df)
        up_df = self.compute_user_product_features(df)

        merged = up_df.merge(u_df, on='user_id', how='left')
        merged = merged.merge(p_df, on='product_id', how='left')

        merged['up_purchase_ratio'] = merged['up_total_purchases'] / np.maximum(merged['user_total_orders'], 1)
        merged['up_orders_since_last'] = merged['user_total_orders'] - merged['up_last_order_number']
        return merged
