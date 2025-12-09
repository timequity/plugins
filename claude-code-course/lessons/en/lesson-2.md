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

**Task:** Create a `greeting` skill that greets in a friendly way.

**Requirements:**
1. Path: `.claude/skills/greeting/SKILL.md`
2. Triggers: "hello", "hi", "greet"
3. Should respond with a friendly greeting when activated

**Steps:**
1. Create folder `.claude/skills/greeting/`
2. Create `SKILL.md` file with proper structure
3. Write instructions for Claude

**Verification:**
After creating, write "hello" — I should respond specially (according to the skill).

<details>
<summary>Hint</summary>

```markdown
---
name: greeting
description: |
  Greets the user.
  Use when: user says hello.
  Triggers: "hello", "hi", "greet".
---

# Greeting

When user greets:
- Respond friendly
- Ask how you can help
- Use their name if known
```

</details>

When done, say "done" and I'll verify the result.

---

## Practice Verification

When user says "done", run verification:

```bash
# Lesson 2 check
SKILL_FILE=".claude/skills/greeting/SKILL.md"
if [ -f "$SKILL_FILE" ]; then
  # Check frontmatter
  if head -20 "$SKILL_FILE" | grep -q "^name:" && \
     head -20 "$SKILL_FILE" | grep -q "^description:"; then
    echo "✓ Skill created with proper structure!"
  else
    echo "✗ File exists but missing frontmatter (name/description)"
  fi
else
  echo "✗ File .claude/skills/greeting/SKILL.md not found"
fi
```

**On success:**
- Update progress: `practice_completed: true`
- Show congratulations and suggest moving to lesson 3

**On failure:**
- Explain what's wrong (path? structure?)
- Show example of correct frontmatter
