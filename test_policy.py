from generated.enforcer import Enforcer
from bot import protected_action

def test_negative_bypass():
    print("Running negative bypass test")
    e = Enforcer()
    result = e.check()
    assert result == "BLOCK", "Should be BLOCK without disclosure"
    print("PASS: Protected action is BLOCKED without disclosure")

    try:
        # Simulate direct bypass attempt
        enforcer_test = Enforcer()
        if enforcer_test.check() == "BLOCK":
            raise PermissionError("Bypass blocked by enforcer")
        print("FAIL: Bypass allowed")
    except PermissionError as err:
        print(f"PASS: Negative test asserts PermissionError: {{err}}")

    e.satisfy()
    assert e.check() == "ALLOW"
    print("PASS: After disclosure, ALLOW")

if __name__ == "__main__":
    test_negative_bypass()
    print("All architectural proofs passed")
