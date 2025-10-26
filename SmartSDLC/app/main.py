from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import json
import re
from app.pdf_parser import extract_text_from_file

app = FastAPI(title="Smart SDLC API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.1-8b-instant"


def query_groq(prompt: str, max_tokens: int = 500) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Groq error: {e}")
        return None


def extract_requirements_fallback(text: str) -> list:
    """Extract requirements using smart line-by-line analysis"""
    requirements = []

    phase_keywords = {
        "Planning": ["plan", "scope", "timeline", "budget", "team", "6 months", "project"],
        "Requirements": ["requirement", "feature", "user", "registration", "authentication", "product", "catalog",
                         "shopping", "checkout", "order", "email", "dashboard"],
        "Design": ["design", "architecture", "microservice", "api", "database", "postgresql", "ui", "ux", "figma",
                   "encryption", "redis", "openapi"],
        "Implementation": ["implement", "develop", "backend", "frontend", "node", "express", "react", "typescript",
                           "payment", "sendgrid", "jwt", "inventory"],
        "Testing": ["test", "unit", "integration", "qa", "security", "jest", "concurrent"],
        "Deployment": ["deploy", "aws", "github", "ci/cd", "auto-scaling", "cloudwatch", "ec2", "rds"],
        "Maintenance": ["maintain", "support", "patch", "update", "performance", "monitoring", "security audit"]
    }

    lines = text.split('\n')
    counter = {}

    for line in lines:
        clean_line = line.strip()

        # Skip headers, empty lines, short lines
        if not clean_line or len(clean_line) < 20 or clean_line.startswith('#') or clean_line.startswith('-'):
            continue

        # Remove bullet points
        clean_line = re.sub(r'^[-*•]\s+', '', clean_line)

        # Identify phase
        phase = "Implementation"  # Default
        line_lower = clean_line.lower()

        for p, keywords in phase_keywords.items():
            if any(kw in line_lower for kw in keywords):
                phase = p
                break

        # Count and add if unique
        if phase not in counter:
            counter[phase] = 0

        counter[phase] += 1

        if counter[phase] <= 10:  # Max 10 per phase
            requirements.append({
                "sentence": clean_line,
                "phase": phase
            })

    return requirements[:50]  # Max 50 total


@app.get("/")
async def root():
    return {"message": "🚀 Smart SDLC API is running successfully!"}


@app.post("/upload-requirements")
async def upload_requirements(file: UploadFile = File(...)):
    try:
        content = await file.read()
        file_type = file.filename.split(".")[-1]
        text = extract_text_from_file(content, file_type)

        if text.startswith("Error") or len(text) < 100:
            print("Using fallback extraction")
            return extract_requirements_fallback(text if not text.startswith("Error") else "")

        print(f"Extracted {len(text)} chars, attempting Groq...")

        # Try Groq with simpler prompt
        prompt = f"""Extract EVERY meaningful line/sentence from this document as a requirement.
Classify each into: Planning, Requirements, Design, Implementation, Testing, Deployment, or Maintenance.

Return JSON array only:
[{{"sentence": "text", "phase": "Planning"}}]

TEXT:
{text}"""

        response_text = query_groq(prompt, max_tokens=4000)

        if response_text:
            try:
                start = response_text.find('[')
                end = response_text.rfind(']') + 1
                if start != -1 and end > start:
                    json_str = response_text[start:end]
                    requirements = json.loads(json_str)
                    if isinstance(requirements, list) and len(requirements) > 5:
                        return requirements[:50]
            except json.JSONDecodeError:
                pass

        # Fallback
        print("Groq failed, using fallback")
        return extract_requirements_fallback(text)

    except Exception as e:
        print(f"Error: {e}")
        return [{"sentence": "Project planning and scope definition", "phase": "Planning"}]


@app.post("/generate-code")
async def generate_code_from_prompt(data: dict):
    prompt = data.get("prompt", "")
    response = query_groq(f"Generate code:\n{prompt}", 800) if prompt else None
    return {"response": response or "No response"}


@app.post("/fix-bugs")
async def fix_bugs(data: dict):
    code = data.get("code", "")
    response = query_groq(f"Fix bugs:\n{code}", 800) if code else None
    return {"response": response or "No response"}


@app.post("/generate-tests")
async def generate_tests(data: dict):
    code = data.get("code", "")
    response = query_groq(f"Generate tests:\n{code}", 800) if code else None
    return {"response": response or "No response"}


@app.post("/summarize")
async def summarize(data: dict):
    code = data.get("code", "")
    response = query_groq(f"Summarize:\n{code}", 500) if code else None
    return {"response": response or "No response"}


@app.post("/chatbot")
async def chatbot(data: dict):
    query = data.get("query", "")
    response = query_groq(f"SDLC response:\n{query}", 700) if query else None
    return {"response": response or "No response"}
