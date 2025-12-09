---
name: brainstorming
description: |
  Refine ideas into detailed designs through Socratic dialogue.
  Use when: user has rough idea, needs to clarify requirements, explore approaches.
  Triggers: "brainstorm", "discuss idea", "I'm thinking about", "what if",
  "help me think through", "explore options", "/brainstorm".
---

# Brainstorming Ideas Into Designs

Turn rough ideas into fully formed designs through natural collaborative dialogue.
Integrated with idea-validation — brainstorming is an optional deep-dive before PRD creation.

## When to Use

| Trigger | Action |
|---------|--------|
| `/brainstorm` command | Full brainstorm session |
| Short idea (<10 words) | Suggest brainstorm in /ship |
| Complex project type | Suggest brainstorm in /ship |
| User asks "what if" / "help me think" | Start brainstorm |
| User has detailed description | Skip to idea-validation |

## Brainstorm Flow

### Phase 1: Understand the Core

1. **Clarify the idea** — ask what they're trying to build
2. **Identify type** — Web App, Telegram Bot, API, CLI, etc.
3. **Find the problem** — what pain point does it solve?
4. **Define success** — how will we know it works?

**Questions to ask (one at a time):**
```
"Расскажи подробнее — что именно это должно делать?"
"Кто будет этим пользоваться? В каком контексте?"
"Какую проблему это решает?"
"Как понять что получилось?"
```

### Phase 2: Explore Approaches (Type-Specific)

Based on project type, explore key decisions:

#### For Telegram Bot:
- Commands vs conversational?
- Need database?
- External API integrations?
- Webhooks vs polling?

#### For Web App:
- Authentication needed?
- Realtime features?
- Single page or multi-page?
- Admin panel?

#### For API:
- REST vs GraphQL?
- Public or internal?
- Auth method?
- Rate limiting?

#### For CLI:
- Interactive or one-shot?
- Config file support?
- Output format (text/JSON/table)?

### Phase 3: Define Boundaries

Ask about constraints and non-goals:

```
"Что точно НЕ должно быть в MVP?"
"Есть ограничения? Бесплатные сервисы only? Дедлайн?"
"Какой масштаб ожидаешь — 10 пользователей или 10000?"
```

### Phase 4: Present Design Summary

Once you understand:

```markdown
## Резюме

**Проект:** {name}
**Тип:** {type}
**Проблема:** {one sentence}
**Пользователь:** {who}

**MVP Features:**
1. {Feature 1}
2. {Feature 2}
3. {Feature 3}

**Не делаем:**
- {Non-goal 1}
- {Non-goal 2}

**Ограничения:**
- {Constraint 1}

Всё верно? Готов создать PRD?
```

## Integration with idea-validation

After brainstorm completes:

1. **Pass collected info** to idea-validation skill
2. **Skip redundant questions** — don't re-ask what brainstorm covered
3. **Generate appropriate PRD** — Full PRD after full brainstorm

```
Brainstorm Complete → idea-validation → PRD.md (Full)
```

## Key Principles

| Principle | Why |
|-----------|-----|
| One question at a time | Don't overwhelm |
| Multiple choice when possible | Easier to answer |
| YAGNI ruthlessly | Remove unnecessary features |
| Explore alternatives | Propose 2-3 approaches |
| Validate incrementally | Present sections, validate each |
| No technical jargon | User chooses nothing technical |

## Standalone Usage

If user runs `/brainstorm` without `/ship`:

```
User: /brainstorm I want to make a bot that tracks expenses

Claude: [Starts brainstorm]
"Интересная идея! Давай уточним детали.
Это для Telegram, Discord, или другой платформы?"

[After brainstorm]
Claude: "Готово! Хочешь сразу начать строить? Могу запустить /ship"
```
