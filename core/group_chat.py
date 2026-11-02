import torch
import copy
import datetime as dt
from core.data import Data
from core.system_prompt_group import SystemPromptGroup
from core.model import Model
import random


class GroupChat():
    show_logs = True

    def __init__(self, user_info, characters=None, model_info=Data.models["gemma-3-4b-it"], chat_settings=None, max_messages_in_context=17):
        self.id = random.randint(1000000000000000, 9999999999999999)
        self.messages_in_context = max_messages_in_context
        self.user_info = user_info
        self.characters = characters
        self.chat_model = Model(model_info)

        self.system_prompt = SystemPromptGroup(self.user_info, self.characters)

        if chat_settings is None:
            self.chat_settings = Data.roleplay_chat_params
        else:
            self.chat_settings = chat_settings

        self.messages_initial = self.system_prompt.messages_initial
        self.messages = copy.deepcopy(self.messages_initial)
        self.messages_recent = copy.deepcopy(self.messages_initial)

    def append_message(self, new_message):
        self.messages.append(new_message)

    def delete_blank_message(self):
        last_message = self.messages[len(self.messages) - 1]['content']
        del self.messages[-2:]
        self.messages[len(self.messages) - 1]['content'] += "\n" + last_message

    def update_messages_initial(self, active_character_name):
        self.system_prompt.update_messages_initial(active_character_name)
        self.messages[0] = copy.deepcopy(self.messages_initial[0])
        self.messages_recent[0] = copy.deepcopy(self.messages_initial[0])

    def update_messages_recent(self):
        length = len(self.messages)
        if length < self.messages_in_context:
            self.messages_recent = copy.deepcopy(self.messages)
        else:
            value = 2
            if length % 2 == 0:
                value = 3
            self.messages_recent = copy.deepcopy(
                self.messages_initial) + copy.deepcopy(self.messages[-(self.messages_in_context - value):])

    def generate_output(self, message_text=None, active_character_name=None):
        start = dt.datetime.now()

        new_message = {"role": "user", "content": message_text}
        self.append_message(new_message)
        self.update_messages_recent()
        ai_reply = False

        if message_text == "" and active_character_name:
            ai_reply = True

        if active_character_name:
            self.update_messages_initial(active_character_name)

        chat_template_kwargs = {
            "tokenize": True,
            "add_generation_prompt": True,
            "return_dict": True,
            "return_tensors": "pt",
        }

        input_ids = self.chat_model.tokenizer.apply_chat_template(
            self.messages_recent,
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

        reply = f"{active_character_name.capitalize()}: {reply}"
        new_message = {"role": "assistant", "content": reply}
        self.append_message(new_message)

        if ai_reply:
            self.delete_blank_message()

        self.update_messages_recent()

        end = dt.datetime.now()
        if GroupChat.show_logs:
            print(f"Time to reply: {end - start}")

        return reply
