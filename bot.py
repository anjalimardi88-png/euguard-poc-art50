from generated.enforcer import Enforcer
import uuid, json, time

enforcer = Enforcer()

def log_evidence(context, decision, policy_version):
    event = {
        "event_id": uuid.uuid4().hex[:8],
        "interaction_id": context.get("interaction_id", "unknown"),
        "user_id": context.get("user_id", "unknown"),
        "decision": decision,
        "policy_version": policy_version,
        "timestamp": int(time.time())
    }
    with open("evidence.log", "a") as f:
        f.write(json.dumps(event)+"\n")

def protected_action(user_input: str, context: dict):
    result = enforcer.check(context)
    if result["decision"] == "BLOCK":
        log_evidence(context, "BLOCKED", result["policy_version"])
        raise PermissionError(f"BLOCKED: {result['obligation']} must be shown first")
    
    log_evidence(context, "ALLOWED", result["policy_version"])
    return f"AI Response to: {user_input} for user {context['user_id']}"
