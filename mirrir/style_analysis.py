# mirrir/style_analysis.py

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def analyze_user_style(user_input):
    system_message = {
        "role": "system",
        "content": (
            "You're a writing style analyst. Given a single user message, "
            "extract the tone (e.g. casual, serious, confused), "
            "formality level (formal/informal), "
            "and a short description of the sentence style (e.g. short phrases, run-on, emojis, etc). "
            "Respond only in a valid JSON object with keys: tone, formality, sentence_style."
        )
    }

    messages = [
        system_message,
        {"role": "user", "content": user_input}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.3
        )
        content = response.choices[0].message.content.strip()
        return eval(content)  # Convert string dict to real dict (alternatively, use `json.loads`)
    except Exception as e:
        print(f"[Style analysis error: {e}]")
        return {}