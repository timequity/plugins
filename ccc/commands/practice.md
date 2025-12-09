# /ccc:practice — Practice Task

Starts practice for current lesson.

## Syntax

```
/ccc:practice
```

## Algorithm

### 1. Load Progress

Get `current_lesson` from `~/.claude-course/progress.json`.

### 2. Check Readiness

If `theory_read: false` for current lesson:
```
First read the lesson {N} theory.

Type `/ccc:lesson {N}` to read the material.
```

### 3. Show Task

Practice tasks are in lesson files (## Practice section).

### 4. Task Format

```
# Practice: Lesson {N}

## Task

{Clear description of what to do}

## Steps

1. {Step 1}
2. {Step 2}
3. {Step 3}

## Verification

When done, say "done" and I'll verify the result.

## Hint

<details>
<summary>Need help?</summary>

{Hint without full solution}

</details>
```

### 5. Update Attempt Counter

On each practice launch:
```json
"N": {
  "practice_attempts": practice_attempts + 1
}
```

### 6. Verify Completion

When user says "done" or "verify":
1. Run verification (depends on task)
2. If successful:
   - Update `practice_completed: true`
   - Update `completed_at: ISO_DATE`
   - Update `current_lesson: N + 1`
   - Show congratulations
3. If unsuccessful:
   - Explain what's wrong
   - Suggest trying again

### 7. Successful Completion

```
Great! Lesson {N} practice completed.

You learned:
- {Skill 1}
- {Skill 2}

Progress: ████████░░░░░░░░░░░░ {X}/5

Ready for next lesson? Type `/ccc:lesson {N+1}`
```

### 8. Final Lesson Completion

If N = 5 and practice is successful:
```
Congratulations! You've completed the entire Claude Code course!

████████████████████ 100%

Now you know:
- CLI basics and commands
- How to create skills
- How to work with agents
- How to configure hooks
- How to build applications

What's next?
- Create your first plugin for marketplace
- Share your experience with the community
```

And update `completed: true` in progress.

## Practices by Lesson

| Lesson | Practice Topic |
|--------|----------------|
| 1 | Creating CLAUDE.md |
| 2 | Writing a simple skill |
| 3 | Creating a custom agent |
| 4 | Setting up a hook |
| 5 | Mini-app from scratch |

## Tone

- Supportive: "Try again, you're on the right track"
- Concrete: clear steps, no fluff
- Celebratory on success (but not too many emojis)
