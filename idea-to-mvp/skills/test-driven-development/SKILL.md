---
name: test-driven-development
description: |
  Auto-TDD during code generation. User doesn't see the process.
  Use when: generating any production code in MVP pipeline.
  Triggers: internal use only, called by build/add commands.
---

# Test-Driven Development (Hidden)

Every code generation follows TDD. User sees only results.

## Pipeline Integration

When generating code:

1. **Write test first** — based on feature description
2. **Verify fails** — run test, confirm failure
3. **Write minimal code** — just enough to pass
4. **Verify passes** — all tests green
5. **Report to user** — ✅ or ❌

## User Experience

```
User: "Add login page"
    ↓
[Write login test → Fail → Implement → Pass]
    ↓
User sees: "✅ Login page added"
```

User never sees:
- Test code (unless they ask)
- Red/green cycle
- Intermediate failures

## Test Patterns by Feature

| Feature | Test Pattern |
|---------|--------------|
| Auth | Can register, login, logout |
| CRUD | Create, read, update, delete work |
| UI | Component renders, handles clicks |
| API | Endpoint returns expected data |
| Validation | Rejects invalid input |

## Failure Handling

If tests fail after implementation:

1. Fix automatically if possible
2. If not fixable, inform user:
   - "Having trouble with [feature]. Can you clarify [specific question]?"
3. Never show raw error stack

## Verification

Before showing ✅ to user:

- [ ] All new tests pass
- [ ] Existing tests still pass
- [ ] No console errors/warnings
- [ ] Build succeeds
