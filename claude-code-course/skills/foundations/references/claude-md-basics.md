# CLAUDE.md Basics

## What is CLAUDE.md?

A file that gives Claude permanent instructions for your project.

Claude reads it **automatically** at the start of every conversation.

## Where to Put It

```
your-project/
├── CLAUDE.md        ← Project root (most common)
├── src/
│   └── CLAUDE.md    ← Directory-specific (optional)
├── package.json
└── ...
```

## What to Include

### 1. Project Overview (Required)
```markdown
# CLAUDE.md

## Project
E-commerce API built with FastAPI and PostgreSQL.
```

### 2. Tech Stack
```markdown
## Stack
- Backend: FastAPI (Python 3.11)
- Database: PostgreSQL + SQLAlchemy
- Auth: JWT tokens
- Deploy: Docker + Railway
```

### 3. Key Commands
```markdown
## Commands
- `make dev` — start development server
- `make test` — run pytest
- `make lint` — run ruff
```

### 4. Code Style
```markdown
## Style
- Use type hints everywhere
- Prefer composition over inheritance
- Tests go in tests/ mirroring src/ structure
```

### 5. Important Files
```markdown
## Key Files
- `src/main.py` — app entry point
- `src/api/` — route handlers
- `src/models/` — SQLAlchemy models
```

## Minimal Example

```markdown
# CLAUDE.md

## Project
Task management CLI in Rust.

## Commands
- `cargo run` — run the app
- `cargo test` — run tests

## Style
- Use thiserror for errors
- Keep functions under 50 lines
```

## Full Example

```markdown
# CLAUDE.md

## Project
Real-time chat application with React frontend and Node.js backend.

## Stack
- Frontend: React 18 + TypeScript + Tailwind
- Backend: Node.js + Express + Socket.io
- Database: MongoDB
- Auth: Passport.js + sessions

## Structure
```
client/          # React app
server/          # Express API
  src/
    routes/      # API endpoints
    models/      # Mongoose schemas
    socket/      # WebSocket handlers
```

## Commands
- `npm run dev` — start both client and server
- `npm test` — run Jest tests
- `npm run build` — production build

## Style
- Functional components with hooks
- No class components
- Use Zod for validation
- Prefer named exports

## Current Focus
Working on group chat feature. See docs/group-chat.md for spec.
```

## Tips

### Do
- Keep it under 100 lines
- Update when project changes
- Include what's NOT obvious

### Don't
- List every file
- Repeat what's in README
- Include sensitive data (keys, passwords)

## Try It

1. Create `CLAUDE.md` in your project root
2. Add project name and 2-3 key facts
3. Start a new Claude Code conversation
4. Ask: "What do you know about this project?"

Claude should mention details from your CLAUDE.md.
