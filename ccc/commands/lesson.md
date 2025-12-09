# /lesson N — Go to Specific Lesson

Opens lesson by number.

## Syntax

```
/ccc:lesson 1
/ccc:lesson 2
...
/ccc:lesson 5
```

## Algorithm

### 1. Validate Number

Check that N is 1-5. If not:
```
Lesson {N} doesn't exist. Available lessons: 1-5.
```

### 2. Load Lesson Content

Lesson content is in:
```
ccc/skills/lessons/
├── lesson-1.md
├── lesson-2.md
├── lesson-3.md
├── lesson-4.md
└── lesson-5.md
```

Read `lesson-{N}.md` from the lessons skill directory and show content.

### 3. Update Progress

Progress file: `./progress.json` (in current directory)

If file doesn't exist, create it:
```json
{"version":"1.0.0","current_lesson":1,"lessons":{},"completed":false}
```

1. Set `current_lesson: N`
2. If no entry for lesson N, create:
   ```json
   "N": {
     "started_at": "ISO_DATE",
     "theory_read": false,
     "practice_completed": false,
     "practice_attempts": 0
   }
   ```
3. Save progress to `~/.claude-course/progress.json`

### 4. Lesson Format

After showing theory:
```
---

Theory complete! Now for practice.

Type `/ccc:practice` to start the hands-on task.
```

And update `theory_read: true`.

## Lesson Structure

Each lesson contains:
1. **Title** — lesson name
2. **Goals** — what you'll learn
3. **Theory** — core concepts (short blocks)
4. **Examples** — code or commands
5. **Summary** — key points

## Tone

- Use "you" informally
- Explain simply, no jargon
- Show real examples
- After theory — straight to practice
