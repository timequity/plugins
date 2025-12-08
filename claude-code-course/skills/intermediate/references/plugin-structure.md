# Plugin Structure

## What Are Plugins?

Bundles of skills, commands, and agents that can be shared or sold.

## Directory Structure

```
my-plugin/
├── .claude-plugin/
│   └── marketplace.json    # Plugin metadata
├── SKILL.md                # Optional: entry point skill
├── skills/
│   ├── skill-one/
│   │   └── SKILL.md
│   └── skill-two/
│       ├── SKILL.md
│       └── references/
├── commands/
│   ├── cmd-one.md
│   └── cmd-two.md
└── agents/
    └── my-agent.md
```

## marketplace.json

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does",
  "author": "your-name",
  "price": 0,
  "category": "development",
  "tags": ["tag1", "tag2"],
  "skills": [
    "./skills/skill-one",
    "./skills/skill-two"
  ],
  "agents": [
    "./agents/my-agent.md"
  ]
}
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier |
| `version` | Yes | Semver (1.0.0) |
| `description` | Yes | One-line summary |
| `author` | Yes | Your name/handle |
| `price` | Yes | 0 for free |
| `category` | Yes | development, education, etc. |
| `tags` | No | Search keywords |
| `skills` | No | Paths to skills |
| `agents` | No | Paths to agents |

## Categories

- `development` — coding tools
- `education` — learning materials
- `productivity` — workflow helpers
- `writing` — content creation
- `data` — data analysis

## Adding Commands

Commands go in `commands/` directory:

```
commands/
├── build.md      # /build command
├── test.md       # /test command
└── deploy.md     # /deploy command
```

Each file becomes a slash command with the filename.

### Command with prefix

For namespaced commands like `/my:build`:
```
commands/
└── my/
    └── build.md   # /my:build
```

Or use colons in filename:
```
commands/
└── my:build.md    # /my:build
```

## Adding Agents

Agents are autonomous workers Claude can spawn:

```markdown
---
name: code-reviewer
description: Reviews code changes for issues
tools: [Read, Glob, Grep, Bash]
---

# Code Reviewer Agent

Review code changes and report issues.

## Process
1. Get list of changed files
2. Read each file
3. Check for issues
4. Report findings

## Output Format
...
```

## Exercise: Create a Mini Plugin

### Step 1: Create structure
```bash
mkdir -p my-first-plugin/{.claude-plugin,skills/greeting,commands}
```

### Step 2: Create marketplace.json
```json
{
  "name": "my-first-plugin",
  "version": "1.0.0",
  "description": "My first Claude Code plugin",
  "author": "me",
  "price": 0,
  "category": "productivity",
  "tags": ["learning", "first"],
  "skills": ["./skills/greeting"]
}
```

### Step 3: Create a skill
`skills/greeting/SKILL.md`:
```markdown
---
name: greeting
description: |
  Personalized greetings.
  Use when: user says hello or asks for greeting.
---

# Greeting Skill

Greet users warmly based on time of day.

- Morning (5-12): "Good morning!"
- Afternoon (12-17): "Good afternoon!"
- Evening (17-21): "Good evening!"
- Night (21-5): "Working late? Nice dedication!"
```

### Step 4: Create a command
`commands/hello.md`:
```markdown
Say hello using the greeting skill.
Check current time and give appropriate greeting.
```

### Step 5: Test it
```
/hello
```

## Local vs Published Plugins

### Local (development)
Put in your project's `.claude/` or a directory you control.

### Published (marketplace)
Submit to marketplace for others to install via `cpm install`.

## Tips

- Start small (1-2 skills)
- Test locally first
- Use clear descriptions
- Include examples in skills
