import uuid
from bot import protected_action

ctx = {
    "interaction_id": uuid.uuid4().hex,
    "user_id": "user_123",
    "is_first_interaction": True,
    "user_directly_interacts": True,
    "disclosure_shown": False
}

try:
    print(protected_action("Hello", ctx))
except PermissionError as e:
    print(f"Disclosure required: {e}")
    ctx["disclosure_shown"] = True
    print(protected_action("Hello after disclosure", ctx))
