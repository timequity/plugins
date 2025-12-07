---
description: Fix a flaky test by replacing timing guesses with condition-based waiting
---

# /debug:flaky

Fix flaky tests using condition-based-waiting skill.

## Process

1. **Identify timing dependency**
   - Find `setTimeout`, `sleep`, arbitrary delays
   - Check what condition the delay is waiting for

2. **Replace with condition polling**
   ```typescript
   // ❌ Before
   await sleep(100);
   expect(result).toBeDefined();

   // ✅ After
   await waitFor(() => getResult() !== undefined);
   ```

3. **Test stability**
   - Run test 10+ times
   - Run in parallel with other tests
   - Run under load

## Common Patterns

| Waiting For | Solution |
|-------------|----------|
| Event | `waitFor(() => events.find(...))` |
| State change | `waitFor(() => state === 'ready')` |
| DOM element | `await screen.findByRole(...)` |
| File creation | `waitFor(() => existsSync(path))` |

## When Timeout IS Needed

Document with comment explaining why:

```typescript
// Wait for 2 ticks at 100ms interval
await waitForEvent('STARTED');
await sleep(200);
```
