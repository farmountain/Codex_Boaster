from fastapi import APIRouter
from pydantic import BaseModel
from backend.hipcortex_bridge import log_event
import stripe
import os

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class ChargeRequest(BaseModel):
    user_id: str
    plan: str  # "starter", "pro", "enterprise"
    email: str


@router.post("/charge")
async def charge(req: ChargeRequest):
    try:
        price_lookup = {
            "starter": os.getenv("STRIPE_PRICE_STARTER"),
            "pro": os.getenv("STRIPE_PRICE_PRO"),
            "enterprise": os.getenv("STRIPE_PRICE_ENTERPRISE"),
        }
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": price_lookup[req.plan], "quantity": 1}],
            mode="subscription",
            success_url=f"{os.getenv('FRONTEND_URL')}/success",
            cancel_url=f"{os.getenv('FRONTEND_URL')}/cancel",
            customer_email=req.email,
            metadata={"user_id": req.user_id, "plan": req.plan},
        )

        log_event(
            "MonetizerAgent",
            {
                "user_id": req.user_id,
                "plan": req.plan,
                "checkout_url": session.url,
            },
        )

        return {"checkout_url": session.url}
    except Exception as e:  # pragma: no cover - unexpected failures
        return {"error": str(e)}, 500
