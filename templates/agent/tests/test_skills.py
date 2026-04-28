"""Unit tests for the skill loader."""

from pathlib import Path

from src.skills.loader import load_skills, _parse_skill_file


def test_load_builtin_skills():
    skills_dir = Path(__file__).resolve().parent.parent / "skills"
    skills = load_skills(skills_dir)
    assert "review-code" in skills
    assert "explain-code" in skills
    assert "refactor" in skills


def test_parse_skill_with_frontmatter(tmp_path: Path):
    skill_file = tmp_path / "test-skill.md"
    skill_file.write_text(
        "---\n"
        "description: A test skill\n"
        "allowed_tools: [read_file, bash]\n"
        "---\n"
        "Do something useful."
    )
    skill = _parse_skill_file(skill_file)
    assert skill.name == "test-skill"
    assert skill.description == "A test skill"
    assert skill.allowed_tools == ["read_file", "bash"]
    assert skill.prompt == "Do something useful."
