# TestingKit — Per-Module Boundary Disposition

**Status:** Approved assessment  
**Date:** 2026-06-17  
**Repo:** `KooshaPari/TestingKit`  
**Charter:** [`phenotype-registry/docs/rationalization/boundary-shaping.md`](https://github.com/KooshaPari/phenotype-registry/blob/main/docs/rationalization/boundary-shaping.md)  
**Audit:** [`docs/audit/BLOCK-C-AUDIT.md`](../audit/BLOCK-C-AUDIT.md)  
**Registry:** [`phenotype-registry/BOUNDARY_OWNERS.md`](https://github.com/KooshaPari/phenotype-registry/blob/main/BOUNDARY_OWNERS.md) — `test` domain  
**Wave B:** [`docs/disposition/wave-b-absorption.md`](../disposition/wave-b-absorption.md)

> **Doctrine:** Stubs and scaffolds receive an owner and a migration path — not silent deletion.
> Hard delete applies only after absorption evidence and consumer manifest scan (registry gate §5).

---

## 1. Summary — recommended end-state

**TestingKit is a split testing boundary**, not a monolith to delete or keep unchanged.

| Concern | Owner after disposition |
|---------|-------------------------|
| Rust fleet test helpers (`timeout`, `mock`, fixtures, infra) | **TestingKit** `rust/` (canonical; archived repo OK) |
| HexaKit testing crates (bdd, contract, fixtures, infra) | **TestingKit** `rust/` via Wave B absorption |
| Python MCP QA, pytest plugins, quality/analysis CLIs | **phenotype-python-sdk** `packages/testing-kit` |
| xDD / property / mutation frameworks (long-term) | **phenoXddLib** — evaluate after Wave B lands |
| E2E journey harness + keyframe CI | **phenotype-journeys** |
| Per-repo Playwright / docsite test scaffolds | **phenokits-commons** |
| Org reusable CI workflows | **phenotype-org-governance** / `KooshaPari/.github` |
| Compliance scanner (governance/docs scan) | **TestingKit** `rust/phenotype-compliance-scanner` |
| Health integration wire on compliance scanner | **PhenoObservability** (optional feature, defer) |
| This repository | **KEEP_ARCHIVED** — active Rust boundary; Python redirect to SDK |

**Do not** treat python-sdk file parity as permission to delete this repo. Rust workspace + Wave B inbound remain unique.

---

## 2. Method

- Git tree `main` @ 634517a (2026-06-17, post PR #2 Wave B restore)
- Cross-repo compare: `phenotype-python-sdk/packages/testing-kit`, HexaKit DISPOSITION rows #4, #10–#12, #40–#41
- Registry: `BOUNDARY_OWNERS.md` testing plane split, `projects/TestingKit.json`, batch3 audit
- Prior work: PR #2 `wave-b-absorption.md`, `BOUNDARY.md`

---

## 3. Top-level modules — disposition table

| # | Module (path) | What it is | Disposition | Target repo | Rationale |
|---|---------------|------------|-------------|-------------|-----------|
| 1 | `rust/phenotype-testing/` | Async/sync test helpers (`timeout`, `random_port`, …) | **DYNAMIC-KEEP** | TestingKit | Fleet Rust test utilities; buildable today |
| 2 | `rust/phenotype-mock/` | Call-recording mock context | **DYNAMIC-KEEP** | TestingKit | Active dev-dependency pattern |
| 3 | `rust/phenotype-test-fixtures/` | Cross-crate fixture data | **DYNAMIC-KEEP** | TestingKit | Wave B #41 **landed** |
| 4 | `rust/phenotype-test-infra/` | Test-process orchestration | **DYNAMIC-KEEP** | TestingKit | Wave B #40 **landed** |
| 5 | `rust/phenotype-compliance-scanner/` | Docs/governance compliance scan library | **DYNAMIC-KEEP** | TestingKit | Unique scanner; no CLI binary |
| 6 | `rust/phenotype-compliance-scanner` `health-integration` feature | Wires findings to `phenotype-health` | **DECOMPOSE** | PhenoObservability | Observability owns health runtime |
| 7 | `rust/phenotype-bdd/` (pending) | BDD harness from HexaKit | **ABSORB** | TestingKit | Wave B #4 — stub in HexaKit |
| 8 | `rust/phenotype-contract/` (pending) | Contract test trait | **ABSORB** | TestingKit | Wave B #10 — migrate as set |
| 9 | `rust/phenotype-contracts/` (pending) | Contract value types | **ABSORB** | TestingKit | Wave B #11 |
| 10 | `rust/phenotype-contract-tests/` (pending) | Contract test runner | **ABSORB** | TestingKit | Wave B #12 |
| 11 | `python/mcp-qa/` | MCP QA framework + pytest plugins | **ABSORB** | phenotype-python-sdk `packages/testing-kit/python/mcp-qa` | Reconciled 2026-06-17; SDK canonical |
| 12 | `python/pheno-quality-cli/` | Quality CLI entrypoints | **ABSORB** | phenotype-python-sdk `packages/testing-kit` | SDK copy is consumer default |
| 13 | `python/pheno-quality-tools/` | Quality tooling library | **ABSORB** | phenotype-python-sdk `packages/testing-kit` | Same |
| 14 | `python/pheno-testing-cli/` | Testing CLI | **ABSORB** | phenotype-python-sdk `packages/testing-kit` | Same |
| 15 | `python/pheno-analysis-cli/` | Analysis CLI | **ABSORB** | phenotype-python-sdk `packages/testing-kit` | Same |
| 16 | `python/qa-kit/` | QA kit umbrella + logging helpers | **ABSORB** | phenotype-python-sdk `packages/testing-kit` | Same |
| 17 | `docs/journeys/manifests/` | Journey manifest stubs | **DECOMPOSE** | phenotype-journeys | BOUNDARY_OWNERS: journeys not owned here |
| 18 | `docs/operations/journey-traceability.md` | Journey traceability spec | **ABSORB** | phenotype-journeys | Reference until cut |
| 19 | `docs/disposition/wave-b-absorption.md` | Wave B lane status | **DYNAMIC-KEEP** | TestingKit | Active absorption tracker |
| 20 | `docs/adr/ADR-001`–`005` | Aspirational architecture ADRs | **DYNAMIC-KEEP** → slim | phenotype-registry session artifacts | Historical; trim on archive freeze |
| 21 | `docs/research/` | SOTA testing research | **DYNAMIC-KEEP** | TestingKit until archive | Evidence for boundary decisions |
| 22 | `docs/operations/iconography/` | Unused SVG assets | **DELETE** | — | No fleet consumer; ponytail on cut PR |
| 23 | `docs/reference/fr_coverage_matrix.md` | FR trace matrix | **DYNAMIC-KEEP** | TestingKit / AgilePlus | Trim with root markdown zoo |
| 24 | `.github/workflows/journey-gate.yml` | Journey keyframe CI (stub) | **DECOMPOSE** | phenotype-journeys | Gate belongs at journey owner |
| 25 | `.github/workflows/` (ci, deny, codeql, …) | Repo CI | **DYNAMIC-KEEP** | Until archive freeze | Rust workspace still buildable |
| 26 | Root governance (`SPEC.md`, `PLAN.md`, `PRD.md`, …) | Planning markdown zoo | **DYNAMIC-KEEP** → slim | phenotype-registry | Trim on cut PR; keep README redirect |
| 27 | `BOUNDARY.md` | Boundary lock | **DYNAMIC-KEEP** | TestingKit | Links to this disposition |
| 28 | Repo itself | Split testing boundary host | **KEEP_ARCHIVED** | phenotype-registry `projects/TestingKit.json` | Rust canonical; Py redirect; HOLD DELETE |

---

## 4. Supersession map

| Retired surface | Successor | Evidence |
|-----------------|-----------|----------|
| Python packages for fleet consumers | `phenotype-python-sdk/packages/testing-kit` | batch3 audit; mcp-qa reconcile |
| HexaKit `crates/phenotype-test-*` duplicates | TestingKit `rust/` | Wave B DISPOSITION + PR #2 |
| TestingKit as Python install target | SDK `pip install phenotype-sdk[testing]` (target) | `BOUNDARY_OWNERS` split |
| Monolithic testing-kit in one repo | Split plane (SDK / XddLib / journeys / commons) | `ZERO_LOOP_ECOSYSTEM_PLAN` |

---

## 5. Execution phases

| Phase | Scope | Acceptance |
|-------|-------|------------|
| **P0** (this PR) | Block-C disposition + audit + consolidation plan | Docs on `main` |
| **P1** | Land Wave B bdd/contract family under `rust/` | HexaKit stubs removed |
| **P2** | README redirect + consumer repoint (Py → SDK, Rust git dep docs) | No stale install paths |
| **P3** | Journey/iconography ponytail cut | Defer to phenotype-journeys |
| **P4** | crates.io publish for Rust workspace | Fleet manifest repoint |
| **P5** | Re-evaluate archive delete gate | All 5 registry conditions PASS |

---

## 6. Related documents

- [`docs/audit/BLOCK-C-AUDIT.md`](../audit/BLOCK-C-AUDIT.md)
- [`docs/audit/BLOCK-C-CONSOLIDATION-PLAN.md`](../audit/BLOCK-C-CONSOLIDATION-PLAN.md)
- [`docs/disposition/wave-b-absorption.md`](../disposition/wave-b-absorption.md)
- [`BOUNDARY.md`](../../BOUNDARY.md)
- [phenotype-registry `projects/TestingKit.json`](https://github.com/KooshaPari/phenotype-registry/blob/main/projects/TestingKit.json)
