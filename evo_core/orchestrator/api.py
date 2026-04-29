# evo_core/orchestrator/api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

router = APIRouter(prefix="/orchestrator", tags=["orchestrator"])

class TaskRequest(BaseModel):
    task: str
    session_id: str
    context: Optional[Dict[str, Any]] = None
    priority: int = 5

class OrchestratorAPI:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    async def handle_task(self, request: TaskRequest):
        try:
            result = await self.orchestrator.process_task(
                task=request.task,
                session_id=request.session_id,
                context=request.context or {},
                priority=request.priority
            )
            return {"status": "success", "result": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# This will be attached in main.py later
