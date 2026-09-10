# EU-Guard - Article 50 Compliance Compiler

`policy.yaml -> compiler.py -> generated/enforcer.py -> runtime`

Real compiler POC for EU AI Act Article 50.
Per-interaction enforcement with generic compilation.

**Evidence:** structured evidence log with event_id, 
interaction_id, user_id, policy_version, timestamp.
Tamper-evident log (hash chain) planned for v1.1.

**Usage:**
python compiler.py
python test.py
