---
description: Add a new feature to current project
---

# Add Feature

Add a new feature to the current project.

## Process

1. **Create beads issue**:
   ```bash
   bd create --type=feature --title="$ARGUMENTS" --priority=1
   ```

2. **Ask about dependencies**:
   Use AskUserQuestion:
   ```
   question: "Эта фича зависит от других?"
   header: "Deps"
   options:
     - label: "Нет зависимостей"
       description: "Можно делать сразу"
     - label: "Зависит от существующей"
       description: "Выберу из списка"
   ```

3. **If dependencies needed**:
   - Show `bd list --status=open`
   - Ask which issue blocks this one
   - Run `bd dep add {new-issue} {blocker}`

4. **Show result**:
   ```
   ## Added: {issue-id}

   Title: $ARGUMENTS
   Priority: P1
   Dependencies: {deps or "none"}

   Next:
     • /next — Start working
     • /status — See all features
   ```
