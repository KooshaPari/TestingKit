# TestingKit

**Comprehensive Testing Framework for Phenotype Microservices**

TestingKit provides unified testing abstractions, fixtures, and utilities for building reliable tests across Phenotype services. It simplifies test setup, reduces boilerplate, and enforces consistent testing patterns throughout the organization.

## Overview

TestingKit packages production-grade testing infrastructure into reusable libraries. It covers unit testing, integration testing, property-based testing, and end-to-end testing across multiple languages. The toolkit includes test doubles (mocks, stubs, fakes), fixtures, containers, and assertion helpers designed for microservice environments.

## Technology Stack

- **Languages**: Rust (primary), Python (secondary), Go (benchmarking)
- **Test Frameworks**:
  - **Rust**: pytest/cargo-test, Criterion (benchmarks), proptest (property-based)
  - **Python**: pytest, hypothesis (property-based), Factory Boy (fixtures)
  - **Go**: testing/t, testify, Table-driven tests
- **Infrastructure**: 
  - **Testcontainers** — Docker-based service isolation (PostgreSQL, Redis, Kafka, etc.)
  - **Criterion** — Statistical benchmarking
  - **proptest/hypothesis** — Property-based testing
  - **Fixtures** — Pre-built test data and service configurations

## Key Features

- **Test Fixtures**: Comprehensive fixture factories for all core data types
- **Service Mocks**: In-memory and HTTP-mock implementations of all major services
- **Testcontainers Integration**: Isolated database/queue environments with automatic cleanup
- **Benchmarking Harness**: Criterion integration with automatic regression detection
- **Property-Based Testing**: proptest (Rust) and hypothesis (Python) configuration and examples
- **Assertion Helpers**: Custom assertions for domain types and API responses
- **Test Utilities**: Builders for complex test scenarios, randomization, fake data generation
- **CI Integration**: Parallel test execution, failure isolation, and timeout handling
- **Documentation**: Test recipes for common patterns (authentication, async, distributed)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/KooshaPari/TestingKit.git
cd TestingKit

# Review testing patterns and philosophy
cat docs/TESTING_PHILOSOPHY.md

# Run all tests
cargo test --workspace
pytest tests/

# Run benchmarks
cargo bench --workspace

# Generate test coverage
cargo tarpaulin --workspace --out Html

# Build documentation
cargo doc --workspace --no-deps --open
```

## Project Structure

```
TestingKit/
├── crates/
│   ├── testing-core/              # Base testing abstractions
│   │   ├── fixtures/              # Test data builders
│   │   ├── mocks/                 # Mock implementations
│   │   └── assertions/            # Custom assertion macros
│   ├── testing-db/                # Database testing (testcontainers)
│   ├── testing-http/              # HTTP mocking and assertions
│   ├── testing-async/             # Async/concurrent test utilities
│   ├── testing-property/          # Property-based test config
│   └── testing-benchmark/         # Benchmarking and regression tests
├── tests/
│   ├── integration/               # Example integration tests
│   ├── recipes/                   # Test recipe examples
│   │   ├── auth_testing.rs        # Authentication test patterns
│   │   ├── api_testing.rs         # API endpoint test patterns
│   │   └── state_machine.rs       # Stateful testing patterns
│   └── fixtures/                  # Pre-built test scenarios
├── python/
│   ├── testing_kit/               # Python testing utilities
│   ├── tests/                     # Python integration tests
│   └── fixtures/                  # Python test data factories
└── docs/
    ├── TESTING_PHILOSOPHY.md      # Core testing principles
    ├── RECIPES.md                 # Common test patterns
    ├── FIXTURES.md                # Fixture factory usage
    ├── PROPERTY_BASED.md          # Property test strategies
    └── BENCHMARKING.md            # Performance testing
```

## Related Phenotype Projects

- **AgilePlus** — Uses TestingKit for comprehensive test suites (1000+ tests)
- **HexaKit** — All adapters include TestingKit fixtures and mocks
- **ValidationKit** — Uses property-based testing from TestingKit
- **PhenoPlugins** — Plugin testing framework built on TestingKit

## Quality & Testing

TestingKit itself maintains >95% test coverage:
- Unit tests for all fixture factories and mocks
- Integration tests for testcontainer configurations
- Benchmarks tracking framework overhead
- Recipes tested against real Phenotype services

```bash
cargo test --workspace --all-features
cargo tarpaulin --workspace --out Html --output-dir target/coverage
cargo bench --workspace
```

## Testing Best Practices

TestingKit enforces Phenotype testing standards:
1. **Test-First**: Write tests before implementation
2. **Clear Intent**: Test names describe behavior, not implementation
3. **Fixture Reuse**: Use factory builders instead of hardcoded test data
4. **Property-Based**: Use proptest for domain model invariants
5. **Isolated**: Mock external services, use testcontainers for integration
6. **Fast**: Unit tests <100ms; integration <1s per test
7. **Documented**: Include doc comments explaining non-obvious assertions

See `CLAUDE.md` for complete testing governance and requirements.

## Governance

All work tracked in AgilePlus. New testing utilities must:
- Pass all existing tests (regression prevention)
- Include documentation with examples
- Provide both sync and async variants where applicable
- Be compatible with Rust 1.75+

---

**Version**: v0.1.0  
**Last Updated**: 2026-04-25
