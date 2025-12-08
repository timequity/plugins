---
name: rust-project-init
description: |
  Initializes Rust project with protection and base dependencies.
  Run ONCE at project start before any TDD cycles.
  Creates: .gitignore, .pre-commit-config.yaml, Cargo.toml with deps.
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

## Output Format

```
## Project Initialized

**Path**: /path/to/project
**Type**: api (Axum)

### Protection
- [x] .gitignore (target/, secrets)
- [x] .pre-commit-config.yaml
- [x] pre-commit installed

### Dependencies (via Context7)
- axum = "0.8.1"
- tokio = "1.43"
- serde = "1.0"
- axum-test = "18.1" (dev)

### Verification
- cargo check: PASS
- pre-commit: PASS

## Ready for TDD
Run: Task[tdd-test-writer] to start RED phase
```

## Rules

- Run ONCE per project
- Use `cargo search` for versions (fast, reliable, no API key)
- Context7 optional — for docs/examples only
- Create .env.example if project needs env vars
