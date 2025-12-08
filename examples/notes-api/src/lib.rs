use axum::{routing::get, Router, Json, http::StatusCode};
use serde::{Deserialize, Serialize};
use uuid::Uuid;
use chrono::{DateTime, Utc};

#[derive(Serialize)]
pub struct NotesResponse {
    pub data: Vec<()>,
    pub total: u32,
}

#[derive(Serialize)]
pub struct Note {
    pub id: Uuid,
    pub title: String,
    pub content: String,
    pub created_at: DateTime<Utc>,
}

#[derive(Deserialize)]
pub struct CreateNoteRequest {
    pub title: String,
    pub content: String,
}

pub async fn get_notes() -> Json<NotesResponse> {
    Json(NotesResponse {
        data: vec![],
        total: 0,
    })
}

pub async fn create_note(
    Json(payload): Json<CreateNoteRequest>,
) -> (StatusCode, Json<Note>) {
    let note = Note {
        id: Uuid::new_v4(),
        title: payload.title,
        content: payload.content,
        created_at: Utc::now(),
    };

    (StatusCode::CREATED, Json(note))
}

pub fn create_app() -> Router {
    Router::new()
        .route("/health", get(|| async { "OK" }))
        .route("/notes", get(get_notes).post(create_note))
}
