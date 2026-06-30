import pandas as pd
from app.models_loader import (
    feature_order_stage1,
    feature_order_stage2,
)

def map_payload_stage1(payload: dict) -> pd.DataFrame:
    row = [payload.get(f, 0.0) for f in feature_order_stage1]
    return pd.DataFrame([row], columns=feature_order_stage1)

def map_payload_stage2(payload: dict) -> pd.DataFrame:
    row = [payload.get(f, 0.0) for f in feature_order_stage2]
    return pd.DataFrame([row], columns=feature_order_stage2)
