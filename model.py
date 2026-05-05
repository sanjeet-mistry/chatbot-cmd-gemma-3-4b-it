from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch


class Model:

    models_folder = "./models/"
    cache = {}

    def __init__(self, model_name="gemma-3-4b-it"):

        if model_name not in Model.cache:

            model_path = Model.models_folder + model_name

            tokenizer = AutoTokenizer.from_pretrained(model_path)

            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                quantization_config=BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16
                ),
                device_map="cuda"
            )

            Model.cache[model_name] = {
                "tokenizer": tokenizer,
                "model": model
            }

        self.tokenizer = Model.cache[model_name]["tokenizer"]
        self.model = Model.cache[model_name]["model"]
