# Fullstack Developer Plugin

Complete skill set for fullstack developers: backend (Python/Node/Rust), frontend (React), DevOps, testing, and code review.

## Skills

| Skill | Description | Lines |
|-------|-------------|-------|
| **backend-core** | API design, auth, security, databases | ~600 |
| **backend-python** | FastAPI, SQLAlchemy, uv, ruff, pytest | ~450 |
| **backend-nodejs** | Hono/NestJS, Drizzle, Vitest, TypeScript | ~550 |
| **backend-rust** | Axum, SQLx, tokio, serde | ~630 |
| **frontend-react** | React 19, TypeScript, Tailwind, TanStack Query | ~830 |
| **devops** | Docker, GitHub Actions, CI/CD, Fly.io | ~910 |
| **code-review** | Review workflow, checklists, feedback patterns | ~180 |
| **testing** | Unit, integration, E2E, mocking patterns | ~470 |

## Commands

- `/dev review` — Code review current changes
- `/dev test` — Run tests with analysis
- `/dev deploy` — Help with deployment setup

## Agents

- `code-reviewer` — Automated code review with severity categorization

## Installation

```bash
cpm install fullstack-developer
```

## Usage

Skills are triggered automatically based on context. Example triggers:

- "fastapi", "python backend" → `backend-python`
- "react", "component" → `frontend-react`
- "docker", "deploy" → `devops`
- "write tests" → `testing`

## License

Proprietary — CC Market
