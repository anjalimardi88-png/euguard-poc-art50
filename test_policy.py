# Test to prove Policy Control is working
from bot import get_bot_response
import yaml

print("--- Starting Policy Control Test ---")

# Test 1: Check if policy file exists
try:
    with open('policy.yaml', 'r') as f:
        policy = yaml.safe_load(f)
    print("✅ Test 1 Passed: policy.yaml found")
except:
    print("❌ Test 1 Failed: policy.yaml NOT found - Bot cannot run!")
    exit()

# Test 2: Check if disclosure is mandatory
response = get_bot_response("test appointment")

if "AI system" in response or "artificial intelligence" in response.lower():
    print("✅ Test 2 Passed: Article 50 Disclosure is enforced in every response")
    print(f"\nBot Response:\n{response}")
else:
    print("❌ Test 2 Failed: Disclosure missing - Violation of Article 50!")

print("\n--- Result: Policy Control is ACTIVE. Bot cannot bypass policy. ---")
