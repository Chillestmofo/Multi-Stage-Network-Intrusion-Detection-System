import os

# Absolute path to backend directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_DIR = os.path.join(BASE_DIR, "models")
ARTIFACT_DIR = os.path.join(BASE_DIR, "artifacts")

NORMAL_THRESHOLD = 0.90

ATTACK_THRESHOLDS = {
    "DoS": 0.85,
    "DDoS": 0.90,
    "PortScan": 0.85,
    "BruteForce": 0.80,
    "WebAttack": 0.80,
}

MARGIN = 0.15
