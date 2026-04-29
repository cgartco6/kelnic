# backend/routes/payouts.py
from fastapi import APIRouter
from .marketing import TaskRequest

router = APIRouter()

@router.post("/run")
async def run_payout_task(request: TaskRequest):
    from backend.main import app
    result = await app.state.orchestrator.process_task(
        task=request.task,
        session_id=request.session_id,
        context=request.context
    )
    return {"success": True, "result": result}
