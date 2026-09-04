# EuGuard - Article 50 POC - Compliance Compiler

**Real Company: EuGuard**
**Article: EU AI Act Article 50**

Live Demo: [Your Render Link Here After Deploy]

## Final Architecture Map (CENTER FLOW)

This repo proves Architecture Enforces, not App Remembers.

**Flow:** `Article 50 Requirement -> policy.yaml (9-field, List) -> compiler.py -> generated/enforcer.py -> bot.py runtime with enforce() -> evidence.log ALCOA+`

### Before (Config Reader - WRONG):
`policy.yaml -> app reads config -> formats response`

### Now (Compliance Compiler - CORRECT):
`regulation -> machine-readable policy -> compiler.py -> generated control -> enforced runtime -> evidence event`

> "The architecture enforces the invariant, not the application remembers to comply." - Anjali

## 6 Fixes Done as per Feedback

1. **Contract Fix:** policy.yaml is now List (not Dict) - `rules: [...]`
2. **9-field Semantics:** actor, subject, trigger, condition, obligation, exceptions, timing, enforcement, evidence, legal_source
3. **Independent Enforcement:** `BLOCK_UNTIL_SATISFIED` in generated/enforcer.py, not in bot.py
4. **Negative/Bypass Test:** test_policy.py proves protected action cannot run when BLOCK
5. **Narrow Obligation:** Only `ART50_DISCLOSURE_001` - first interaction disclosure
6. **3 Outputs Separated:** Policy (policy.yaml), Generated Control (generated/enforcer.py), Evidence (evidence.log)

## How to Test Hot-Reload (Proof of Compiler)

1. Change `policy.yaml` obligation text
2. Run `python compiler.py`
3. See `generated/enforcer.py` auto-changes
4. Run `python test_policy.py` - runtime behavior changes without editing validator

## Files

- `policy.yaml` - Machine-readable policy (9-field)
- `compiler.py` - Compiler: yaml -> executable enforcer
- `generated/enforcer.py` - Auto-generated control with BLOCK/ALLOW
- `bot.py` - Runtime that calls enforce()
- `test_policy.py` - Negative test + happy path
- `main.py` - Live Website combining Map + Playground
- `evidence.log` - ALCOA+ compliant evidence
