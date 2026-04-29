from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def list_templates():
    return {"templates": []}

@router.get("/{tier_id}")
async def get_template(tier_id: str):
    return {"tier": tier_id}
