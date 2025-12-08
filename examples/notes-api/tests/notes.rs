use axum::http::StatusCode;
use axum_test::TestServer;
use notes_api::create_app;

#[tokio::test]
async fn test_get_notes_returns_empty_list_with_200() {
    let app = create_app();
    let server = TestServer::new(app).unwrap();

    let response = server.get("/notes").await;

    response.assert_status(StatusCode::OK);
    response.assert_json(&serde_json::json!({
        "data": [],
        "total": 0
    }));
}
