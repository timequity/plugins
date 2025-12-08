# Building MCP Servers

## What You'll Build

Custom integrations that give Claude new capabilities.

```
┌─────────────┐
│   Claude    │
│   Code      │
└──────┬──────┘
       │ MCP
       ▼
┌─────────────┐
│ Your Server │──► Database
│             │──► API
│             │──► Anything!
└─────────────┘
```

## Two Approaches

| Approach | Language | Best For |
|----------|----------|----------|
| FastMCP | Python | Quick prototypes, Python devs |
| MCP SDK | TypeScript | Production, Node ecosystem |

## FastMCP (Python)

### Installation
```bash
pip install fastmcp
```

### Minimal Server

```python
# server.py
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def hello(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

### Run it
```bash
python server.py
```

### Configure in Claude Code

`.mcp.json`:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["path/to/server.py"]
    }
  }
}
```

## FastMCP: Real Example

Weather lookup server:

```python
# weather_server.py
from fastmcp import FastMCP
import httpx

mcp = FastMCP("weather")

@mcp.tool()
async def get_weather(city: str) -> str:
    """Get current weather for a city."""
    async with httpx.AsyncClient() as client:
        # Using wttr.in (no API key needed)
        resp = await client.get(f"https://wttr.in/{city}?format=3")
        return resp.text

@mcp.tool()
def convert_temp(celsius: float) -> dict:
    """Convert Celsius to Fahrenheit and Kelvin."""
    return {
        "celsius": celsius,
        "fahrenheit": celsius * 9/5 + 32,
        "kelvin": celsius + 273.15
    }

if __name__ == "__main__":
    mcp.run()
```

## MCP SDK (TypeScript)

### Installation
```bash
npm install @modelcontextprotocol/sdk
```

### Minimal Server

```typescript
// server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "my-server",
  version: "1.0.0",
});

server.setRequestHandler("tools/list", async () => ({
  tools: [{
    name: "hello",
    description: "Say hello",
    inputSchema: {
      type: "object",
      properties: {
        name: { type: "string", description: "Name to greet" }
      },
      required: ["name"]
    }
  }]
}));

server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "hello") {
    const name = request.params.arguments.name;
    return { content: [{ type: "text", text: `Hello, ${name}!` }] };
  }
  throw new Error("Unknown tool");
});

const transport = new StdioServerTransport();
server.connect(transport);
```

### Run it
```bash
npx ts-node server.ts
```

## MCP Concepts

### Tools
Functions Claude can call:

```python
@mcp.tool()
def search_database(query: str) -> list[dict]:
    """Search the database for records."""
    # Your implementation
    return results
```

### Resources
Data Claude can access:

```python
@mcp.resource("config://app")
def get_config() -> str:
    """Application configuration."""
    return json.dumps(config)
```

### Prompts
Pre-defined prompts:

```python
@mcp.prompt()
def analyze_prompt(data: str) -> str:
    """Prompt for data analysis."""
    return f"Analyze this data and provide insights:\n\n{data}"
```

## Exercise: Build a Notes Server

Simple server to save and retrieve notes.

### Step 1: Create server

```python
# notes_server.py
from fastmcp import FastMCP
import json
from pathlib import Path

mcp = FastMCP("notes")
NOTES_FILE = Path("notes.json")

def load_notes() -> dict:
    if NOTES_FILE.exists():
        return json.loads(NOTES_FILE.read_text())
    return {}

def save_notes(notes: dict):
    NOTES_FILE.write_text(json.dumps(notes, indent=2))

@mcp.tool()
def add_note(title: str, content: str) -> str:
    """Add a new note."""
    notes = load_notes()
    notes[title] = content
    save_notes(notes)
    return f"Note '{title}' saved."

@mcp.tool()
def get_note(title: str) -> str:
    """Get a note by title."""
    notes = load_notes()
    return notes.get(title, f"Note '{title}' not found.")

@mcp.tool()
def list_notes() -> list[str]:
    """List all note titles."""
    return list(load_notes().keys())

@mcp.tool()
def delete_note(title: str) -> str:
    """Delete a note."""
    notes = load_notes()
    if title in notes:
        del notes[title]
        save_notes(notes)
        return f"Note '{title}' deleted."
    return f"Note '{title}' not found."

if __name__ == "__main__":
    mcp.run()
```

### Step 2: Configure

`.mcp.json`:
```json
{
  "mcpServers": {
    "notes": {
      "command": "python",
      "args": ["notes_server.py"]
    }
  }
}
```

### Step 3: Test

```
You: "Save a note titled 'meeting' with today's action items"
Claude: [uses add_note tool]

You: "What notes do I have?"
Claude: [uses list_notes tool]
```

## Debugging MCP Servers

### Check server runs standalone
```bash
python server.py
# Should start without errors
```

### Check Claude Code sees it
Ask Claude: "What MCP tools do you have?"

### Common issues
- Wrong Python/Node path in command
- Missing dependencies
- Server crashes on startup

## Publishing MCP Servers

### PyPI (Python)
```bash
pip install build twine
python -m build
twine upload dist/*
```

### npm (TypeScript)
```bash
npm publish
```

Then users install with:
```bash
pip install your-mcp-server
# or
npm install your-mcp-server
```

## Tips

- Start simple (one tool)
- Test standalone first
- Add tools incrementally
- Document each tool clearly
- Handle errors gracefully
