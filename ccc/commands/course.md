# /ccc:course — Main Course Command

Command to start and continue the Claude Code course.

## Argument Handling

If user entered:
- `/ccc:course` — show progress and continue
- `/ccc:lesson N` — go to lesson N
- `/ccc:practice` — start practice for current lesson
- `/ccc:progress` — detailed progress
- `/ccc:reset` — reset progress
- `/ccc:help` — show help

## Algorithm

### 1. Load Progress

Use `progress-manager` skill to load:

```bash
PROGRESS_FILE="$HOME/.claude-course/progress.json"
if [ -f "$PROGRESS_FILE" ]; then
  cat "$PROGRESS_FILE"
else
  echo '{"version":"1.0.0","current_lesson":1,"lessons":{},"completed":false}'
fi
```

### 2. Show Welcome

**New user** (no file or current_lesson=1, lessons={}):

```
# Welcome to Claude Code Course!

Master Claude Code in 5 practical lessons — from basics to building a full application.

## Lessons

| # | Topic | Time |
|---|-------|------|
| 1 | Claude Code Basics | ~15 min |
| 2 | Your First Skill | ~20 min |
| 3 | Agent Helpers | ~25 min |
| 4 | Hooks and Automation | ~20 min |
| 5 | Building an Application | ~30 min |

Ready to start? Say "yes" or type `/ccc:lesson 1`
```

**Continuing user** (has progress):

```
# Claude Code Course

## Your Progress

[PROGRESS_BAR]

| # | Lesson | Status |
|---|--------|--------|
| 1 | Claude Code Basics | ✓ |
| 2 | Your First Skill | ● in progress |
| 3 | Agent Helpers | ○ |
| 4 | Hooks and Automation | ○ |
| 5 | Building an Application | ○ |

**Continue lesson 2?** Say "yes" or choose another lesson.
```

### 3. Progress Bar Generation

```
Completed: ████████░░ 2/5 (40%)
```

Formula: for each lesson with `practice_completed: true` — one filled block.

### 4. Lesson Statuses

| Status | Symbol | Condition |
|--------|--------|-----------|
| Completed | ✓ | `practice_completed: true` |
| In progress | ● | `theory_read: true` or `started_at` exists |
| Not started | ○ | No entry in `lessons` |

### 5. Handling "yes" Response

If user confirms:
1. Update progress: set `started_at` for current lesson
2. Redirect to `/ccc:lesson N` where N = current_lesson

## Auto-save Progress

**IMPORTANT:** Save progress automatically on every state change!

### Save Function

```bash
save_progress() {
  mkdir -p "$HOME/.claude-course"
  cat > "$HOME/.claude-course/progress.json" << 'PROGRESS'
$PROGRESS_JSON
PROGRESS
}
```

### When to Save

| Event | What to update |
|-------|----------------|
| Lesson started | `started_at`, `current_lesson` |
| Theory read | `theory_read: true` |
| Practice success | `practice_completed: true`, `completed_at`, `current_lesson++` |
| Practice failed | `practice_attempts++` |
| Course completed | `completed: true` |

## Communication Tone

- Friendly, supportive
- Use "you" informally
- Minimal emojis (max 1-2 per message)
- Short phrases, no fluff

## Examples

**User**: `/ccc:course`
**Response** (new): Show welcome with lessons table

**User**: `/ccc:course`
**Response** (continuing): Show progress bar and suggest continuing

**User**: `/ccc:reset`
**Response**: "Progress reset. Start over?" + delete progress file
