from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import hashlib, time, json, os

app = FastAPI()

# --- REAL ENFORCER (No compiler needed) ---
class Enforcer:
    def __init__(self):
        self.last_hash_val = "0"*64
    def last_hash(self):
        return self.last_hash_val
    def check(self, payload: dict):
        is_ai = payload.get("is_ai_generated", False)
        is_disclosed = payload.get("is_disclosed", False)
        allowed = not (is_ai and not is_disclosed)
        decision = "ALLOW" if allowed else "BLOCK_UNTIL_SATISFIED"
        record = {"ts": time.time(), "payload": payload, "decision": decision, "prev": self.last_hash_val}
        h = hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()
        self.last_hash_val = h
        return {"allowed": allowed, "decision": decision, "evidence_hash": h, "article": "Article-50"}

enforcer = Enforcer()

# --- ROUTES ---
@app.get("/", response_class=HTMLResponse)
def home():
    with open(os.path.join(os.path.dirname(__file__), "../index.html"), "r") as f:
        return f.read()

@app.get("/api")
def root():
    return {"product": "EU-Guard", "article": "Article-50", "status": "Live"}

@app.get("/api/evidence")
def evidence():
    return {
        "policy": "EU-AI-Act-Article-50 v1.0.1",
        "enforcement": "BLOCK_UNTIL_SATISFIED",
        "last_hash": enforcer.last_hash(),
        "status": "Tamper-Evident Live"
    }

@app.post("/api/check")
def check(payload: dict):
    return enforcer.check(payload)
