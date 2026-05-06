from chat import Chat
from character import Character
from data import Data
from assistant import Assistant

pass_context = False
context_file = {
    "name": "./week-3/chatbot-cmd-class/data/swapnil-info.txt",
    "type": "text"
}
mode = "roleplay"

if mode == "roleplay":
    character1 = Character(Data.characters[1], Data.user_info)
    chat = Chat("roleplay", Data.user_info,
                character1, Data.roleplay_chat_params)
elif mode == "assistant":
    assistant1 = Assistant(Data.assistants[1], Data.user_info)
    # chat = Chat(mode, Data.user_info, assistant1, Data.assistant_classify_chat_params, 0)
    # chat = Chat(mode, Data.user_info, assistant1, Data.assistant_chat_params, 0)
while 1:
    message_text = input(f"{Data.user_info['name']} (User):\n").strip()
    if (message_text.lower() == "quit" or message_text.lower() == "q"):
        break
    if pass_context:
        from embeddings_old import return_similarity_scores
        results = return_similarity_scores(
            context_file["type"], context_file["name"], message_text, 10)
        reply = chat.generate_output(message_text, results)
    else:
        reply = chat.generate_output(message_text)
    if mode == "assistant":
        print(f"Assistant:\n{reply}\n")
    elif mode == "roleplay":
        print(f"{character1.name} (Assistant):\n{reply}\n")

chat.export_chat_text()
