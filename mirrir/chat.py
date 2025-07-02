# chat.py
# Responsible for generating grounded, reflective responses that match the user's tone

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# Define Mirrir's behavior
def respond_to_user(user_input, memory =None):
    tone = memory.get("tone", "neutral") if memory else "neutral"
    formality = memory.get("formality", "informal") if memory else "informal"
    sentence_style = memory.get("sentence_style", "plain") if memory else "plain"
    favorite_things = ", ".join(memory.get("favorite_things", [])) if memory else ""
    common_feelings = ", ".join(memory.get("common_feelings", [])) if memory else ""
    feel_better_methods = ", ".join(memory.get("feel_better_methods", [])) if memory else ""

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
            temperature=0.6
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error: {e}]"