# Example: backend/routes/books.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_books():
    return {"message": "Books endpoint - coming soon"}
