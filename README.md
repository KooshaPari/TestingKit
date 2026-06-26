# TestingKit

> Polyglot test-utilities monorepo for the Phenotype ecosystem.
> Both Rust crates and Python packages are functional with real source code.

## Status

- **Rust workspace (`rust/`)** — present and buildable. Contains five crates
  with real source.
- **Python tree (`python/`)** — **seven in-tree packages** with real source code
  (see layout below). These are standalone Python packages with `pyproject.toml`
  manifests, not submodules.
- **License** — no `LICENSE` file is currently committed. This repo is **not**
  yet under a published OSS license; treat it as source-available within the
  Phenotype org until a license is added.

## Layout

```
TestingKit/
├── python/                                          # seven in-tree Python packages
│   ├── mcp-qa/                                      # MCP server testing framework (20K+ LOC)
│   ├── pheno-analysis-cli/                          # Unified code analysis CLI suite
│   ├── pheno-quality/                               # Core quality analysis library
│   ├── pheno-quality-cli/                           # Quality analysis CLI tool
│   ├── pheno-quality-tools/                         # Quality analysis tools & framework
│   ├── pheno-testing-cli/                           # Testing toolkit CLI (property, coverage, etc.)
│   └── qa-kit/                                      # QA testing & reporting framework
└── rust/
    ├── phenotype-testing/                     # async/sync test helpers
    ├── phenotype-mock/                        # call-recording mock context
    ├── phenotype-test-fixtures/               # cross-crate fixture data
    ├── phenotype-test-infra/                  # test-process orchestration
    └── phenotype-compliance-scanner/          # docs/governance compliance scans
```

## Python packages — what's actually there

The Python tree contains **~93K LOC across 7 packages** (verified 2026-06). Each package
is a standalone installable Python package with its own `pyproject.toml` manifest.

### `mcp-qa`

Comprehensive testing framework for Model Context Protocol (MCP) servers. Provides
mocking, collaboration testing, UI testing, OAuth flow testing, and reporting.

```python
from mcp_qa.mocking.server import create_mock_server

server = await create_mock_server()
await server.start()
# ... run tests against mock server ...
await server.stop()
```

Subpackages: `mocking`, `collaboration`, `core`, `reporters`, `ui`, `oauth`, `adapters`.

### `pheno-analysis-cli`

Unified code analysis suite. Provides CLI tools for quality analysis, dead-code
detection, test-coverage analysis, and response-time analysis.

### `pheno-quality`

Core quality analysis library. Provides compliance scanning, architectural
validation, integration gates, and plugin infrastructure.

### `pheno-quality-cli`

CLI tooling for `pheno-quality`. Exposes quality checks via a command-line
interface with rich output formatting.

### `pheno-quality-tools`

Extended quality analysis framework with registry-based plugin discovery,
integration gates, and architectural validators.

### `pheno-testing-cli`

Comprehensive testing toolkit extracted from the PhenoSDK. Generates test data,
property-based tests, duration tracking, and security testing utilities.

### `qa-kit`

Standalone QA testing and reporting framework designed for use outside the
Phenotype ecosystem. Deployable as an independent tool.

## Rust crates — what's actually there

Python packages are in-tree packages with real source code; Rust crates are
in the `rust/` workspace.

### `phenotype-testing`

Plain helper functions, not a macro framework:

```rust
use phenotype_testing::{timeout, timeout_default, block_on, test_id, random_port};
use std::time::Duration;

#[tokio::test]
async fn example() {
    let result = timeout(async { 42 }, Duration::from_millis(100)).await;
    assert_eq!(result.unwrap(), 42);
}
```

Public API (see `rust/phenotype-testing/src/lib.rs`):
`timeout`, `timeout_default`, `block_on`, `test_id`, `random_port`,
`wait_for`.

### `phenotype-mock`

Call-recording mock context, not a `mockall` re-export:

```rust
use phenotype_mock::{CallRecord, MockContext};

let ctx = MockContext::new();
ctx.record_call("get", vec!["id-1".to_string()]);
assert!(ctx.verify_called("get"));
```

Public API: `CallRecord`, `MockContext` (see `rust/phenotype-mock/src/lib.rs`).

### `phenotype-compliance-scanner`

Scans a project for documentation and governance compliance. Cargo features:

- `async-scan` (default) — parallel async scanning
- `health-integration` (default) — wires findings into `phenotype-health`

```bash
cd rust
cargo build -p phenotype-compliance-scanner
```

Library entry points live in `rust/phenotype-compliance-scanner/src/lib.rs`
(`Severity`, `ComplianceError`, etc.). There is **no** `main.rs` / CLI binary
in this crate today; integrate via the library API.

### `phenotype-test-fixtures`, `phenotype-test-infra`

Stubs for fixture data and process orchestration. Inspect their `src/` trees
before depending on them.

## Local development

```bash
cd rust
cargo build --workspace
cargo test --workspace
cargo clippy --workspace -- -D warnings
cargo fmt --check
```

See each Python package's `pyproject.toml` for build instructions. Most use
`setuptools` or `hatchling` as the build backend and can be installed with
`pip install -e python/<package>/`.

## Consuming the Rust crates

These crates are not yet published to crates.io. Use a git dependency:

```toml
[dev-dependencies]
phenotype-testing = { git = "https://github.com/KooshaPari/TestingKit", branch = "main" }
phenotype-mock    = { git = "https://github.com/KooshaPari/TestingKit", branch = "main" }
```

## Roadmap

- Add a `LICENSE` file (likely Apache-2.0 OR MIT, per Phenotype-org default).
- Publish stable Rust crates to crates.io.
- Publish stable Python packages to PyPI.

## Contributing

Issues and PRs welcome. Please match what is actually in the repo when adding
documentation — earlier drafts of this README described APIs (`assert_golden`,
`async_test`, `MockClient`, a `phenotype-compliance-scanner` CLI binary, a
`qa-kit` umbrella package, dual MIT/Apache license) that did not exist in
the source tree.
