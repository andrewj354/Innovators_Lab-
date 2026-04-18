use ax_proxy::proxy; // гіпотетичний або кастомний проксі-хендлер
use axum::{
    routing::{get, post},
    http::{StatusCode, Request},
    response::{IntoResponse, Response},
    Router, extract::State,
};
use std::net::SocketAddr;

#[derive(Clone)]
struct AppState {
    client: reqwest::Client,
    // Тут можна зберігати адреси мікросервісів
    teams_service_url: String,
    tasks_service_url: String,
}

#[tokio::main]
async fn main() {
    let state = AppState {
        client: reqwest::Client::new(),
        teams_service_url: "http://127.0.0.1:8001".to_string(),
        tasks_service_url: "http://127.0.0.1:8002".to_string(),
    };

    let app = Router::new()

        .route("/api/teams/*path", get(proxy_handler).post(proxy_handler))
        .route("/api/tasks/*path", get(proxy_handler).post(proxy_handler))
        .with_state(state);

    let addr = SocketAddr::from(([0, 0, 0, 0], 8000));
    println!("API Gateway запущено на {}", addr);
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn proxy_handler(
    State(state): State<AppState>,
    req: Request<axum::body::Body>,
) -> Response {
    let path = req.uri().path();
    
    let target_url = if path.starts_with("/api/teams") {
        format!("{}{}", state.teams_service_url, path)
    } else if path.starts_with("/api/tasks") {
        format!("{}{}", state.tasks_service_url, path)
    } else {
        return StatusCode::NOT_FOUND.into_response();
    };

    StatusCode::OK.into_response() // Заглушка
}