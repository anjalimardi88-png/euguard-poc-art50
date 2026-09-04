import yaml
import datetime

POLICY_FILE = "policy.yaml"
EVIDENCE_FILE = "evidence.log"

def load_policy():
    with open(POLICY_FILE, 'r') as f:
        data = yaml.safe_load(f)
        return data[0]

def log_evidence(ghotona):
    somoy = datetime.datetime.utcnow().isoformat()
    lekha = f"{somoy} | {ghotona} | ALCOA+\n"
    with open(EVIDENCE_FILE, 'a') as log:
        log.write(lekha)
    print(f"[PROMAN JOMA HOLO] {lekha}")

def bot_uttor(user_kotha, disclosure_hoeche=False):
    policy = load_policy()
    if not disclosure_hoeche and policy['enforcement'] == "BLOCK_UNTIL_SATISFIED":
        disclosure = f"DISCLOSURE [{policy['legal_source']}]: Apni ekjon AI Assistant ({policy['actor']}) er sathe kotha bolchen."
        log_evidence(f"{policy['obligation']} - {policy['trigger']} te trigger holo")
        return disclosure, True
    return f"Bot er Uttor: {user_kotha}", disclosure_hoeche

if __name__ == "__main__":
    disclosure = False
    msg = "Hello"
    uttor, disclosure = bot_uttor(msg, disclosure)
    print(uttor)
