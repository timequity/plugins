---
name: language-selector
description: |
  Manages course language preference.
  Use when: user starts course or wants to change language.
  Internal skill - detects language from user input.
---

# Language Selector

Determines and stores the user's preferred language for the course.

## Language Detection

### Automatic Detection

Detect language from user's first message:
- Russian characters (а-яА-Я) → `ru`
- English or other → `en`

### Explicit Selection

If user says:
- "на русском" / "russian" / "ru" → set `ru`
- "in english" / "english" / "en" → set `en`

## Storage

Language preference is stored in progress file:

```json
{
  "version": "1.0.0",
  "language": "en",  // or "ru"
  "current_lesson": 1,
  ...
}
```

## Content Paths

Based on language, use appropriate content:

| Language | Lessons Path | Commands Path |
|----------|--------------|---------------|
| `en` | `lessons/en/lesson-N.md` | `commands/en/*.md` |
| `ru` | `lessons/ru/lesson-N.md` | `commands/ru/*.md` |

## First Run Prompt

If no language set, show:

```
# Claude Code Course

Choose your language / Выберите язык:

1. English
2. Русский

Type "1" or "2", or just start chatting in your preferred language.
```

## Changing Language

User can change language anytime with:
- `/course lang en` — switch to English
- `/course lang ru` — switch to Russian

This updates the `language` field in progress.json.

## Implementation

```bash
# Check language in progress
LANG=$(jq -r '.language // "en"' "$HOME/.claude-course/progress.json" 2>/dev/null || echo "en")

# Use appropriate content
LESSONS_PATH="lessons/$LANG"
COMMANDS_PATH="commands/$LANG"
```
