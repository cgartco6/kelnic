from fastapi import APIRouter
router = APIRouter()

@router.get("/interactions")
async def get_interactions():
    return []
