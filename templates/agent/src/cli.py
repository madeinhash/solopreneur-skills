"""Interactive CLI — terminal interface for the agent.

Mirrors Claude Code's REPL experience:
- Rich terminal output with colors
- Interactive permission prompts (ask mode)
- Skill invocation via /skill-name
- Tool call visibility
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from src.config import settings
from src.engine.agent_loop import AgentLoop, EventType
from src.logger import logger
from src.permissions.checker import PermissionChecker
from src.skills import load_skills
from src.tools import get_tool_registry

console = Console()


async def interactive_permission_callback(tool_name: str, args: dict[str, Any], reason: str) -> bool:
    """Prompt user for permission in the terminal."""
    console.print()
    console.print(Panel(
        f"[bold yellow]Tool:[/] {tool_name}\n"
        f"[bold yellow]Args:[/] {json.dumps(args, indent=2, ensure_ascii=False)[:500]}\n"
        f"[bold yellow]Reason:[/] {reason}",
        title="[bold red]Permission Required[/]",
        border_style="red",
    ))
    response = input("Allow? (y/n): ").strip().lower()
    return response in ("y", "yes")


async def run_cli() -> None:
    registry = get_tool_registry()
    permission_checker = PermissionChecker()
    skills = load_skills()
    session_messages: list[dict[str, Any]] = []

    console.print(Panel(
        f"[bold]Agent CLI[/] — model: {settings.llm_model} | mode: {settings.permission_mode}\n"
        f"Tools: {', '.join(registry.names())}\n"
        f"Skills: {', '.join(f'/{name}' for name in skills) or '(none)'}\n\n"
        "Type your message, /skill-name to invoke a skill, or 'exit' to quit.",
        title="[bold cyan]Agent Service[/]",
        border_style="cyan",
    ))

    while True:
        try:
            console.print()
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye.[/]")
            break

        if not user_input:
            continue
        if user_input.lower() == "exit":
            console.print("[dim]Goodbye.[/]")
            break

        # Handle skill invocation: /skill-name [args]
        if user_input.startswith("/"):
            parts = user_input[1:].split(" ", 1)
            skill_name = parts[0]
            skill_args = parts[1] if len(parts) > 1 else ""
            if skill_name in skills:
                skill = skills[skill_name]
                user_input = f"{skill.prompt}\n\n{skill_args}".strip()
                console.print(f"[dim]Invoking skill: {skill_name}[/]")
            else:
                console.print(f"[red]Unknown skill: /{skill_name}[/]")
                console.print(f"[dim]Available: {', '.join(f'/{n}' for n in skills)}[/]")
                continue

        loop = AgentLoop(
            registry=registry,
            permission_checker=permission_checker,
            permission_callback=interactive_permission_callback,
        )

        async for event in loop.run(user_input, session_messages=session_messages):
            if event.type == EventType.TOOL_CALL:
                tool_name = event.data["tool"]
                console.print(f"\n[dim]  Tool: {tool_name}[/]")

            elif event.type == EventType.TOOL_RESULT:
                output = event.data["output"]
                is_error = event.data.get("is_error", False)
                style = "red" if is_error else "dim"
                # Show truncated output
                display = output[:300] + "..." if len(output) > 300 else output
                console.print(f"  [{style}]{display}[/{style}]")

            elif event.type == EventType.ASSISTANT_MESSAGE:
                content = event.data.get("content", "")
                if content:
                    console.print()
                    console.print(Markdown(content))

            elif event.type == EventType.ERROR:
                console.print(f"\n[bold red]Error:[/] {event.data.get('error', '')}")

            elif event.type == EventType.DONE:
                pass

        # Persist conversation for multi-turn
        session_messages = loop.messages


def main() -> None:
    asyncio.run(run_cli())


if __name__ == "__main__":
    main()
