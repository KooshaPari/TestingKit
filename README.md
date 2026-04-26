# TestingKit

> Test utilities SDK for the Phenotype ecosystem — Python and Rust crates that
> provide fixtures, mocks, compliance scanners, and analysis CLIs shared across
> every Phenotype-org repository.

TestingKit is a polyglot monorepo. Each language tree is a self-contained
workspace; pick the one that matches your project's stack.

## Layout

```
TestingKit/
├── python/
│   ├── pheno-testing/             # core fixtures + assertion helpers
│   ├── pheno-quality/             # lint/format/coverage glue
│   ├── pheno-analysis-cli/        # static-analysis CLI
│   ├── mcp-qa/                    # MCP-server compliance probes
│   └── qa-kit/                    # umbrella package, re-exports the above
└── rust/
    ├── phenotype-testing/         # async-test harness + golden-file helpers
    ├── phenotype-mock/            # mockall-based mock builders
    ├── phenotype-test-fixtures/   # cross-crate fixture data
    ├── phenotype-test-infra/      # docker/process orchestration for tests
    └── phenotype-compliance-scanner/  # repo-level compliance audits
```

## Install

### Python

```bash
pip install pheno-testing pheno-quality        # individual crates
# or:
pip install qa-kit                              # umbrella
```

### Rust

Add to `Cargo.toml`:

```toml
[dev-dependencies]
phenotype-testing       = { git = "https://github.com/KooshaPari/TestingKit", branch = "main" }
phenotype-mock          = { git = "https://github.com/KooshaPari/TestingKit", branch = "main" }
phenotype-test-fixtures = { git = "https://github.com/KooshaPari/TestingKit", branch = "main" }
```

## Quick start

### Python — golden-file assertion

```python
from pheno_testing import assert_golden

def test_render():
    output = render_report(sample_data())
    assert_golden("tests/golden/report.txt", output)
```

### Rust — async harness with mock

```rust
use phenotype_testing::async_test;
use phenotype_mock::MockClient;

#[async_test]
async fn fetches_and_parses() {
    let mut client = MockClient::new();
    client.expect_fetch().returning(|_| Ok("hello".into()));
    let result = service::run(&client).await.unwrap();
    assert_eq!(result, "HELLO");
}
```

## Running the suite locally

```bash
# Python
cd python && uv run pytest

# Rust
cd rust && cargo test --workspace
```

## Compliance scanner

`phenotype-compliance-scanner` audits a target repo against Phenotype-org
conventions (LICENSE files, `cargo deny`, README, CI). Run it against the repo
you want to check:

```bash
cargo run -p phenotype-compliance-scanner -- --path /path/to/repo
```

## Contributing

Issues and PRs welcome. New crates should follow the existing naming
(`pheno-*` for Python, `phenotype-*` for Rust) and ship with tests and a
package-level README.

## License

Dual-licensed under [Apache License 2.0](LICENSE-APACHE) or
[MIT License](LICENSE-MIT) at your option.
