from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
import datetime as dt


class Summary():

    model_path = "./models/gemma-3-4b-it"

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16
    )

    print("CUDA available:", torch.cuda.is_available())
    print("CUDA version:", torch.version.cuda)

    tokenizer = AutoTokenizer.from_pretrained(model_path)

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        quantization_config=bnb_config,  # Apply quantization here
        device_map="auto"  # Auto will perfectly map it to your GPU now
    )

    show_logs = True

    def generate_summary(self, message_text, names=None, genders=None):
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
- Include important actions and dialogue.
- Do not use pronouns.
- No markdown. No prefixes. No new lines.
- Maximum 20 words.

Summary:"""  # Added "Summary:" to give the model a clear starting point

        inputs = Summary.tokenizer(prompt, return_tensors="pt").to("cuda")

        with torch.inference_mode():
            outputs = Summary.model.generate(
                **inputs,
                max_new_tokens=40,
                do_sample=False,
                repetition_penalty=1.1,  # Slightly increased to stop repetition
                eos_token_id=Summary.tokenizer.eos_token_id  # Stop at end of sentence
            )

        # Only decode the NEW tokens (ignoring the prompt)
        new_tokens = outputs[0][len(inputs["input_ids"][0]):]
        response = Summary.tokenizer.decode(
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
