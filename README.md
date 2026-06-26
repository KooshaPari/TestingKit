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
├── python/                                    # seven in-tree Python packages
│   ├── pheno-testing/
│   ├── pheno-quality/
│   ├── pheno-analysis-cli/
│   ├── mcp-qa/
│   └── qa-kit/
└── rust/
    ├── phenotype-testing/                     # async/sync test helpers
    ├── phenotype-mock/                        # call-recording mock context
    ├── phenotype-test-fixtures/               # cross-crate fixture data
    ├── phenotype-test-infra/                  # test-process orchestration
    └── phenotype-compliance-scanner/          # docs/governance compliance scans
```

## Rust crates — what's actually there

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
