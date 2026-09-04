def bot_uttor(user_input, disclosure_done):
    if not disclosure_done:
        disclosure_done = True
        return "Disclosure: I am an AI Assistant, not a human. How can I help you?", disclosure_done

    if "human" in user_input.lower():
        return "I am an AI Assistant.", disclosure_done

    return f"Response to: {user_input}", disclosure_done
