---
description: Work on next ready issue (TDD cycle)
---

# Next Issue (TDD Cycle)

Work on the next ready issue from beads.

## Process

1. **Find ready issue**:
   ```bash
   bd ready --limit=1
   ```

2. **If no issues**:
   ```
   All features complete!

   Next:
     • /review — Code review
     • bd create "New feature" — Add feature
   ```

3. **If issue found**:
   - Show issue details
   - Run Task[tdd-test-writer] for RED phase
   - Run Task[rust-developer] for GREEN phase

4. **Show progress after completion**:
   ```
   ## Completed: {issue-id}

   Progress: {closed}/{total} features

   Next:
     • /next — Continue with next feature
     • /review — Code review
     • /status — Full progress
   ```
