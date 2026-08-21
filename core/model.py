from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch


class Model:

    models_folder = "./models/"
    cache = {}

    def __init__(self, model_name="qwen-3.5-4b"):

        if model_name not in Model.cache:

            model_path = Model.models_folder + model_name

            tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                trust_remote_code=True
            )

            model_info = AutoModelForCausalLM.from_pretrained(
                model_path,
                quantization_config=BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.bfloat16  # Changed to bfloat16 for Qwen stability
                ),
                device_map="cuda",
                trust_remote_code=True
            )

            Model.cache[model_name] = {
                "tokenizer": tokenizer,
                "model": model_info
            }

        self.tokenizer = Model.cache[model_name]["tokenizer"]
        self.model_info = Model.cache[model_name]["model"]
