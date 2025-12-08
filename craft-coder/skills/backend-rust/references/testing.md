# Rust Testing Patterns

## Setup

```toml
# Cargo.toml
[dev-dependencies]
axum-test = "15"
tokio = { version = "1", features = ["rt-multi-thread", "macros"] }
```

## API Tests with axum-test

```rust
// tests/api_tests.rs
use axum_test::TestServer;
use serde_json::json;

async fn create_test_app() -> TestServer {
    let pool = create_test_pool().await;
    let app = create_app(pool);
    TestServer::new(app).unwrap()
}

#[tokio::test]
async fn test_create_user() {
    let server = create_test_app().await;

    let response = server
        .post("/users")
        .json(&json!({
            "email": "test@example.com",
            "name": "Test User"
        }))
        .await;

    response.assert_status_created();
    let user: User = response.json();
    assert_eq!(user.email, "test@example.com");
}

#[tokio::test]
async fn test_get_user_not_found() {
    let server = create_test_app().await;

    let response = server.get("/users/999").await;

    response.assert_status_not_found();
}

#[tokio::test]
async fn test_list_users() {
    let server = create_test_app().await;

    // Create test data
    server
        .post("/users")
        .json(&json!({"email": "a@example.com", "name": "A"}))
        .await;
    server
        .post("/users")
        .json(&json!({"email": "b@example.com", "name": "B"}))
        .await;

    let response = server.get("/users").await;

    response.assert_status_ok();
    let users: Vec<User> = response.json();
    assert_eq!(users.len(), 2);
}
```

## Test Database Setup

```rust
// tests/common/mod.rs
use sqlx::{PgPool, postgres::PgPoolOptions};
use std::sync::Once;

static INIT: Once = Once::new();

pub async fn create_test_pool() -> PgPool {
    INIT.call_once(|| {
        dotenvy::dotenv().ok();
    });

    let database_url = std::env::var("TEST_DATABASE_URL")
        .unwrap_or_else(|_| "postgres://localhost/myapp_test".to_string());

    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await
        .expect("Failed to create test pool");

    // Run migrations
    sqlx::migrate!("./migrations")
        .run(&pool)
        .await
        .expect("Failed to run migrations");

    // Clean tables
    sqlx::query!("TRUNCATE users, posts CASCADE")
        .execute(&pool)
        .await
        .ok();

    pool
}
```

## Unit Tests

```rust
// src/services/user.rs
pub fn validate_email(email: &str) -> bool {
    email.contains('@') && email.len() >= 5
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_validate_email_valid() {
        assert!(validate_email("test@example.com"));
        assert!(validate_email("a@b.c"));
    }

    #[test]
    fn test_validate_email_invalid() {
        assert!(!validate_email("invalid"));
        assert!(!validate_email("@"));
        assert!(!validate_email("a@b"));
    }
}
```

## Async Tests

```rust
#[tokio::test]
async fn test_async_function() {
    let result = some_async_function().await;
    assert!(result.is_ok());
}

// With timeout
#[tokio::test]
#[timeout(5000)] // 5 seconds
async fn test_with_timeout() {
    slow_operation().await;
}
```

## Mocking with mockall

```toml
# Cargo.toml
[dev-dependencies]
mockall = "0.12"
```

```rust
use mockall::automock;

#[automock]
pub trait EmailService {
    async fn send(&self, to: &str, subject: &str, body: &str) -> Result<(), Error>;
}

#[tokio::test]
async fn test_password_reset() {
    let mut mock = MockEmailService::new();
    mock.expect_send()
        .with(
            mockall::predicate::eq("test@example.com"),
            mockall::predicate::always(),
            mockall::predicate::always(),
        )
        .times(1)
        .returning(|_, _, _| Ok(()));

    let service = AuthService::new(mock);
    let result = service.forgot_password("test@example.com").await;

    assert!(result.is_ok());
}
```

## Test Fixtures

```rust
pub struct TestFixtures {
    pub pool: PgPool,
}

impl TestFixtures {
    pub async fn new() -> Self {
        Self {
            pool: create_test_pool().await,
        }
    }

    pub async fn create_user(&self, email: &str, name: &str) -> User {
        sqlx::query_as!(
            User,
            "INSERT INTO users (email, name) VALUES ($1, $2) RETURNING *",
            email,
            name
        )
        .fetch_one(&self.pool)
        .await
        .unwrap()
    }
}

#[tokio::test]
async fn test_with_fixtures() {
    let fixtures = TestFixtures::new().await;
    let user = fixtures.create_user("test@example.com", "Test").await;

    // Use user in test...
}
```

## Running Tests

```bash
# All tests
cargo test

# Specific test
cargo test test_create_user

# With output
cargo test -- --nocapture

# Single-threaded (for DB tests)
cargo test -- --test-threads=1

# Integration tests only
cargo test --test api_tests
```

## Test Organization

```
tests/
├── common/
│   └── mod.rs           # Shared test utilities
├── api_tests.rs         # API integration tests
└── service_tests.rs     # Service unit tests

src/
├── lib.rs
└── services/
    └── user.rs          # Contains #[cfg(test)] mod tests
```
