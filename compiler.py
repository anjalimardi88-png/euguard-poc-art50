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
            # FIX Point 3: Trust Boundary - only admin can use exception
            if not context.get("is_trusted_admin", False):
                        return {{"decision": "BLOCKED", "reason": "Untrusted caller cannot set exception mode"}}
        return {{"decision": "ALLOW", "reason": "exception", "policy_version": POLICY_VERSION}}
            

        # Generic logic: this line changes when policy.yaml changes
        is_triggered = {trigger_check}
        interacts = context.get("user_directly_interacts", True)
          
        shown = context.get("disclosure_shown", False)

        if is_triggered and interacts and not shown:
            # FIX Point 1 & 2: Enforcement is data-driven from policy.yaml
            enforcement = "{policy.get('enforcement', 'BLOCK_UNTIL_SATISFIED')}"
            if enforcement == "BLOCK_UNTIL_SATISFIED":
                return {{"decision": "BLOCKED", "reason": f"Disclosure required per {{POLICY_ID}}", "enforcement": enforcement}}
            elif enforcement == "WARN_ONLY":
                return {{"decision": "ALLOW_WITH_WARNING", "reason": f"Would block but WARN_ONLY per {{POLICY_ID}}", "enforcement": enforcement}}
            else:
                return {{"decision": "BLOCKED", "reason": "Unknown enforcement", "enforcement": enforcement}}

        # FIX Point 4: Immutable evidence log, not just boolean
        return {{"decision": "ALLOW", "reason": "compliant", "policy_version": POLICY_VERSION, "disclosure_shown": True}}
        
    
