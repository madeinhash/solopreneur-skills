---
description: Recommended Claude Code permission settings for development. Allows most commands freely, blocks destructive rm operations.
---

## Claude Code Permission Setup

Add this to your project's `.claude/settings.local.json` to avoid constant permission prompts during development:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm *)",
      "Bash(npx *)",
      "Bash(node *)",
      "Bash(python *)",
      "Bash(pip *)",
      "Bash(pytest *)",
      "Bash(git *)",
      "Bash(gh *)",
      "Bash(cat *)",
      "Bash(ls *)",
      "Bash(find *)",
      "Bash(grep *)",
      "Bash(rg *)",
      "Bash(mkdir *)",
      "Bash(touch *)",
      "Bash(cp *)",
      "Bash(mv *)",
      "Bash(chmod *)",
      "Bash(echo *)",
      "Bash(pwd)",
      "Bash(which *)",
      "Bash(env *)",
      "Bash(export *)",
      "Bash(source *)",
      "Bash(cd *)",
      "Bash(head *)",
      "Bash(tail *)",
      "Bash(wc *)",
      "Bash(sort *)",
      "Bash(uniq *)",
      "Bash(diff *)",
      "Bash(curl *)",
      "Bash(wget *)",
      "Bash(docker *)",
      "Bash(docker-compose *)",
      "Bash(seq *)",
      "Bash(timeout *)",
      "Bash(tsc *)",
      "Bash(ruff *)",
      "Bash(mypy *)",
      "Bash(uvicorn *)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(rm -r /*)",
      "Bash(sudo rm *)",
      "Bash(rm -rf /)"
    ]
  }
}
```

This allows all common development commands while blocking destructive `rm` operations.
