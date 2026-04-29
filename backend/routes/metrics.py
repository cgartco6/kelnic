# backend/routes/metrics.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_metrics():
    return {
        "total_agents": 13,
        "active_sessions": 4,
        "tasks_processed_today": 87,
        "system_health": "excellent"
    }
