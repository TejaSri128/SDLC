from app.ai_engine import generate

def generate_code(prompt: str):
    code_prompt = f"Write Python code for the following requirement:\n{prompt}"
    return generate(code_prompt)


# Directory: SmartSDLC/app/bug_fixer.py
from app.ai_engine import generate

def fix_code(code: str):
    prompt = f"Fix the following buggy Python code:\n{code}"
    return generate(prompt)
