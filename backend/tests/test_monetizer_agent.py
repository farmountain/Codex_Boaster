from unittest.mock import MagicMock, patch

from backend.agents.monetizer_agent import MonetizerAgent
from backend.integrations.hipcortex_bridge import HipCortexBridge


def test_charge_creates_stripe_charge_and_logs():
    hc = HipCortexBridge(base_url="http://test")
    hc.log_event = MagicMock()

    with patch("backend.agents.monetizer_agent.stripe.Charge.create") as mock_charge:
        agent = MonetizerAgent(hc, api_key="sk_test")
        agent.charge("cus_123", 1000)
        mock_charge.assert_called_once_with(
            amount=1000,
            currency="usd",
            customer="cus_123",
            description="Codex Booster usage charge",
        )

    hc.log_event.assert_any_call(
        {
            "agent": "monetizer",
            "event": "charge_attempt",
            "user": "cus_123",
            "amount": 1000,
        }
    )
    hc.log_event.assert_any_call(
        {
            "agent": "monetizer",
            "event": "charged",
            "user": "cus_123",
            "amount": 1000,
        }
    )
