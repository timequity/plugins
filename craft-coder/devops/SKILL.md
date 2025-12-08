---
name: devops
description: |
  DevOps essentials: Docker, CI/CD pipelines, deployment strategies.
  Use when: containerizing apps, setting up CI/CD, deploying to production.
  Triggers: "docker", "dockerfile", "ci/cd", "github actions", "deploy",
  "kubernetes", "compose", "container", "pipeline".
---

# DevOps Essentials

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Docker | [docker.md](references/docker.md) — Best practices, compose, optimization |
| CI/CD | [ci-cd.md](references/ci-cd.md) — GitHub Actions patterns, deployment strategies |

**Assets (ready to copy):**
- `assets/Dockerfile.node` — Multi-stage Node.js Dockerfile
- `assets/Dockerfile.python` — Multi-stage Python Dockerfile
- `assets/github-actions.yaml` — Complete CI/CD pipeline template

## Decision Trees

### Deployment Strategy

```
Where to deploy?
├─ Single app, simple → Fly.io, Railway, Render
├─ Multiple services → VPS + Docker Compose
├─ Scale needed → Kubernetes (managed: GKE, EKS)
└─ Edge/Serverless → Vercel, Cloudflare Workers
```

### Container Strategy

```
What to containerize?
├─ Development → Docker Compose (all services)
├─ Production single app → Multi-stage Dockerfile
├─ Production multiple → Compose or K8s
└─ Local tools → Dev containers
```

## Docker

### Multi-stage Dockerfile (Node)

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/package.json ./
USER nodejs
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### Multi-stage Dockerfile (Python)

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .

FROM python:3.12-slim AS runner
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src ./src
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0"]
```

### Multi-stage Dockerfile (Rust)

```dockerfile
FROM rust:1.75-alpine AS builder
RUN apk add --no-cache musl-dev
WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src
RUN cargo build --release

FROM alpine:3.19 AS runner
RUN adduser -D appuser
COPY --from=builder /app/target/release/myapp /usr/local/bin/
USER appuser
EXPOSE 3000
CMD ["myapp"]
```

### Docker Compose

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/app
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## GitHub Actions

### Basic CI Pipeline

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install
      - run: pnpm lint
      - run: pnpm test
      - run: pnpm build
```

### With Database

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    env:
      DATABASE_URL: postgres://test:test@localhost:5432/test

    steps:
      - uses: actions/checkout@v4
      - run: pnpm install
      - run: pnpm db:migrate
      - run: pnpm test
```

### Deploy to Fly.io

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: superfly/flyctl-actions/setup-flyctl@master

      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

### Docker Build & Push

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
```

## Quick Reference

### Docker Commands

```bash
# Build
docker build -t myapp .
docker build -t myapp:v1 --target builder .

# Run
docker run -p 3000:3000 myapp
docker run -d --name myapp -p 3000:3000 myapp
docker run --rm -it myapp sh

# Compose
docker compose up -d
docker compose down
docker compose logs -f api
docker compose exec api sh

# Cleanup
docker system prune -af
docker volume prune -f
```

### Fly.io Commands

```bash
fly launch              # Initialize
fly deploy              # Deploy
fly logs                # View logs
fly ssh console         # SSH into container
fly secrets set KEY=val # Set env vars
fly scale count 2       # Scale instances
```

## Anti-patterns

| Don't | Do Instead |
|-------|------------|
| `latest` tag | Specific version tags |
| Root user in container | Non-root user |
| Secrets in Dockerfile | Runtime env vars / secrets |
| Single-stage builds | Multi-stage builds |
| `npm install` in prod | `npm ci` |
| No health checks | Health check endpoints |
| Manual deploys | CI/CD automation |
