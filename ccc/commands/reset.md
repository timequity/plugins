# /ccc:course:reset — Reset Progress

Deletes all progress and starts course from scratch.

## Syntax

```
/ccc:course:reset
```

## Algorithm

### 1. Request Confirmation

```
Are you sure you want to reset progress?

This will delete:
- All completed lessons
- Attempt statistics
- Course start date

Type "yes" to confirm or "no" to cancel.
```

### 2. On Confirmation

```bash
rm -f "$HOME/.claude-course/progress.json"
```

And show:
```
Progress reset.

Ready to start over? Type `/ccc:course`
```

### 3. On Cancel

```
Reset cancelled. Your progress is saved.

Current lesson: {N}
Continue: `/ccc:course`
```

## Important

- Always ask for confirmation
- Don't delete automatically
- Show what will be deleted
