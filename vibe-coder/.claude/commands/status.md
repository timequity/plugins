---
description: Show project progress and next actions
---

# Project Status

Show current project progress and available actions.

## Process

1. **Get beads stats**:
   ```bash
   bd stats
   bd list
   bd ready
   ```

2. **Show visual progress**:
   ```
   ## Project: {name}

   Progress: ████████░░ {percent}% ({closed}/{total})

   Completed:
     ✓ Feature 1
     ✓ Feature 2

   In Progress:
     ⏳ Feature 3

   Ready:
     ○ Feature 4
     ○ Feature 5

   Blocked:
     ⊘ Feature 6 (blocked by Feature 4)
   ```

3. **Show next actions**:
   ```
   Actions:
     • /next — Work on next feature
     • /review — Code review
     • /add "feature" — Add new feature
   ```

4. **Show test status**:
   ```bash
   cargo test --lib 2>&1 | tail -3
   ```
