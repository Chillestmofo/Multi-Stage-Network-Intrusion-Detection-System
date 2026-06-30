from fastapi import APIRouter
from app.decision import detect

router = APIRouter()

@router.post("/predict")
def predict(payload: dict):
    return detect(payload)
