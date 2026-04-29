from fastapi import APIRouter, Request
router = APIRouter()

@router.post("/stripe")
async def stripe_webhook(request: Request):
    return {"status": "ok"}

@router.post("/paypal")
async def paypal_webhook(request: Request):
    return {"status": "ok"}

@router.post("/payfast")
async def payfast_webhook(request: Request):
    return {"status": "ok"}
