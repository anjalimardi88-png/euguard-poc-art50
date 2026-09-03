# EuGuard POC - Article 50 Enforcement
import yaml

# Load policy
with open('policy.yaml', 'r') as f:
    policy = yaml.safe_load(f)

def get_bot_response(user_query):
    # Mandatory Article 50 Disclosure
    disclosure = policy['rules']['disclosure_text']
    
    # Simulated Appointment Booking
    response = f"{disclosure}\n\nHello! I can help you book an appointment. You said: {user_query}"
    
    # Mandatory Logging as per policy
    log_entry = f"LOG: User interaction logged for compliance - Query: {user_query}"
    print(log_entry)
    
    return response

# Example Usage
if __name__ == "__main__":
    print(get_bot_response("I need a doctor appointment"))
    print("\n--- Policy Control Proved ---")
    print("This bot cannot answer without Article 50 disclosure")
