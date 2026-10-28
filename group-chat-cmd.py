from core.character import Character
from core.data import Data
from core.group_chat import GroupChat

# model = Data.models["gemma-3-4b-it"]
# if model["family"] == "qwen":
#     chat_parameters = Data.qwen_roleplay_params
# elif model["family"] == "gemma":
#     if model["sub-family"] == "gemma-4":
#         chat_parameters = Data.roleplay_chat_params_gemma_4
#     else:
#         chat_parameters = Data.roleplay_chat_params

character_nums = [12, 2]
characters = []
for num in character_nums:
    character = Character(Data.characters[num], Data.user_info)
    characters.append(character)

group_chat = GroupChat(Data.user_info, characters)
firstTime = True

while 1:
    if firstTime:
        message_text = input(f"{Data.user_info['name']} (User):\n").strip()
        firstTime = False
    else:
        user_reply = input(
            "Do you want to reply yourself? (y/n): "
        ).strip().lower() == "y"
        if user_reply:
            message_text = input(f"{Data.user_info['name']} (User):\n").strip()
        else:
            message_text = ""

    active_character = input(
        "Which character do you want to reply? (Type their name): ").lower()
    reply = group_chat.generate_output(message_text, active_character)
    print(f"\n{active_character} (Assistant):\n{reply}\n")
