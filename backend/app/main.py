from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.predict import router
from app.auth import verify_token, optional_verify_token
import json
import os
from pathlib import Path

app = FastAPI(title="Multi-Stage IDS")

# Load model metadata
metadata_path = Path(__file__).parent / "artifacts" / "model_metadata.json"
try:
    with open(metadata_path, 'r') as f:
        MODEL_METADATA = json.load(f)
except FileNotFoundError:
    MODEL_METADATA = {"model_version": "unknown", "error": "metadata not found"}

# Global detection storage (circular buffer - keeps last 500)
detections_history = []

# Threat-only storage (keeps last 1000 attacks permanently)
threats_storage = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def health():
    return {
        "status": "IDS backend running",
        "model_version": MODEL_METADATA.get("model_version", "unknown"),
        "auth_enabled": bool(os.getenv("IDS_API_TOKEN"))
    }

@app.get("/detections")
def get_detections():
    return detections_history

@app.get("/threats")
def get_threats():
    """Returns only detected attacks/threats"""
    return threats_storage

@app.get("/model-info")
def get_model_info():
    """Returns model metadata and performance metrics"""
    return MODEL_METADATA

@app.delete("/threats", dependencies=[Depends(verify_token)])
def clear_threats():
    """Clear all stored threats (requires authentication)"""
    threats_storage.clear()
    return {"status": "threats cleared", "count": 0}

@app.post("/report", dependencies=[Depends(verify_token)])
def report_detection(detection: dict):
    # Add to general detections (circular buffer)
    detections_history.append(detection)
    if len(detections_history) > 500:
        detections_history.pop(0)
    
    # If it's an attack, also store in threats (larger limit)
    if detection.get("is_attack", False):
        threats_storage.append(detection)
        if len(threats_storage) > 1000:
            threats_storage.pop(0)
    
    return {"status": "reported"}
