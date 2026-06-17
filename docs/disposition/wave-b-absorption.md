# Wave B absorption — HexaKit testing crates → TestingKit

**Session:** 20260617-ecosystem-disposition-wave  
**Lane:** Wave B testing  
**Authority:** [HexaKit DISPOSITION](https://github.com/KooshaPari/HexaKit/blob/main/docs/boundary/DISPOSITION.md) rows #4, #10–#12, #40–#41

## Summary

HexaKit still carries duplicate testing crates. TestingKit is the canonical owner for fleet test utilities. This lane adds pointer stubs in HexaKit and documents absorption status here.

| Disposition # | HexaKit path | TestingKit path | Status |
|---|---|---|---|
| 4 | `crates/phenotype-bdd` | `rust/phenotype-bdd` | Stub only — absorption pending |
| 10 | `crates/phenotype-contract` | `rust/phenotype-contract` | Stub only — absorption pending |
| 11 | `crates/phenotype-contracts` | `rust/phenotype-contracts` | Stub only — absorption pending |
| 12 | `crates/phenotype-contract-tests` | `rust/phenotype-contract-tests` | No HexaKit crate checkout; disposition row only |
| 40 | `crates/phenotype-test-infra` | `rust/phenotype-test-infra` | **Landed** in TestingKit |
| 41 | `crates/phenotype-test-fixtures` | `rust/phenotype-test-fixtures` | **Landed** in TestingKit |

## Consumer guidance

1. Add path or git dependencies against **TestingKit**, not HexaKit, for all rows above.
2. Treat HexaKit `MIGRATED.md` files as redirect stubs until removal PRs merge.
3. Contract family (#10–#12) should migrate as a set to preserve trait/type/runner cohesion.

## Follow-up lanes

- **HexaKit:** remove duplicate workspace members and implementation after downstream repoint PRs.
- **TestingKit:** land `phenotype-bdd`, `phenotype-contract`, `phenotype-contracts`, `phenotype-contract-tests` under `rust/`.
- **phenotype-registry:** sync `registry/disposition-index.json` rows (see manual sync note below).

## Registry sync (manual)

`disposition-index.json` on phenotype-registry currently includes ids **4** and **40** only. After this lane merges, update or open a registry PR to add:

```json
{"id": 10, "path": "crates/phenotype-contract", "disposition": "ABSORB", "target": "TestingKit", "wave": "B", "fsm": "in_progress", "core_lang": "rust"},
{"id": 11, "path": "crates/phenotype-contracts", "disposition": "ABSORB", "target": "TestingKit", "wave": "B", "fsm": "in_progress", "core_lang": "rust"},
{"id": 12, "path": "crates/phenotype-contract-tests", "disposition": "ABSORB", "target": "TestingKit", "wave": "B", "fsm": "in_progress", "core_lang": "rust"},
{"id": 41, "path": "crates/phenotype-test-fixtures", "disposition": "ABSORB", "target": "TestingKit", "wave": "B", "fsm": "in_progress", "core_lang": "rust"}
```

Set `fsm` to `in_progress` for ids **4**, **40** when stubs land; `done` when HexaKit duplicates are removed.

## References

- [BOUNDARY.md](../../BOUNDARY.md)
- [HexaKit crate-relocation runbook](https://github.com/KooshaPari/HexaKit/blob/main/docs/operations/crate-relocation-runbook.md)
- [phenotype-registry disposition-index](https://github.com/KooshaPari/phenotype-registry/blob/main/registry/disposition-index.json)
