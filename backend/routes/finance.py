from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def get_finance():
    return {"upgrade_funds": 0}
