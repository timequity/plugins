# Custom Agents

## What Are Agents?

Autonomous workers Claude can spawn to handle complex tasks.

```
┌─────────────────┐
│  Main Claude    │
│                 │
│  "Review this   │
│   PR please"    │
└────────┬────────┘
         │ spawns
         ▼
┌─────────────────┐
│  Review Agent   │
│                 │
│  - Reads diff   │
│  - Checks style │
│  - Reports back │
└─────────────────┘
```

## Why Use Agents?

| Main Claude | Agent |
|-------------|-------|
| Interactive conversation | Autonomous work |
| Uses your context window | Has own context |
| Waits for you | Works in background |
| General purpose | Specialized task |

## Agent File Structure

```
agents/
└── code-reviewer.md
```

Or in plugin:
```
my-plugin/
└── agents/
    └── code-reviewer.md
```

## Agent Format

```markdown
---
name: code-reviewer
description: Reviews code changes and reports issues
tools: [Read, Glob, Grep, Bash]
model: haiku
---

# Code Reviewer Agent

## Task
Review code changes and identify issues.

## Process
1. Get changed files: `git diff --name-only HEAD~1`
2. Read each file
3. Check for issues:
   - Security vulnerabilities
   - Performance problems
   - Style violations
   - Logic errors
4. Report findings

## Output Format
```
## Review Summary

### Critical Issues
- [file:line] Description

### Warnings
- [file:line] Description

### Suggestions
- [file:line] Description
```
```

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier |
| `description` | Yes | What agent does |
| `tools` | Yes | List of allowed tools |
| `model` | No | haiku (fast), sonnet (balanced), opus (smart) |

## Tool Permissions

Agents must declare which tools they can use:

```yaml
tools: [Read, Glob, Grep]           # Read-only
tools: [Read, Write, Edit, Bash]    # Full access
tools: [Read, Grep, WebFetch]       # Research
```

Available tools:
- `Read` — Read files
- `Write` — Create files
- `Edit` — Modify files
- `Glob` — Find files by pattern
- `Grep` — Search file contents
- `Bash` — Run commands
- `WebFetch` — Fetch URLs
- `WebSearch` — Search web

## Model Selection

| Model | Speed | Cost | Best For |
|-------|-------|------|----------|
| `haiku` | Fast | Low | Simple tasks, file searching |
| `sonnet` | Medium | Medium | Most tasks (default) |
| `opus` | Slow | High | Complex reasoning |

## Example: Test Runner Agent

```markdown
---
name: test-runner
description: Runs tests and reports failures with suggested fixes
tools: [Read, Bash, Grep]
model: haiku
---

# Test Runner Agent

## Task
Run test suite and analyze failures.

## Process

### 1. Detect test framework
- Check for pytest.ini, package.json, Cargo.toml
- Determine test command

### 2. Run tests
```bash
# Python
pytest --tb=short

# Node
npm test

# Rust
cargo test
```

### 3. Analyze failures
For each failure:
- Extract error message
- Find relevant source code
- Suggest fix

## Output
```
## Test Results

**Passed:** X
**Failed:** Y

### Failures

#### test_user_login
**Error:** AssertionError: expected 200, got 401
**File:** tests/test_auth.py:42
**Suggestion:** Check if auth token is being set correctly
```
```

## Example: Documentation Agent

```markdown
---
name: doc-generator
description: Generates documentation for code
tools: [Read, Glob, Grep, Write]
model: sonnet
---

# Documentation Generator

## Task
Generate documentation for undocumented code.

## Process

1. Find files needing docs:
   - Functions without docstrings
   - Classes without descriptions
   - Modules without README

2. For each item:
   - Read the code
   - Understand purpose
   - Generate documentation

3. Output as markdown or update source

## Documentation Style
- Start with one-line summary
- Explain parameters and return values
- Include usage example
- Note any gotchas
```

## Invoking Agents

### Via Task tool
Claude uses the Task tool internally to spawn agents.

### Via command
Create a command that invokes the agent:

`commands/review.md`:
```markdown
Use the code-reviewer agent to review recent changes.

Run: `git diff HEAD~1` to see what changed, then spawn the agent.
```

## Exercise: Build a Code Reviewer

### Step 1: Create agent file

`agents/my-reviewer.md`:
```markdown
---
name: my-reviewer
description: Quick code review for style and obvious issues
tools: [Read, Glob, Grep, Bash]
model: haiku
---

# My Code Reviewer

## Task
Review staged changes for common issues.

## Process

1. Get staged files:
```bash
git diff --cached --name-only
```

2. For each file, check:
   - TODO comments left in code
   - Console.log / print statements
   - Commented-out code blocks
   - Very long functions (>50 lines)

3. Report findings

## Output
List issues found with file:line references.
If no issues: "✅ Code looks good!"
```

### Step 2: Create command

`commands/quick-review.md`:
```markdown
Run my-reviewer agent on staged changes.
```

### Step 3: Test
```bash
git add some-file.js
```
Then: `/quick-review`

## Tips

- Keep agents focused (one job)
- Use haiku for speed when possible
- Limit tool access to what's needed
- Include clear output format
- Test with real scenarios
