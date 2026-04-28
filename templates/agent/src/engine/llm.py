"""LLM client — wraps LiteLLM for multi-provider support.

LiteLLM gives us a unified interface to OpenAI, Anthropic, Azure, Bedrock, etc.
Just set LLM_MODEL in .env (e.g. "gpt-4o", "claude-sonnet-4-20250514", "azure/gpt-4o").
"""

from __future__ import annotations

from typing import Any

import litellm

from src.config import settings
from src.logger import logger


async def chat_completion(
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]] | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    """Call LLM with tool-calling support. Returns the raw response dict."""
    model = model or settings.llm_model

    kwargs: dict[str, Any] = {
        "model": model,
        "messages": messages,
    }
    if tools:
        kwargs["tools"] = tools

    logger.debug("llm_request", model=model, message_count=len(messages), has_tools=bool(tools))

    response = await litellm.acompletion(**kwargs)

    logger.debug("llm_response", model=model, stop_reason=response.choices[0].finish_reason)
    return response  # type: ignore[return-value]
