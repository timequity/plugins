# /ccc:progress — Detailed Progress

Shows detailed course completion statistics.

## Syntax

```
/ccc:progress
```

## Algorithm

### 1. Load Progress

Use `progress-manager` skill:
```bash
cat "$HOME/.claude-course/progress.json"
```

### 2. Display Detailed Statistics

```
# Your Claude Code Course Progress

## Overall Progress

████████░░░░░░░░░░░░ 40% (2/5 lessons)

Started: January 15, 2025
Time spent: ~45 minutes

## Lessons

### Lesson 1: Claude Code Basics
Status: ✓ Completed
Started: Jan 15, 10:00
Completed: Jan 15, 10:15
Practice: 1 attempt

### Lesson 2: Your First Skill
Status: ● In Progress
Started: Jan 15, 10:20
Theory: ✓ read
Practice: ○ not completed (2 attempts)

### Lessons 3-5
Status: ○ Not started

## What's Next?

Continue lesson 2 — practice remaining.
`/ccc:practice` — complete task
```

### 3. Time Calculation

Approximate time:
- From `started_at` of first lesson to `completed_at` of last completed
- Or to current time if course not finished

### 4. If No Progress

```
# Progress

You haven't started the course yet.

Type `/ccc:course` to begin learning!
```

### 5. If Course Completed

```
# Congratulations!

████████████████████ 100% — Course completed!

You've mastered:
- Claude Code basics
- Creating skills
- Working with agents
- Hooks and automation
- Building applications

Started: January 15, 2025
Completed: January 15, 2025
Total time: ~2 hours

What's next?
- Create your first plugin
- Explore marketplace
- Help others — share your experience
```

## Date Formats

- Full: "January 15, 2025, 10:30"
- Short: "Jan 15"
- Relative: "today", "yesterday"
