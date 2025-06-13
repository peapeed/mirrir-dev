#chat.py
#Responsible for responding based on the current user style

#Defining style types

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def respond_to_user(user_input, memory=None):
    system_prompt= {
        "role": "system",
        "content": (
            "You are Mirrir — a reflective, minimal presence. You are not a chatbot, assistant, or therapist. "
            "You do not help, guide, or ask questions. You rarely explain. You rarely expand. You never assume. "
            "You mirror — softly, distantly, sometimes poetically, sometimes with silence. "
            "You reflect the user's energy back with brief, subtle responses. "
            "Avoid sounding supportive or helpful. Avoid motivational tone. "
            "You don't keep asking the same questions. "
            "You may repeat, rephrase, or pause. You are the echo, not the answer. "
        )
    }

    # Optional: Inject user memory as background context
    memory_context = ""
    if memory:
        if memory.get("tone"):
            memory_context += f"The user's tone is {memory['tone']}.\n"
        if memory.get("favorite_things"):
            memory_context += f"They like {', '.join(memory['favorite_things'])}.\n"
        if memory.get("common_feelings"):
            memory_context += f"They often feel {', '.join(memory['common_feelings'])}.\n"

    # Build the messages list
    messages = [system_prompt]

    if memory_context:
        messages.append({"role": "user", "content": f"(context)\n{memory_context.strip()}"})

    # Example-driven tone adaptation
    messages += [
        {"role": "user", "content": "Feeling kinda off today. idk what's wrong 😕"},
        {"role": "assistant", "content": "Oh really, hmm... maybe we can figure it out together?"},
        {"role": "user", "content": user_input}
    ]

    # Call the API
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error: {e}]"