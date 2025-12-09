# What is Claude Code?

## Quick Answer

Claude Code = Claude AI + your file system + developer tools

It's an **agentic coding assistant** that runs in your terminal and can directly interact with your project.

## Claude Chat vs Claude Code

| Capability | Claude Chat | Claude Code |
|------------|-------------|-------------|
| Answer questions | Yes | Yes |
| Read your files | No | Yes |
| Edit your files | No | Yes |
| Run commands | No | Yes |
| Use external tools | No | Yes (via MCP) |
| Remember project context | No | Yes (CLAUDE.md) |

## What Claude Code Can Do

### Read Files
```
You: "What does src/main.rs do?"
Claude: [reads the file and explains]
```

### Edit Files
```
You: "Add error handling to this function"
Claude: [edits the file directly]
```

### Run Commands
```
You: "Run the tests"
Claude: [executes npm test or pytest]
```

### Multi-step Tasks
```
You: "Refactor auth module and update tests"
Claude: [plans → edits multiple files → runs tests → reports]
```

## How It Works

```
┌─────────────────────────────────────┐
│           Your Terminal             │
│  ┌───────────────────────────────┐  │
│  │        Claude Code            │  │
│  │  ┌─────────┐  ┌────────────┐  │  │
│  │  │ Claude  │←→│   Tools    │  │  │
│  │  │   AI    │  │ - Read     │  │  │
│  │  │         │  │ - Write    │  │  │
│  │  │         │  │ - Edit     │  │  │
│  │  │         │  │ - Bash     │  │  │
│  │  │         │  │ - Search   │  │  │
│  │  └─────────┘  └────────────┘  │  │
│  └───────────────────────────────┘  │
│                 ↕                   │
│         Your Project Files          │
└─────────────────────────────────────┘
```

## Key Concepts

### Tools
Built-in capabilities Claude can use:
- **Read** — view file contents
- **Write** — create new files
- **Edit** — modify existing files
- **Bash** — run shell commands
- **Glob/Grep** — search files

### Context
Claude sees:
- Current working directory
- Files you mention or it reads
- CLAUDE.md instructions
- Conversation history

### Permissions
Claude asks before:
- Editing files
- Running commands
- Making changes

You stay in control.

## Try It

Ask Claude Code something only it can answer:

```
"What files are in this project?"
"Show me the most recently modified file"
"What's in my package.json?"
```

Watch how it uses tools to find and read the information.
