import yaml
import os

print("Compiling policy.yaml to generated/enforcer.py")

with open('policy.yaml', 'r') as f:
    data = yaml.safe_load(f)

if isinstance(data, dict):
    raise ValueError("Policy must be a list, not dict")

if not isinstance(data, list) or not isinstance(data[0], dict):
    raise ValueError("Policy rule must be a dict inside a list")

policy = data[0]
os.makedirs('generated', exist_ok=True)

code = f'''
import datetime

POLICY_ID = "{policy['id']}"
ENFORCEMENT_MODE = "{policy['enforcement']}"

class Enforcer:
    def __init__(self):
        self.satisfied = False

    def check(self):
        if ENFORCEMENT_MODE == "BLOCK_UNTIL_SATISFIED" and not self.satisfied:
            self.log_event("BLOCK", "disclosure_missing")
            return "BLOCK"
        self.log_event("ALLOW", "disclosure_satisfied")
        return "ALLOW"

    def satisfy(self):
        self.satisfied = True

    def log_event(self, decision, reason):
        timestamp = datetime.datetime.now().isoformat()
        with open("evidence.log", "a") as log_file:
            log_file.write(f"[{{timestamp}}] POLICY={{POLICY_ID}} | Actor={policy['actor']} | Decision={{decision}} | Reason={{reason}} | ALCOA+ | Attributable Legible Contemporaneous Original Accurate\\n")
'''

with open('generated/enforcer.py', 'w') as out:
    out.write(code)

print("Success: generated/enforcer.py created")
