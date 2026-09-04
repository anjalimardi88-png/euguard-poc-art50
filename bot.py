from generated.enforcer import Enforcer

enforcer = Enforcer()

def protected_action(user_input):
    decision = enforcer.check()
    if decision == "BLOCK":
        raise PermissionError(f"Blocked by {{enforcer.__class__.__name__}}: Disclosure required")
    return f"AI response to: {{user_input}}"

def get_bot_response(user_input):
    try:
        return protected_action(user_input)
    except PermissionError:
        disclosure = "Disclosure: You are interacting with an AI Assistant under EU AI Act Article 50."
        enforcer.satisfy()
        answer = protected_action(user_input)
        return f"{{disclosure}} {{answer}}"
