import torch
import copy
import datetime as dt
from core.data import Data
from core.system_prompt_group import SystemPromptGroup
import random


class GroupChat():
    show_logs = True

    def __init__(self, user_info, characters=None, model_info=Data.models["gemma-3-4b-it"], messages_initial=[], chat_settings=None, max_messages_in_context=17):
        self.id = random.randint(1000000000000000, 9999999999999999)
        self.messages_in_context = max_messages_in_context

        if chat_settings is None:
            self.chat_settings = Data.default_chat_params
        else:
            self.chat_settings = chat_settings

        self.messages_initial = copy.deepcopy(messages_initial)
        self.messages = copy.deepcopy(self.messages_initial)
        self.messages_recent = copy.deepcopy(self.messages_initial)
