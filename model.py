from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch


class Model():
    def __init__(self, model_path="./models/gemma-3-4b-it"):
        self.model_path = model_path
        self.bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model_info = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            quantization_config=self.bnb_config,  # Apply quantization here
            device_map="cuda"
        )
