//! Integration tests for `phenotype-testing`.
//!
//! These exercise the public async helpers (`timeout`, `wait_for`,
//! `retry_async`, `block_on`) in realistic combinations that are awkward
//! to express as inline `#[cfg(test)]` unit tests.
//!
//! They live in a separate `tests/` directory so they are compiled as a
//! distinct crate against the public API surface only.

use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::time::{Duration, Instant};

use phenotype_testing::{
    block_on, generators, retry_async, test_id, timeout, timeout_default, wait_for,
};

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn timeout_completes_with_real_async_work() {
    let started = Instant::now();
    let result = timeout(
        async {
            tokio::time::sleep(Duration::from_millis(25)).await;
            "ready"
        },
        Duration::from_secs(2),
    )
    .await;

    assert_eq!(result.unwrap(), "ready");
    assert!(
        started.elapsed() >= Duration::from_millis(20),
        "timeout should have actually awaited the inner future"
    );
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn timeout_default_aborts_long_running_task() {
    // Default is 5s. Use a sleep that is longer than 5s and verify it aborts early.
    let started = Instant::now();
    let result = timeout_default(async {
        tokio::time::sleep(Duration::from_secs(30)).await;
        "never reached"
    })
    .await;

    assert!(result.is_err(), "default timeout should have elapsed");
    // Should have returned essentially immediately; allow generous slack for CI.
    assert!(
        started.elapsed() < Duration::from_secs(1),
        "default-timeout future should bail quickly, took {:?}",
        started.elapsed()
    );
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn wait_for_polls_until_condition_true() {
    let counter = Arc::new(AtomicUsize::new(0));
    let target = 5usize;

    // Background task that increments the counter 10 times with small sleeps.
    let c2 = counter.clone();
    tokio::spawn(async move {
        for _ in 0..10 {
            tokio::time::sleep(Duration::from_millis(15)).await;
            c2.fetch_add(1, Ordering::SeqCst);
        }
    });

    let reached = wait_for(
        move || {
            let c = counter.clone();
            async move { c.load(Ordering::SeqCst) >= target }
        },
        Duration::from_secs(2),
    )
    .await;

    assert!(
        reached,
        "wait_for should have observed the counter reach {}",
        target
    );
    assert!(counter.load(Ordering::SeqCst) >= target);
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn wait_for_returns_false_on_timeout() {
    let reached = wait_for(
        || async { false }, // never true
        Duration::from_millis(50),
    )
    .await;

    assert!(!reached);
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn retry_async_recovers_after_transient_failures() {
    let attempts = Arc::new(AtomicUsize::new(0));
    let a2 = attempts.clone();

    let result: Result<&'static str, &'static str> = retry_async(
        move || {
            let a = a2.clone();
            async move {
                let n = a.fetch_add(1, Ordering::SeqCst) + 1;
                if n < 4 {
                    Err("not yet")
                } else {
                    Ok("ok")
                }
            }
        },
        10,
        Duration::from_millis(1),
    )
    .await;

    assert_eq!(result.unwrap(), "ok");
    assert_eq!(attempts.load(Ordering::SeqCst), 4);
}

#[test]
fn block_on_runs_future_to_completion_on_current_thread() {
    // Verify block_on correctly drives a tokio future from sync context.
    let value = block_on(async { 21 + 21 });
    assert_eq!(value, 42);
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn test_id_and_generators_produce_unique_values() {
    let mut ids = std::collections::HashSet::new();
    for _ in 0..50 {
        ids.insert(test_id());
    }
    // test_id uses a u64 random — collision probability is negligible for 50 entries.
    assert_eq!(ids.len(), 50, "test_id() should produce unique values");

    let email = generators::random_email();
    assert!(email.contains('@'), "random_email must contain '@'");
    assert_eq!(email.split('@').nth(1), Some("example.com"));

    let uuid = generators::random_uuid();
    let parts: Vec<&str> = uuid.split('-').collect();
    assert_eq!(parts.len(), 5, "random_uuid must produce 5 segments");
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn timeout_chained_inside_retry_async() {
    // Realistic pattern: each retry attempt is itself bounded by a timeout.
    let attempts = Arc::new(AtomicUsize::new(0));
    let a2 = attempts.clone();

    let result: Result<i32, String> = retry_async(
        move || {
            let a = a2.clone();
            async move {
                let n = a.fetch_add(1, Ordering::SeqCst);
                // First 2 attempts "hang"; timeout will fire and we treat as error.
                if n < 2 {
                    timeout(
                        async {
                            tokio::time::sleep(Duration::from_secs(30)).await;
                            1
                        },
                        Duration::from_millis(20),
                    )
                    .await
                    .map_err(|_| "attempt timed out".to_string())
                } else {
                    Ok(99)
                }
            }
        },
        5,
        Duration::from_millis(1),
    )
    .await;

    assert_eq!(result.unwrap(), 99);
    assert_eq!(attempts.load(Ordering::SeqCst), 3);
}