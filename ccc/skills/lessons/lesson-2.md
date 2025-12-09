# Lesson 2: Your First Skill

**Time:** ~20 minutes

## Learning Goals

After this lesson you will:
- Understand what skills are and why they're useful
- Know the SKILL.md file structure
- Create your first working skill
- Test skills

---

## What Are Skills?

A **skill** is an instruction for Claude that activates on a trigger.

Example: you have a Python project. Explaining how to run tests every time is tedious. A `python-tests` skill does this automatically.

```
Without skill: "Run pytest in tests/ folder, use -v flag, show coverage"
With skill: "run tests" → skill fills in all details
```

---

## Where Skills Live

```
your-project/
├── .claude/
│   └── skills/
│       └── my-skill/
│           └── SKILL.md    ← This is a skill
└── src/
```

Skills live in `.claude/skills/{skill-name}/SKILL.md`

---

## SKILL.md Structure

```markdown
---
name: my-skill
description: |
  Brief description.
  Use when: when to use.
  Triggers: keywords.
---

# Skill Content

Instructions for Claude...
```

### Frontmatter (required)

| Field | Description |
|-------|-------------|
| `name` | Unique skill name |
| `description` | When and why to use |

### Triggers

Triggers — words that activate the skill:
- "run tests" → triggers: "tests", "pytest"
- "create component" → triggers: "component"

Claude determines when to use a skill based on description and triggers.

---

## Example: Git Skill

```markdown
---
name: git-commit
description: |
  Helps create meaningful commits.
  Use when: user wants to commit changes.
  Triggers: "commit", "save changes".
---

# Git Commit Helper

When user wants to commit:

1. Show `git status` and `git diff --stat`
2. Suggest commit message:
   - Format: type(scope): description
   - Types: feat, fix, docs, refactor, test
3. Ask for confirmation before committing

## Good Message Examples

- feat(auth): add password reset flow
- fix(api): handle null response from server
- docs(readme): update installation steps
```

---

## How Claude Chooses a Skill

1. You write: "make a commit"
2. Claude sees trigger "commit" in skill description
3. Claude reads SKILL.md
4. Claude follows instructions

If triggers match multiple skills — Claude chooses the most appropriate one.

---

## Summary

- Skills = reusable instructions
- Live in `.claude/skills/{name}/SKILL.md`
- Frontmatter: name + description (with triggers)
- Claude activates by keywords

---

## Practice

Now I'll demonstrate creating a skill.

**Task:** Create a `code-style` skill that enforces coding standards.

**Watch me do it:**

---

## Practice Execution

**IMPORTANT:** As the tutor, YOU (Claude) must execute this practice, not the user.

1. Create the skill directory and file:

```bash
mkdir -p .claude/skills/code-style
cat > .claude/skills/code-style/SKILL.md << 'EOF'
---
name: code-style
description: |
  Enforces coding style guidelines.
  Use when: reviewing or writing code.
  Triggers: "code style", "lint", "format", "clean up code".
---

# Code Style Guide

When writing or reviewing code:

## Rules
- Use 2-space indentation
- Prefer const over let
- Use descriptive variable names
- Add comments for complex logic

## Example
```js
// Good
const getUserById = async (id) => {
  const user = await db.users.find(id);
  return user;
};
```
EOF
```

2. Show the user what was created:
```bash
cat .claude/skills/code-style/SKILL.md
```

3. Explain and congratulate:
```
✓ Practice completed!

I created a skill at .claude/skills/code-style/SKILL.md

Key parts:
- Frontmatter (---) with name, description, triggers
- Instructions that Claude follows when skill activates

Now when you say "check code style", this skill guides my response.

Ready for Lesson 3? Type `/ccc:lesson 3` or say "next"
```

**After execution:**
- Update progress: `practice_completed: true`, `current_lesson: 3`
- Clean up: `rm -rf .claude/skills/code-style` (demo only)
