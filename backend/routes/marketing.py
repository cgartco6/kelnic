# backend/routes/marketing.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

class TaskRequest(BaseModel):
    task: str
    session_id: str
    context: Dict[str, Any] = {}

@router.post("/run")
async def run_marketing_task(request: TaskRequest, app_state=Depends(lambda: None)):
    try:
        orchestrator = app_state.orchestrator if app_state else None
        if not orchestrator:
            raise HTTPException(status_code=500, detail="Orchestrator not initialized")

        result = await orchestrator.process_task(
            task=request.task,
            session_id=request.session_id,
            context=request.context
        )
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
