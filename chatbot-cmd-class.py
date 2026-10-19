from core.chat import Chat
from core.character import Character
from core.data import Data
from core.assistant import Assistant

pass_context = False
context_file = {
    "name": "./week-3/chatbot-cmd-class/data/swapnil-info.txt",
    "type": "text"
}
mode = "roleplay"
model = Data.models["gemma-4-e4b-it"]
response_length = Data.response_length["medium"]
if model["family"] == "qwen":
    chat_parameters = Data.qwen_roleplay_params
elif model["family"] == "gemma":
    if model["sub-family"] == "gemma-4":
        chat_parameters = Data.roleplay_chat_params_gemma_4
    else:
        chat_parameters = Data.roleplay_chat_params
chat_parameters['max_new_tokens'] = response_length["tokens"]

if mode == "roleplay":
    character1 = Character(
        Data.characters[12], Data.user_info, True, chat_parameters['max_new_tokens'])
    chat = Chat("roleplay", Data.user_info,
                character1, chat_parameters, 11, model)
elif mode == "assistant":
    assistant1 = Assistant(Data.assistants[1], Data.user_info)
    # chat = Chat(mode, Data.user_info, assistant1, Data.assistant_classify_chat_params, 0)
    # chat = Chat(mode, Data.user_info, assistant1, Data.assistant_chat_params, 0)
while 1:
    message_text = input(f"{Data.user_info['name']} (User):\n").strip()
    if (message_text.lower() == "quit" or message_text.lower() == "q"):
        break
    if pass_context:
        from core.embeddings_old import return_similarity_scores
        results = return_similarity_scores(
            context_file["type"], context_file["name"], message_text, 10)
        reply = chat.generate_output(message_text, results)
    else:
        reply = chat.generate_output(message_text)
    if mode == "assistant":
        print(f"Assistant:\n{reply}\n")
    elif mode == "roleplay":
        print(f"\n{character1.name} (Assistant):\n{reply}\n")

chat.export_chat_text()
