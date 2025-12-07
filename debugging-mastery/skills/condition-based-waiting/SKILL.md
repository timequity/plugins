---
name: condition-based-waiting
description: Replace arbitrary timeouts with condition polling. Eliminate flaky tests.
---

# Condition-Based Waiting

## Core Principle

Wait for actual condition, not a guess about timing.

## Pattern

```typescript
// ❌ Guessing
await sleep(50);
expect(result).toBeDefined();

// ✅ Waiting for condition
await waitFor(() => getResult() !== undefined);
expect(result).toBeDefined();
```

## Quick Patterns

| Scenario | Pattern |
|----------|---------|
| Event | `waitFor(() => events.find(e => e.type === 'DONE'))` |
| State | `waitFor(() => machine.state === 'ready')` |
| Count | `waitFor(() => items.length >= 5)` |
| File | `waitFor(() => fs.existsSync(path))` |

## Implementation

```typescript
async function waitFor<T>(
  condition: () => T | undefined,
  description: string,
  timeoutMs = 5000
): Promise<T> {
  const start = Date.now();
  while (true) {
    const result = condition();
    if (result) return result;
    if (Date.now() - start > timeoutMs) {
      throw new Error(`Timeout: ${description}`);
    }
    await sleep(10);
  }
}
```

## When Timeout IS Correct

```typescript
// Timed behavior (100ms ticks)
await waitForEvent('STARTED');
await sleep(200); // 2 ticks - documented
```

Document WHY with comment.
