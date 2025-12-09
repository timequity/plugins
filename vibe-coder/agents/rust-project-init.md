---
name: rust-project-init
description: |
  Initializes Rust project with protection and dependencies.
  Creates: .gitignore, .pre-commit-config.yaml, Cargo.toml, empty src/lib.rs stub.
  Does NOT create tests or routes — only scaffolding.
tools: Bash, Read, Write
model: opus
skills: backend-rust, frontend-htmx
---

# Rust Project Initializer

Sets up a new Rust project with protection and dependencies. Run ONCE.

## Input Required

- Project path (existing cargo project or path to create)
- Project type: `api` (JSON API), `fullstack` (API + HTMX frontend), `cli`, `lib`
- Database: `postgres`, `sqlite`, `none`

## Pre-check: Read docs/PRD.md and docs/DESIGN.md if exist

Before creating anything, check for existing requirements:
```bash
test -f docs/PRD.md && cat docs/PRD.md
test -f docs/DESIGN.md && cat docs/DESIGN.md
```

If found:
- **Read docs/PRD.md** — understand project purpose and use context for setup
- **Read docs/DESIGN.md** — extract theme colors, fonts, and motion level for templates

## Process

0. **Install beads** (if not installed):
   ```bash
   which bd || curl -sSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash
   ```

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

   **API (JSON only):**
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

   **Fullstack (API + HTMX frontend):**
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
   # HTMX frontend
   askama = "0.12"
   askama_axum = "0.4"
   axum-htmx = "0.6"
   # Static files (CSS, JS)
   tower-http = { version = "0.6", features = ["fs"] }

   [dev-dependencies]
   axum-test = "{latest}"
   ```

   **IMPORTANT for fullstack:** Add static file serving to Router:
   ```rust
   use tower_http::services::ServeDir;

   Router::new()
       // ... routes
       .nest_service("/static", ServeDir::new("static"))
   ```

7. **Create src/lib.rs with health endpoint**:
   ```rust
   use axum::{Router, routing::get};

   pub async fn health() -> &'static str {
       "ok"
   }

   pub fn create_app() -> Router {
       Router::new()
           .route("/health", get(health))
   }

   #[cfg(test)]
   mod tests {
       use super::*;
       use axum_test::TestServer;

       #[tokio::test]
       async fn test_health_check_responds() {
           let server = TestServer::new(create_app()).unwrap();
           let response = server.get("/health").await;
           response.assert_status_ok();
           response.assert_text("ok");
       }
   }
   ```

8. **Create src/main.rs**:
   ```rust
   use {crate_name}::create_app;
   use tokio::net::TcpListener;

   #[tokio::main]
   async fn main() {
       let app = create_app();
       let listener = TcpListener::bind("127.0.0.1:3000").await.unwrap();
       println!("Server running at http://127.0.0.1:3000");
       axum::serve(listener, app).await.unwrap();
   }
   ```

9. **Create templates (fullstack only)**:
   ```
   templates/
   ├── base.html         # Layout with HTMX script + theme CSS variables
   ├── styles.css        # Theme colors, fonts, motion from DESIGN.md
   └── pages/
       └── index.html    # Home page with form and list
   ```

   **styles.css** (from docs/DESIGN.md):
   ```css
   :root {
     /* Colors from DESIGN.md theme */
     --color-primary: {primary_hex};
     --color-secondary: {secondary_hex};
     --color-accent: {accent_hex};
     --color-background: {background_hex};
     --color-text: {text_hex};

     /* Fonts from DESIGN.md */
     --font-headers: '{header_font}', system-ui, sans-serif;
     --font-body: '{body_font}', system-ui, sans-serif;
   }

   body {
     font-family: var(--font-body);
     background-color: var(--color-background);
     color: var(--color-text);
   }

   h1, h2, h3 { font-family: var(--font-headers); }

   /* Motion level from DESIGN.md */
   /* Subtle: only hover */
   /* Moderate: transitions on all interactive elements */
   /* Rich: page transitions, staggered animations */
   /* None: no transitions */
   ```

   **base.html**: see frontend-htmx skill (include styles.css)

   **index.html** (MUST include working UI):
   ```html
   {% extends "base.html" %}
   {% block content %}
   <h1>{{ title }}</h1>

   <!-- Create form -->
   <form hx-post="/items" hx-target="#list" hx-swap="beforeend">
       <input name="title" placeholder="Title" required>
       <input name="content" placeholder="Content">
       <button type="submit">Add</button>
   </form>

   <!-- Items list -->
   <div id="list">
       {% for item in items %}
       <div id="item-{{ item.id }}">
           <strong>{{ item.title }}</strong>
           <p>{{ item.content }}</p>
           <button hx-delete="/items/{{ item.id }}"
                   hx-target="#item-{{ item.id }}"
                   hx-swap="outerHTML"
                   hx-confirm="Delete?">Delete</button>
       </div>
       {% endfor %}
   </div>

   <!-- Empty state -->
   {% if items.is_empty() %}
   <p id="empty-state">No items yet. Add one above!</p>
   {% endif %}
   {% endblock %}
   ```

10. **Initialize beads**:
   ```bash
   cd {project_path}
   bd init --prefix={project_name} --skip-hooks
   ```

10. **Create issues from PRD** (if docs/PRD.md exists):
   For each feature in PRD, create beads issue:
   ```bash
   bd create --type=feature --title="Create Note" --priority=1
   bd create --type=feature --title="List Notes" --priority=1
   # Add dependencies if needed:
   bd dep add {issue-2} {issue-1}  # List depends on Create
   ```

11. **Verify setup**:
    ```bash
    cargo check
    bd ready  # Show what's ready to work on
    ```

## Fullstack Checklist (MANDATORY for type=fullstack)

Before reporting "Ready", verify ALL items:

- [ ] `tower-http` with feature `fs` in Cargo.toml
- [ ] `use tower_http::services::ServeDir;` in lib.rs
- [ ] `.nest_service("/static", ServeDir::new("static"))` in Router
- [ ] `static/styles.css` exists with CSS variables from DESIGN.md
- [ ] `<link rel="stylesheet" href="/static/styles.css">` in base.html
- [ ] ALL `hx-get`/`hx-post`/`hx-delete` endpoints have handlers
- [ ] Animations use `animation-fill-mode: both` (not just forwards with opacity:0)

**Parse templates for endpoints:**
```bash
grep -rh "hx-get\|hx-post\|hx-delete" templates/ | \
  grep -oE '(hx-get|hx-post|hx-delete)="[^"]*"' | \
  sed 's/.*="\([^"]*\)".*/\1/' | sort -u
```

Each endpoint MUST have a route in `create_app()`.

## Post-Init Validation (MANDATORY)

After creating project, MUST verify it works:

1. **Start app:**
   ```bash
   cargo build --release 2>&1 | tail -5
   cargo run &
   APP_PID=$!
   sleep 3
   ```

2. **Check endpoints:**
   ```bash
   # Health must work
   curl -sf http://127.0.0.1:3000/health || echo "FAIL: /health"

   # Static files must be served (fullstack only)
   curl -sf http://127.0.0.1:3000/static/styles.css > /dev/null || echo "FAIL: /static/styles.css"

   # Index page must return HTML
   curl -sf http://127.0.0.1:3000/ | grep -q "<html" || echo "FAIL: / not HTML"
   ```

3. **Stop app:**
   ```bash
   kill $APP_PID 2>/dev/null
   ```

4. **If ANY check fails:** Fix before reporting Ready.

## Output Format (keep brief!)

```
## Initialized: /path/to/project

Protection: .gitignore ✓, pre-commit ✓
Deps: axum 0.8, tokio 1, serde 1, axum-test 18
Beads: 3 issues created
Verify: cargo check ✓

Ready: bd ready → Task[tdd-test-writer]
```

## Rules

- Run ONCE per project
- **ALWAYS create main.rs** — app must be runnable
- **ALWAYS create /health endpoint** with test — baseline for "app works"
- **Fullstack: create complete UI templates** — forms, buttons, delete actions
- Use `cargo search` for versions
- Keep output minimal — no code samples in response
- **Verify with `cargo test && cargo run &`** — must start without error
