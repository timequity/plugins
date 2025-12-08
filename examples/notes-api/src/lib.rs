use axum::{routing::get, Router};

pub fn create_app() -> Router {
    Router::new().route("/health", get(|| async { "OK" }))
}
