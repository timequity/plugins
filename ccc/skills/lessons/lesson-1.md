# Lesson 1: Claude Code Basics

**Time:** ~15 minutes

## Learning Goals

After this lesson you will:
- Understand what Claude Code is and how it works
- Know the basic terminal commands
- Communicate effectively with Claude
- Create your first file through dialogue

---

## What is Claude Code?

Claude Code is a CLI tool that turns Claude into your programming partner. You chat with it in the terminal, and it helps write code, search files, and run commands.

**Key difference from ChatGPT/web Claude:**
- Claude Code works in YOUR terminal
- Sees YOUR files
- Can EXECUTE commands (with your permission)

---

## Interface

When you run `claude`, you see:

```
╭─────────────────────────────────────╮
│  Claude Code                        │
│  /help for commands                 │
╰─────────────────────────────────────╯

>
```

`>` — type your messages here.

---

## Basic Commands

| Command | What it does |
|---------|--------------|
| `/help` | Shows help |
| `/clear` | Clears conversation history |
| `/compact` | Compresses context (for long conversations) |
| `/cost` | Shows tokens spent |
| `Ctrl+C` | Interrupts current action |
| `Esc` → `Esc` | Exit Claude Code |

Try typing `/help` right now!

---

## Communicating Effectively with Claude

### Rule 1: Be Specific

```
❌ Bad: "Make it pretty"
✓ Good: "Add 16px padding between sections"
```

### Rule 2: Provide Context

```
❌ Bad: "Fix the bug"
✓ Good: "The login() function returns null instead of a user object"
```

### Rule 3: Break Down Large Tasks

```
❌ Bad: "Create an e-commerce site"
✓ Good: "Create a Product model with name, price, description fields"
```

### Rule 4: Verify Results

Claude can make mistakes. Always check what it did:
- Read the generated code
- Run tests
- Verify the logic

---

## What Claude Can Do

| Can | Cannot |
|-----|--------|
| Read your files | Read other computers |
| Run commands | Run without permission |
| Search code | Access internet* |
| Create files | Delete system files |

*Claude can use web search if enabled.

---

## Summary

- Claude Code — CLI for working with Claude in terminal
- `/help` — your friend
- Specific prompts = better results
- Claude can make mistakes — verify

---

## Practice

Now I'll demonstrate what you learned by creating a file.

**Task:** Create a CLAUDE.md file for a sample project.

**Watch me do it:**

```
I'll create a CLAUDE.md file that describes a hypothetical project.
This shows how Claude Code can create files through conversation.
```

---

## Practice Execution

**IMPORTANT:** As the tutor, YOU (Claude) must execute this practice, not the user.

1. Create the file:

```bash
cat > CLAUDE.md << 'EOF'
# CLAUDE.md

## Project
A simple CLI todo app for learning Claude Code.

## Stack
- Node.js
- SQLite for storage

## Commands
- `npm start` — run the app
- `npm test` — run tests
EOF
```

2. Show the user what was created:
```bash
cat CLAUDE.md
```

3. Update progress and congratulate:
```
✓ Practice completed!

I just created a CLAUDE.md file. This is how you describe projects to Claude.
Key sections: Project (what it is), Stack (technologies), Commands (how to run).

Ready for Lesson 2? Type `/ccc:lesson 2` or just say "next"
```

**After execution:**
- Update progress: `practice_completed: true`, `current_lesson: 2`
- Clean up: `rm CLAUDE.md` (it was just a demo)
