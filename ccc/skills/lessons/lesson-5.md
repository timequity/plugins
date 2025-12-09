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

### 1. Create the project structure:

```bash
mkdir -p todo-app/.claude/skills/todo-style
```

### 2. Create the HTML (with congratulations overlay):

```bash
cat > todo-app/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Todos - Claude Code Course</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div id="congrats" class="congrats-overlay">
    <div class="congrats-content">
      <h1>Congratulations!</h1>
      <p>You completed the Claude Code Course</p>
      <div class="stats">5 lessons completed</div>
      <button onclick="closeCongrats()">Start Using Your App</button>
    </div>
    <div class="confetti" id="confetti"></div>
  </div>

  <div class="container">
    <h1>My Todos</h1>
    <div class="input-row">
      <input type="text" id="input" placeholder="Add a task..." onkeypress="handleKey(event)">
      <button onclick="addTodo()">Add</button>
    </div>
    <ul id="list"></ul>
    <div class="footer">Built with Claude Code</div>
  </div>
  <script src="app.js"></script>
</body>
</html>
EOF
```

### 3. Create the CSS (Tech Innovation theme + glassmorphism):

```bash
cat > todo-app/style.css << 'EOF'
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  min-height: 100vh;
  background: linear-gradient(135deg, #1e1e1e 0%, #0a1628 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.container {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 32px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 8px 32px rgba(0, 102, 255, 0.2);
}

h1 {
  color: #fff;
  font-size: 28px;
  margin-bottom: 24px;
  text-align: center;
}

.input-row {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
}

input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid rgba(0, 102, 255, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
  font-size: 16px;
  outline: none;
  transition: border-color 0.2s;
}

input:focus { border-color: #0066ff; }
input::placeholder { color: rgba(255, 255, 255, 0.4); }

button {
  padding: 12px 24px;
  background: linear-gradient(135deg, #0066ff, #00ffff);
  border: none;
  border-radius: 8px;
  color: #1e1e1e;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 102, 255, 0.4);
}

ul { list-style: none; }

li {
  padding: 14px 16px;
  margin-bottom: 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  animation: slideIn 0.3s ease;
}

li.done { opacity: 0.5; text-decoration: line-through; }
li span { cursor: pointer; flex: 1; }
li button { padding: 4px 12px; background: rgba(255, 0, 0, 0.2); font-size: 12px; }

.footer {
  text-align: center;
  color: rgba(255, 255, 255, 0.3);
  font-size: 12px;
  margin-top: 24px;
}

/* Congrats Overlay */
.congrats-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(10, 22, 40, 0.95);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.5s ease;
}

.congrats-overlay.hidden { display: none; }

.congrats-content {
  text-align: center;
  animation: scaleIn 0.5s ease 0.2s both;
}

.congrats-content h1 {
  font-size: 48px;
  background: linear-gradient(135deg, #0066ff, #00ffff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 16px;
}

.congrats-content p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 20px;
  margin-bottom: 8px;
}

.stats {
  color: #00ffff;
  font-size: 14px;
  margin-bottom: 32px;
}

.congrats-content button {
  padding: 16px 32px;
  font-size: 18px;
  animation: pulse 2s infinite;
}

/* Confetti */
.confetti {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  pointer-events: none;
  overflow: hidden;
}

.confetti-piece {
  position: absolute;
  width: 10px;
  height: 10px;
  top: -10px;
  animation: fall 3s linear forwards;
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes scaleIn { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
@keyframes slideIn { from { transform: translateX(-20px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
@keyframes pulse { 0%, 100% { box-shadow: 0 0 0 0 rgba(0, 102, 255, 0.4); } 50% { box-shadow: 0 0 0 15px rgba(0, 102, 255, 0); } }
@keyframes fall { to { transform: translateY(100vh) rotate(720deg); opacity: 0; } }
EOF
```

### 4. Create the JavaScript (with localStorage and confetti):

```bash
cat > todo-app/app.js << 'EOF'
let todos = JSON.parse(localStorage.getItem('todos') || '[]');

function saveTodos() {
  localStorage.setItem('todos', JSON.stringify(todos));
}

function addTodo() {
  const input = document.getElementById('input');
  const text = input.value.trim();
  if (text) {
    todos.push({ id: Date.now(), text, done: false });
    saveTodos();
    render();
    input.value = '';
  }
}

function handleKey(e) {
  if (e.key === 'Enter') addTodo();
}

function toggleTodo(id) {
  const todo = todos.find(t => t.id === id);
  if (todo) { todo.done = !todo.done; saveTodos(); render(); }
}

function deleteTodo(id) {
  todos = todos.filter(t => t.id !== id);
  saveTodos();
  render();
}

function render() {
  const list = document.getElementById('list');
  list.innerHTML = todos.map(t => `
    <li class="${t.done ? 'done' : ''}">
      <span onclick="toggleTodo(${t.id})">${t.text}</span>
      <button onclick="deleteTodo(${t.id})">Delete</button>
    </li>
  `).join('');
}

function closeCongrats() {
  document.getElementById('congrats').classList.add('hidden');
}

function createConfetti() {
  const container = document.getElementById('confetti');
  const colors = ['#0066ff', '#00ffff', '#ffffff', '#ff6b6b', '#ffd93d'];
  for (let i = 0; i < 50; i++) {
    const piece = document.createElement('div');
    piece.className = 'confetti-piece';
    piece.style.left = Math.random() * 100 + '%';
    piece.style.background = colors[Math.floor(Math.random() * colors.length)];
    piece.style.animationDelay = Math.random() * 2 + 's';
    piece.style.animationDuration = (2 + Math.random() * 2) + 's';
    container.appendChild(piece);
  }
}

render();
createConfetti();
EOF
```

### 5. Create the style skill:

```bash
cat > todo-app/.claude/skills/todo-style/SKILL.md << 'EOF'
---
name: todo-style
description: |
  Style guide for todo app.
  Use when: modifying styles.
  Triggers: "style", "css", "design".
---

# Todo App Styles (Tech Innovation Theme)

## Colors
- Primary: #0066ff (Electric Blue)
- Accent: #00ffff (Neon Cyan)
- Background: #1e1e1e (Dark Gray)
- Text: #ffffff

## Design
- Glassmorphism cards
- 16px border radius
- Gradient buttons
- Smooth animations
EOF
```

### 6. Show what was created:

```bash
find todo-app -type f
```

### 7. Open in browser (cross-platform):

```bash
# macOS
open todo-app/index.html 2>/dev/null || \
# Linux
xdg-open todo-app/index.html 2>/dev/null || \
# Windows (Git Bash / WSL)
start todo-app/index.html 2>/dev/null || \
echo "Open todo-app/index.html in your browser"
```

### 8. Congratulate:

```
✓ Course completed!

████████████████████ 100%

Your graduation gift: a beautiful todo app with confetti!

The app is saved in: ./todo-app/
You can open it anytime in your browser.

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
- DO NOT delete the app — it's the user's graduation gift!
