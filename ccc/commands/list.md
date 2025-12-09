# /ccc:list — List All Lessons

Shows all lessons with completion statuses.

## Syntax

```
/ccc:list
```

## Algorithm

### 1. Load Progress

```bash
cat "$HOME/.claude-course/progress.json" 2>/dev/null || echo '{}'
```

### 2. Show Lessons Table

```
# Claude Code Course Lessons

| # | Lesson | Time | Status |
|---|--------|------|--------|
| 1 | Claude Code Basics | ~15 min | ✓ |
| 2 | Your First Skill | ~20 min | ● |
| 3 | Agent Helpers | ~25 min | ○ |
| 4 | Hooks and Automation | ~20 min | ○ |
| 5 | Building an Application | ~30 min | ○ |

**Legend:** ✓ completed • ● in progress • ○ not started

Current: Lesson 2
Command: `/ccc:lesson 2` to continue
```

### 3. Statuses

| Symbol | Condition |
|--------|-----------|
| ✓ | `practice_completed: true` |
| ● | `started_at` exists but `practice_completed: false` |
| ○ | No entry in `lessons` |

### 4. If No Progress

```
# Claude Code Course Lessons

| # | Lesson | Time | Status |
|---|--------|------|--------|
| 1 | Claude Code Basics | ~15 min | ○ |
| 2 | Your First Skill | ~20 min | ○ |
| 3 | Agent Helpers | ~25 min | ○ |
| 4 | Hooks and Automation | ~20 min | ○ |
| 5 | Building an Application | ~30 min | ○ |

Start course: `/ccc:course`
```
