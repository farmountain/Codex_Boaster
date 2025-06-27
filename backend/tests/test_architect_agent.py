from backend.agents.architect_agent import ArchitectAgent
from backend.integrations.hipcortex_bridge import HipCortexBridge
from unittest.mock import MagicMock


def test_plan_logs_and_returns_dict():
    hc = HipCortexBridge(base_url="http://test")
    hc.log_event = MagicMock()
    agent = ArchitectAgent(hc)

    goal = "create a todo app"
    plan = agent.plan(goal)

    assert isinstance(plan, dict)
    assert plan["goal"] == goal

    hc.log_event.assert_any_call({"agent": "architect", "event": "received_goal", "goal": goal})
    hc.log_event.assert_any_call({"agent": "architect", "event": "plan_complete", "plan": plan})
