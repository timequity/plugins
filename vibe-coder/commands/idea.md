---
description: Start building from a simple idea
---

# /idea - Validate and document your idea

Use the idea-validation skill to understand what the user wants to build.

## Flow

### Step 1: Identify Project Type

If not clear from user's description, ask:
```
question: "Какой тип проекта?"
header: "Type"
options:
  - Web App (SaaS)
  - Telegram Bot
  - REST/GraphQL API
  - CLI Tool
```

### Step 2: Offer Brainstorm

Based on complexity, offer deeper exploration:
- Short description -> suggest brainstorm
- Complex type (Telegram, Mobile) -> suggest brainstorm
- Detailed description -> suggest skip

### Step 3: Ask Core Questions

One question at a time:
1. **Problem** — "Какую проблему это решает?"
2. **User** — "Кто будет этим пользоваться?"
3. **Core Action** — "Что первое делает пользователь?"
4. **Success** — "Как понять что сработало?"

### Step 4: Type-Specific Questions (if brainstorm)

Ask additional questions based on project type.

### Step 5: Create PRD

Generate appropriate PRD:
- Skip brainstorm -> Minimal PRD (5 sections)
- Partial -> Standard PRD (8 sections)
- Full brainstorm -> Full PRD (12 sections)

Save to `docs/PRD.md`

### Step 6: Validate

```bash
python3 ~/.claude/skills/idea-validation/scripts/validate_prd.py --path .
```

### Step 7: Next Steps

```
PRD saved to docs/PRD.md

Summary:
- Type: {project type}
- Features: {count}
- Complexity: {minimal/standard/full}

Ready to start building?
  - /ship - Full automation
  - /build - Just build (skip validation)
```

## Rules

- Ask type FIRST — determines question flow
- One question at a time — don't overwhelm
- Adaptive depth — simple projects get simple PRD
- No technical jargon — user chooses nothing technical
- Always save PRD.md — never internal-only
