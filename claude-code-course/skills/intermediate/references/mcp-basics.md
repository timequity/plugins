# MCP Basics

## What is MCP?

**Model Context Protocol** — a standard for connecting Claude to external tools and data.

```
┌─────────────┐     MCP      ┌─────────────┐
│   Claude    │◄────────────►│  MCP Server │
│   Code      │              │  (tools)    │
└─────────────┘              └─────────────┘
                                   │
                                   ▼
                             ┌─────────────┐
                             │  Database   │
                             │  API        │
                             │  Filesystem │
                             └─────────────┘
```

## Why Use MCP?

| Without MCP | With MCP |
|-------------|----------|
| Claude can only use built-in tools | Claude can use ANY tool you provide |
| Limited to file operations | Database queries, API calls, etc. |
| Manual copy-paste for data | Direct access to data sources |

## Common MCP Servers

| Server | What it does |
|--------|--------------|
| `filesystem` | Access files outside working dir |
| `sqlite` | Query SQLite databases |
| `postgres` | Query PostgreSQL |
| `github` | GitHub API operations |
| `slack` | Slack integration |
| `memory` | Persistent memory storage |

## Configuration

### Project-level: `.mcp.json`

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "./data.db"]
    }
  }
}
```

### Global: Claude Code settings

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-filesystem", "/path/to/allowed/dir"]
    }
  }
}
```

## MCP Server Anatomy

```json
{
  "mcpServers": {
    "server-name": {
      "command": "how to run it",
      "args": ["arguments", "to", "pass"],
      "env": {
        "API_KEY": "optional env vars"
      }
    }
  }
}
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `command` | Yes | Executable (npx, uvx, node, python) |
| `args` | Yes | Command arguments |
| `env` | No | Environment variables |

## Example: SQLite Server

### Step 1: Create `.mcp.json`
```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "./mydata.db"]
    }
  }
}
```

### Step 2: Restart Claude Code

### Step 3: Use it
```
You: "Query the users table"
Claude: [uses sqlite MCP to run query]
```

## Example: Filesystem Server

Access files outside your project:

```json
{
  "mcpServers": {
    "home-files": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-filesystem", "/Users/me/Documents"]
    }
  }
}
```

Now Claude can read/write files in ~/Documents.

## Finding MCP Servers

- **Official**: github.com/anthropics/mcp-servers
- **Community**: Search "mcp-server" on npm/PyPI
- **Build your own**: See Advanced level

## Exercise: Set Up Your First MCP

### Option A: SQLite (if you have Python/uv)

1. Create test database:
```bash
sqlite3 test.db "CREATE TABLE notes (id INTEGER PRIMARY KEY, text TEXT); INSERT INTO notes (text) VALUES ('Hello MCP!');"
```

2. Create `.mcp.json`:
```json
{
  "mcpServers": {
    "notes-db": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "./test.db"]
    }
  }
}
```

3. Restart Claude Code

4. Test:
```
You: "What's in the notes table?"
```

### Option B: Just understand

If you can't set up MCP now, that's fine. Key takeaways:
- MCP connects Claude to external tools
- Configured via `.mcp.json` or settings
- Many pre-built servers available

## Troubleshooting

### Server not connecting
- Check command exists (`which npx`, `which uvx`)
- Verify args are correct
- Restart Claude Code after config changes

### Permission errors
- MCP servers need explicit paths
- Check file/directory permissions

## Tips

- Start with one server
- Use project-level config for project-specific tools
- Global config for always-available tools
