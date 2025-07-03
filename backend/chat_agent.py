from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from backend.hipcortex_bridge import store_chat_snapshot
from backend.logger import log_event

router = APIRouter()


class Message(BaseModel):
    """Single chat message."""

    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Payload for /api/chat requests."""

    session_id: str
    message: str
    history: List[Message]


@router.post("/api/chat")
async def chat_with_codex(req: ChatRequest):
    """Stateful chat endpoint routing input to the appropriate agent."""
    try:
        user_input = req.message.lower()

        if "project" in user_input:
            agent_response = "I'll ask ArchitectAgent to plan your project."
            actions = ["plan_project"]
            reflexion = "Detected intent to scaffold a project."
        elif "test" in user_input:
            agent_response = "Triggering TestSuiteAgent to generate UAT/SIT cases."
            actions = ["run_tests"]
            reflexion = "Inferred testing intent."
        else:
            agent_response = "Not sure yet. Could you clarify?"
            actions = []
            reflexion = "Unable to match intent."

        snapshot_id = store_chat_snapshot(
            {
                "session_id": req.session_id,
                "messages": [m.dict() for m in req.history] + [{"role": "user", "content": req.message}],
                "reply": agent_response,
                "agent": actions[0] if actions else "ChatAgent",
            }
        )

        await log_event(
            "ChatAgent",
            {"session": req.session_id, "agent": actions[0] if actions else "ChatAgent"},
        )

        log_chat(req.session_id, req.message, agent_response)

        return {
            "response": agent_response,
            "actions": actions,
            "reflexion_summary": reflexion,
            "memory_log": f"Logged to session {req.session_id}",
            "snapshot_id": snapshot_id,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def log_chat(session_id: str, user_msg: str, agent_msg: str) -> None:
    """Simple stdout logger for chat exchanges."""
    print(f"[{session_id}] User: {user_msg} | Codex: {agent_msg}")
