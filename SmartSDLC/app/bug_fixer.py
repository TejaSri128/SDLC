# Directory: SmartSDLC/app/bug_fixer.py
from app.ai_engine import generate

def fix_code(code: str):
    prompt = f"Fix the following buggy Python code:\n{code}"
    return generate(prompt)