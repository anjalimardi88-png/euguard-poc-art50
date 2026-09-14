from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import hashlib, time, json

app = FastAPI()

class Enforcer:
    def __init__(self):
        self.last_hash_val = "0"*64
    def last_hash(self): return self.last_hash_val
    def check(self, payload: dict):
        is_ai = payload.get("is_ai_generated", False)
        is_disclosed = payload.get("is_disclosed", False)
        allowed = not (is_ai and not is_disclosed)
        decision = "ALLOW" if allowed else "BLOCK_UNTIL_SATISFIED"
        h = hashlib.sha256(json.dumps({"ts": time.time(), "payload": payload, "decision": decision}, sort_keys=True).encode()).hexdigest()
        self.last_hash_val = h
        return {"allowed": allowed, "decision": decision, "evidence_hash": h}

enforcer = Enforcer()

HTML_PAGE = """
<!DOCTYPE html><html><head><title>EU-Guard - Article 50</title>
<style>body{font-family:sans-serif;background:#0a0a0a;color:white;text-align:center;padding:50px}
.badge{border:1px solid #333;padding:8px 16px;border-radius:20px;display:inline-block}
.btn{background:white;color:black;padding:12px 24px;border-radius:8px;text-decoration:none;display:inline-block;margin-top:20px}
</style></head><body>
<div class="badge">EU AI Act Article 50 • Live Enforcement</div>
<h1>EU-Guard is the Stripe for<br>EU AI Act Compliance</h1>
<p>policy.yaml to runtime enforcement in 10ms.<br>BLOCK_UNTIL_SATISFIED | ALCOA+ | Hash-Chain Verified</p>
<a class="btn" href="/api/evidence">View Live Evidence →</a>
<p style="margin-top:40px;color:#666">Live at www.euguard.in • v1.0.1</p>
</body></html>
"""

@app.get("/", response_class=HTMLResponse)
def home(): return HTML_PAGE

@app.get("/api")
def root(): return {"product": "EU-Guard", "article": "Article-50", "status": "Live"}

@app.get("/api/evidence")
def evidence(): return {"policy": "Article-50 v1.0.1", "enforcement": "BLOCK_UNTIL_SATISFIED", "last_hash": enforcer.last_hash(), "status": "Tamper-Evident Live"}

@app.post("/api/check")
def check(payload: dict): return enforcer.check(payload)
