---
name: brainstorming
description: |
  Refine ideas into designs through Socratic dialogue.
  Use when: user has a rough idea, needs to clarify requirements, explore approaches.
  Triggers: "brainstorm", "discuss idea", "I'm thinking about", "what if",
  "help me think through", "explore options".
---

# Brainstorming Ideas Into Designs

Turn rough ideas into fully formed designs through natural collaborative dialogue.

## Process

### 1. Understand the Idea

- Check current project context first (files, docs, recent commits)
- Ask questions **one at a time**
- Prefer multiple choice when possible
- Focus on: purpose, constraints, success criteria

### 2. Explore Approaches

- Propose 2-3 different approaches with trade-offs
- Lead with your recommendation and explain why
- Present options conversationally

### 3. Present the Design

Once you understand what you're building:
- Break into sections of 200-300 words
- Ask after each section: "Does this look right so far?"
- Cover: architecture, components, data flow, error handling
- Be ready to go back and clarify

## Key Principles

| Principle | Why |
|-----------|-----|
| One question at a time | Don't overwhelm |
| Multiple choice preferred | Easier to answer |
| YAGNI ruthlessly | Remove unnecessary features |
| Explore alternatives | Always propose 2-3 approaches |
| Incremental validation | Present in sections, validate each |

## After the Design

**If continuing to implementation:**
1. "Ready to build?"
2. Use stack-selector to choose template
3. Start /mvp:build pipeline
