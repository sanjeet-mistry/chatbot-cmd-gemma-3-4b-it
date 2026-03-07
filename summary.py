from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import datetime as dt


class Summary():
    model_path = "./models/gemma-3-4b-it"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        dtype=torch.bfloat16,
        device_map="auto"
    )
    show_logs = True

    def generate_summary(self, message_text):
        start = dt.datetime.now()
        prompt = f"""Summarize the following message in ONE short sentence.

Message: {message_text}

Write the summary in THIRD PERSON.

Speaker names:
user = Sandy
assistant = Lisa

Rules:
- The summary must use the speaker's name (Sandy or Lisa)
- Do NOT use I, me, my, or we
- One line only
- No explanations
- No quotes
- Only return summary and nothing else

Output format:
summary"""
        inputs = Summary.tokenizer(
            prompt, return_tensors="pt").to(Summary.model.device)

        outputs = Summary.model.generate(
            **inputs,
            max_new_tokens=30,
            do_sample=False
        )

        prompt_length = inputs["input_ids"].shape[1]
        new_tokens = outputs[0][prompt_length:]
        response = Summary.tokenizer.decode(
            new_tokens, skip_special_tokens=True)
        end = dt.datetime.now()
        if self.show_logs:
            print(response)
            print(f"Summary time: {end - start}")
        return response
