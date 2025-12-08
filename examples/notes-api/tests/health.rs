use axum::http::StatusCode;
use axum_test::TestServer;
use notes_api::create_app;

#[tokio::test]
async fn test_health_returns_ok_with_200() {
    let app = create_app();
    let server = TestServer::new(app).unwrap();

    let response = server.get("/health").await;

    response.assert_status(StatusCode::OK);
    response.assert_text("OK");
}
