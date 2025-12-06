---
name: testing
description: |
  Cross-language testing patterns: unit, integration, E2E testing strategies.
  Use when: writing tests, setting up test infrastructure, or improving coverage.
  Triggers: "test", "testing", "unit test", "integration test", "e2e",
  "coverage", "mock", "fixture".
---

# Testing Patterns

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Mocking | [mocking.md](references/mocking.md) — Python, TypeScript, Rust mocking patterns |

## Test Pyramid

```
        /  E2E  \        Few, slow, expensive
       /─────────\
      / Integration \    Some, medium speed
     /───────────────\
    /      Unit        \  Many, fast, cheap
   /─────────────────────\
```

## When to Use Each

| Type | Tests What | Speed | When |
|------|-----------|-------|------|
| **Unit** | Single function/class | Fast | Pure logic, calculations |
| **Integration** | Components together | Medium | DB queries, API calls |
| **E2E** | Full user flow | Slow | Critical paths only |

## Test Structure (AAA)

```python
def test_user_creation():
    # Arrange - Setup test data
    user_data = {"email": "test@example.com", "name": "Test"}

    # Act - Execute the code
    user = user_service.create(user_data)

    # Assert - Verify results
    assert user.email == "test@example.com"
    assert user.id is not None
```

## Naming Convention

```
test_<what>_<scenario>_<expected>

# Examples:
test_create_user_valid_data_returns_user()
test_create_user_duplicate_email_raises_error()
test_get_user_not_found_returns_none()
```

## Unit Test Patterns

### Testing Pure Functions

```python
# Function
def calculate_discount(price: float, percentage: float) -> float:
    return price * (1 - percentage / 100)

# Test
def test_calculate_discount():
    assert calculate_discount(100, 10) == 90
    assert calculate_discount(50, 50) == 25
    assert calculate_discount(100, 0) == 100
```

### Testing Edge Cases

```python
@pytest.mark.parametrize("input,expected", [
    ("", False),           # Empty
    ("a@b.c", True),       # Minimal valid
    ("test@example.com", True),
    ("invalid", False),    # No @
    ("@example.com", False), # No local part
    ("test@", False),      # No domain
])
def test_validate_email(input, expected):
    assert validate_email(input) == expected
```

### Testing Exceptions

```python
def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_invalid_input_raises_with_message():
    with pytest.raises(ValueError) as exc_info:
        process_data(None)
    assert "cannot be None" in str(exc_info.value)
```

## Integration Test Patterns

### Database Tests

```python
@pytest.fixture
async def db_session():
    # Setup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        yield session

    # Teardown
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def test_create_and_fetch_user(db_session):
    # Create
    user = User(email="test@example.com", name="Test")
    db_session.add(user)
    await db_session.commit()

    # Fetch
    result = await db_session.get(User, user.id)
    assert result.email == "test@example.com"
```

### API Tests

```python
async def test_api_create_user(client):
    response = await client.post(
        "/users",
        json={"email": "test@example.com", "name": "Test"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
```

## Mocking Patterns

### When to Mock

```
Mock:
├─ External APIs (payment, email, SMS)
├─ Time/dates (for deterministic tests)
├─ Random values
└─ Slow operations

Don't Mock:
├─ The code you're testing
├─ Simple data structures
└─ Things you can use real instances of
```

### Mock Examples

```python
# Python
from unittest.mock import Mock, patch, AsyncMock

@patch("services.email.send_email")
def test_signup_sends_email(mock_send):
    mock_send.return_value = True
    signup("test@example.com")
    mock_send.assert_called_once_with("test@example.com", subject=ANY)

# Async mock
@patch("services.payment.charge", new_callable=AsyncMock)
async def test_checkout(mock_charge):
    mock_charge.return_value = {"id": "ch_123"}
    result = await checkout(cart)
    assert result.payment_id == "ch_123"
```

```typescript
// TypeScript (Vitest)
import { vi } from 'vitest';

vi.mock('./email', () => ({
  sendEmail: vi.fn().mockResolvedValue(true)
}));

test('signup sends email', async () => {
  await signup('test@example.com');
  expect(sendEmail).toHaveBeenCalledWith('test@example.com', expect.any(String));
});
```

## Fixtures & Factories

### Fixture Pattern

```python
@pytest.fixture
def user():
    return User(id=1, email="test@example.com", name="Test")

@pytest.fixture
def admin_user(user):
    user.role = "admin"
    return user

def test_with_fixtures(user, admin_user):
    assert user.role != "admin"
    assert admin_user.role == "admin"
```

### Factory Pattern

```python
def create_user(**overrides):
    defaults = {
        "email": f"test-{uuid4()}@example.com",
        "name": "Test User",
        "role": "user"
    }
    return User(**{**defaults, **overrides})

def test_with_factory():
    user = create_user(role="admin")
    assert user.role == "admin"
```

## Coverage Goals

| Type | Target | Notes |
|------|--------|-------|
| Unit tests | 80%+ | Focus on logic |
| Integration | Key paths | DB operations, APIs |
| E2E | Critical flows | Signup, checkout |

### What NOT to Test

- Framework code (it's already tested)
- Trivial getters/setters
- Third-party libraries
- Generated code

## Anti-patterns

| Don't | Do Instead |
|-------|------------|
| Test implementation details | Test behavior |
| Duplicate prod logic in tests | Use different approach |
| Flaky tests | Fix or delete |
| Test everything | Test what matters |
| Mock everything | Use real when possible |
| Giant test functions | Small, focused tests |
