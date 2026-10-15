from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch


class Model:

    models_folder = "./models/"
    cache = {}

    def __init__(self, model_info):

        if model_info["name"] not in Model.cache:

            self.model_info = model_info
            self.model_name = model_info["name"]

            model_path = Model.models_folder + self.model_name

            tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                trust_remote_code=True
            )

            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                quantization_config=BitsAndBytesConfig(
                    load_in_4bit=True,
                    # Changed to bfloat16 for Qwen stability
                    bnb_4bit_compute_dtype=torch.bfloat16 if self.model_info[
                        "family"] == "qwen" else torch.float16
                ),
                device_map="cuda",
                trust_remote_code=True
            )

            Model.cache[self.model_name] = {
                "tokenizer": tokenizer,
                "model": model
            }

        self.tokenizer = Model.cache[self.model_name]["tokenizer"]
        self.model = Model.cache[self.model_name]["model"]
