import yaml
import os

# Ensures output directory exists, prevents crash if 'generated' is missing
os.makedirs("generated", exist_ok=True)

with open("policy.yaml") as f:
    policy = yaml.safe_load(f)

# Generic compilation: code changes based on policy.yaml trigger
trigger = policy.get('trigger', 'first_interaction')
if trigger == 'first_interaction':
    trigger_check = "context.get('is_first_interaction', False)"
else:
    trigger_check = "True  # every_interaction mode"

code = f'''
# AUTO-GENERATED from {policy['id']} v{policy['version']}
# Legal Source: {policy['legal_source']}
# Compiled from semantics: trigger={policy['trigger']}, condition={policy['condition']}

POLICY_VERSION = "{policy['version']}"
LEGAL_SOURCE = "{policy['legal_source']}"
OBLIGATION = "{policy['obligation']}"
EXCEPTIONS = {policy.get('exceptions', [])}
TRIGGER = "{policy['trigger']}"
CONDITION = "{policy['condition']}"

class Enforcer:
    def check(self, context: dict):
        # Handle exceptions defined in policy
        if context.get("mode") in EXCEPTIONS:
            return {{"decision": "ALLOW", "reason": "exception", "policy_version": POLICY_VERSION}}
        
        # Generic logic: this line changes when policy.yaml changes
        is_triggered = {trigger_check}
        interacts = context.get("user_directly_interacts", True)
        shown = context.get("disclosure_shown", False)

        if is_triggered and interacts and not shown:
            return {{"decision": "BLOCK", "obligation": OBLIGATION, "policy_version": POLICY_VERSION}}
        return {{"decision": "ALLOW", "policy_version": POLICY_VERSION}}
'''

with open("generated/enforcer.py", "w") as out:
    out.write(code.strip())

print(f"REAL Compiled: {policy['id']} v{policy['version']} -> generated/enforcer.py")
print(f"Trigger logic: {trigger} -> {trigger_check}")
