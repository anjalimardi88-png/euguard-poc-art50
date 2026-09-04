from bot import bot_uttor

disclosure_done = False
print("EU-Guard Bot Started (type 'exit' to stop)")

while True:
    user_input = input("You: ")
    if user_input == "exit":
        break
    response, disclosure_done = bot_uttor(user_input, disclosure_done)
    print(response)
