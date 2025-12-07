---
name: testing-anti-patterns
description: Avoid testing mock behavior, production pollution, and incomplete mocks. Tests verify real behavior.
---

# Testing Anti-Patterns

## Iron Laws

1. NEVER test mock behavior
2. NEVER add test-only methods to production
3. NEVER mock without understanding dependencies

## Anti-Pattern 1: Testing Mocks

```typescript
// ❌ Testing mock exists
expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();

// ✅ Test real behavior
expect(screen.getByRole('navigation')).toBeInTheDocument();
```

## Anti-Pattern 2: Test-Only Methods

```typescript
// ❌ In production class
class Session {
  destroy() { /* only used in tests */ }
}

// ✅ In test utilities
export function cleanupSession(session) { ... }
```

## Anti-Pattern 3: Mocking Without Understanding

```typescript
// ❌ Mock breaks test logic
vi.mock('ConfigWriter'); // Prevents write test needs!

// ✅ Mock only the slow part
vi.mock('SlowNetworkCall');
```

## Anti-Pattern 4: Incomplete Mocks

```typescript
// ❌ Partial
const mock = { status: 'success' };

// ✅ Complete
const mock = {
  status: 'success',
  data: { ... },
  metadata: { ... }
};
```

## Red Flags

- Assert on `*-mock` test IDs
- Methods only called in tests
- Mock setup > 50% of test
- Mocking "just to be safe"
