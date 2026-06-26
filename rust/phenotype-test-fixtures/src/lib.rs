//! Test fixtures and builders for phenotype testing.
//!
//! Provides factory functions and builders for creating test data,
//! mock objects, and common test scenarios.

#![doc = r#"
# Phenotype Test Fixtures

Reusable test fixtures for Phenotype workspace crates.

## Usage

```rust
use phenotype_test_fixtures::TestData;

let data = TestData::new("test", 42i32);
```
"#]

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use uuid::Uuid;

/// Common test data containers.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TestData<T> {
    pub id: Uuid,
    pub name: String,
    pub value: T,
    pub created_at: DateTime<Utc>,
    pub metadata: HashMap<String, String>,
}

impl<T: Default> TestData<T> {
    pub fn new(name: impl Into<String>, value: T) -> Self {
        Self {
            id: Uuid::new_v4(),
            name: name.into(),
            value,
            created_at: Utc::now(),
            metadata: HashMap::new(),
        }
    }

    pub fn with_metadata(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.metadata.insert(key.into(), value.into());
        self
    }
}

/// Test scenario definition.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TestScenario {
    pub name: String,
    pub description: String,
    pub setup: Vec<TestStep>,
    pub execution: Vec<TestStep>,
    pub teardown: Vec<TestStep>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TestStep {
    pub name: String,
    pub action: String,
    pub expected_result: String,
}

/// Test environment configuration.
#[derive(Debug)]
pub struct TestEnv {
    pub temp_dir: tempfile::TempDir,
    pub env_vars: HashMap<String, String>,
}

impl TestEnv {
    pub fn new() -> std::io::Result<Self> {
        Ok(Self {
            temp_dir: tempfile::tempdir()?,
            env_vars: HashMap::new(),
        })
    }

    pub fn path(&self) -> &std::path::Path {
        self.temp_dir.path()
    }

    pub fn set_env(&mut self, key: impl Into<String>, value: impl Into<String>) {
        self.env_vars.insert(key.into(), value.into());
    }
}

/// Assertion helpers for tests.
pub mod assertions {
    use std::fmt::Debug;

    /// Assert that a result is Ok and return the value.
    pub fn assert_ok<T, E: Debug>(result: Result<T, E>) -> T {
        match result {
            Ok(v) => v,
            Err(e) => panic!("Expected Ok, got Err: {:?}", e),
        }
    }

    /// Assert that a result is Err.
    pub fn assert_err<T: Debug, E>(result: Result<T, E>) -> E {
        match result {
            Ok(v) => panic!("Expected Err, got Ok: {:?}", v),
            Err(e) => e,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_data_creation() {
        let data = TestData::new("test", 42i32);
        assert_eq!(data.name, "test");
        assert_eq!(data.value, 42);
        assert!(data.metadata.is_empty());
    }

    #[test]
    fn test_env_creation() {
        let env = TestEnv::new().unwrap();
        assert!(env.path().exists());
    }

    #[test]
    fn test_data_with_metadata() {
        let data = TestData::new("widget", 7i64)
            .with_metadata("k1", "v1")
            .with_metadata("k2", "v2");
        assert_eq!(data.metadata.get("k1"), Some(&"v1".to_string()));
        assert_eq!(data.metadata.get("k2"), Some(&"v2".to_string()));
        assert_eq!(data.metadata.len(), 2);
    }

    #[test]
    fn test_data_unique_ids() {
        let a = TestData::<i32>::new("a", 1);
        let b = TestData::<i32>::new("b", 2);
        assert_ne!(a.id, b.id);
    }

    #[test]
    fn test_env_set_env_var() {
        let mut env = TestEnv::new().unwrap();
        env.set_env("MY_KEY", "MY_VAL");
        env.set_env("MY_KEY", "OVERRIDE");
        assert_eq!(env.env_vars.get("MY_KEY"), Some(&"OVERRIDE".to_string()));
        assert_eq!(env.env_vars.len(), 1);
    }

    #[test]
    fn test_test_step_construction() {
        let step = TestStep {
            name: "step1".to_string(),
            action: "act".to_string(),
            expected_result: "ok".to_string(),
        };
        assert_eq!(step.name, "step1");
        assert_eq!(step.action, "act");
        assert_eq!(step.expected_result, "ok");
    }

    #[test]
    fn test_test_scenario_construction() {
        let scenario = TestScenario {
            name: "scenario_a".to_string(),
            description: "desc".to_string(),
            setup: vec![TestStep {
                name: "s".to_string(),
                action: "a".to_string(),
                expected_result: "r".to_string(),
            }],
            execution: vec![],
            teardown: vec![],
        };
        assert_eq!(scenario.name, "scenario_a");
        assert_eq!(scenario.setup.len(), 1);
        assert_eq!(scenario.execution.len(), 0);
        assert_eq!(scenario.teardown.len(), 0);
    }

    #[test]
    fn test_assertions_assert_ok() {
        let r: Result<i32, &str> = Ok(42);
        let v = assertions::assert_ok(r);
        assert_eq!(v, 42);
    }

    #[test]
    #[should_panic(expected = "Expected Ok")]
    fn test_assertions_assert_ok_panics_on_err() {
        let r: Result<i32, &str> = Err("nope");
        let _ = assertions::assert_ok(r);
    }

    #[test]
    fn test_assertions_assert_err() {
        let r: Result<i32, &str> = Err("nope");
        let e = assertions::assert_err(r);
        assert_eq!(e, "nope");
    }

    #[test]
    #[should_panic(expected = "Expected Err")]
    fn test_assertions_assert_err_panics_on_ok() {
        let r: Result<i32, &str> = Ok(42);
        let _ = assertions::assert_err(r);
    }
}
