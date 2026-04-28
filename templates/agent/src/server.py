"""FastAPI server — REST API for the agent service."""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import FastAPI

from src.config import settings
from src.engine.agent_loop import AgentLoop, EventType
from src.logger import logger
from src.permissions.checker import PermissionChecker
from src.schemas import ChatRequest, ChatResponse, HealthResponse
from src.skills import load_skills
from src.tools import get_tool_registry

app = FastAPI(title="Agent Service", version="1.0.0")

# Session storage (in production, use Redis or database)
_sessions: dict[str, list[dict[str, Any]]] = {}


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="healthy", version="1.0.0")


@app.get("/api/tools")
async def list_tools() -> list[dict[str, str]]:
    """List all available tools."""
    registry = get_tool_registry()
    return [{"name": t.name, "description": t.description, "read_only": t.is_read_only} for t in registry.all()]


@app.get("/api/skills")
async def list_skills() -> list[dict[str, str]]:
    """List all available skills."""
    skills = load_skills()
    return [{"name": s.name, "description": s.description} for s in skills.values()]


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    """Send a message to the agent. Returns the final response."""
    session_id = req.session_id or str(uuid.uuid4())
    session_messages = _sessions.get(session_id, [])

    logger.info("chat_request", session_id=session_id, message=req.message[:100])

    registry = get_tool_registry()
    permission_checker = PermissionChecker()

    loop = AgentLoop(
        registry=registry,
        permission_checker=permission_checker,
    )

    final_content = ""
    tool_calls_count = 0

    async for event in loop.run(req.message, session_messages=session_messages):
        if event.type == EventType.ASSISTANT_MESSAGE:
            final_content = event.data.get("content", "")
        elif event.type == EventType.TOOL_CALL:
            tool_calls_count += 1
        elif event.type == EventType.DONE:
            final_content = event.data.get("content", "") or final_content

    # Persist session
    _sessions[session_id] = loop.messages

    return ChatResponse(
        response=final_content,
        session_id=session_id,
        tool_calls_count=tool_calls_count,
    )
