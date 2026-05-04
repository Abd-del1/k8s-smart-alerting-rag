from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI(
    title="Kubernetes Smart Alerting System",
    description="AI-powered smart alerting system for Kubernetes using RAG and OpenAI",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "smart-alert-api",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/alerts")
async def receive_alert(request: Request):
    payload = await request.json()

    return {
        "status": "received",
        "message": "Alert received successfully",
        "alert_payload": payload
    }
