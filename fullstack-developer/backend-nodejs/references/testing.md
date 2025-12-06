# Node.js Testing with Vitest

## Setup

```bash
pnpm add -D vitest @vitest/coverage-v8
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      exclude: ['node_modules', 'dist', '**/*.test.ts'],
    },
  },
});
```

```json
// package.json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage"
  }
}
```

## Test Patterns

### Basic Tests

```typescript
import { describe, it, expect } from 'vitest';

describe('UserService', () => {
  it('should create a user', async () => {
    const user = await userService.create({
      email: 'test@example.com',
      name: 'Test User',
    });

    expect(user).toMatchObject({
      email: 'test@example.com',
      name: 'Test User',
    });
    expect(user.id).toBeDefined();
  });
});
```

### API Tests with Hono

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import app from '../src/index';

describe('Users API', () => {
  it('POST /users - creates user', async () => {
    const res = await app.request('/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'test@example.com', name: 'Test' }),
    });

    expect(res.status).toBe(201);
    const data = await res.json();
    expect(data.email).toBe('test@example.com');
  });

  it('GET /users/:id - returns 404 for unknown user', async () => {
    const res = await app.request('/users/999');
    expect(res.status).toBe(404);
  });
});
```

### Test Database Setup

```typescript
// tests/setup.ts
import { beforeAll, afterAll, beforeEach } from 'vitest';
import { migrate } from 'drizzle-orm/postgres-js/migrator';
import { db, client } from '../src/db';

beforeAll(async () => {
  await migrate(db, { migrationsFolder: './drizzle/migrations' });
});

beforeEach(async () => {
  // Clean tables before each test
  await db.delete(posts);
  await db.delete(users);
});

afterAll(async () => {
  await client.end();
});
```

### Mocking

```typescript
import { describe, it, expect, vi } from 'vitest';

// Mock module
vi.mock('../src/services/email', () => ({
  sendEmail: vi.fn().mockResolvedValue(true),
}));

import { sendEmail } from '../src/services/email';

describe('Auth', () => {
  it('sends password reset email', async () => {
    await authService.forgotPassword('test@example.com');

    expect(sendEmail).toHaveBeenCalledWith(
      'test@example.com',
      expect.stringContaining('Reset'),
      expect.any(String)
    );
  });
});
```

### Spy on Functions

```typescript
import { vi, expect } from 'vitest';

const spy = vi.spyOn(userService, 'create');

await createUserHandler(mockContext);

expect(spy).toHaveBeenCalledOnce();
expect(spy).toHaveBeenCalledWith({ email: 'test@example.com', name: 'Test' });
```

### Fixtures / Factories

```typescript
// tests/factories/user.ts
import { db } from '../../src/db';
import { users, type NewUser } from '../../src/db/schema';

export async function createUser(overrides: Partial<NewUser> = {}) {
  const [user] = await db.insert(users).values({
    email: `test-${Date.now()}@example.com`,
    name: 'Test User',
    ...overrides,
  }).returning();
  return user;
}

// In tests
it('gets user by id', async () => {
  const user = await createUser({ name: 'John' });
  const result = await userService.findById(user.id);
  expect(result?.name).toBe('John');
});
```

### Snapshot Testing

```typescript
it('returns correct user shape', async () => {
  const user = await userService.create({ email: 'test@example.com', name: 'Test' });

  expect(user).toMatchSnapshot({
    id: expect.any(Number),
    createdAt: expect.any(Date),
  });
});
```

## Running Tests

```bash
# Watch mode (default)
pnpm test

# Single run
pnpm test:run

# With coverage
pnpm test:coverage

# Specific file
pnpm test users.test.ts

# Filter by name
pnpm test -t "creates user"
```

## Matchers Reference

```typescript
expect(value).toBe(exact);           // ===
expect(value).toEqual(deep);         // Deep equality
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeDefined();
expect(value).toContain(item);       // Array/string contains
expect(value).toHaveLength(n);
expect(value).toMatchObject(subset); // Object contains
expect(fn).toThrow();
expect(fn).toThrowError(/message/);
expect(promise).resolves.toBe(x);
expect(promise).rejects.toThrow();
```
