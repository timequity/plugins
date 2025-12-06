# CLAUDE.md

## Project

**plugins** — коллекция плагинов для Claude Code Marketplace.
Каждый плагин — готовая конфигурация Claude Code для определённой профессии.

## Structure

```
plugins/
├── fullstack-developer/    # Full-Stack Web Dev plugin
│   ├── CLAUDE.md
│   ├── README.md
│   └── .claude/
│       ├── commands/
│       ├── skills/
│       └── agents/
└── ... (другие плагины)
```

## Plugin Structure

Каждый плагин — полноценный Claude Code plugin:
```
plugin-name/
├── CLAUDE.md               # Инструкции для Claude
├── README.md               # Документация
├── .claude-plugin/
│   └── manifest.json       # Plugin manifest
└── .claude/
    ├── commands/           # Slash-команды
    ├── skills/             # Навыки
    └── agents/             # Кастомные агенты
```

## Related Projects

- **claude-code-marketplace** — бэкенд маркетплейса
- **claude-plugin-manager** — CLI для установки плагинов
