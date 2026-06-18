# TestingKit — Status

**Last updated:** 2026-06-17  
**Disposition:** [`docs/boundary/DISPOSITION.md`](docs/boundary/DISPOSITION.md)  
**Audit:** [`docs/audit/BLOCK-C-AUDIT.md`](docs/audit/BLOCK-C-AUDIT.md)

## Boundary verdict

**SPLIT / KEEP_ARCHIVED** — active Rust testing boundary; Python slice canonical in SDK.

| Layer | Status | Canonical owner |
|-------|--------|-----------------|
| Python (mcp-qa, CLIs, qa-kit) | Absorbed | `phenotype-python-sdk/packages/testing-kit` |
| Rust workspace (5 crates) | Active | **This repo** `rust/` |
| Wave B inbound (bdd, contract family) | Pending | **This repo** `rust/` (from HexaKit) |
| Journeys / E2E | Decompose | `phenotype-journeys` |
| Test scaffolds | Not owned | `phenokits-commons` |

## Consumer guidance

- **Python:** install from [`phenotype-python-sdk`](https://github.com/KooshaPari/phenotype-python-sdk) `packages/testing-kit` — not this archived repo.
- **Rust:** git dependency on `KooshaPari/TestingKit` `main` until crates.io publish (see README).

## Next actions

1. Merge Block-C disposition PR.
2. Complete Wave B Rust absorption (PR #1 + HexaKit stub removal).
3. Update README redirect (Phase 3 of consolidation plan).
