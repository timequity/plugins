---
description: Run code review and optionally create issues
---

# Code Review

Run code review and offer to create beads issues from findings.

## Process

1. **Run Task[rust-code-reviewer]**

2. **After review, ask user**:
   Use AskUserQuestion:
   ```
   question: "Создать issues из ревью?"
   header: "Issues"
   multiSelect: true
   options:
     - label: "{issue 1 title}"
       description: "{severity}: {brief description}"
     - label: "{issue 2 title}"
       description: "{severity}: {brief description}"
     ...
   ```

3. **Create selected issues**:
   ```bash
   bd create --type=task --title="{title}" --priority={1 for Important, 2 for Minor}
   ```

4. **Show result**:
   ```
   ## Review Complete

   Created {n} issues from review.

   Next:
     • /next — Work on issues
     • /status — See all issues
   ```
