---
name: root-cause-tracing
description: Trace bugs backward through call stack to find original trigger. Fix at source, not symptom.
---

# Root Cause Tracing

## Core Principle

**Never fix where error appears. Trace back to source.**

## The Process

### 1. Observe Symptom
```
Error: query failed with null user_id
```

### 2. Find Immediate Cause
```typescript
db.query('SELECT * FROM orders WHERE user_id = ?', [userId]);
```

### 3. Ask: What Called This?
```
OrderService.getOrders(userId)
  → OrderController.list()
  → router.get('/orders')
  → auth middleware
```

### 4. Keep Tracing Up
- `userId = null`
- Where did null come from?
- Auth middleware didn't set user

### 5. Find Original Trigger
```typescript
// Bug: didn't handle expired tokens
if (token.expired) {
  // Falls through with req.user = undefined
}
```

## Adding Instrumentation

```typescript
async function getOrders(userId: string) {
  console.error('DEBUG:', {
    userId,
    typeof: typeof userId,
    stack: new Error().stack,
  });
}
```

## Key Principle

```
Found cause → Can trace up? → YES → Keep tracing
                            → NO → NEVER fix just symptom
```

Fix at source. Add validation at each layer.
