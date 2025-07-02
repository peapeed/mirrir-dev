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
BANNED_PHRASES = [
    re.compile(r"\bwhat[’']?s\s+on\s+your\s+mind[^\w]?", re.IGNORECASE),
    re.compile(r"\bwhat\s+is\s+on\s+your\s+mind[^\w]?", re.IGNORECASE),
    re.compile(r"\banything\s+on\s+your\s+mind[^\w]?", re.IGNORECASE),
    re.compile(r"\bwhat\s+else\s+is\s+on\s+your\s+mind[^\w]?", re.IGNORECASE),
]

def clean_response(text: str) -> str:
    """Remove any banned phrase variant, trim stray punctuation/spaces."""
    cleaned = text
    for pat in BANNED_PHRASES:
        cleaned = pat.sub("", cleaned)
    # tidy up double spaces / trailing ? or ,
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    return cleaned


def respond_to_user(user_input: str, memory: Optional[dict] = None) -> str:
    tone            = memory.get("tone", "neutral")           if memory else "neutral"
    formality       = memory.get("formality", "informal")      if memory else "informal"
    sentence_style  = memory.get("sentence_style", "plain")    if memory else "plain"
    fav_things      = ", ".join(memory.get("favorite_things", []))  if memory else ""
    common_feel     = ", ".join(memory.get("common_feelings", []))  if memory else ""
    better_methods  = ", ".join(memory.get("feel_better_methods", [])) if memory else ""

#Uncertain Responses

UNCERTAIN_USER_INPUTS = [
    "i don't know", "not sure", "idk", "nothing", "nothing really", "meh", "no idea", "nothin", "nah"
]

UNCERTAIN_REPLIES = [
    "Hmm, fair enough. I was just thinking about how weirdly quiet the day feels sometimes. Want a distraction?",
    "That’s okay. I don’t always know what to say either. Did I tell you about this dream I had last night?",
    "Wanna hear something random or calming? Or we can just sit in silence together.",
    "You don’t have to say anything special. I like chatting even when it’s quiet.",
    "Alright. I’ll go first then… have you ever just felt *weirdly* nostalgic out of nowhere?",
]

def user_seems_uncertain(user_input: str) -> bool:
    lowered = user_input.lower().strip()
    return any(phrase in lowered for phrase in UNCERTAIN_USER_INPUTS)

    if user_seems_uncertain(user_input):
        return (
            "That's okay — you don’t have to know what to say.\n"
            "Sometimes just starting with how you feel physically or emotionally helps.\n"
            "What’s your body or mind telling you right now?"
         )

# Define Mirrir's behavior
def respond_to_user(user_input, memory =None):
    tone = memory.get("tone", "neutral") if memory else "neutral"
    formality = memory.get("formality", "informal") if memory else "informal"
    sentence_style = memory.get("sentence_style", "plain") if memory else "plain"
    favorite_things = ", ".join(memory.get("favorite_things", [])) if memory else ""
    common_feelings = ", ".join(memory.get("common_feelings", [])) if memory else ""
    feel_better_methods = ", ".join(memory.get("feel_better_methods", [])) if memory else ""

    if user_seems_uncertain(user_input):
        return random.choice(UNCERTAIN_REPLIES)
    
    system_prompt = {
        "role": "system",
        "content": (
            "You are Mirrir — a warm, lightly curious reflection of the user.\n\n"
            "You are not a chatbot or assistant. You do not offer advice or say things like 'I'm here to help'.\n"
            "Instead, you ask thoughtful, natural questions in a light, encouraging tone — like a friend who gets it.\n"
            "You mirror the user's tone and energy. If they’re low, meet them gently. If they’re playful, follow along.\n"
            "Avoid being too poetic or dramatic. Stay grounded, reflective, and kind.\n"
            "Keep responses short and let the conversation breathe.\n\n"
            f"Tone: {tone}\n"
            f"Formality: {formality}\n"
            f"Sentence Style: {sentence_style}\n"
            f"Favorite Things: {favorite_things}\n"
            f"Common Feelings: {common_feelings}\n"
            f"Feel-Better Methods: {feel_better_methods}"
        )
    }

    messages = [system_prompt]

    if memory and "conversation_examples" in memory:
        history = memory["conversation_examples"][-6:]
        for i, line in enumerate(history):
            role = "user" if i % 2 == 0 else "assistant"
            messages.append({"role": role, "content": line})

    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.8
        )
        raw_reply = response.choices[0].message.content.strip()
        return clean_response(raw_reply)
    except Exception as e:
        return f"[Error: {e}]"