---
name: course-help
description: |
  Help and navigation for Claude Code Course.
  Use when: user asks about the course, lessons, or progress.
  Triggers: "help", "course help", "what lessons", "my progress".
---

# Claude Code Course

Interactive course to master Claude Code in 5 hands-on lessons.

## Lessons Overview

| # | Lesson | Duration | Topics |
|---|--------|----------|--------|
| 1 | Основы Claude Code | 15 min | CLI, commands, prompting |
| 2 | Твой первый скилл | 20 min | SKILL.md, triggers, structure |
| 3 | Агенты-помощники | 25 min | Agents, Task tool, automation |
| 4 | Хуки и автоматизация | 20 min | Hooks, pre-commit, workflows |
| 5 | Собираем приложение | 30 min | Full project from scratch |

## Commands

| Command | Description |
|---------|-------------|
| `/course` | Start or continue the course |
| `/course lesson 1` | Go to specific lesson |
| `/course practice` | Practice current lesson |
| `/course progress` | Show your progress |
| `/course reset` | Reset progress and start over |

## How It Works

1. **Theory** — Short explanation with examples
2. **Practice** — Hands-on task in your terminal
3. **Check** — Verify you completed the task
4. **Next** — Move to next lesson

## Progress Tracking

Your progress is saved in `~/.claude-course/progress.json`.
You can continue from where you left off.

## Tips

- Complete lessons in order (they build on each other)
- Practice tasks are done in YOUR terminal
- Ask questions anytime — the tutor agent helps
- Each lesson takes 15-30 minutes
