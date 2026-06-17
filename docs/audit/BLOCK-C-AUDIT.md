# Block-C Audit — KooshaPari/TestingKit

**Date:** 2026-06-17  
**Auditor:** ecosystem disposition wave (Block-C)  
**Charter:** [`phenotype-registry/docs/rationalization/boundary-shaping.md`](https://github.com/KooshaPari/phenotype-registry/blob/main/docs/rationalization/boundary-shaping.md)  
**Registry:** [`phenotype-registry/BOUNDARY_OWNERS.md`](https://github.com/KooshaPari/phenotype-registry/blob/main/BOUNDARY_OWNERS.md) §Testing / QA  
**Wave B:** [`docs/disposition/wave-b-absorption.md`](../disposition/wave-b-absorption.md)

---

## Executive summary

| Signal | Finding |
|--------|---------|
| **Repo role** | Split testing boundary — Rust fleet utilities + legacy Python tree (now canonical in SDK) |
| **Boundary lock** | **ACTIVE** for Rust workspace; Python consumers redirect to `phenotype-python-sdk` |
| **Python absorption** | **COMPLETE** — `packages/testing-kit` reconciled (34 blob divergences, 2026-06-17) |
| **Wave B (HexaKit)** | **PARTIAL** — `phenotype-test-infra` + `phenotype-test-fixtures` landed; bdd/contract family pending |
| **GitHub archive flag** | **ARCHIVED** — intentional; boundary remains active per registry gate |
| **Primary risk** | README stale (claims empty Python submodules); testing plane split not yet fleet-default |
| **Recommended action** | Publish Block-C disposition; execute Wave B landing + consumer repoint; **HOLD DELETE** |

---

## Baseline checks

| Check | Result | Notes |
|-------|--------|-------|
| Rust workspace builds (`cargo build --workspace`) | **PASS** | 5 member crates on `main` |
| `phenotype-test-infra` + `phenotype-test-fixtures` present | **PASS** | Wave B rows #40, #41 landed |
| `phenotype-bdd` / contract family in `rust/` | **FAIL** | Absorption pending from HexaKit (#4, #10–#12) |
| Python `mcp-qa` tree on `main` | **PASS** | ~200+ source files; canonical copy now in SDK |
| SDK reconcile (`testing-kit-mcp-qa-reconcile`) | **PASS** | `projects/TestingKit.json` — delete eligible for Python slice only |
| `BOUNDARY.md` Wave B owns list | **PASS** | Updated in PR #2 |
| `docs/boundary/DISPOSITION.md` | **FAIL** | This Block-C PR |
| README accuracy | **FAIL** | Still describes empty Python submodules; LICENSE now present |
| Journey manifests populated | **FAIL** | `journey-gate.yml` stub; manifests empty |
| Testing plane split documented | **FAIL** | BOUNDARY_OWNERS split table not reflected in-repo |

---

## Testing plane split (registry authority)

Per `BOUNDARY_OWNERS.md` §Testing / QA — **file parity in python-sdk does not close the boundary**:

| Slice | Canonical owner | TestingKit role after Block-C |
|-------|-----------------|-------------------------------|
| MCP QA, pytest plugins, quality CLIs | `phenotype-python-sdk/packages/testing-kit` | **Redirect** — source frozen; SDK is consumer default |
| xDD / BDD / property / mutation (Rust) | `phenoXddLib` (long-term) / **TestingKit** (Wave B near-term) | **Land Wave B** then evaluate xDD split |
| E2E journey harness | `phenotype-journeys` | **DECOMPOSE** — `docs/journeys/` is reference only |
| Per-repo test scaffolds (Playwright, CI harness) | `phenokits-commons` | **Does not own** |
| Org CI policy workflows | `phenotype-org-governance` + HexaKit `.template.*` | **Does not own** |
| Rust fleet test helpers (timeout, mock, fixtures, infra) | **TestingKit** `rust/` | **DYNAMIC-KEEP** — canonical until crates.io publish |

---

## Cross-repo boundary overlaps

| Concern | Also present in | Canonical owner | TestingKit role |
|---------|-----------------|-----------------|-----------------|
| Python testing packages | `phenotype-python-sdk/packages/testing-kit` | **phenotype-python-sdk** | Migration source (frozen) |
| HexaKit testing crates | `HexaKit/crates/phenotype-*` | **TestingKit** | Absorption target (Wave B) |
| Compliance scanner + health | `PhenoObservability` | **Split** — scanner stays; health wire optional | `health-integration` feature → PO later |
| BDD/contract runners | `phenoXddLib` (target) | **TBD** post-Wave-B | Near-term owner via Wave B |
| Journey keyframes / manifests | `phenotype-journeys` | **phenotype-journeys** | Stub manifests only |
| Domain SDK monolith plan | `RATIONALIZATION_PLAN.md` | **Retired** per ADR-ECO-006 | TestingKit stays domain-named |

---

## Archive gate status

Per `BOUNDARY_OWNERS.md` delete gate (5 conditions):

| # | Condition | Status |
|---|-----------|--------|
| 1 | Canonical owner named | **PASS** — split owners documented |
| 2 | Inbound absorptions merged | **PARTIAL** — Python done; Wave B Rust pending |
| 3 | Outbound consumers repointed | **PARTIAL** — SDK default for Py; Rust git deps still point here |
| 4 | Scaffold hooks at owner | **PARTIAL** — SDK has testing-kit; Rust not on crates.io |
| 5 | No unique slice only in source | **FAIL** — Rust workspace unique to this repo |

**Verdict:** **KEEP_ARCHIVED** — boundary active; **not** delete-eligible despite Python absorption.

---

## Related documents

- [`docs/boundary/DISPOSITION.md`](../boundary/DISPOSITION.md)
- [`docs/audit/BLOCK-C-CONSOLIDATION-PLAN.md`](./BLOCK-C-CONSOLIDATION-PLAN.md)
- [`phenotype-registry/projects/TestingKit.json`](https://github.com/KooshaPari/phenotype-registry/blob/main/projects/TestingKit.json)
- [`phenotype-python-sdk/packages/testing-kit/docs/operations/testing-kit-mcp-qa-reconcile.md`](https://github.com/KooshaPari/phenotype-python-sdk/blob/main/packages/testing-kit/docs/operations/testing-kit-mcp-qa-reconcile.md)
