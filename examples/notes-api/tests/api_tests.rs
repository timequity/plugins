use axum::http::StatusCode;
use axum_test::TestServer;
use notes_api::create_app;

#[tokio::test]
async fn test_health_returns_ok() {
    let server = TestServer::new(create_app()).unwrap();

    let response = server.get("/health").await;

    response.assert_status(StatusCode::OK);
    response.assert_text("OK");
}

#[tokio::test]
async fn test_get_notes_returns_empty_list() {
    let server = TestServer::new(create_app()).unwrap();

    let response = server.get("/notes").await;

    response.assert_status(StatusCode::OK);
    response.assert_json(&serde_json::json!({"data": [], "total": 0}));
}

#[tokio::test]
async fn test_create_note_returns_201_with_created_note() {
    let server = TestServer::new(create_app()).unwrap();

    let response = server
        .post("/notes")
        .json(&serde_json::json!({
            "title": "Test Note",
            "content": "This is test content"
        }))
        .await;

    response.assert_status(StatusCode::CREATED);

    let body: serde_json::Value = response.json();
    assert!(body.get("id").is_some(), "Response should contain 'id'");
    assert_eq!(body["title"], "Test Note");
    assert_eq!(body["content"], "This is test content");
    assert!(body.get("created_at").is_some(), "Response should contain 'created_at'");
}
