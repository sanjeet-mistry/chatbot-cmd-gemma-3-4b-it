from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import copy
import datetime as dt
import os
import random


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
    show_logs = True

    def __init__(self, user_name, ai_name):
        self.id = random.randint(10000000, 99999999)
        self.user_name = user_name
        self.ai_name = ai_name
        self.messages_initial = [
            {
                "role": "user",
                "content": "Answer in under 100 words.\nKeep answers short and concise.\nYou are Lisa and are 21.\nYou are a Twitch streamer.\nYou are bold, playful and bratty.\nYou are my friend.\nI am Sandy and I am 27.\nI work as a software engineer."
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
        self.update_messages_recent()

    def update_messages_recent(self):
        if (len(self.messages) > Chat.messages_recent_size):
            if len(self.messages) % 2 == 0:
                self.messages_recent = self.messages_initial + \
                    copy.deepcopy(
                        self.messages[-(Chat.messages_recent_size - 3):])
            else:
                self.messages_recent = self.messages_initial + \
                    copy.deepcopy(
                        self.messages[-(Chat.messages_recent_size - 2):])
        else:
            self.messages_recent = self.messages

    def generate_output(self, message_text):
        start = dt.datetime.now()
        new_message = {"role": "user", "content": message_text}
        self.messages.append(new_message)
        self.update_messages_recent()
        self.summarize_message(new_message)
        if Chat.show_logs:
            print(len(self.messages_recent))

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
        self.update_messages_recent()
        end = dt.datetime.now()
        if Chat.show_logs:
            print(f"Time to reply: {end - start}")
        self.summarize_message(new_message)
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

    def summarize_message(self, message=None):
        prompt = f"""Compress the meaning of the message into a short summary.

        Message role: {message["role"]}
        Message text: {message["content"]}

        Output exactly in this format:
        {message["role"]}|||summary

        Rules:
        - One line only
        - No explanations
        - No quotes
        - Only return output and nothing else
        """
        inputs = Chat.tokenizer(
            prompt, return_tensors="pt").to(Chat.model.device)

        outputs = Chat.model.generate(
            **inputs,
            max_new_tokens=50,
            temperature=0.2
        )

        prompt_length = inputs["input_ids"].shape[1]
        new_tokens = outputs[0][prompt_length:]
        response = Chat.tokenizer.decode(new_tokens, skip_special_tokens=True)
        response = response.split("\n")[0].strip()
        print(response)
        # self.messages_summ.append(response)
