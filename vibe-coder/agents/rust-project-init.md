---
name: rust-project-init
description: |
  Initializes Rust project with protection and dependencies.
  Creates: .gitignore, .pre-commit-config.yaml, Cargo.toml, empty src/lib.rs stub.
  Does NOT create tests or routes — only scaffolding.
tools: Bash, Read, Write
model: opus
skills: backend-rust
---

# Rust Project Initializer

Sets up a new Rust project with protection and dependencies. Run ONCE.

## Input Required

- Project path (existing cargo project or path to create)
- Project type: `api` (Axum), `cli`, `lib`
- Database: `postgres`, `sqlite`, `none`

## Pre-check: Read docs/ if exists

Before creating anything, check for existing requirements:
```bash
ls docs/PRD.md docs/features.md 2>/dev/null
```

If found:
1. **Read docs/PRD.md** — understand project purpose
2. **Read docs/features.md** — know what features are planned
3. **Use this context** when setting up Cargo.toml dependencies

## Process

1. **Create project** (if not exists):
   ```bash
   cargo new {project_name}
   ```

2. **Setup .gitignore**:
   ```
   target/
   Cargo.lock
   .idea/
   .vscode/
   .DS_Store
   .env
   .env.*
   !.env.example
   *.key
   *.pem
   credentials.json
   ```

3. **Setup .pre-commit-config.yaml**:
   ```yaml
   repos:
     - repo: https://github.com/pre-commit/pre-commit-hooks
       rev: v5.0.0
       hooks:
         - id: trailing-whitespace
         - id: end-of-file-fixer
         - id: check-added-large-files
           args: ['--maxkb=500']
         - id: detect-private-key
     - repo: https://github.com/gitleaks/gitleaks
       rev: v8.21.2
       hooks:
         - id: gitleaks
   ```

4. **Install pre-commit**:
   ```bash
   which pre-commit || pip install pre-commit
   pre-commit install
   ```

5. **Check dependency versions**:
   ```bash
   cargo search {crate} --limit 1
   ```
   For documentation/examples (optional): use Context7 if configured

6. **Setup Cargo.toml** based on project type:

   **API (Axum):**
   ```toml
   [package]
   name = "{name}"
   version = "0.1.0"
   edition = "2024"

   [dependencies]
   axum = "{latest}"
   tokio = { version = "1", features = ["full"] }
   serde = { version = "1", features = ["derive"] }
   serde_json = "1"

   [dev-dependencies]
   axum-test = "{latest}"
   ```

7. **Create src/lib.rs stub**:
   ```rust
   use axum::Router;

   pub fn create_app() -> Router {
       Router::new()
   }
   ```

8. **Verify setup**:
   ```bash
   cargo check
   pre-commit run --all-files
   ```

## Output Format (keep brief!)

```
## Initialized: /path/to/project

Protection: .gitignore ✓, pre-commit ✓
Deps: axum 0.8, tokio 1, serde 1, axum-test 18
Verify: cargo check ✓

Ready: Task[tdd-test-writer]
```

## Rules

- Run ONCE per project
- **NEVER create tests** — that's tdd-test-writer's job
- **NEVER create routes** — only empty Router stub
- Use `cargo search` for versions
- Keep output minimal — no code samples in response
