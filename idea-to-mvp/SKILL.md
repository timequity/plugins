---
name: idea-to-mvp
description: |
  Vibe coding: build apps by describing what you want. No technical decisions needed.
  Use when: user wants to create an app, website, MVP, or prototype.
  Triggers: "build app", "create website", "make MVP", "I have an idea",
  "хочу приложение", "создать сайт", "сделать MVP".
---

# Idea to MVP

Build production-ready apps through conversation. User describes WHAT, AI handles HOW.

## Philosophy

```
User sees:                    Under the hood:
┌─────────────────┐          ┌──────────────────────┐
│ "I want an app  │    →     │ • Stack selection    │
│  for expense    │          │ • Code generation    │
│  tracking"      │          │ • TDD + testing      │
└─────────────────┘          │ • Security checks    │
                             │ • Code review        │
┌─────────────────┐          │ • Build verification │
│ ✅ Done!        │    ←     └──────────────────────┘
│ [Preview] [Deploy]
└─────────────────┘
```

## Workflow

### 1. Idea Refinement
Use `brainstorming` skill for Socratic dialogue:
- One question at a time
- Multiple choice when possible
- 2-3 approaches with trade-offs
- YAGNI ruthlessly

### 2. Validation
Use `idea-validation` skill:
- "What problem does this solve?"
- "Who has this problem?"
- No technical questions
- Output: internal PRD (user doesn't see)

### 3. Build
Invisible pipeline:
1. `stack-selector` → choose tech stack automatically
2. Generate project from template
3. `ui-generator` → create UI components
4. `test-driven-development` → TDD cycle
5. `auto-testing` → run tests
6. `security-check` → OWASP validation
7. `code-review-auto` → fix issues before showing

### 4. Iterate
User says "add [feature]":
1. `feature-builder` → understand requirement
2. Generate code with TDD
3. Run validation pipeline
4. Update preview

### 5. Deploy
User says "deploy" or "publish":
1. `deploy-automation` → choose platform
2. Configure hosting
3. Return production URL

## Commands

| Command | Purpose |
|---------|---------|
| `/mvp:brainstorm` | Refine idea with Socratic dialogue |
| `/mvp:idea` | Start from scratch with simple questions |
| `/mvp:build` | Create the app (full pipeline) |
| `/mvp:add` | Add feature to existing app |
| `/mvp:preview` | Show current state |
| `/mvp:deploy` | Publish to production |

## Design Integration

All UI uses:
- `frontend-design` skill for distinctive aesthetics
- `theme-factory` for consistent colors/fonts
- Anti "AI slop" — no generic purple gradients

## Hidden Validation

Every code change runs through:
1. TDD (test first, then implement)
2. Automated tests
3. Security checks (OWASP)
4. Code review (auto-fix issues)

User only sees ✅ or ❌ — never the process.

## Templates

| Template | When to use |
|----------|-------------|
| nextjs-supabase | Web apps, SaaS, dashboards |
| fastapi-postgres | APIs, backends, AI/ML projects |
| hono-drizzle | Edge, serverless, Cloudflare |
| landing-page | Marketing sites, portfolios |

Stack selector chooses automatically based on requirements.
