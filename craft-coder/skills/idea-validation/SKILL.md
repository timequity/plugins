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

## Questions (use AskUserQuestion tool with options)

Use AskUserQuestion tool for each question. Always provide 3-4 relevant options based on the idea context.

**Q1: Problem**
```
question: "Какую проблему это решает?"
header: "Problem"
options:
  - label: "[contextual option 1]"
    description: "Based on idea"
  - label: "[contextual option 2]"
    description: "Based on idea"
  - label: "[contextual option 3]"
    description: "Based on idea"
# User can always select "Other" to type custom answer
```

**Q2: User**
```
question: "Кто будет этим пользоваться?"
header: "User"
options:
  - label: "Для себя"
    description: "Личное использование"
  - label: "AI агенты"
    description: "Через API/MCP"
  - label: "Команда"
    description: "Совместная работа"
```

**Q3: Core Action**
```
question: "Что первое делает пользователь?"
header: "Action"
options:
  - label: "[contextual action 1]"
    description: "Based on idea"
  - label: "[contextual action 2]"
    description: "Based on idea"
  - label: "[contextual action 3]"
    description: "Based on idea"
```

**Q4: Success**
```
question: "Как понять что сработало?"
header: "Success"
options:
  - label: "[contextual outcome 1]"
    description: "Based on idea"
  - label: "[contextual outcome 2]"
    description: "Based on idea"
  - label: "[contextual outcome 3]"
    description: "Based on idea"
```

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
