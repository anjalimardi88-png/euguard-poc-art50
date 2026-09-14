import datetime
import os
import threading
import json
import logging

# --- Production Config ---
POLICY_ID = os.getenv("POLICY_ID", "ART50_DISCLOSURE_001")
ENFORCEMENT_MODE = os.getenv("ENFORCEMENT_MODE", "BLOCK_UNTIL_SATISFIED")

logger = logging.getLogger("euguard")
logger.setLevel(logging.INFO)

class Enforcer:
    def __init__(self):
        self._satisfied = False
        self._lock = threading.Lock()

    def check(self, actor_id: str = "AI_Agent"):
        """Checks if action is allowed under Article 50."""
        with self._lock:
            is_satisfied = self._satisfied

        if ENFORCEMENT_MODE == "BLOCK_UNTIL_SATISFIED" and not is_satisfied:
            self.log_event("BLOCK", "disclosure_missing", actor_id)
            return {
                "decision": "BLOCK",
                "allowed": False,
                "policy_id": POLICY_ID,
                "reason": "Disclosure required under Article 50"
            }
        
        self.log_event("ALLOW", "disclosure_satisfied", actor_id)
        return {
            "decision": "ALLOW",
            "allowed": True,
            "policy_id": POLICY_ID
        }

    def satisfy(self, actor_id: str = "Human_User"):
        """Marks disclosure as satisfied."""
        with self._lock:
            self._satisfied = True
        
        self.log_event("SATISFY", "user_provided_disclosure", actor_id)
        return {
            "status": "satisfied",
            "policy_id": POLICY_ID,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

    def log_event(self, decision: str, reason: str, actor_id: str = "AI_Agent"):
        """ALCOA+ Compliant evidence logging - no file write, safe for Vercel."""
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        evidence = {
            "timestamp": timestamp,
            "policy_id": POLICY_ID,
            "actor": actor_id,
            "decision": decision,
            "reason": reason,
            "alcoa_plus": "Attributable, Legible, Contemporaneous, Original, Accurate, Complete, Consistent, Enduring, Available",
            "compliance": "EU AI Act Article 50"
        }
        # Logs to Vercel Runtime Logs as JSON - no crash
        logger.info(json.dumps(evidence))
        return evidence

# Singleton instance to be used by your API routes
enforcer = Enforcer()
