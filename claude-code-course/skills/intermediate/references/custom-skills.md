# Custom Skills

## What Are Skills?

Reusable instruction sets that extend Claude's capabilities.

Think of them as "expert modes" you can create and share.

## Skill Structure

```
.claude/
└── skills/
    └── my-skill/
        ├── SKILL.md           # Required: main instructions
        └── references/        # Optional: supporting docs
            ├── patterns.md
            └── examples.md
```

## SKILL.md Format

```markdown
---
name: my-skill
description: |
  What this skill does.
  Use when: [trigger conditions]
  Triggers: "keyword1", "keyword2", "phrase".
---

# Skill Title

Instructions for Claude when this skill is active.

## Section 1
...

## Section 2
...
```

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase, hyphens) |
| `description` | Yes | What it does + when to use |

### Description Best Practices

```yaml
description: |
  One line: what it does.
  Use when: specific situations.
  Triggers: "word1", "word2", "phrase".
```

The `Triggers:` line helps Claude know when to activate automatically.

## Skill Content

After frontmatter, write instructions Claude should follow:

```markdown
---
name: api-reviewer
description: |
  Review API designs for best practices.
  Use when: reviewing REST/GraphQL APIs.
  Triggers: "review api", "api design review".
---

# API Review

Check these aspects:

## Naming
- Resources are nouns (users, posts)
- Collections are plural
- No verbs in URLs

## HTTP Methods
- GET: read only
- POST: create
- PUT: full update
- PATCH: partial update
- DELETE: remove

## Response Codes
- 200: success
- 201: created
- 400: bad request
- 404: not found
- 500: server error

## Checklist
When reviewing, check:
- [ ] Consistent naming
- [ ] Correct HTTP methods
- [ ] Proper status codes
- [ ] Error response format
- [ ] Pagination for lists
```

## Adding References

For complex skills, add supporting docs:

```
my-skill/
├── SKILL.md
└── references/
    ├── checklist.md      # Detailed checklist
    ├── examples.md       # Code examples
    └── anti-patterns.md  # What to avoid
```

Reference them in SKILL.md:
```markdown
See [checklist](references/checklist.md) for detailed review steps.
```

## Exercise: Create Your First Skill

### Step 1: Create directory
```bash
mkdir -p .claude/skills/daily-standup
```

### Step 2: Create SKILL.md
```markdown
---
name: daily-standup
description: |
  Generate daily standup updates.
  Use when: user asks for standup or daily update.
  Triggers: "standup", "daily update", "what did I do".
---

# Daily Standup Generator

Help create concise standup updates.

## Format
```
Yesterday: [what was done]
Today: [what's planned]
Blockers: [any issues]
```

## Process
1. Check recent git commits: `git log --oneline -10`
2. Look at modified files: `git status`
3. Summarize in standup format

## Keep It Brief
- Max 2-3 items per section
- Focus on outcomes, not tasks
- Mention blockers early
```

### Step 3: Test it
```
You: "help me write my standup"
Claude: [uses daily-standup skill]
```

## Tips

### Do
- Keep skills focused (one job)
- Include concrete examples
- Add triggers for auto-activation
- Use checklists for processes

### Don't
- Make skills too broad
- Skip the frontmatter
- Forget to test activation
