from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
import json

app = FastAPI()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

class Command(BaseModel):
    text: str


@app.get("/")
def root():
    return {"status": "Warmwind AI brain running"}


@app.post("/parse")
def parse_command(cmd: Command):

    prompt = f"""
You are an OS command parser.

Return ONLY valid JSON.
No explanation. No text.

User command: "{cmd.text}"

Rules:
- If user wants to open a website, return FULL URL
- Always include https://

JSON format:
{{
  "intent": "open_web",
  "target": "https://example.com"
}}
"""

    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0
        },
        timeout=15
    )

    content = r.json()["choices"][0]["message"]["content"]
    return json.loads(content)
