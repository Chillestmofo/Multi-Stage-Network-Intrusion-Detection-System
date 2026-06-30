import joblib
from app.config import MODEL_DIR, ARTIFACT_DIR

# Stage-1 feature order
feature_order_stage1 = joblib.load(
    f"{ARTIFACT_DIR}/feature_order.pkl"
)

# Stage-2 feature order (leak-free)
feature_order_stage2 = joblib.load(
    f"{ARTIFACT_DIR}/feature_order_stage2.pkl"
)

# Models
normal_filter = joblib.load(f"{MODEL_DIR}/normal_filter.pkl")

attack_models = {
    "DoS": joblib.load(f"{MODEL_DIR}/dos_model.pkl"),
    "DDoS": joblib.load(f"{MODEL_DIR}/ddos_model.pkl"),
    "PortScan": joblib.load(f"{MODEL_DIR}/portscan_model.pkl"),
    "BruteForce": joblib.load(f"{MODEL_DIR}/bruteforce_model.pkl"),
    "WebAttack": joblib.load(f"{MODEL_DIR}/webattack_model.pkl"),
}
