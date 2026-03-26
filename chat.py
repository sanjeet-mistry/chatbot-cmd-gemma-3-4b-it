from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
import copy
import datetime as dt
import os
import random


class Chat():
    model_path = "./models/gemma-3-4b-it"
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16
    )
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        quantization_config=bnb_config,  # Apply quantization here
        device_map="auto"
    )
    # number of recent messages to add in context including the initial messages
    messages_recent_size = 11
    show_logs = True

    def __init__(self, user_info, ai, mode):
        self.id = random.randint(1000000000, 9999999999)
        self.user_name = user_info["name"]
        self.user_gender = user_info["gender"]
        self.ai_name = ai.name
        self.mode = mode
        if self.mode == "roleplay":
            self.ai_gender = ai.gender
        self.messages_initial = ai.messages_initial
        self.messages = [
        ]
        self.messages = self.messages_initial + self.messages
        self.messages_recent = copy.deepcopy(self.messages)
        self.use_summ = False
        if self.use_summ:
            from summary import Summary
            self.messages_summ = copy.deepcopy(self.messages)
            self.messages_summ_recent = copy.deepcopy(self.messages)
            self.summary = Summary()
            Chat.messages_recent_size = 21

    def update_messages_recent(self):
        messages_recent = None
        messages = None
        if self.use_summ:
            messages = self.messages_summ
            messages_recent = self.messages_summ_recent
        else:
            messages = self.messages
            messages_recent = self.messages_recent
        if (len(messages) > Chat.messages_recent_size):
            if len(messages) % 2 == 0:
                messages_recent = self.messages_initial + \
                    copy.deepcopy(
                        messages[-(Chat.messages_recent_size - 3):])
            else:
                messages_recent = self.messages_initial + \
                    copy.deepcopy(
                        messages[-(Chat.messages_recent_size - 2):])
        else:
            messages_recent = messages
        if self.use_summ:
            self.messages_summ_recent = messages_recent
        else:
            self.messages_recent = messages_recent

    def generate_output(self, message_text):
        start = dt.datetime.now()
        new_message = {"role": "user", "content": message_text}
        self.append_new_message(new_message)
        self.check_to_create_summary()
        self.update_messages_recent()

        if self.use_summ:
            input_ids = Chat.tokenizer.apply_chat_template(
                self.messages_summ_recent,
                tokenize=True,
                add_generation_prompt=True,
                return_tensors="pt").to("cuda")
        else:
            input_ids = Chat.tokenizer.apply_chat_template(
                self.messages_recent,
                tokenize=True,
                add_generation_prompt=True,
                return_tensors="pt").to("cuda")

        with torch.inference_mode():
            outputs = Chat.model.generate(
                **input_ids,
                max_new_tokens=150,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                top_k=40)

        prompt_length = input_ids["input_ids"].shape[-1]
        new_tokens = outputs[0][prompt_length:]
        # Decode only assistant reply
        reply = Chat.tokenizer.decode(new_tokens, skip_special_tokens=True)

        new_message = {"role": "assistant", "content": reply}
        self.append_new_message(new_message)
        self.check_to_create_summary()
        self.update_messages_recent()
        end = dt.datetime.now()
        if Chat.show_logs:
            print(f"Time to reply: {end - start}")
        return reply

    def export_chat_text(self):
        filename = "week-3/chatbot-cmd-class/chats/chat-" + \
            str(self.id) + ".txt"
        if not os.path.exists(filename):
            f = open(filename, "w", encoding="utf-8")
            for message in self.messages:
                if message["role"] == "user":
                    f.write(
                        f"{self.user_name} (User):\n{message['content']}\n\n")
                else:
                    f.write(f"{self.ai_name} (AI):\n{message['content']}\n\n")
            f.close()

    def check_to_create_summary(self):
        if self.use_summ:
            messages_summ_len = len(self.messages_summ)
            condition = messages_summ_len > 8
            if condition:
                message = self.messages_summ[messages_summ_len - 7]
                message_role = message["role"]
                message_text = message["content"]
                if message_role == "user":
                    if self.mode == "assistant":
                        genders = [self.user_gender, None]
                    elif self.mode == "roleplay":
                        genders = [self.user_gender, self.ai_gender]
                    names = [self.user_name, self.ai_name]
                else:
                    if self.mode == "assistant":
                        genders = [None, self.user_gender]
                    elif self.mode == "roleplay":
                        genders = [self.ai_gender, self.user_gender]
                    names = [self.ai_name, self.user_name]
                summary_text = self.summary.generate_summary(
                    message_text, names, genders)
                self.messages_summ[messages_summ_len -
                                   7]["content"] = summary_text

    def append_new_message(self, new_message):
        self.messages.append(new_message)
        if (self.use_summ):
            self.messages_summ.append(new_message)
