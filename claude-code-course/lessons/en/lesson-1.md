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

Your turn!

**Task:** Create a file `hello.txt` in the current directory with the text "Hello from Claude!"

**How to do it:**
1. Ask Claude to create the file
2. Verify it was created (`ls` or `cat hello.txt`)

**Hint:** Just write "Create a file hello.txt with text Hello from Claude!"

When done, say "done" and I'll verify the result.

---

## Practice Verification

When user says "done", run verification:

```bash
# Lesson 1 check
if [ -f "hello.txt" ] && grep -q "Hello" hello.txt; then
  echo "✓ Practice completed!"
else
  echo "✗ File hello.txt not found or doesn't contain greeting"
fi
```

**On success:**
- Update progress: `practice_completed: true`
- Show congratulations and suggest moving to lesson 2

**On failure:**
- Explain what's wrong
- Suggest trying again
