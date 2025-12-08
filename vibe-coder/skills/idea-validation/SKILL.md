---
name: idea-validation
description: |
  Simple conversation to understand what the user wants to build.
  Use when: user describes an app idea, wants to create something new.
  Triggers: "I want to build", "create app", "make website", "build MVP",
  "хочу создать", "сделать приложение".
---

# Idea Validation

Understand what the user wants without technical jargon.

## Questions (ask one at a time)

1. **What problem does this solve?**
   - "What's frustrating about the current way?"
   - One sentence answer is enough

2. **Who has this problem?**
   - "Who would use this daily?"
   - Specific person, not "everyone"

3. **What's the first thing they'd do?**
   - "When they open the app, what happens?"
   - Core action, not features list

4. **How do they know it worked?**
   - "What does success look like?"
   - Concrete outcome

## Output

Internal PRD (user doesn't see):

```markdown
## Problem
[One sentence]

## User
[Specific persona]

## Core Action
[Primary workflow]

## Success Metric
[How user knows it worked]
```

## Rules

- **No technical questions** — user shouldn't choose database or framework
- **One question at a time** — don't overwhelm
- **Accept short answers** — "for me" is valid for "who uses it"
- **Move fast** — 4 questions max, then start building
