# Skills Introduction

## What Are Skills?

Reusable instructions that extend Claude's capabilities.

Think of them as "expert modes" Claude can activate.

## Skills vs Commands

| Aspect | Commands | Skills |
|--------|----------|--------|
| Triggered by | `/command-name` | Keywords or explicit call |
| Scope | Single action | Ongoing behavior |
| Format | One prompt | Detailed instructions |
| Example | `/test` runs tests | `code-review` skill analyzes all changes |

## How Skills Work

```
┌─────────────────────────────────────┐
│  You: "review this code"            │
│              ↓                      │
│  Claude detects: code review needed │
│              ↓                      │
│  Loads: code-review skill           │
│              ↓                      │
│  Follows skill's review checklist   │
│              ↓                      │
│  Returns: structured feedback       │
└─────────────────────────────────────┘
```

## Using Skills

### Automatic (by keyword)
Skills can trigger automatically based on what you say:

```
You: "help me brainstorm this feature"
Claude: [activates brainstorming skill, uses Socratic method]
```

### Explicit invocation
Ask Claude directly:

```
You: "use the code-review skill"
Claude: [loads and follows code-review instructions]
```

## Where Skills Come From

### 1. Built into Claude Code
Some skills are built-in and always available.

### 2. Plugins
Install plugins that include skills:

```bash
cpm install fullstack-developer
```

Now skills like `backend-python`, `frontend-react` are available.

### 3. Local (your project)
Create in `.claude/skills/`:

```
.claude/
└── skills/
    └── my-skill/
        └── SKILL.md
```

## Skill File Structure

File: `.claude/skills/api-design/SKILL.md`

```markdown
---
name: api-design
description: |
  Design RESTful APIs following best practices.
  Use when: user asks about API design, endpoints, or REST.
---

# API Design Skill

## Principles
- Use nouns for resources: /users, /posts
- HTTP verbs for actions: GET, POST, PUT, DELETE
- Consistent error format

## Checklist
- [ ] Resource naming is clear
- [ ] Proper HTTP status codes
- [ ] Pagination for lists
- [ ] Versioning strategy
```

## Skill Frontmatter

The `---` section at the top:

```yaml
---
name: skill-name           # identifier
description: |
  What this skill does.
  Use when: [triggers]     # when to activate
---
```

## Finding Available Skills

```
You: "what skills do you have?"
Claude: [lists installed skills]

You: "tell me about the brainstorming skill"
Claude: [describes what it does]
```

## Try It

### See what's available
Ask: "What skills are available?"

### Use one explicitly
Ask: "Use the brainstorming skill to help me design a feature"

### Check triggers
Ask: "What triggers the code-review skill?"
