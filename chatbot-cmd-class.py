from chat import Chat
from character import Character
from data import Data
from assistant import Assistant

mode = "roleplay"

character1 = Character(Data.characters[0], Data.user_info)
assistant1 = Assistant(Data.assistants[2], Data.user_info)
chat = Chat(Data.user_info, character1, "roleplay", Data.roleplay_chat_params)
# chat = Chat(user_info, assistant1, mode, assistant_classify_chat_params, 0)
while 1:
    message_text = input(f"{Data.user_info['name']} (User):\n").strip()
    if (message_text.lower() == "quit" or message_text.lower() == "q"):
        break
    reply = chat.generate_output(message_text)
    if mode == "assistant":
        print(f"Assistant:\n{reply}\n")
    elif mode == "roleplay":
        print(f"{character1.name} (Assistant):\n{reply}\n")

chat.export_chat_text()
