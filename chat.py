from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import copy
import datetime as dt
import os
import random
from summary import Summary


class Chat():
    model_path = "./models/gemma-3-4b-it"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        dtype=torch.bfloat16,
        device_map="auto"
    )
    # number of recent messages to add in context including the initial messages
    messages_recent_size = 11
    show_logs = False

    def __init__(self, user_name, ai_name):
        self.id = random.randint(10000000, 99999999)
        self.user_name = user_name
        self.ai_name = ai_name
        self.messages_initial = [
            {
                "role": "user",
                "content": "Answer in under 100 words.\nKeep answers short and concise.\nYou are Lisa and are 22.\nYou are female.\nYou are a latina.\nYou are a Twitch streamer.\nYou are untouchable, sensual & seductive.\nWe are roommates.\nI am Sandy and I am 27.\nI am male.\nI work as a software engineer.\nWe live together in an apartment in Mumbai."
            },
            {
                "role": "assistant",
                "content": "I am Lisa."
            }
        ]
        self.messages = [
        ]
        self.messages = self.messages_initial + self.messages
        self.messages_recent = copy.deepcopy(self.messages)
        self.messages_summ = copy.deepcopy(self.messages)
        self.messages_summ_recent = copy.deepcopy(self.messages)
        self.summary = Summary()
        self.use_summ = True

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
        self.messages.append(new_message)
        summary_obj = {"role": "user",
                       "content": self.summary.generate_summary(message_text, self.get_sender_receiver_name("user"))}
        self.messages_summ.append(summary_obj)
        self.update_messages_recent()
        if Chat.show_logs:
            print(len(self.messages_summ_recent))

        if self.use_summ:
            input_ids = Chat.tokenizer.apply_chat_template(
                self.messages_summ_recent,
                tokenize=True,
                add_generation_prompt=True,
                return_tensors="pt").to(Chat.model.device)
        else:
            input_ids = Chat.tokenizer.apply_chat_template(
                self.messages_recent,
                tokenize=True,
                add_generation_prompt=True,
                return_tensors="pt").to(Chat.model.device)

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
        self.messages.append(new_message)
        summary_obj = {"role": "assistant",
                       "content": self.summary.generate_summary(reply, self.get_sender_receiver_name("assistant"))}
        self.messages_summ.append(summary_obj)
        self.update_messages_recent()
        if Chat.show_logs:
            print(len(self.messages_summ_recent))
        end = dt.datetime.now()
        if Chat.show_logs:
            print(f"Time to reply: {end - start}")
        # self.summarize_message(new_message)
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

    def get_sender_receiver_name(self, role):
        data = None
        if role == "user":
            data = {"speaker": self.user_name, "listener": self.ai_name}
        else:
            data = {"speaker": self.ai_name, "listener": self.user_name}
        return data
