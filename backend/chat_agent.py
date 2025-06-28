from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from backend.codex_router import route_prompt_to_agent
from backend.hipcortex_bridge import store_chat_snapshot, log_event

router = APIRouter()


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    session_id: str
    messages: List[ChatMessage]


@router.post("/chat")
async def chat(req: ChatRequest):
    last_msg = req.messages[-1].content
    full_history = [m.dict() for m in req.messages]

    agent_reply, route_info = route_prompt_to_agent(last_msg, history=full_history)

    snapshot_id = store_chat_snapshot(
        {
            "session_id": req.session_id,
            "messages": full_history,
            "reply": agent_reply,
            "agent": route_info.get("agent", "ChatAgent"),
        }
    )

    log_event("ChatAgent", {"session": req.session_id, "agent": route_info.get("agent")})

    return {
        "reply": agent_reply,
        "agent": route_info.get("agent"),
        "snapshot_id": snapshot_id,
    }
