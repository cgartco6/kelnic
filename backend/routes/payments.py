from fastapi import APIRouter, Request, HTTPException
import stripe
import os
router = APIRouter()

@router.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    # Forward to orchestrator or process directly
    return {"status": "ok"}

@router.post("/create-checkout")
async def create_checkout(tier: str, price: float, email: str):
    # Call payment agent
    return {"url": "https://checkout.stripe.com/pay/..."}
