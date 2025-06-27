from backend.agents.reflexion_agent import ReflexionAgent
from backend.integrations.hipcortex_bridge import HipCortexBridge
from unittest.mock import MagicMock, patch


def test_reflect_generates_strategy_and_logs():
    hc = HipCortexBridge(base_url="http://test")
    hc.log_event = MagicMock()

    with patch("backend.agents.reflexion_agent.EffortEvaluator") as EE, patch(
        "backend.agents.reflexion_agent.ConfidenceRegulator"
    ) as CR:
        ee = EE.return_value
        cr = CR.return_value
        ee.analyze.return_value = "high"
        cr.regulate.return_value = "new strategy"

        agent = ReflexionAgent(hc)
        strategy = agent.reflect("failed")

        assert strategy == "new strategy"
        hc.log_event.assert_any_call({"agent": "reflexion", "feedback": "failed"})
        hc.log_event.assert_any_call(
            {"agent": "reflexion", "effort": "high", "instruction": "new strategy"}
        )

