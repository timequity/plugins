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

1. Find validation script:
   ```
   Glob: **/skills/idea-validation/scripts/validate_prd.py
   ```

2. Run with found path:
   ```bash
   python3 {found_script_path} --path .
   ```

If script not found, skip validation (non-blocking).

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

## Phase 2.5: Project Validation (MANDATORY)

After project initialization, verify everything works before TDD:

### Step 2.5.1: Start App
```bash
cargo run &
APP_PID=$!
sleep 3
```

### Step 2.5.2: Verify Endpoints
```bash
# Health endpoint
curl -sf http://127.0.0.1:3000/health || echo "FAIL: /health"

# Static files (fullstack only)
curl -sf http://127.0.0.1:3000/static/styles.css > /dev/null || echo "FAIL: static files"

# Index page returns HTML
curl -sf http://127.0.0.1:3000/ | grep -q "<html" || echo "FAIL: index not HTML"

# All hx-* endpoints exist (parse from templates)
for endpoint in $(grep -rh "hx-get\|hx-post" templates/ 2>/dev/null | grep -oE '"[^"]*"' | tr -d '"' | sort -u); do
  curl -sf "http://127.0.0.1:3000$endpoint" > /dev/null || echo "WARN: $endpoint may not exist"
done
```

### Step 2.5.3: Verify Beads
```bash
bd doctor
bd ready  # должен показать первую задачу
```

### Step 2.5.4: Stop App
```bash
kill $APP_PID 2>/dev/null
```

### Step 2.5.5: Handle Failures

**If ANY check fails:**
1. Run `Task[debugger]` with symptom description
2. Apply suggested fixes
3. Re-run validation
4. Only proceed to Phase 3 when all checks pass

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
   ```
   Glob: **/skills/security-check/scripts/security_scan.py
   ```
   ```bash
   python3 {found_script_path} --path . --threshold medium
   ```

2. **Quality gate**:
   ```
   Glob: **/skills/verification-gate/scripts/verify.py
   ```
   ```bash
   python3 {found_script_path} --path .
   ```

3. **If scripts not found**: Skip (non-blocking), but warn

4. **If issues found**: Run `Task[debugger]` to fix, then re-run

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
