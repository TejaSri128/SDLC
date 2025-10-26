# Directory: SmartSDLC/app/summarizer.py
from app.ai_engine import generate

def summarize_code(code: str):
    prompt = f"Summarize the purpose of this Python code:\n{code}"
    return generate(prompt)