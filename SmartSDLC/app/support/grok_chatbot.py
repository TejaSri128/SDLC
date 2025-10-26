import requests

# Use the provided Grok API key directly here for quick testing
GROQ_API_KEY = "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"

def query_grok_chatbot(prompt: str) -> str:
    if not GROQ_API_KEY:
        return "⚠️ Groq API key is missing."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100,
        "temperature": 0.5
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Groq API error: {str(e)}"
