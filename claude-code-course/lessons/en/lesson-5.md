# Lesson 5: Building an Application

**Time:** ~30 minutes

## Learning Goals

In this final lesson you will:
- Combine all knowledge from previous lessons
- Create a complete application from scratch
- Configure skills, agents, and hooks
- Deploy the result

---

## What We'll Create

A simple application — **Todo List** with ability to:
- Add tasks
- Mark as completed
- Delete tasks

**Technologies:** HTML + JavaScript (no frameworks).

---

## Plan

| Step | What we do | Claude Code Tool |
|------|------------|------------------|
| 1 | Project structure | Command |
| 2 | HTML + CSS | Skill |
| 3 | JavaScript logic | Agent |
| 4 | Auto-formatting | Hook |
| 5 | Deploy | Command |

---

## Step 1: Create Project

Create structure:

```
todo-app/
├── .claude/
│   ├── skills/
│   │   └── todo-style/
│   │       └── SKILL.md
│   ├── agents/
│   │   └── todo-logic.md
│   └── settings.json
├── index.html
├── style.css
└── app.js
```

**Task:** Ask Claude to create this structure.

---

## Step 2: Skill for Styles

Create a skill that knows your app's style:

```markdown
---
name: todo-style
description: |
  Styles for Todo app.
  Use when: need to add or change styles.
  Triggers: "styles", "css", "design".
---

# Todo App Styles

## Color Scheme
- Background: #f5f5f5
- Cards: #ffffff
- Accent: #4CAF50
- Text: #333333

## Rules
- Minimalist design
- Rounded corners (8px)
- Shadows for cards
- Hover animations
```

---

## Step 3: Agent for Logic

Create an agent that writes JavaScript:

```markdown
---
name: todo-logic
description: Implements Todo app logic.
tools:
  - Read
  - Write
  - Edit
model: sonnet
---

# Todo Logic Agent

Implement Todo list functionality.

## Requirements

1. Store in localStorage
2. Functions: addTodo, toggleTodo, deleteTodo
3. Render list on changes
4. No external dependencies

## Data Structure

```js
const todos = [
  { id: 1, text: "Task", done: false }
]
```
```

---

## Step 4: Hook for Formatting

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

---

## Step 5: Deploy

Options:
1. **GitHub Pages** — free hosting for static sites
2. **Vercel** — one-click deploy
3. **Netlify** — Vercel alternative

**For GitHub Pages:**

```bash
# Create repository
gh repo create todo-app --public

# Push code
git add .
git commit -m "Initial commit"
git push -u origin main

# Enable Pages
# Go to: Settings → Pages → Source: main branch
```

---

## Putting It All Together

Now you have:

| Component | File | Purpose |
|-----------|------|---------|
| Skill | `.claude/skills/todo-style/SKILL.md` | Style knowledge |
| Agent | `.claude/agents/todo-logic.md` | Writing logic |
| Hook | `.claude/settings.json` | Auto-formatting |

Try:
1. "Add a clear all button" → skill suggests styles
2. "Implement task sorting" → agent writes code
3. Any edit → hook formats

---

## Practice

**Task:** Create a Todo project structure with a style skill.

**Minimum Requirements:**
1. Folder `todo-app/` with files `index.html`, `style.css`, `app.js`
2. Skill `todo-app/.claude/skills/todo-style/SKILL.md`

**Steps:**
1. Ask Claude to create project structure
2. Create style skill (use knowledge from lesson 2)
3. Ask Claude to add basic HTML and CSS

**Bonus (optional):**
- Add logic agent
- Configure formatting hook
- Deploy to GitHub Pages

---

## Congratulations!

You've completed the entire Claude Code course!

```
████████████████████ 100%
```

**Now you know how to:**
- Communicate effectively with Claude
- Create skills for repeating tasks
- Use agents for complex work
- Automate routine with hooks
- Build applications with Claude Code

---

## What's Next?

1. **Create your own plugin** — share skills with community
2. **Explore other plugins** — see what others have created
3. **Experiment** — try new combinations of skills and agents

---

Thanks for taking the course! Good luck programming with Claude!

---

## Practice Verification

When user says "done", run verification:

```bash
# Lesson 5 check
if [ -d "todo-app" ] && \
   [ -f "todo-app/index.html" ] && \
   [ -f "todo-app/.claude/skills/todo-style/SKILL.md" ]; then
  echo "✓ Project created with proper structure!"
else
  echo "✗ Check structure:"
  echo "  - todo-app/index.html"
  echo "  - todo-app/style.css"
  echo "  - todo-app/app.js"
  echo "  - todo-app/.claude/skills/todo-style/SKILL.md"
fi
```

**On success:**
- Update progress: `practice_completed: true`, `completed: true`
- Show final congratulations with 100% progress bar

**On failure:**
- Show which files are missing
- Suggest creating missing ones
