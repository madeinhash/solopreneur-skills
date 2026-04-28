"""Web fetch tool — fetch and extract content from URLs."""

from __future__ import annotations

import re
from typing import Any

import httpx

from src.tools.base import Tool
from src.types import ToolResult


class WebFetchTool(Tool):
    @property
    def name(self) -> str:
        return "web_fetch"

    @property
    def description(self) -> str:
        return "Fetch content from a URL. Returns the page text (HTML tags stripped). Useful for reading web pages, APIs, docs."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to fetch"},
            },
            "required": ["url"],
        }

    @property
    def is_read_only(self) -> bool:
        return True

    async def execute(self, args: dict[str, Any]) -> ToolResult:
        url = args["url"]
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
                resp = await client.get(url, headers={"User-Agent": "AgentBot/1.0"})
                resp.raise_for_status()

            content_type = resp.headers.get("content-type", "")
            text = resp.text

            # Strip HTML tags for readable output
            if "html" in content_type:
                text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL)
                text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
                text = re.sub(r"<[^>]+>", " ", text)
                text = re.sub(r"\s+", " ", text).strip()

            # Truncate
            if len(text) > 50_000:
                text = text[:50_000] + "\n... (content truncated)"

            return ToolResult(output=text or "(empty response)")
        except Exception as e:
            return ToolResult(output=f"Error fetching URL: {e}", is_error=True)
