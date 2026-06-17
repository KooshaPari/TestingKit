# Boundary Lock: Fleet testing utilities

**Status:** ACTIVE — canonical testing-boundary repo for Phenotype polyrepo.

## Owns

- Shared test utilities SDK consumed by fleet repos
- Test scaffold generation patterns (import, do not duplicate per-repo)
- **Wave B (from HexaKit):**
  - `rust/phenotype-bdd` — BDD test harness (absorption pending)
  - `rust/phenotype-contract` — contract test trait (absorption pending)
  - `rust/phenotype-contracts` — contract value types (absorption pending)
  - `rust/phenotype-contract-tests` — contract test runner (absorption pending)
  - `rust/phenotype-test-infra` — test infra utilities (**landed**)
  - `rust/phenotype-test-fixtures` — test fixtures (**landed**)

## Does NOT own

- E2E landing harness (`phenotype-e2e-base`)
- Journey/UI harness (`phenotype-journeys`)

## Future consolidation

Fleet repos import TestingKit; per-repo test boilerplate absorbs here over time. HexaKit retains `MIGRATED.md` pointer stubs until downstream references clear.

See [docs/disposition/wave-b-absorption.md](./docs/disposition/wave-b-absorption.md) for Wave B lane status.
