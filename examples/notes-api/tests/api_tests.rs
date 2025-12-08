use axum::http::StatusCode;
use axum_test::TestServer;
use notes_api::create_app;
use serde_json::json;
use uuid;

#[tokio::test]
async fn test_health_endpoint_returns_ok() {
    // Arrange
    let app = create_app();
    let server = TestServer::new(app).unwrap();

    // Act
    let response = server.get("/health").await;

    // Assert
    assert_eq!(
        response.status_code(),
        StatusCode::OK,
        "Health endpoint should return 200 OK"
    );
    assert_eq!(
        response.text(),
        "OK",
        "Health endpoint should return 'OK' in the body"
    );
}

#[tokio::test]
async fn test_get_notes_returns_empty_list() {
    // Arrange
    let app = create_app();
    let server = TestServer::new(app).unwrap();

    // Act
    let response = server.get("/notes").await;

    // Assert
    assert_eq!(
        response.status_code(),
        StatusCode::OK,
        "GET /notes should return 200 OK"
    );

    let expected = json!({
        "data": [],
        "total": 0
    });

    assert_eq!(
        response.json::<serde_json::Value>(),
        expected,
        "GET /notes should return empty list with total count"
    );
}

#[tokio::test]
async fn test_create_note_returns_created() {
    // Arrange
    let app = create_app();
    let server = TestServer::new(app).unwrap();

    // Act
    let response = server
        .post("/notes")
        .json(&json!({
            "title": "Test",
            "content": "Content"
        }))
        .await;

    // Assert
    assert_eq!(
        response.status_code(),
        StatusCode::CREATED,
        "POST /notes should return 201 CREATED"
    );

    let body = response.json::<serde_json::Value>();

    // Verify response has all required fields
    assert!(body.get("id").is_some(), "Response should have 'id' field");
    assert!(body.get("title").is_some(), "Response should have 'title' field");
    assert!(body.get("content").is_some(), "Response should have 'content' field");
    assert!(body.get("created_at").is_some(), "Response should have 'created_at' field");

    // Verify field values
    assert_eq!(
        body.get("title").and_then(|v| v.as_str()),
        Some("Test"),
        "Response title should match request"
    );
    assert_eq!(
        body.get("content").and_then(|v| v.as_str()),
        Some("Content"),
        "Response content should match request"
    );

    // Verify id is a valid UUID
    let id_str = body.get("id").and_then(|v| v.as_str()).expect("id should be a string");
    assert!(
        uuid::Uuid::parse_str(id_str).is_ok(),
        "id should be a valid UUID"
    );
}
