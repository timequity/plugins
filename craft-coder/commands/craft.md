---
description: Guided project creation with explanations
---

# /craft - Pair Programming Project Setup

User wants to build: $ARGUMENTS

Mode detection from arguments:
- Contains `--learn` → Learning mode (detailed explanations)
- Contains `--fast` → Fast mode (minimal dialogue)
- Default → Balanced mode (key decisions explained)

## Step 1/5: Requirements Gathering

### 1.1 Parse Project Name
Extract project name from arguments (remove flags).

### 1.2 Project Type (if not obvious)
```
question: "What type of project?"
header: "Type"
options:
  - label: "Web App"
    description: "Full-stack web application"
  - label: "REST API"
    description: "Backend service with JSON endpoints"
  - label: "CLI Tool"
    description: "Command-line utility"
  - label: "Library"
    description: "Reusable code package"
```

### 1.3 Core Questions
Use AskUserQuestion for:
1. **Problem** — "What problem does this solve?"
2. **Users** — "Who will use this?"
3. **Core Action** — "What's the main user action?"
4. **Success** — "How do you measure success?"

### 1.4 Create docs/PRD.md
Save answers to PRD.

---

## Step 2/5: Architecture Design

### 2.1 Analyze Requirements
Based on PRD, identify:
- Data storage needs
- API requirements
- UI complexity
- Performance constraints

### 2.2 Show Architecture Rationale (BALANCED/LEARN modes)

```markdown
## Architecture Analysis

Based on your requirements:
- {requirement_1} → suggests {approach_1}
- {requirement_2} → suggests {approach_2}

Proposed structure:
```
src/
├── lib.rs        # Business logic (testable)
├── main.rs       # Entry point (thin)
├── handlers/     # HTTP handlers
└── models/       # Data types
```

**Why this structure?**
- lib.rs pattern: Enables unit testing without HTTP
- Thin main.rs: Clear entry point, easy to understand
- Handlers separate: Each <50 lines for maintainability
```

### 2.3 User Confirmation
```
question: "Does this architecture look good?"
header: "Arch"
options:
  - label: "Yes, continue"
    description: "Accept proposed structure"
  - label: "Adjust"
    description: "I want to modify something"
  - label: "Explain more"
    description: "Need more details"
```

---

## Step 3/5: Stack Selection

### 3.1 Analyze Constraints
Map requirements to tech constraints:
- Single binary → Rust or Go
- Fast startup → Bun, Go, Rust
- Team familiarity → consider existing skills
- Persistence needs → SQLite vs Postgres

### 3.2 Show Tradeoff Table (BALANCED/LEARN modes)

```markdown
## Stack Analysis

| Option | Pros | Cons | Fit |
|--------|------|------|-----|
| Rust + Axum | Fast, safe, single binary | Learning curve | ★★★ |
| Go + Chi | Simple, fast | Less type safety | ★★☆ |
| Node + Hono | JS ecosystem, fast | Not single binary | ★☆☆ |

**Recommendation:** Rust + Axum

**Why?**
- Your requirement "{req}" eliminates {eliminated_options}
- Rust matches your constraint "{constraint}"
```

### 3.3 Stack Confirmation
```
question: "Which stack?"
header: "Stack"
options:
  - label: "{recommended} (Recommended)"
    description: "Best fit for your requirements"
  - label: "{alternative_1}"
    description: "{reason}"
  - label: "{alternative_2}"
    description: "{reason}"
```

### 3.4 Log Decision
Call decision-logger skill to write to docs/DECISIONS.md:
```markdown
## ADR-001: Technology Stack

**Context:** Building {project_name} with requirements {list}

**Decision:** {chosen_stack}

**Rationale:**
- {reason_1}
- {reason_2}

**Alternatives Considered:**
- {alt_1}: Rejected because {why}
- {alt_2}: Rejected because {why}
```

---

## Step 4/5: Project Initialization

### 4.1 Initialize Project
Based on chosen stack:
- Rust: `Task[rust-project-init]` with type and database
- Other: appropriate init agent

### 4.2 Show What Was Created (BALANCED/LEARN modes)

```markdown
## Project Initialized

Files created:
- `Cargo.toml` — Dependencies: {list}
- `src/lib.rs` — App logic with /health endpoint
- `src/main.rs` — Server entry point
- `templates/` — HTML templates (if fullstack)
- `static/` — CSS/JS assets (if fullstack)

**Why these defaults?**
- /health endpoint: Industry standard for liveness checks
- lib.rs pattern: Enables `cargo test` without starting server
```

### 4.3 Verify Setup
```bash
cargo check
cargo test
```

Show results to user.

---

## Step 5/5: First Feature

### 5.1 Show Ready Issues
```bash
bd ready
```

### 5.2 Explain TDD Approach (LEARN mode)

```markdown
## TDD Workflow

We'll implement the first feature using Test-Driven Development:

1. **RED** — Write a failing test
   - Describes expected behavior
   - Fails because feature doesn't exist

2. **GREEN** — Minimal code to pass
   - Just enough to make test pass
   - No premature optimization

3. **REFACTOR** — Improve code quality
   - Clean up without changing behavior
   - Tests still pass

Ready to start?
```

### 5.3 Offer Next Steps
```
question: "What's next?"
header: "Next"
options:
  - label: "Implement first feature"
    description: "Start TDD cycle with Task[tdd-test-writer]"
  - label: "Review architecture"
    description: "Go back to adjust structure"
  - label: "Stop here"
    description: "Continue manually later"
```

---

## Mode-Specific Behavior

### LEARN mode (`--learn`)
- Show ALL explanations
- Include "Why?" sections
- Add learning resources links
- Slower, more educational

### FAST mode (`--fast`)
- Skip explanations
- Use defaults where sensible
- Minimal questions
- Maximum speed

### BALANCED mode (default)
- Key decisions explained briefly
- Skip obvious explanations
- `/why` available for details
- Good speed/understanding balance

---

## Output Format

```markdown
## Crafted: {project_name}

Type: {project_type}
Stack: {chosen_stack}
Features: {count} planned

Decisions logged: docs/DECISIONS.md
Requirements: docs/PRD.md

Next:
  `/why` — Explain last decision
  `/next` — Start implementing
```
