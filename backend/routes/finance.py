# backend/routes/finance.py
from fastapi import APIRouter
from .marketing import TaskRequest   # Reuse the same model

router = APIRouter()

@router.post("/run")
async def run_finance_task(request: TaskRequest):
    # Same logic as marketing for now (we can customize later)
    from backend.main import app
    orchestrator = app.state.orchestrator
    result = await orchestrator.process_task(
        task=request.task,
        session_id=request.session_id,
        context=request.context
    )
    return {"success": True, "result": result}
