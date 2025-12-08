# CI/CD Patterns

## Pipeline Stages

```
Code Push → Lint → Test → Build → Deploy
           └──────┬──────┘
              PR Checks
                            └────┬────┘
                            Main only
```

## GitHub Actions Patterns

### Caching

```yaml
# Node.js with pnpm
- uses: pnpm/action-setup@v3
  with:
    version: 9

- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'pnpm'

# Python with uv
- uses: astral-sh/setup-uv@v3
  with:
    enable-cache: true

# Rust
- uses: Swatinem/rust-cache@v2

# Docker layers
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### Matrix Builds

```yaml
jobs:
  test:
    strategy:
      matrix:
        node: [18, 20, 22]
        os: [ubuntu-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
```

### Conditional Jobs

```yaml
jobs:
  deploy:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    needs: [test, build]
    runs-on: ubuntu-latest
```

### Secrets & Environments

```yaml
jobs:
  deploy:
    environment: production  # Requires approval
    steps:
      - run: echo ${{ secrets.API_KEY }}
```

### Artifacts

```yaml
# Upload
- uses: actions/upload-artifact@v4
  with:
    name: build
    path: dist/

# Download
- uses: actions/download-artifact@v4
  with:
    name: build
    path: dist/
```

## Deployment Strategies

### Blue-Green

```yaml
deploy:
  steps:
    - name: Deploy to staging slot
      run: az webapp deployment slot create...

    - name: Run smoke tests
      run: curl https://staging.myapp.com/health

    - name: Swap slots
      run: az webapp deployment slot swap...
```

### Canary

```yaml
deploy:
  steps:
    - name: Deploy canary (10%)
      run: kubectl set image... --replicas=1

    - name: Monitor metrics
      run: ./scripts/check-metrics.sh

    - name: Full rollout
      run: kubectl rollout resume...
```

### Rolling Update

```yaml
# Default in Kubernetes
apiVersion: apps/v1
kind: Deployment
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

## Fly.io Deployment

```yaml
# fly.toml
app = "myapp"
primary_region = "ams"

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 3000
  force_https = true

[http_service.concurrency]
  type = "connections"
  hard_limit = 25
  soft_limit = 20

[[services.http_checks]]
  interval = 10000
  timeout = 2000
  path = "/health"
```

```yaml
# GitHub Action
- uses: superfly/flyctl-actions/setup-flyctl@master
- run: flyctl deploy --remote-only
  env:
    FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

## Branch Protection

```yaml
# Required status checks
# In GitHub Settings → Branches → Branch protection rules

# Required:
# - test
# - lint
# - build

# Recommended:
# - Require PR reviews (1+)
# - Dismiss stale reviews
# - Require up-to-date branches
```

## Release Workflow

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build
        run: pnpm build

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
          generate_release_notes: true
```
