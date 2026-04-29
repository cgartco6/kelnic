from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def get_resources():
    return {"cpu": 0, "memory": 0}
