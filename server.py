from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import os

app = FastAPI()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

class Command(BaseModel):
    text: str

@app.post("/parse")
def parse_command(cmd: Command):
    prompt = f"""
You are an OS command parser.
Return ONLY JSON.

User command: "{cmd.text}"

Allowed intents:
- open_web (gmail, youtube, google)
- open_app (chrome, vscode)
- exit

JSON format:
{{"intent":"...", "target":"..."}}
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
        }
    )

    content = r.json()["choices"][0]["message"]["content"]
    return json.loads(content)
