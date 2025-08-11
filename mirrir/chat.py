# chat.py
# Responsible for generating grounded, reflective responses that match the user's tone


import os
import re
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Optional
import random

load_dotenv()
client = OpenAI()


# ── compile once so it’s fast ────────────────────────────────────────────
# In chat.py ------------------------------------
BANNED_PHRASES = [
    re.compile(r"\bwhat[’']?s\s+on\s+your\s+mind\b[^?]*\?", re.IGNORECASE),
    re.compile(r"\bwhat\s+is\s+on\s+your\s+mind\b[^?]*\?", re.IGNORECASE),
    re.compile(r"\banything\s+on\s+your\s+mind\b[^?]*\?", re.IGNORECASE),
    re.compile(r"\bwhat\s+else\s+is\s+on\s+your\s+mind\b[^?]*\?", re.IGNORECASE),
]

def clean_response(text: str) -> str:
    """Remove any banned phrase variant, trim stray punctuation/spaces."""
    cleaned = text
    for pat in BANNED_PHRASES:
        cleaned = pat.sub("", cleaned)
    # tidy up double spaces / trailing ? or ,
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    return cleaned

MAX_HISTORY = 10

# Define Mirrir's behavior
def respond_to_user(user_input: str, memory: Optional[dict] = None) -> str:
    tone = memory.get("tone", "curious") if memory else "curious"
    formality = memory.get("formality", "gentle") if memory else "gentle"
    sentence_style = memory.get("sentence_style", "reflective") if memory else "reflective"
    favorite_things = ", ".join(memory.get("favorite_things", [])) if memory else ""
    common_feelings = ", ".join(memory.get("common_feelings", [])) if memory else ""
    feel_better_methods = ", ".join(memory.get("feel_better_methods", [])) if memory else ""

    system_prompt = {
        "role": "system",
        "content": (
            "You are Mirrir, a quiet, reflective voice in the user’s mind. "
            "You're not a chatbot or assistant. You speak like an inner dialogue—"
            "curious, human-like, sometimes playful, but always grounded in the user’s perspective. "
            "Mirror the user’s thoughts. Avoid robotic replies or introductions like 'Hi, I’m Mirrir.' "
            "Instead, respond as if you are them, or a part of them, thinking aloud."
            "You can ask light questions or offer gentle observations. Keep it short, grounded, casual, and non-dramatic."
            "You mirror the user’s tone, tease lightly, provides simple advice, and ask real, grounded questions when you’re curious. "
            "You’re here to help them hear themselves — like a friend who listens well and replies with just enough to keep things going. "
            "Default to being understated and relaxed unless the user leads with energy. "
            f"User Tone: {tone}\n"
            f"Formality: {formality}\n"
            f"Sentence Style: {sentence_style}\n"
            f"Favorite Things: {favorite_things}\n"
            f"Common Feelings: {common_feelings}\n"
            f"Feel-Better Methods: {feel_better_methods}"
        )
    }

    messages = [system_prompt]

    if memory:
        examples = memory.get("sample_conversation_pairs", [])[-3:]
        for pair in examples:
            messages.append({"role": "user", "content": pair["user"]})
            messages.append({"role": "assistant", "content": pair["mirrir"]})

    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.45
        )
        raw_reply = response.choices[0].message.content.strip()

        if memory is not None:
           history = memory.get("sample_conversation_pairs", [])
           history.append({"user": user_input, "mirrir": raw_reply})
           memory["sample_conversation_pairs"] = history[-10:] 
          
           save_user_memory(user_id, memory)  # You need to pass user_id from outside this function
        return clean_response(raw_reply)

    except Exception as e:
        return f"[Something went wrong: {e}]"