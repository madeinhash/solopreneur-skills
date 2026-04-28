from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Server
    port: int = 8080
    env: Literal["development", "production"] = "development"

    # LLM (via LiteLLM — model string like "gpt-4o", "claude-sonnet-4-20250514", etc.)
    llm_model: str = "gpt-4o"
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    # Agent
    agent_max_iterations: int = 25
    agent_system_prompt_file: str = "prompts/system.md"

    # Permissions
    permission_mode: Literal["ask", "auto", "strict"] = "ask"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parent.parent


settings = Settings()
