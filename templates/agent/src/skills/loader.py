"""Skill system — markdown-based reusable prompts.

Mirrors Claude Code's Skill/Command system:
- Skills are markdown files in the skills/ directory
- Each skill has optional YAML frontmatter (description, model, allowed_tools)
- Skills can be invoked by name, expanding into the agent's prompt

Example skill file (skills/review-code.md):
    ---
    description: Review code for bugs and improvements
    allowed_tools: [read_file, glob, grep]
    ---
    Review the following code for bugs, security issues, and improvements...
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.logger import logger


@dataclass
class Skill:
    name: str
    description: str
    prompt: str
    allowed_tools: list[str] = field(default_factory=list)
    model: str | None = None
    source_path: Path | None = None


def load_skills(skills_dir: Path | None = None) -> dict[str, Skill]:
    """Load all skill files from the skills directory."""
    if skills_dir is None:
        skills_dir = Path(__file__).resolve().parent.parent.parent / "skills"

    if not skills_dir.exists():
        return {}

    skills: dict[str, Skill] = {}
    for path in sorted(skills_dir.glob("*.md")):
        try:
            skill = _parse_skill_file(path)
            skills[skill.name] = skill
            logger.debug("skill_loaded", name=skill.name, path=str(path))
        except Exception as e:
            logger.warn("skill_load_error", path=str(path), error=str(e))

    return skills


def _parse_skill_file(path: Path) -> Skill:
    """Parse a skill markdown file with optional YAML frontmatter."""
    content = path.read_text()
    name = path.stem  # filename without .md

    # Parse frontmatter
    frontmatter: dict[str, Any] = {}
    prompt = content
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if fm_match:
        fm_text, prompt = fm_match.groups()
        # Simple YAML-like parsing (avoid pyyaml dependency)
        for line in fm_text.strip().splitlines():
            line = line.strip()
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                val = val.strip()
                # Handle list values: [a, b, c]
                if val.startswith("[") and val.endswith("]"):
                    val = [v.strip().strip("'\"") for v in val[1:-1].split(",")]
                frontmatter[key] = val

    return Skill(
        name=name,
        description=frontmatter.get("description", f"Skill: {name}"),
        prompt=prompt.strip(),
        allowed_tools=frontmatter.get("allowed_tools", []),
        model=frontmatter.get("model"),
        source_path=path,
    )
