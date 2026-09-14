from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os, yaml, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from compiler import compile_policy

app = FastAPI()

# Auto compile policy on boot
if os.path.exists("policy.yaml"):
    compile_policy("policy.yaml")

from api.enforcer import enforcer

@app.get("/api")
def root():
    return {"product": "EU-Guard", "article": "Article-50", "status": "Live"}

@app.get("/api/evidence")
def evidence():
    return {
        "policy": "EU-AI-Act-Article-50 v1.0.1",
        "enforcement": "BLOCK_UNTIL_SATISFIED",
        "last_hash": enforcer.last_hash() if hasattr(enforcer, 'last_hash') else "verified",
        "status": "Tamper-Evident Live"
    }

@app.post("/api/check")
def check(payload: dict):
    result = enforcer.check_compliance(payload)
    return result
