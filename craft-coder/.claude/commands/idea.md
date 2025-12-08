---
description: Start building from a simple idea
---

# New Project from Idea

User wants to build: $ARGUMENTS

Run the idea-validation skill to understand requirements, then initialize project.

## Process

1. **Validate idea** using AskUserQuestion:
   - Q1: Problem (3 contextual options)
   - Q2: User (Для себя / AI агенты / Команда)
   - Q3: Core Action (3 contextual options)
   - Q4: Success Metric (3 contextual options)

2. **Create docs/PRD.md** with answers

3. **Ask project type**:
   - Rust API (Axum)
   - Node.js API
   - Python API
   - Other

4. **Run Task[rust-project-init]** (or appropriate init for type)

5. **Show status**:
   ```
   ## Project Created: {name}

   PRD: docs/PRD.md
   Issues: bd list

   Next: /next to start TDD cycle
   ```
