---
name: claude-code-mastery
description: |
  Master Claude Code from zero to expert through Socratic learning.
  Use when: user wants to learn Claude Code, asks "how do I...", or is confused about features.
  Triggers: "learn Claude Code", "teach me", "how does this work", "I'm new to Claude Code",
  "научи меня", "как пользоваться", "я новичок".
---

# Claude Code Mastery

Learn Claude Code through guided, progressive skill building.

## Philosophy

```
Not this:                      This:
┌─────────────────┐           ┌─────────────────┐
│ Read 50 pages   │           │ "What do you    │
│ of docs         │     →     │  want to build?"│
│ Then try stuff  │           │                 │
└─────────────────┘           │ Let's learn by  │
                              │ doing that.     │
                              └─────────────────┘
```

## How It Works

### 1. Assessment (Socratic)
`learning-path` skill asks questions to determine:
- Current experience level
- What you want to accomplish
- Learning style preference

### 2. Level Placement
Based on assessment, routes to appropriate track:

| Level | For | Focus |
|-------|-----|-------|
| Foundations | New to Claude Code | Basic commands, file operations, chat |
| Intermediate | Know basics | Tools, MCP, hooks, customization |
| Advanced | Power users | Custom agents, skills, complex workflows |

### 3. Progressive Learning
Each level builds on previous:
- Hands-on exercises
- Real project examples
- Reference cards for quick lookup

## Entry Point

Start with `/mastery:assess` or just ask "teach me Claude Code".

The learning-path skill will guide you from there.

## Skills Structure

```
skills/
├── learning-path/     # Assessment + routing
├── foundations/       # Level 1: Basics
│   └── references/    # Quick reference cards
├── intermediate/      # Level 2: Customization
│   └── references/
└── advanced/          # Level 3: Power user
    └── references/
```
