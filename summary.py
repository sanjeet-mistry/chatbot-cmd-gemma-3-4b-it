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

    show_logs = False

    def generate_summary(self, message_text, names, genders):
        start = dt.datetime.now()
        speaker_name = names[0]
        listener_name = names[1]
        speaker_gender = genders[0]
        listener_gender = genders[1]
        prompt = f"""Summarize the message in ONE short sentence in third person.

Message:
{message_text}

Speaker: {speaker_name} ({speaker_gender})
Listener: {listener_name} ({listener_gender})

Rules:
- Use the Speaker's & Listener's name.
- Include important actions and dialogue
- Keep greetings or questions if present
- Do not invent information
- Mention Listener name once.
- Never change genders.
- Do not use pronouns. Repeat names instead.
- No markdown. No prefixes. No new lines.
- Maximum 20 words
"""
        inputs = Summary.tokenizer(
            prompt, return_tensors="pt").to(Summary.model.device)

        outputs = Summary.model.generate(
            **inputs,
            max_new_tokens=30,
            temperature=0.2,
            repetition_penalty=1.1
        )

        prompt_length = inputs["input_ids"].shape[1]
        new_tokens = outputs[0][prompt_length:]
        response = Summary.tokenizer.decode(
            new_tokens, skip_special_tokens=True).strip().lstrip("---\n\n")
        end = dt.datetime.now()
        if self.show_logs:
            print(response)
            print(f"Summary time: {end - start}")
        return response
