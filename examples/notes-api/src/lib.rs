use axum::{routing::get, Json, Router};
use serde::Serialize;

#[derive(Serialize)]
pub struct NotesResponse {
    pub data: Vec<()>,
    pub total: u32,
}

pub async fn get_notes() -> Json<NotesResponse> {
    Json(NotesResponse {
        data: vec![],
        total: 0,
    })
}

pub fn create_app() -> Router {
    Router::new()
        .route("/health", get(|| async { "OK" }))
        .route("/notes", get(get_notes))
}
