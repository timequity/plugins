use axum::{http::StatusCode, routing::get, Json, Router};
use serde::{Deserialize, Serialize};

#[derive(Serialize)]
struct NotesResponse {
    data: Vec<()>,
    total: u32,
}

#[derive(Deserialize)]
struct CreateNoteRequest {
    title: String,
    content: String,
}

#[derive(Serialize)]
struct NoteResponse {
    id: u64,
    title: String,
    content: String,
    created_at: String,
}

async fn get_notes() -> Json<NotesResponse> {
    Json(NotesResponse {
        data: vec![],
        total: 0,
    })
}

async fn create_note(Json(payload): Json<CreateNoteRequest>) -> (StatusCode, Json<NoteResponse>) {
    let note = NoteResponse {
        id: 1,
        title: payload.title,
        content: payload.content,
        created_at: "2025-01-01T00:00:00Z".to_string(),
    };
    (StatusCode::CREATED, Json(note))
}

/// Create the application router.
pub fn create_app() -> Router {
    Router::new()
        .route("/health", get(|| async { "OK" }))
        .route("/notes", get(get_notes).post(create_note))
}
