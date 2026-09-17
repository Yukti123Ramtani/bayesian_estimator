import pytest
import pandas as pd
from src.feature_engineering import FeaturePipeline

def test_feature_pipeline_output():
    mock_df = pd.DataFrame({
        'user_id': [1, 1, 1],
        'product_id': [101, 101, 102],
        'order_id': [10, 11, 11],
        'order_number': [1, 2, 2],
        'add_to_cart_order': [1, 2, 1],
        'reordered': [0, 1, 0]
    })
    
    pipeline = FeaturePipeline()
    df_feat = pipeline.fit_transform(mock_df)
    
    assert 'up_purchase_ratio' in df_feat.columns
    assert 'user_reorder_rate' in df_feat.columns
    assert len(df_feat) == 2
