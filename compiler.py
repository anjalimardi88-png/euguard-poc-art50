import os
import yaml

os.makedirs("generated", exist_ok=True)

with open("policy.yaml") as f:
    policy = yaml.safe_load(f)

policy_id = policy.get('id', 'EU-AI-Act-Article-50')
policy_version = policy.get('version', '1.0.1')
trigger = policy.get('trigger', 'first_interaction')
enforcement = policy.get('enforcement', 'BLOCK_UNTIL_SATISFIED')

# Real: only BLOCK logic, no WARN_ONLY
if trigger == "first_interaction":
    trigger_check = "context.get('is_first_interaction', False)"
else:
    trigger_check = "True"

code = f'''
import time, json, uuid, hashlib

POLICY_ID = "{policy_id}"
POLICY_VERSION = "{policy_version}"
ENFORCEMENT = "{enforcement}"
_last_hash = ""

def log_evidence(context, decision):
    global _last_hash
    event = {{
        "event_id": uuid.uuid4().hex[:8],
        "interaction_id": context.get("interaction_id", uuid.uuid4().hex),
        "user_id": context.get("user_id", "anon"),
        "policy_id": POLICY_ID,
        "policy_version": POLICY_VERSION,
        "decision": decision["decision"],
        "reason": decision["reason"],
        "timestamp": int(time.time()),
        "prev_hash": _last_hash
    }}
    event_json = json.dumps(event, sort_keys=True)
    event_hash = hashlib.sha256(event_json.encode()).hexdigest()
    event["hash"] = event_hash
    _last_hash = event_hash
    with open("evidence.jsonl", "a") as out:
        out.write(json.dumps(event) + "\\n")
    return event

class Enforcer:
    def check(self, context):
        # Exception
        if context.get("research_mode") or context.get("internal_testing"):
            return {{"decision": "ALLOW", "reason": "exception", "disclosure_shown": False}}

        # Disclosure check
        if not context.get("disclosure_done"):
            if {trigger_check}:
                decision = {{"decision": "BLOCKED", "reason": f"Disclosure required per {{POLICY_ID}}", "enforcement": ENFORCEMENT}}
                log_evidence(context, decision)
                return decision
        
        decision = {{"decision": "ALLOW", "reason": "compliant", "policy_version": POLICY_VERSION, "disclosure_shown": True}}
        log_evidence(context, decision)
        return decision
'''

with open("generated/enforcer.py", "w") as out:
    out.write(code)

print("Real compiler done -> generated/enforcer.py with BLOCK_UNTIL_SATISFIED + hash chain")
