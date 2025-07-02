from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from mirrir.chat import respond_to_user         # <- single source of truth
from mirrir.user_memory import (
    load_user_memory, update_user_memory, save_user_memory
)
from mirrir.style_analysis import analyze_user_style

# ─── FastAPI app ──────────────────────────────────────────────────────────
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # DEV ONLY – lock down in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

from typing import Optional

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    session_id: Optional[str] = None

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    reply = respond_to_user(req.message)          # your core logic
    return ChatResponse(reply=reply, session_id=req.session_id)


# ─── Optional CLI loop ────────────────────────────────────────────────────

def main():
    print("Welcome to Mirrir. You can exit anytime by saying 'goodbye'.")
    user_input_name = input("Before we begin... what should I call you? ").strip()
    user_id = user_input_name.lower().replace(" ", "_")

    memory = load_user_memory(user_id)

    #saving names
    if not memory.get("name"):
        memory["name"] = user_input_name
        save_user_memory(user_id, memory)
        
    while True:
        prompt = input("You: ").strip()
        if prompt.lower() in ["quit", "exit", "goodbye"]:
            print("Mirrir: goodbye")
            break

        if not prompt:
            continue  # Skip empty input

        #using style detection analysis
        style_data = analyze_user_style(prompt)

        if style_data:
            for key, value in style_data.items():
                update_user_memory(user_id, key, value)

        # Save to conversation history
        memory = update_user_memory(user_id, "conversation_examples", prompt)

        # Generate response
        response = respond_to_user(prompt, memory)
        print(f"Mirrir: {response}")

        # After response.. Save updated memory
        memory = update_user_memory(user_id, "conversation_examples", response)
        save_user_memory(user_id, memory)

if __name__ == "__main__":
    main()