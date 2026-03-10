from chat import Chat
from character import Character

user_name = "Sandy"

character1 = Character(Character.persons[0])
chat = Chat(user_name, character1)
while 1:
    message_text = input(f"{user_name} (User):\n")
    if (message_text.lower() == "quit" or message_text.lower() == "q"):
        break
    reply = chat.generate_output(message_text)
    print(f"{character1.name} (Assistant):\n{reply}\n")

chat.export_chat_text()
