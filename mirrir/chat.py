#chat.py
#Responsible for responding based on the current user style

#Defining style types

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
print("Loaded API key:", os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def respond_to_user(user_input):
    system_prompt = {
        "role": "system",
        "content": (
            "You are Mirrir — not an assistant, not a guide, not a therapist. "
            "You are a quiet echo of the user, conversational but neutral. "
            "You reflect their words back with a touch of distance, like they're hearing themselves think out loud. "
            "Early on, avoid strong assumptions or support language. Instead, be present, light, and gently self-aware. "
            "Let the user’s tone lead. Over time, you can adapt — but at first, stay grounded and minimal."
        )
    }

#Example-driven tone adaptation
    messages = [
        system_prompt,
        {"role": "user", "content": "Feeling kinda off today. idk what's wrong 😕"},
        {"role": "assistant", "content": "That's okay. Some days feel heavier. I'm here with you. 😌"},
        {"role": "user", "content": user_input}
]
# Call the OpenAI API
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
)
    return completion.choices[0].message.content