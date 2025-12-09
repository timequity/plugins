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

Now I'll demonstrate creating an agent.

**Task:** Create a `code-explorer` agent that finds and summarizes code.

**Watch me do it:**

---

## Practice Execution

**IMPORTANT:** As the tutor, YOU (Claude) must execute this practice, not the user.

1. Create the agent file:

```bash
mkdir -p .claude/agents
cat > .claude/agents/code-explorer.md << 'EOF'
---
name: code-explorer
description: Explores codebase and answers questions about it.
tools:
  - Glob
  - Grep
  - Read
model: haiku
---

# Code Explorer Agent

You are a code exploration assistant.

## Instructions

1. Use Glob to find relevant files
2. Use Grep to search for patterns
3. Use Read to examine file contents
4. Summarize findings concisely

## Response Format

- List relevant files found
- Brief description of each
- Answer the user's question
EOF
```

2. Show the user what was created:
```bash
cat .claude/agents/code-explorer.md
```

3. Explain and congratulate:
```
✓ Practice completed!

I created an agent at .claude/agents/code-explorer.md

Key differences from skills:
- Has `tools:` — what the agent can use
- Has `model:` — which AI model runs it
- Runs as separate process, can work in parallel

Agents are for autonomous, multi-step tasks.

Ready for Lesson 4? Type `/ccc:lesson 4` or say "next"
```

**After execution:**
- Update progress: `practice_completed: true`, `current_lesson: 4`
- Clean up: `rm -rf .claude/agents/code-explorer.md` (demo only)
