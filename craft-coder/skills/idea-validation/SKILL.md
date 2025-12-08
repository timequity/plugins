---
name: idea-validation
description: |
  Validate idea and create PRD. Saves docs/PRD.md to project.
  Use when: user describes an app idea, wants to create something new.
  Triggers: "I want to build", "create app", "make website", "build MVP",
  "хочу создать", "сделать приложение".
---

# Idea Validation

Understand what the user wants. Save to `docs/PRD.md`.

## Questions (ask one at a time)

1. **What problem does this solve?**
   - "What's frustrating about the current way?"

2. **Who has this problem?**
   - "Who would use this daily?"

3. **What's the first thing they'd do?**
   - "When they open the app, what happens?"

4. **How do they know it worked?**
   - "What does success look like?"

## After Questions

Create `docs/PRD.md`:

```markdown
# [Project Name] PRD

## Problem
[One sentence from Q1]

## User
[Specific persona from Q2]

## Core Action
[Primary workflow from Q3]

## Success Metric
[Outcome from Q4]

## Features (to be detailed)
- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3

---
Generated: [date]
Status: Draft
```

Then say:
```
PRD saved to docs/PRD.md

Next: Task[rust-project-init] (creates project + beads issues from PRD)
```

## Rules

- **No technical questions** — user chooses nothing technical
- **One question at a time** — don't overwhelm
- **Save PRD.md** — always persist, never internal-only
- **Move fast** — 4 questions max
