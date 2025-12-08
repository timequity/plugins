#!/usr/bin/env python3
"""
TDD Gate Hook - Enforces Test-Driven Development workflow.

Blocks rust-developer agent if no failing test is referenced.

Usage in .claude/settings.json:
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Task",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/tdd_gate.py"
          }
        ]
      }
    ]
  }
}
"""

import json
import re
import sys


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Not valid JSON, allow
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Only check Task tool
    if tool_name != "Task":
        sys.exit(0)

    subagent_type = tool_input.get("subagent_type", "")
    prompt = tool_input.get("prompt", "")

    # Only enforce for rust-developer (or similar dev agents)
    dev_agents = ["rust-developer", "vibe-coder:rust-developer"]
    if not any(agent in subagent_type for agent in dev_agents):
        sys.exit(0)

    # Check if TDD indicators present
    tdd_indicators = [
        r"failing test",
        r"test.*pass",
        r"make.*green",
        r"\.rs.*test",
        r"test_\w+",
        r"#\[test\]",
        r"cargo test",
        r"RED.*GREEN",
        r"tdd-test-writer",
    ]

    prompt_lower = prompt.lower()
    for pattern in tdd_indicators:
        if re.search(pattern, prompt_lower, re.IGNORECASE):
            # TDD indicator found, allow
            sys.exit(0)

    # Check if this is project creation (allowed without test)
    creation_indicators = [
        r"cargo new",
        r"create.*project",
        r"new.*project",
        r"initialize",
        r"setup.*project",
    ]

    for pattern in creation_indicators:
        if re.search(pattern, prompt_lower, re.IGNORECASE):
            # Project creation, allow
            sys.exit(0)

    # No TDD indicator found - BLOCK
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "TDD VIOLATION: No failing test referenced. "
                    "Use tdd-test-writer first to create a failing test, "
                    "then reference it when calling rust-developer.",
                }
            }
        )
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
