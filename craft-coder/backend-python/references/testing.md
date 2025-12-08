# Python Testing Patterns

## Setup

```bash
uv add --dev pytest pytest-asyncio pytest-cov httpx
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

## Fixtures

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.db.engine import Base, get_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture
async def db_engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(db_engine):
    async_session = sessionmaker(db_engine, class_=AsyncSession)
    async with async_session() as session:
        yield session

@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
    app.dependency_overrides.clear()
```

## Test Patterns

### API Tests

```python
import pytest

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        "/users",
        json={"email": "test@example.com", "name": "Test User"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_user_not_found(client):
    response = await client.get("/users/999")
    assert response.status_code == 404
```

### Service Tests

```python
from src.services.user import UserService

@pytest.mark.asyncio
async def test_user_service_create(db_session):
    service = UserService(db_session)
    user = await service.create(email="test@example.com", name="Test")
    assert user.id is not None
    assert user.email == "test@example.com"
```

### Parametrized Tests

```python
@pytest.mark.parametrize("email,expected_status", [
    ("valid@example.com", 201),
    ("invalid-email", 422),
    ("", 422),
])
@pytest.mark.asyncio
async def test_create_user_validation(client, email, expected_status):
    response = await client.post("/users", json={"email": email, "name": "Test"})
    assert response.status_code == expected_status
```

### Mocking

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_send_email(client):
    with patch("src.services.email.send_email", new_callable=AsyncMock) as mock:
        mock.return_value = True
        response = await client.post("/auth/forgot-password", json={"email": "test@example.com"})
        assert response.status_code == 200
        mock.assert_called_once_with("test@example.com", subject=ANY, body=ANY)
```

### Factory Fixtures

```python
@pytest.fixture
def user_factory(db_session):
    async def create_user(email="test@example.com", name="Test"):
        user = User(email=email, name=name)
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user
    return create_user

@pytest.mark.asyncio
async def test_with_factory(client, user_factory):
    user = await user_factory(email="john@example.com")
    response = await client.get(f"/users/{user.id}")
    assert response.status_code == 200
```

## Running Tests

```bash
# Run all
pytest

# With coverage
pytest --cov=src --cov-report=term-missing

# Specific file/test
pytest tests/test_users.py
pytest tests/test_users.py::test_create_user

# Verbose
pytest -v

# Stop on first failure
pytest -x
```

## Coverage Config

```toml
# pyproject.toml
[tool.coverage.run]
source = ["src"]
omit = ["*/__init__.py", "*/conftest.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```
