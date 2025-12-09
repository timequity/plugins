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

Now I'll demonstrate putting everything together.

**Task:** Create a mini todo-app with a skill.

**Watch me do it:**

---

## Practice Execution

**IMPORTANT:** As the tutor, YOU (Claude) must execute this practice, not the user.

1. Create the project structure:

```bash
mkdir -p todo-demo/.claude/skills/todo-style
```

2. Create the HTML:

```bash
cat > todo-demo/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
  <title>Todo App</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="container">
    <h1>My Todos</h1>
    <input type="text" id="input" placeholder="Add a task...">
    <button onclick="addTodo()">Add</button>
    <ul id="list"></ul>
  </div>
  <script src="app.js"></script>
</body>
</html>
EOF
```

3. Create the CSS:

```bash
cat > todo-demo/style.css << 'EOF'
body { font-family: system-ui; max-width: 400px; margin: 50px auto; }
.container { padding: 20px; }
input { padding: 8px; width: 70%; }
button { padding: 8px 16px; }
ul { list-style: none; padding: 0; }
li { padding: 10px; margin: 5px 0; background: #f5f5f5; border-radius: 4px; }
EOF
```

4. Create the JavaScript:

```bash
cat > todo-demo/app.js << 'EOF'
const todos = [];
function addTodo() {
  const input = document.getElementById('input');
  if (input.value) {
    todos.push(input.value);
    render();
    input.value = '';
  }
}
function render() {
  const list = document.getElementById('list');
  list.innerHTML = todos.map(t => `<li>${t}</li>`).join('');
}
EOF
```

5. Create the style skill:

```bash
cat > todo-demo/.claude/skills/todo-style/SKILL.md << 'EOF'
---
name: todo-style
description: |
  Style guide for todo app.
  Use when: modifying styles.
  Triggers: "style", "css", "design".
---

# Todo App Styles

- Background: #f5f5f5
- Accent: #4CAF50
- Border radius: 4px
- Font: system-ui
EOF
```

6. Show what was created:

```bash
find todo-demo -type f
```

7. Congratulate:

```
✓ Course completed!

████████████████████ 100%

I created a mini todo app with:
- index.html — structure
- style.css — styling
- app.js — functionality
- .claude/skills/todo-style/SKILL.md — style guide

You've learned:
- Claude Code basics
- Creating skills
- Creating agents
- Setting up hooks
- Putting it all together

What's next?
- Build your own project with Claude
- Create custom skills for your workflow
- Share your plugins with the community
```

**After execution:**
- Update progress: `practice_completed: true`, `completed: true`
- Clean up: `rm -rf todo-demo` (demo only)
