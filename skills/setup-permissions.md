---
description: Recommended Claude Code permission settings for development. Allows most commands freely, blocks destructive rm operations.
---

## Claude Code Permission Setup

Add this to your project's `.claude/settings.local.json` to avoid constant permission prompts during development:

```json
{
  "permissions": {
    "allow": [
      "Bash(*)",
      "Read(*)",
      "Write(*)",
      "Edit(*)"
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
