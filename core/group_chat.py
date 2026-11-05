import torch
import copy
import datetime as dt
from core.data import Data
from core.model import Model
from core.utils import get_gender_pronoun
import random


class GroupChat():
    show_logs = True

    def __init__(self, user_info, characters=None, model_info=Data.models["gemma-3-4b-it"], chat_settings=None, max_messages_in_context=25):
        self.id = random.randint(1000000000000000, 9999999999999999)
        self.messages_in_context = max_messages_in_context
        self.user_info = user_info
        self.characters = characters
        self.chat_model = Model(model_info)

        if chat_settings is None:
            self.chat_settings = Data.roleplay_chat_params
        else:
            self.chat_settings = chat_settings

        self.chat_history_full = []
        self.chat_history_recent = []

        self.messages = [
            {
                "role": "user",
                "content": ""
            }
        ]
        self.active_character = characters[0]

    def set_active_character(self, name):
        for character in self.characters:
            if character.name.lower() == name.lower():
                self.active_character = character
                return

    def update_system_prompt(self, active_character_name, max_tokens_output=100):
        self.set_active_character(active_character_name)

        other_characters_short_info = ""
        for character in self.characters:
            if character != self.active_character:
                text = f"{character.name} is a {character.age}-year-old {character.ethnicity} {character.gender}. Relationship with user: {character.relationship}.\n"
                other_characters_short_info += text

        character_names = ", ".join(
            character.name for character in self.characters)

        chat_transcript = "\n".join(
            f"{item['speaker']}: {item['message']}" for item in self.chat_history_recent)

        self.system_prompt = f"""You are {self.active_character.name}, participating in a group chat with {self.user_info['name']} (User) and other characters: {character_names}.

YOUR CHARACTER:
{self.active_character.name} is a {self.active_character.age}-year-old {self.active_character.ethnicity} {self.active_character.gender}.
Appearance: {get_gender_pronoun(self.active_character.gender, 'subject', 'capital')} has {self.active_character.hair_color}, {self.active_character.hair_style} hair and a {self.active_character.body_type} body with {self.active_character.breasts_size} breasts.
Personality: {self.active_character.personality_desc}
Hobbies: {self.active_character.hobbies}.
Kinks: {self.active_character.kinks}.
Occupation: {self.active_character.occupation}.

USER:
{self.user_info['name']}, {self.user_info['age']}-year-old {self.user_info['gender']}.
Hobbies: {self.user_info['hobbies']}.
Your relationship: {self.active_character.relationship}

OTHER CHARACTERS:
{other_characters_short_info}

GROUP CHAT HISTORY:
{chat_transcript}

RULES:
- Always stay in character. Only speak and act as {self.active_character.name}. Never control, impersonate or speak on behalf of other characters or the user.
- This is a shared group conversation. Interact naturally with both the user and other characters.
- Pay attention to who is being addressed. If the user addresses another character, don't assume the message is directed at you. Respond according to the conversation context and your own character's perspective.
- Maintain conversational continuity and remember what each participant has said. Avoid repetitive responses and unnecessary agreement.

RESPONSE FORMAT:
- Never include your name or any speaker label at the beginning of your response.
- Use *action* for non-spoken actions. Keep spoken dialogue outside asterisks.
- Answer in one paragraph.

Never mention being an AI or break character. Keep your response under {max_tokens_output} tokens."""

        self.messages[0]["content"] = self.system_prompt

    def append_message(self, message_text, active_character_name):
        self.chat_history_full.append(
            {
                "speaker": active_character_name.capitalize(),
                "message": message_text
            }
        )

    def update_messages_recent(self):
        self.chat_history_recent = copy.deepcopy(self.chat_history_full[-(
            self.messages_in_context):])

    def generate_output(self, message_text=None, active_character_name=None):
        start = dt.datetime.now()

        if message_text:
            self.append_message(message_text, "user")
            self.update_messages_recent()

        self.update_system_prompt(active_character_name)

        chat_template_kwargs = {
            "tokenize": True,
            "add_generation_prompt": True,
            "return_dict": True,
            "return_tensors": "pt",
        }

        input_ids = self.chat_model.tokenizer.apply_chat_template(
            self.messages,
            **chat_template_kwargs).to("cuda")

        with torch.inference_mode():
            outputs = self.chat_model.model.generate(
                **input_ids,
                max_new_tokens=self.chat_settings.get("max_new_tokens", 100),
                do_sample=self.chat_settings["do_sample"],
                temperature=self.chat_settings["temperature"],
                top_p=self.chat_settings["top_p"],
                top_k=self.chat_settings["top_k"],
                repetition_penalty=self.chat_settings.get("repetition_penalty", 1.0))

        prompt_length = input_ids["input_ids"].shape[-1]
        new_tokens = outputs[0][prompt_length:]
        # Decode only assistant reply
        reply = self.chat_model.tokenizer.decode(
            new_tokens, skip_special_tokens=True).strip()

        self.append_message(reply, active_character_name)
        self.update_messages_recent()

        end = dt.datetime.now()
        if GroupChat.show_logs:
            print(f"Time to reply: {end - start}")

        return reply
