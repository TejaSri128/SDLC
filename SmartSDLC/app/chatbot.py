# Directory: SmartSDLC/app/chatbot.py
from app.ai_engine import generate

def chat_with_sdlc_bot(query: str):
    prompt = f"Answer the following SDLC question like a chatbot assistant:\n{query}"
    return generate(prompt)
