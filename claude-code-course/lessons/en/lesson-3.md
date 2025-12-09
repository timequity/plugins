# Lesson 3: Agent Helpers

**Time:** ~25 minutes

## Learning Goals

After this lesson you will:
- Understand the difference between skills and agents
- Know when to use agents
- Create your first agent
- Delegate tasks

---

## Skill vs Agent

| Skill | Agent |
|-------|-------|
| Instructions | Separate process |
| Works in main context | Works in parallel |
| For simple tasks | For complex autonomous tasks |
| Read by Claude | Launched via Task tool |

**Analogy:**
- Skill = note with instructions ("how to make tea")
- Agent = assistant you can delegate to ("go make tea")

---

## When to Use an Agent

✅ **Use an agent when:**
- Task requires many steps
- Can work in parallel
- Task is autonomous (no dialogue needed)
- Exploring large codebase

❌ **Use a skill when:**
- Need dialogue with user
- Simple one-step task
- Conversation context matters

---

## Where Agents Live

```
your-project/
├── .claude/
│   ├── skills/
│   └── agents/
│       └── researcher.md    ← This is an agent
└── src/
```

Agents live in `.claude/agents/{name}.md`

---

## Agent Structure

```markdown
---
name: researcher
description: Researches codebase and answers questions.
tools:
  - Read
  - Glob
  - Grep
model: haiku
---

# Researcher Agent

You are a code researcher. Your task: find information in the codebase.

## Instructions

1. Use Glob to find files
2. Use Grep to search content
3. Read found files via Read
4. Form a brief answer

## Response Format

- List of found files
- Brief description of each
- Answer to user's question
```

### Frontmatter (required fields)

| Field | Description |
|-------|-------------|
| `name` | Unique agent name |
| `description` | What this agent is for |
| `tools` | Available tools |
| `model` | Model (haiku/sonnet/opus) |

### Available Tools

| Tool | Description |
|------|-------------|
| `Read` | Read files |
| `Write` | Create files |
| `Edit` | Edit files |
| `Glob` | Find files by pattern |
| `Grep` | Search by content |
| `Bash` | Execute commands |

---

## How to Run an Agent

Claude runs agents via Task tool:

```
User: "Find all files where login function is used"

Claude: [Uses Task tool with researcher agent]
        → Agent works in background
        → Returns result
```

You don't run agents directly — Claude decides when to use them based on description.

---

## Choosing a Model

| Model | When to use |
|-------|-------------|
| `haiku` | Fast simple tasks (search, count) |
| `sonnet` | Balance of speed and quality |
| `opus` | Complex tasks requiring reasoning |

**Rule:** start with haiku, upgrade if quality isn't enough.

---

## Summary

- Agents = autonomous helpers for complex tasks
- Live in `.claude/agents/{name}.md`
- Specify tools and model in frontmatter
- Haiku for fast tasks, Opus for complex ones

---

## Practice

**Task:** Create a `file-counter` agent that counts files in the project.

**Requirements:**
1. Path: `.claude/agents/file-counter.md`
2. Tools: Glob, Bash
3. Model: haiku (simple task)
4. Task: count files by type (.js, .ts, .md, etc.)

**Steps:**
1. Create file `.claude/agents/file-counter.md`
2. Add proper frontmatter
3. Write instructions for counting files

**Verification:**
After creating, ask "count files in project" — I should delegate to your agent.

<details>
<summary>Hint</summary>

```markdown
---
name: file-counter
description: Counts files in project by type.
tools:
  - Glob
  - Bash
model: haiku
---

# File Counter Agent

Count files in the project by extension.

## Algorithm

1. Use Glob with pattern `**/*` to get all files
2. Group by extension
3. Output table:

| Type | Count |
|------|-------|
| .ts | 45 |
| .md | 12 |
| ... | ... |

4. Show total count
```

</details>

When done, say "done" and I'll verify the result.

---

## Practice Verification

When user says "done", run verification:

```bash
# Lesson 3 check
AGENT_FILE=".claude/agents/file-counter.md"
if [ -f "$AGENT_FILE" ]; then
  # Check required frontmatter fields
  if head -20 "$AGENT_FILE" | grep -q "^name:" && \
     head -20 "$AGENT_FILE" | grep -q "^tools:" && \
     head -20 "$AGENT_FILE" | grep -q "^model:"; then
    echo "✓ Agent created with proper structure!"
  else
    echo "✗ File exists but missing frontmatter (name/tools/model)"
  fi
else
  echo "✗ File .claude/agents/file-counter.md not found"
fi
```

**On success:**
- Update progress: `practice_completed: true`
- Show congratulations and suggest moving to lesson 4

**On failure:**
- Explain what's wrong
- Remind required fields: name, tools, model
