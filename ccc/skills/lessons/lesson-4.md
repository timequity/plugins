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

Now I'll demonstrate creating a hook.

**Task:** Create a hook that logs when files are edited.

**Watch me do it:**

---

## Practice Execution

**IMPORTANT:** As the tutor, YOU (Claude) must execute this practice, not the user.

1. Create the settings file with hook:

```bash
mkdir -p .claude
cat > .claude/settings.json << 'EOF'
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"[$(date +%H:%M:%S)] Edited: $CLAUDE_FILE_PATH\" >> .claude/edit.log"
          }
        ]
      }
    ]
  }
}
EOF
```

2. Show the user what was created:
```bash
cat .claude/settings.json
```

3. Explain and congratulate:
```
✓ Practice completed!

I created a hook in .claude/settings.json

This hook:
- Triggers after every Edit operation
- Logs the file path and timestamp to .claude/edit.log

Hook structure:
- matcher: which tool triggers it (Edit, Write, Bash, *)
- type: "command" to run shell commands
- command: what to execute

Ready for Lesson 5? Type `/ccc:lesson 5` or say "next"
```

**After execution:**
- Update progress: `practice_completed: true`, `current_lesson: 5`
- Clean up: `rm -rf .claude/settings.json .claude/edit.log` (demo only)
