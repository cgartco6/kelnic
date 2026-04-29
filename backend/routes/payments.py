from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def get_payments():
    return {"message": "payments endpoint"}
