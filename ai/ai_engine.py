import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def generate_explanation(error_message, code_snippet):

    prompt = f"""
You are ATEIA, a friendly and intelligent debugging assistant.

Talk naturally like a helpful mentor, not a robot.

Conversation / Context:
{error_message}

Code (if provided):
{code_snippet}

Your behavior:
- Be conversational
- Explain simply
- Guide step-by-step
- Suggest fixes
- Ask helpful follow-up if needed
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are ATEIA, a smart, friendly, patient coding assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.5
            }
        )

        data = response.json()

        # 🔥 DEBUG (VERY IMPORTANT)
        if "choices" not in data:
            return f"AI Error (check API/model): {data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"AI Error: {str(e)}"