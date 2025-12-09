# Hooks

## What Are Hooks?

Code that runs at specific events in Claude Code.

```
┌──────────────┐
│ Event occurs │ (e.g., session starts)
└──────┬───────┘
       ▼
┌──────────────┐
│  Hook runs   │ (your script)
└──────┬───────┘
       ▼
┌──────────────┐
│   Continue   │ (or block)
└──────────────┘
```

## Hook Types

| Hook | When it runs |
|------|--------------|
| `SessionStart` | When Claude Code starts |
| `PreToolUse` | Before Claude uses a tool |
| `PostToolUse` | After Claude uses a tool |
| `Stop` | When conversation ends |
| `Notification` | When Claude sends notification |

## Configuration

In Claude Code settings (`~/.config/claude-code/settings.json`):

```json
{
  "hooks": {
    "SessionStart": [
      {
        "command": "echo 'Session started at $(date)' >> ~/claude-log.txt"
      }
    ]
  }
}
```

Or project-level in `.claude/settings.json`.

## Hook Structure

```json
{
  "hooks": {
    "HookType": [
      {
        "command": "shell command to run",
        "timeout": 5000,
        "blocking": true
      }
    ]
  }
}
```

### Fields

| Field | Default | Description |
|-------|---------|-------------|
| `command` | Required | Shell command |
| `timeout` | 5000 | Max ms to wait |
| `blocking` | false | Wait for completion? |

## Example: Session Logger

Log when sessions start:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "command": "echo \"$(date): Session in $(pwd)\" >> ~/.claude-sessions.log"
      }
    ]
  }
}
```

## Example: Pre-Tool Validation

Run checks before certain tools:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "command": "if [ \"$TOOL_NAME\" = \"Bash\" ]; then echo 'Bash command: $TOOL_INPUT' >> ~/bash-audit.log; fi",
        "blocking": false
      }
    ]
  }
}
```

## Environment Variables in Hooks

Hooks receive context via environment variables:

### SessionStart
- `$CWD` — current directory

### PreToolUse / PostToolUse
- `$TOOL_NAME` — tool being used (Read, Write, Bash, etc.)
- `$TOOL_INPUT` — JSON input to tool

## Blocking vs Non-Blocking

### Blocking (`"blocking": true`)
- Claude waits for hook to complete
- Can prevent tool use if hook fails (exit code != 0)
- Use for validation

### Non-Blocking (`"blocking": false`)
- Runs in background
- Claude continues immediately
- Use for logging, notifications

## Example: Block Dangerous Commands

Prevent certain bash commands:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "command": "if [ \"$TOOL_NAME\" = \"Bash\" ] && echo \"$TOOL_INPUT\" | grep -q 'rm -rf'; then exit 1; fi",
        "blocking": true
      }
    ]
  }
}
```

If hook exits with code 1, tool use is blocked.

## Exercise: Create a Session Hook

### Step 1: Create settings file

`.claude/settings.json`:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "command": "echo \"🚀 Claude Code session started at $(date)\" && echo \"📁 Working in: $(pwd)\""
      }
    ]
  }
}
```

### Step 2: Restart Claude Code

### Step 3: Verify
You should see the echo output when Claude Code starts.

## Advanced: Hook Scripts

For complex logic, use a script:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "command": "./.claude/hooks/session-start.sh"
      }
    ]
  }
}
```

`.claude/hooks/session-start.sh`:
```bash
#!/bin/bash

# Check for uncommitted changes
if [ -d .git ]; then
  CHANGES=$(git status --porcelain | wc -l)
  if [ "$CHANGES" -gt 0 ]; then
    echo "⚠️  You have $CHANGES uncommitted changes"
  fi
fi

# Remind about daily standup
HOUR=$(date +%H)
if [ "$HOUR" -ge 9 ] && [ "$HOUR" -lt 10 ]; then
  echo "📝 Time for standup?"
fi
```

## Use Cases

| Use Case | Hook Type | Example |
|----------|-----------|---------|
| Audit logging | PreToolUse | Log all bash commands |
| Safety checks | PreToolUse (blocking) | Block dangerous operations |
| Notifications | PostToolUse | Slack alert on deploy |
| Context loading | SessionStart | Show project status |
| Cleanup | Stop | Save session notes |

## Tips

- Start with non-blocking hooks
- Test commands manually first
- Use timeout for slow scripts
- Check exit codes for blocking hooks
