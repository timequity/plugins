---
description: From idea to working app in one command
---

# Ship: Idea → Working App

User wants to build: $ARGUMENTS

Complete automation: validate idea, create project, implement all features, verify quality.

## Phase 1: Idea Validation

1. **Quick questions** using AskUserQuestion:
   - Problem (3 contextual options)
   - User (Для себя / AI агенты / Команда)
   - Core Action (3 contextual options)
   - Success Metric (3 contextual options)

2. **Create docs/PRD.md** with answers

3. **Validate PRD** (run script):
   ```bash
   python3 ~/.claude/skills/idea-validation/scripts/validate_prd.py --path .
   ```

## Phase 2: Project Setup

1. **Ask stack** (default: Rust fullstack):
   - Rust API + HTMX (Recommended)
   - Rust API only
   - Node.js
   - Python

2. **Run Task[rust-project-init]** with appropriate type

## Phase 3: TDD Implementation

Loop until all features done:

1. **Get next issue**:
   ```bash
   bd ready --limit=1
   ```

2. **If issue exists**:
   - Run Task[tdd-test-writer] — RED phase
   - Run Task[rust-developer] — GREEN phase
   - Close issue: `bd close <id>`

3. **Repeat until no issues ready**

## Phase 4: Verification Gate

1. **Security scan**:
   ```bash
   python3 ~/.claude/skills/security-check/scripts/security_scan.py --path . --threshold medium
   ```

2. **Quality gate**:
   ```bash
   python3 ~/.claude/skills/verification-gate/scripts/verify.py --path .
   ```

3. **If issues found**: fix and re-run

## Phase 5: Ship It

1. **Final status**:
   ```
   ## Shipped: {project-name}

   Features: {count} implemented
   Tests: all passing
   Security: clean

   Run: cargo run

   Next:
     • /add — Add more features
     • /deploy — Deploy to production
   ```
