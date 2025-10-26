# Directory: SmartSDLC/app/test_case_generator.py
from app.ai_engine import generate

def generate_test_cases(code: str):
    prompt = f"Generate pytest test cases for the following function:\n{code}"
    return generate(prompt)
