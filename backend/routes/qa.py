from fastapi import APIRouter
router = APIRouter()

@router.get("/results")
async def get_qa():
    return {"status": "ok"}
