from fastapi import FastAPI

from app.routes.fraud import analyze_message_route
from app.schemas.fraud import FraudCheckRequest

app = FastAPI(title="MamaSentry", version="0.1.0")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "MamaSentry is running"}


@app.post("/check-fraud")
def check_fraud(payload: FraudCheckRequest):
    return analyze_message_route(payload)
