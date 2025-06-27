"""MonetizerAgent integrates billing via Stripe."""

from .base import BaseAgent
from backend.integrations.hipcortex_bridge import HipCortexBridge
import stripe

class MonetizerAgent(BaseAgent):
    """Handles usage-based monetization."""

    def __init__(self, hipcortex: HipCortexBridge, api_key: str) -> None:
        self.hipcortex = hipcortex
        stripe.api_key = api_key

    def charge(self, user_id: str, amount: int) -> None:
        """Charge the user for usage via Stripe."""
        self.hipcortex.log_event(
            {
                "agent": "monetizer",
                "event": "charge_attempt",
                "user": user_id,
                "amount": amount,
            }
        )
        stripe.Charge.create(
            amount=amount,
            currency="usd",
            customer=user_id,
            description="Codex Booster usage charge",
        )
        self.hipcortex.log_event(
            {
                "agent": "monetizer",
                "event": "charged",
                "user": user_id,
                "amount": amount,
            }
        )
