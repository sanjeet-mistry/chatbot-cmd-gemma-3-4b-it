from chat import Chat
from character import Character
from data import Data
from assistant import Assistant

user_info = {
    "name": "Sandy",
    "gender": "Male",
    "age": 27,
    "occupation": "Software Developer"
}
assistant_chat_params = {
    "max_new_tokens": 250,
    "temperature": .6,
    "top_p": .9,
    "top_k": 50,
    "do_sample": True
}
assistant_classify_chat_params = {
    "max_new_tokens": 50,
    "temperature": 0,
    "top_p": 1,
    "top_k": 0,
    "do_sample": False
}
roleplay_chat_params = {
    "max_new_tokens": 150,
    "temperature": .7,
    "top_p": .9,
    "top_k": 40,
    "do_sample": True
}

mode = "assistant"

character1 = Character(Data.characters[2], user_info)
assistant1 = Assistant(Data.assistants[2], user_info)
# chat = Chat(user_info, character1, "roleplay", roleplay_chat_params)
chat = Chat(user_info, assistant1, mode, assistant_classify_chat_params, 0)
while 1:
    message_text = input(f"{user_info['name']} (User):\n").strip()
    if (message_text.lower() == "quit" or message_text.lower() == "q"):
        break
    reply = chat.generate_output(message_text)
    if mode == "assistant":
        print(f"Assistant:\n{reply}\n")
    elif mode == "roleplay":
        print(f"{character1.name} (Assistant):\n{reply}\n")

chat.export_chat_text()
