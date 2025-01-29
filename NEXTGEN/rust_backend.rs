use warp::Filter;
use tokio::sync::Mutex;
use std::sync::Arc;

#[tokio::main]
async fn main() {
    let counter = Arc::new(Mutex::new(0));

    let hello = warp::path!("hello" / String)
        .map(|name| format!("Hello, {}!", name));

    let increment = warp::path("increment")
        .map(move || {
            let mut counter = counter.lock().unwrap();
            *counter += 1;
            format!("Counter: {}", *counter)
        });

    let routes = hello.or(increment);

    warp::serve(routes)
        .run(([127, 0, 0, 1], 3030))
        .await;
}
