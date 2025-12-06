---
name: backend-rust
description: |
  Modern Rust backend stack: Axum, SQLx, tokio, serde.
  Use when: building Rust web APIs, high-performance services, or CLI tools.
  Triggers: "axum", "rust backend", "rust api", "sqlx", "tokio",
  "actix", "rust web", "shuttle", "cargo".
---

# Rust Backend Stack

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Testing | [testing.md](references/testing.md) — axum-test, mockall, async tests |

## Tooling

| Tool | Purpose | Why |
|------|---------|-----|
| **Axum** | Web framework | Tower ecosystem, ergonomic |
| **SQLx** | Database | Compile-time checked queries |
| **tokio** | Async runtime | Industry standard |
| **serde** | Serialization | JSON, TOML, etc. |
| **tracing** | Logging | Structured, async-aware |
| **Shuttle** | Deploy | Free tier, simple |

## Project Setup

```bash
cargo new my-api
cd my-api
```

```toml
# Cargo.toml
[package]
name = "my-api"
version = "0.1.0"
edition = "2021"

[dependencies]
axum = "0.7"
tokio = { version = "1", features = ["full"] }
sqlx = { version = "0.8", features = ["runtime-tokio", "postgres", "uuid", "chrono"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
tower-http = { version = "0.5", features = ["cors", "trace"] }
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
dotenvy = "0.15"
thiserror = "1"
uuid = { version = "1", features = ["v4", "serde"] }
chrono = { version = "0.4", features = ["serde"] }

[dev-dependencies]
axum-test = "15"
```

## Project Structure

```
src/
├── main.rs              # Entry point
├── config.rs            # Environment config
├── db.rs                # Database pool
├── error.rs             # Error types
├── routes/
│   ├── mod.rs
│   ├── health.rs
│   └── users.rs
├── models/
│   ├── mod.rs
│   └── user.rs
├── handlers/
│   └── users.rs
└── middleware/
    └── auth.rs
migrations/
└── 001_create_users.sql
tests/
└── api_tests.rs
```

## Axum Patterns

### Basic App

```rust
use axum::{routing::get, Router};
use std::net::SocketAddr;
use tower_http::trace::TraceLayer;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let app = Router::new()
        .route("/health", get(|| async { "OK" }))
        .layer(TraceLayer::new_for_http());

    let addr = SocketAddr::from(([0, 0, 0, 0], 3000));
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

### App State

```rust
use axum::extract::FromRef;
use sqlx::PgPool;

#[derive(Clone, FromRef)]
pub struct AppState {
    pub db: PgPool,
    pub config: Config,
}

// In main.rs
let state = AppState { db: pool, config };
let app = Router::new()
    .route("/users", get(list_users).post(create_user))
    .with_state(state);
```

### Handler with Extractors

```rust
use axum::{
    extract::{Path, State, Json},
    http::StatusCode,
    response::IntoResponse,
};
use sqlx::PgPool;

pub async fn get_user(
    State(db): State<PgPool>,
    Path(id): Path<i32>,
) -> Result<Json<User>, AppError> {
    let user = sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
        .fetch_optional(&db)
        .await?
        .ok_or(AppError::NotFound)?;

    Ok(Json(user))
}

pub async fn create_user(
    State(db): State<PgPool>,
    Json(input): Json<CreateUser>,
) -> Result<impl IntoResponse, AppError> {
    let user = sqlx::query_as!(
        User,
        "INSERT INTO users (email, name) VALUES ($1, $2) RETURNING *",
        input.email,
        input.name
    )
    .fetch_one(&db)
    .await?;

    Ok((StatusCode::CREATED, Json(user)))
}
```

### Request/Response Types

```rust
use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};
use uuid::Uuid;

#[derive(Serialize, sqlx::FromRow)]
pub struct User {
    pub id: i32,
    pub public_id: Uuid,
    pub email: String,
    pub name: String,
    pub created_at: DateTime<Utc>,
}

#[derive(Deserialize)]
pub struct CreateUser {
    pub email: String,
    pub name: String,
}

#[derive(Serialize)]
pub struct UserList {
    pub data: Vec<User>,
    pub total: i64,
}
```

## Error Handling

```rust
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Not found")]
    NotFound,

    #[error("Validation error: {0}")]
    Validation(String),

    #[error("Database error")]
    Database(#[from] sqlx::Error),

    #[error("Internal error")]
    Internal(#[from] anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match &self {
            AppError::NotFound => (StatusCode::NOT_FOUND, "Not found"),
            AppError::Validation(msg) => (StatusCode::BAD_REQUEST, msg.as_str()),
            AppError::Database(_) => (StatusCode::INTERNAL_SERVER_ERROR, "Database error"),
            AppError::Internal(_) => (StatusCode::INTERNAL_SERVER_ERROR, "Internal error"),
        };

        let body = Json(json!({ "error": { "message": message } }));
        (status, body).into_response()
    }
}
```

## SQLx Patterns

### Database Pool

```rust
use sqlx::postgres::PgPoolOptions;

pub async fn create_pool(database_url: &str) -> sqlx::PgPool {
    PgPoolOptions::new()
        .max_connections(5)
        .connect(database_url)
        .await
        .expect("Failed to create pool")
}
```

### Migrations

```sql
-- migrations/001_create_users.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    public_id UUID DEFAULT gen_random_uuid() NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_users_email ON users(email);
```

```bash
# Run migrations
sqlx migrate run

# Create new migration
sqlx migrate add create_posts
```

### Compile-time Checked Queries

```rust
// Requires DATABASE_URL in .env for compile-time checking
let users = sqlx::query_as!(
    User,
    r#"
    SELECT id, public_id, email, name, created_at
    FROM users
    WHERE email LIKE $1
    ORDER BY created_at DESC
    LIMIT $2 OFFSET $3
    "#,
    format!("%{}%", search),
    limit,
    offset
)
.fetch_all(&pool)
.await?;
```

### Transactions

```rust
let mut tx = pool.begin().await?;

sqlx::query!("INSERT INTO users (email, name) VALUES ($1, $2)", email, name)
    .execute(&mut *tx)
    .await?;

sqlx::query!("INSERT INTO profiles (user_id, bio) VALUES ($1, $2)", user_id, bio)
    .execute(&mut *tx)
    .await?;

tx.commit().await?;
```

## Config

```rust
use serde::Deserialize;

#[derive(Clone, Deserialize)]
pub struct Config {
    pub database_url: String,
    pub port: u16,
    pub jwt_secret: String,
}

impl Config {
    pub fn from_env() -> Self {
        dotenvy::dotenv().ok();
        envy::from_env().expect("Failed to load config")
    }
}
```

## Middleware

```rust
use axum::{
    extract::Request,
    http::{header, StatusCode},
    middleware::Next,
    response::Response,
};

pub async fn auth_middleware(
    request: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    let auth_header = request
        .headers()
        .get(header::AUTHORIZATION)
        .and_then(|h| h.to_str().ok())
        .ok_or(StatusCode::UNAUTHORIZED)?;

    if !auth_header.starts_with("Bearer ") {
        return Err(StatusCode::UNAUTHORIZED);
    }

    // Validate token...
    Ok(next.run(request).await)
}

// Apply to routes
let protected = Router::new()
    .route("/me", get(get_current_user))
    .layer(axum::middleware::from_fn(auth_middleware));
```

## Anti-patterns

| Don't | Do Instead |
|-------|------------|
| `unwrap()` in handlers | Use `?` with proper error types |
| `clone()` everywhere | Use `Arc<T>` for shared state |
| Raw SQL strings | Use `sqlx::query!` macro |
| `println!` | Use `tracing::info!` |
| Blocking code in async | Use `spawn_blocking` |
| Manual JSON | Use `serde` derive |
