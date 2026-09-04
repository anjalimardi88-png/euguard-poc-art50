from bot import bot_uttor
import yaml

print("--- Starting Policy Control Test ---")

# Test 1: Check policy file
try:
    with open('policy.yaml', 'r') as f:
        policy = yaml.safe_load(f)
    print("✅ Test 1 Passed: policy.yaml ache")
except:
    print("❌ Test 1 Failed: policy.yaml nei")
    exit()

# Test 2: Check disclosure
uttor, flag = bot_uttor("Hello", False)
if "AI Assistant" in uttor and flag == True:
    print("✅ Test 2 Passed: Disclosure kaj korche")
else:
    print("❌ Test 2 Failed")

print("--- All Tests Done ---")
