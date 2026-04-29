from fastapi import APIRouter
router = APIRouter()

@router.get("/pl")
async def profit_loss():
    return {}
