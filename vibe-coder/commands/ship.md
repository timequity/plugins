---
description: From idea to working app in one command
---

# Ship: Idea -> Working App

User wants to build: $ARGUMENTS

Complete automation: validate idea, create project, implement all features, verify quality.

## Phase 1: Idea Validation

### Step 1.1: Identify Project Type

First, determine project type. If obvious from description, confirm. Otherwise ask:

```
question: "Какой тип проекта?"
header: "Type"
options:
  - label: "Web App (SaaS)"
    description: "Веб-приложение с UI"
  - label: "Telegram Bot"
    description: "Бот для Telegram"
  - label: "REST/GraphQL API"
    description: "Backend сервис"
  - label: "CLI Tool"
    description: "Консольная утилита"
# Other: Mobile App, Discord Bot, Library, Data Pipeline, Browser Extension
```

### Step 1.2: Offer Brainstorm (based on complexity)

| Signal | Action |
|--------|--------|
| Description < 10 words | Suggest brainstorm |
| Complex type (Telegram, Mobile) | Suggest brainstorm |
| Detailed description | Suggest skip |
| User says "быстро"/"simple" | Auto-skip |

```
question: "Хочешь уточнить идею через brainstorm?"
header: "Brainstorm"
options:
  - label: "Да, давай уточним"
    description: "Детальные вопросы -> полный PRD"
  - label: "Нет, идея понятна"
    description: "Быстрые вопросы -> минимальный PRD"
  - label: "Частично"
    description: "Ключевые вопросы только"
```

### Step 1.3: Core Questions (always ask)

1. **Problem** — "Какую проблему это решает?" (3-4 contextual options)
2. **User** — "Кто будет этим пользоваться?" (Для себя / Команда / Публичный сервис)
3. **Core Action** — "Что первое делает пользователь?" (3-4 contextual options)
4. **Success** — "Как понять что сработало?" (3-4 contextual options)

### Step 1.4: Type-Specific Questions (if brainstorm enabled)

**Telegram Bot:**
- Interaction style (commands/dialog/buttons)
- Database needed?
- External integrations?

**Web App:**
- Auth needed?
- Realtime features?

**API:**
- Public or internal?
- Auth method?

**CLI:**
- Interactive or one-shot?
- Output format?

### Step 1.5: Constraints (if full brainstorm)

```
question: "Есть ли ограничения?"
header: "Constraints"
multiSelect: true
options:
  - label: "Бесплатные сервисы only"
  - label: "Быстрый MVP (< 1 недели)"
  - label: "Scale 1000+ пользователей"
  - label: "Нет ограничений"
```

### Step 1.6: Create PRD

Based on brainstorm choice, create appropriate PRD:
- Skip brainstorm -> Minimal PRD
- Partial brainstorm -> Standard PRD
- Full brainstorm -> Full PRD

Save to `docs/PRD.md`

### Step 1.7: Validate PRD

```bash
python3 ~/.claude/skills/idea-validation/scripts/validate_prd.py --path .
```

## Phase 1.5: Design Preferences

**Applies to:** Web App, Mobile App, Browser Extension, Telegram Bot (with Web App UI)

**Skip for:** REST API, GraphQL API, CLI Tool, Data Pipeline, Library

### Step 1.5.1: Check if UI Project

If project type has UI, proceed with design questions. Otherwise skip to Phase 2.

### Step 1.5.2: Design Priority

```
question: "Насколько важен дизайн?"
header: "Design"
options:
  - label: "Профессиональный"
    description: "Уникальный стиль, впечатляет"
  - label: "Функциональный"
    description: "Чистый и понятный"
  - label: "MVP - потом"
    description: "Работает -> достаточно"
```

**If "MVP - потом"** -> Use defaults (Modern Minimalist, system fonts, no animations), skip to Phase 2.

### Step 1.5.3: Aesthetic Direction

```
question: "Какой визуальный стиль?"
header: "Style"
options:
  - label: "Minimalist"
    description: "Пространство, чистые линии"
  - label: "Bold & Modern"
    description: "Яркие акценты, современный"
  - label: "Soft & Friendly"
    description: "Округлые формы, мягкие тона"
  - label: "Dark & Professional"
    description: "Тёмная тема, серьёзный"
```

### Step 1.5.4: Theme Selection

Based on aesthetic, offer 2-3 matching themes from theme-factory:

| Direction | Themes |
|-----------|--------|
| Minimalist | Modern Minimalist, Arctic Frost |
| Bold & Modern | Tech Innovation, Sunset Boulevard |
| Soft & Friendly | Desert Rose, Botanical Garden |
| Dark & Professional | Ocean Depths, Midnight Galaxy |

```
question: "Какая цветовая схема?"
header: "Theme"
options:
  - label: "{Theme 1} ({primary color})"
  - label: "{Theme 2} ({primary color})"
  - label: "Custom"
    description: "Свои цвета"
```

### Step 1.5.5: Animation Level

```
question: "Сколько анимации?"
header: "Motion"
options:
  - label: "Subtle (hover only)"
  - label: "Moderate (transitions)"
  - label: "Rich (page animations)"
  - label: "None"
```

### Step 1.5.6: Create DESIGN.md

Save design specification to `docs/DESIGN.md`:

```markdown
# Design Specification

## Theme: {theme name}
- Primary: {hex}
- Secondary: {hex}
- Accent: {hex}
- Background: {hex}

## Fonts
- Headers: {font}
- Body: {font}

## Motion Level: {level}
```

## Phase 2: Project Setup

### Step 2.1: Ask Stack

```
question: "Какой стек?"
header: "Stack"
options:
  - label: "Rust + HTMX (Recommended)"
    description: "Быстрый fullstack"
  - label: "Rust API only"
    description: "Без UI"
  - label: "Python + FastAPI"
    description: "Python backend"
  - label: "Node.js"
    description: "JavaScript/TypeScript"
```

### Step 2.2: Initialize Project

Based on stack choice:
- Rust: Run `Task[rust-project-init]`
- Python: Run `Task[python-project-init]`
- Node: Run `Task[node-project-init]`

Agent reads `docs/PRD.md` + `docs/DESIGN.md` and creates:
- Project structure
- Dependencies
- Health endpoint with test
- UI templates with selected theme (colors as CSS variables)
- Fonts configured in base styles
- Motion level applied to components
- Beads issues from PRD features

## Phase 3: TDD Implementation

Loop until all features done:

1. **Get next issue**:
   ```bash
   bd ready --limit=1
   ```

2. **If issue exists**:
   - Run `Task[tdd-test-writer]` — RED phase (write failing test)
   - Run `Task[rust-developer]` — GREEN phase (implement to pass)
   - Close issue: `bd close <id>`

3. **Repeat until no issues ready**

## Phase 4: Verification Gate

1. **Security scan**:
   ```bash
   python3 ~/.claude/skills/security-check/scripts/security_scan.py --path . --threshold medium
   ```

2. **Quality gate**:
   ```bash
   python3 ~/.claude/skills/verification-gate/scripts/verify.py --path .
   ```

3. **If issues found**: fix and re-run

## Phase 5: Ship It

1. **Final status**:
   ```
   ## Shipped: {project-name}

   Type: {project type}
   Features: {count} implemented
   Tests: all passing
   Security: clean

   Run: cargo run (or appropriate command)

   Next:
     - /add - Add more features
     - /deploy - Deploy to production
   ```
