# EU-Guard - Article 50 Compliance Compiler POC

This is a Proof of Concept for EU AI Act Article 50 compliance, implemented as a compliance compiler, not just a policy-driven application.

## Architecture Flow

`Article 50 requirement -> policy.yaml (9-field executable) -> compiler.py (compiler) -> generated/enforcer.py (auto-generated control) -> bot.py runtime with enforce() -> evidence.log (ALCOA+)`

This demonstrates:
- Regulation to machine-readable policy
- Policy to generated executable control
- Enforced runtime behaviour
- Evidence generation

## 6 Fixes Implemented (Final Map)

1.  **Contract Fix (List vs Dict):** Policy is enforced as a LIST to avoid key override issues. Dict input is rejected.
2.  **Sentence to 9-Field Semantics:** Policy contains actor, subject, trigger, condition, obligation, exceptions, timing, enforcement, evidence, legal_source.
3.  **Independent Enforcement:** Uses `BLOCK_UNTIL_SATISFIED` instead of `disclosure + answer`. Runtime blocks if disclosure is missing.
4.  **Weak Test to Negative Bypass Test:** Test now asserts `PermissionError` on bypass attempt, proving protected action cannot execute without policy satisfaction.
5.  **Broad to One Narrow Obligation:** Scoped to `ART50_DISCLOSURE_001` only - disclosure that user is interacting with AI.
6.  **Missing 3 Outputs:** Now generates 3 separated outputs: `policy.yaml`, `generated/enforcer.py`, `evidence.log`.

## Files

- `policy.yaml`: Machine-readable policy representation (9 fields)
- `compiler.py`: Compiles YAML policy to executable Rego/Python control
- `generated/enforcer.py`: Auto-generated runtime control (DO NOT EDIT MANUALLY)
- `bot.py`: Application runtime that calls `enforcer.check()` for BLOCK/ALLOW
- `main.py`: Entry point
- `test_policy.py`: Negative bypass test proving architectural enforcement
- `evidence.log`: ALCOA+ compliant evidence events

## How to Run

1. Compile policy:
   `python compiler.py`

2. Run bot:
   `python main.py`

3. Run architectural proof test:
   `python test_policy.py`

4. Check evidence:
   `cat evidence.log`

## Key Test

Change `policy.yaml` -> run `compiler.py` -> runtime behaviour changes without editing `bot.py`. This proves it is a compiler.
