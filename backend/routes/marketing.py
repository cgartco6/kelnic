from fastapi import APIRouter
router = APIRouter()

@router.post("/campaigns")
async def create_campaign():
    return {"status": "queued"}
