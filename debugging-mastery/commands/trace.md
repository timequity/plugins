---
description: Trace an error back to its root cause through the call stack
---

# /debug:trace

Trace backward through call chain to find original trigger. Use root-cause-tracing skill.

## Process

1. **Observe symptom** - What error appears?
2. **Find immediate cause** - What code triggers it?
3. **Trace upward** - What called this? With what values?
4. **Find source** - Where does bad data originate?
5. **Fix at source** - Not at symptom location

## Adding Instrumentation

When manual tracing isn't enough:

```typescript
console.error('DEBUG:', {
  value,
  typeof: typeof value,
  stack: new Error().stack,
});
```

## Key Rule

**Never fix where error appears. Fix where bad data originates.**
