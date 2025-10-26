import os
from dotenv import load_dotenv
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import torch

load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HF_TOKEN")

# Authenticate securely
login(HUGGINGFACE_TOKEN)

model_name = "ibm-granite/granite-3.3-2b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

def generate(prompt: str, max_tokens: int = 300):
    return generator(prompt, max_new_tokens=max_tokens)[0]['generated_text']
