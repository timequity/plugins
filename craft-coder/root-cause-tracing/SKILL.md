---
name: root-cause-tracing
description: Use when errors occur deep in execution and you need to trace back to find the original trigger - systematically traces bugs backward through call stack to identify source of invalid data
---

# Root Cause Tracing

## Overview

Bugs often manifest deep in the call stack. Your instinct is to fix where the error appears, but that's treating a symptom.

**Core principle:** Trace backward through the call chain until you find the original trigger, then fix at the source.

## When to Use

- Error happens deep in execution (not at entry point)
- Stack trace shows long call chain
- Unclear where invalid data originated
- Need to find which code triggers the problem

## The Tracing Process

### 1. Observe the Symptom

```
Error: database query failed with null user_id
```

### 2. Find Immediate Cause

**What code directly causes this?**
```typescript
await db.query('SELECT * FROM orders WHERE user_id = ?', [userId]);
```

### 3. Ask: What Called This?

```typescript
OrderService.getOrders(userId)
  → called by OrderController.list()
  → called by router.get('/orders')
  → called by auth middleware
```

### 4. Keep Tracing Up

**What value was passed?**
- `userId = null`
- Where did null come from?
- Auth middleware didn't set user on request

### 5. Find Original Trigger

**Where did the problem originate?**
```typescript
// Auth middleware bug: didn't handle expired tokens
if (token.expired) {
  // Missing: return error response
  // Falls through with req.user = undefined
}
```

## Adding Stack Traces

When you can't trace manually, add instrumentation:

```typescript
async function getOrders(userId: string) {
  const stack = new Error().stack;
  console.error('DEBUG getOrders:', {
    userId,
    typeOfUserId: typeof userId,
    stack,
  });
  // ... rest of function
}
```

**Run and capture:**
```bash
npm test 2>&1 | grep 'DEBUG getOrders'
```

## Real Example

**Symptom:** `.git` created in source directory during tests

**Trace chain:**
1. `git init` runs in `process.cwd()` ← empty cwd parameter
2. WorktreeManager called with empty projectDir
3. Session.create() passed empty string
4. Test accessed `context.tempDir` before beforeEach
5. setupTest() returns `{ tempDir: '' }` initially

**Root cause:** Top-level variable initialization accessing empty value

**Fix:** Made tempDir a getter that throws if accessed too early

## Key Principle

```
Found immediate cause
    ↓
Can trace one level up? → YES → Trace backwards
    ↓                              ↓
    NO                        Is this the source?
    ↓                              ↓
NEVER fix just              YES → Fix at source
the symptom                        ↓
                             Add validation at each layer
                                   ↓
                             Bug impossible
```

**NEVER fix just where the error appears.** Trace back to find the original trigger.

## Stack Trace Tips

- **In tests:** Use `console.error()` not logger - logger may be suppressed
- **Before operation:** Log before the dangerous operation, not after it fails
- **Include context:** Directory, cwd, environment variables
- **Capture stack:** `new Error().stack` shows complete call chain

## Integration

**Used by:**
- **systematic-debugging** - Phase 1, Step 5 calls this skill

**Pairs with:**
- **defense-in-depth** - After finding root cause, add validation at each layer
