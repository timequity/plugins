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

### Step 7: Design Preferences (UI projects only)

**If project type has UI** (Web App, Mobile, Browser Extension, Telegram with Web App):

```
question: "Насколько важен дизайн?"
header: "Design"
options:
  - label: "Профессиональный"
    description: "Уникальный стиль"
  - label: "Функциональный"
    description: "Чистый и понятный"
  - label: "MVP - потом"
    description: "Работает -> достаточно"
```

**If not MVP**, ask:
1. Aesthetic direction (Minimalist / Bold / Soft / Dark)
2. Theme selection (2-3 options from theme-factory)
3. Animation level (Subtle / Moderate / Rich / None)

Save to `docs/DESIGN.md`

**If MVP or non-UI project** -> Skip design questions

### Step 8: Next Steps

```
PRD saved to docs/PRD.md
{Design saved to docs/DESIGN.md}  # if UI project

Summary:
- Type: {project type}
- Features: {count}
- Complexity: {minimal/standard/full}
- Design: {theme name} / MVP defaults / N/A

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
