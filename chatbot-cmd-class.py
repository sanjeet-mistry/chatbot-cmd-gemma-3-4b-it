from chat import Chat

chat = Chat("Sandy", "Lisa")
while 1:
    message_text = input("User:\n")
    if (message_text.lower() == "quit" or message_text.lower() == "q"):
        break
    reply = chat.generate_output(message_text)
    print(f"Lisa:\n{reply}\n")

chat.export_chat_text()
