import torch
import datetime as dt
from core.model import Model


class Summary():

    show_logs = False

    def __init__(self, model_name=None):
        if model_name == None:
            self.model = Model()
        else:
            self.model = Model(model_name)

    def generate_summary(self, message_text, names=None, genders=None):
        start = dt.datetime.now()

        speaker_name = names[0]
        listener_name = names[1]
        speaker_gender = genders[0]
        listener_gender = genders[1]

        prompt = f"""Summarize the message in ONE short sentence in third person.

Message:
{message_text}

Speaker: {speaker_name}{f" ({speaker_gender})" if speaker_gender else ""}
Listener: {listener_name}{f" ({listener_gender})" if listener_gender else ""}

Rules:
- Use the Speaker's & Listener's name.
- Include important actions and dialogue.
- Do not use pronouns.
- No markdown. No prefixes. No new lines.
- Maximum 20 words.

Summary:"""  # Added "Summary:" to give the model a clear starting point

        inputs = self.model.tokenizer(
            prompt, return_tensors="pt").to("cuda")

        with torch.inference_mode():
            outputs = self.model.model_info.generate(
                **inputs,
                max_new_tokens=40,
                do_sample=False,
                repetition_penalty=1.1,  # Slightly increased to stop repetition
                eos_token_id=self.model.tokenizer.eos_token_id  # Stop at end of sentence
            )

        # Only decode the NEW tokens (ignoring the prompt)
        new_tokens = outputs[0][len(inputs["input_ids"][0]):]
        response = self.model.tokenizer.decode(
            new_tokens, skip_special_tokens=True).strip()

        # Final cleanup: Grab only the first line and remove any trailing dashes/rules
        response = response.split('\n')[0].split('---')[0].strip()
        # Remove any leading "- " if the model tried to make a list
        if response.startswith("- "):
            response = response[2:]

        end = dt.datetime.now()
        if self.show_logs:
            print(f"Summary: {response}")
            print(f"Summary time: {end - start}")

        return response
