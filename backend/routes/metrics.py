from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def get_metrics():
    return {"revenue": 0, "users": 0}
