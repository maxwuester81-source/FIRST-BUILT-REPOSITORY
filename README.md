# COA Epistemic Runtime - 001B

**Branch Ledger & Evidence Gate for MAX OS / City of Agents**

Epistemically safe persistent storage and validation for multi-agent hypothesis evaluation, branch history, and Canon promotion.

## Overview

This system provides:

1. **BRANCH_LEDGER_V1** — Persistent ledger of all hypothesis branches with full provenance
2. **PR_EVIDENCE_GATE_V1** — Deterministic validation before promotion to Canon
3. **Governance Guards** — Prevent autonomous writes, uncontrolled escalation, Canon corruption
4. **Rollback Representation** — Escape routes always reconstructible, never lost

## Architecture

```
src/
├── core/
│   ├── branch_ledger.py          # Ledger data models & operations
│   ├── evidence_gate.py           # Evidence validation logic
│   ├── provenance.py              # Provenance chain tracking
│   └── governance.py              # Canon/write protection guards
├── storage/
│   ├── ledger_store.py            # Abstract ledger interface
│   ├── sqlite_adapter.py          # SQLite implementation
│   └── migrations.py              # Schema initialization
├── types/
│   ├── branch.py                  # Branch data structures
│   ├── evidence.py                # Evidence types
│   └── decisions.py               # Gate decision enums
└── utils/
    └── validation.py              # Schema validators
```

## Key Concepts

### Branch Ledger
Every hypothesis is recorded as a **branch** in the ledger:
- `branch_id` — unique identifier
- `parent_id` — parent branch (enables rollback)
- `task_id` — associated task
- `hypothesis` — the claim being tested
- `status` — active | falsified | pruned | merged
- `assumptions` — what we assume true
- `evidence` — supporting evidence with confidence
- `counterevidence` — contradicting evidence with weight
- `provenance_chain` — full history of decisions

Falsified and pruned branches remain queryable for analysis and rollback planning.

### Evidence Gate
Before any branch is promoted to Canon:

```
Evidence Gate Checks:
  ✓ Evidence sufficiency
  ✓ Counterevidence detected
  ✓ Provenance complete
  ✓ Unresolved contradictions identified
  ✓ Risk class acceptable
  ✓ Canon impact assessed
  ✓ Capability compliance verified
  ✓ Resource budget compliant
  ✓ Stopping policy respected
  ✓ Branch disagreement resolved
  ✓ Rollback path available
  ✓ Human approval (if critical)

Possible Outputs:
  - PASS               → Safe to promote
  - FAIL               → Rejected (evidence insufficient or contradicts)
  - BLOCKED_BY_EVIDENCE → Unresolved issues (more evidence needed)
  - HUMAN_APPROVAL_REQUIRED → Critical action, requires sign-off
```

**Important:** A high score alone does NOT produce PASS. Evidence quality matters.

### Governance Guards

1. **No Autonomous Canon Writes**
   - All Canon promotion requires human approval
   - Score-based escalation is blocked

2. **No Uncontrolled External Writes**
   - External I/O (network, files, Drive) disabled by default
   - Requires explicit capability grant + approval

3. **Capability Escalation Defense**
   - Unauthorized promotion (read → write) is rejected
   - Escalation requires explicit approval

4. **Resource Budget Enforcement**
   - Branches exceeding budget fail gate
   - Resource compliance verified before PASS

5. **Stopping Policy Enforcement**
   - Even high-confidence branches fail if stopping condition met
   - Policy is not overrideable by score

### Rollback Representation

Rollback is **represented, not executed**:
- Every branch has `parent_id` — unwind path always available
- Gate check: "Is rollback available?" must pass before PASS
- Pruned branches marked with `pruning_reason` — why they were discarded
- To rollback: inspect parent branch, developer initiates revert (not autonomous)

## Storage

**SQLite** (`data/branch_ledger.db`)

- Persistent across restarts
- Queryable with SQL
- ACID transactions (safe rollback)
- No external service dependency
- Git-ignored (data/ directory)

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_branch_ledger.py

# With coverage
pytest --cov=src tests/

# Verbose output
pytest -v
```

## Test Categories

- **test_branch_ledger.py** — Persistence, recovery, schema validation
- **test_evidence_gate.py** — Gate logic, evidence checking, contradiction detection
- **test_provenance.py** — Chain recovery, assumption tracking, evidence linkage
- **test_governance.py** — Canon protection, external write blocking, capability escalation
- **test_integration.py** — Full hypothesis → ledger → gate workflow
- **test_regression.py** — No autonomous writes, no autonomy bypass

## Implementation Notes

- **No external dependencies** — Python 3.9+ stdlib only
- **Minimal architecture** — Designed to integrate with existing MAX OS runtime
- **Human-centered** — Decisions require approval, not autonomous
- **Provenance-first** — Every decision is logged and recoverable
- **Test-driven** — 40+ tests verify governance constraints

## Next Steps

See `COA_EPISTEMIC_001B_VERIFICATION_REPORT.md` for test results and remaining gaps.

## License

MIT
