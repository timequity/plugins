# Lesson 4: Hooks and Automation

**Time:** ~20 minutes

## Learning Goals

After this lesson you will:
- Understand what hooks are and why they're useful
- Know hook types and when to use them
- Create a hook for auto-formatting
- Automate routine tasks

---

## What Are Hooks?

A **hook** is a command that automatically executes at a specific moment.

Example: every time Claude edits a file, automatically run formatting. That's a hook!

```
Claude: [Edit file]
  ↓
Hook: [Runs prettier]
  ↓
Result: file is formatted
```

---

## Hook Types

| Type | When it triggers |
|------|------------------|
| `PreToolUse` | BEFORE using a tool |
| `PostToolUse` | AFTER using a tool |
| `Notification` | On events (session start, etc.) |

### PreToolUse

Executes before tool. Can:
- Add information to context
- Block action (if returns error)

### PostToolUse

Executes after tool. Can:
- Process result
- Run additional commands

---

## Where Hooks Are Configured

In file `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATH"
          }
        ]
      }
    ]
  }
}
```

---

## Hook Structure

```json
{
  "matcher": "Edit",          // Which tool
  "hooks": [
    {
      "type": "command",      // Type: command
      "command": "command"    // What to execute
    }
  ]
}
```

### Matcher

Which tool to watch:
- `"Edit"` — file editing
- `"Write"` — file creation
- `"Bash"` — command execution
- `"*"` — any tool

### Environment Variables

| Variable | Description |
|----------|-------------|
| `$CLAUDE_FILE_PATH` | File path |
| `$CLAUDE_TOOL_NAME` | Tool name |
| `$CLAUDE_TOOL_INPUT` | Input data (JSON) |

---

## Example: Format After Edit

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

**What happens:**
1. Claude edits file
2. Hook runs prettier
3. File is automatically formatted

---

## Example: Check Before Commit

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'git commit'; then npm test || exit 1; fi"
          }
        ]
      }
    ]
  }
}
```

**What happens:**
1. Claude wants to git commit
2. Hook runs tests
3. If tests fail — commit is blocked

---

## Blocking Actions

If hook returns non-zero exit code — action is blocked:

```json
{
  "type": "command",
  "command": "exit 1"  // Blocks action
}
```

Use for:
- Checking before dangerous operations
- Validating input data
- Protecting critical files

---

## Summary

- Hooks = automatic actions
- PreToolUse — before, PostToolUse — after
- Configured in `.claude/settings.json`
- Can block actions (exit 1)

---

## Practice

**Task:** Create a hook that shows notification after file creation.

**Requirements:**
1. Type: PostToolUse
2. Matcher: Write
3. Command: `echo "Created file: $CLAUDE_FILE_PATH"`

**Steps:**
1. Create or edit `.claude/settings.json`
2. Add hooks section
3. Configure PostToolUse for Write

**Verification:**
After creating, ask me to create any file — a message should appear.

<details>
<summary>Hint</summary>

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"✓ Created file: $CLAUDE_FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

</details>

When done, say "done" and I'll verify the result.

---

## Practice Verification

When user says "done", run verification:

```bash
# Lesson 4 check
SETTINGS_FILE=".claude/settings.json"
if [ -f "$SETTINGS_FILE" ]; then
  # Check for hooks section
  if grep -q '"hooks"' "$SETTINGS_FILE" && \
     grep -q '"PostToolUse"' "$SETTINGS_FILE"; then
    echo "✓ Hooks configured!"
  else
    echo "✗ File exists but missing hooks/PostToolUse section"
  fi
else
  echo "✗ File .claude/settings.json not found"
fi
```

**On success:**
- Update progress: `practice_completed: true`
- Show congratulations and suggest moving to lesson 5

**On failure:**
- Explain settings.json structure
- Show minimal example with hooks
