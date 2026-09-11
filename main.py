from fastapi import FastAPI
from generated.enforcer import Enforcer
import uuid, os

app = FastAPI(title="EU-Guard Real Product - Art 50")

# Make sure generated folder exists
os.makedirs("generated", exist_ok=True)

@app.get("/")
def home():
    return {"status": "Real Product Live", "product": "EU-Guard Art 50 BLOCK_UNTIL_SATISFIED"}

@app.post("/chat")
def chat(user_id: str, message: str, disclosure_done: bool = False, is_first: bool = True):
    from generated.enforcer import Enforcer
    enforcer = Enforcer()
    context = {
        "interaction_id": uuid.uuid4().hex,
        "user_id": user_id,
        "is_first_interaction": is_first,
        "disclosure_done": disclosure_done
    }
    decision = enforcer.check(context)
    if decision["decision"] == "BLOCKED":
        return {"blocked": True, "msg": "AI Disclosure Required per EU AI Act Art 50", "evidence": decision}
    return {"blocked": False, "answer": f"Processed: {message}", "evidence": decision}
