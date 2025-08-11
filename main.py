from dotenv import load_dotenv
load_dotenv()
from mirrir.user_memory import get_chat_history, add_to_chat_history

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mirrir.onboarding import router as onboarding_router

# ─── FastAPI app ──────────────────────────────────────────────────────────
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allows all origins — for testing only
    allow_credentials=True,   # Important if you use cookies/auth
    allow_methods=["*"],      # Allow all HTTP methods
    allow_headers=["*"],      # Allow all headers
)

app.include_router(onboarding_router)

from mirrir.chat import respond_to_user         # <- single source of truth
from mirrir.user_memory import (
    load_user_memory, update_user_memory, save_user_memory
)
from mirrir.style_analysis import analyze_user_style

from typing import Optional

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    session_id: Optional[str] = None

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    session_id = req.session_id or "default"

    memory = load_user_memory(session_id)
    reply = respond_to_user(req.message, memory)

    # Update memory with the conversation turn
    update_user_memory(session_id, "conversation_examples", {"user": req.message, "mirrir": reply})

    return ChatResponse(reply=reply, session_id=session_id)


# ─── Optional CLI loop ────────────────────────────────────────────────────

def main():
    print("Welcome to Mirrir. You can exit anytime by saying 'goodbye'.")
    user_input_name = input("Before we begin... what should I call you? ").strip()
    user_id = user_input_name.lower().replace(" ", "_")

    memory = load_user_memory(user_id)

    #saving names
    if memory.get("name") in [None, ""]:
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
        memory = update_user_memory(user_id, "conversation_examples", {"user": prompt, "mirrir": response})

        # Generate response
        response = respond_to_user(prompt, memory)
        print(f"Mirrir: {response}")

        # After response.. Save updated memory
        memory = update_user_memory(user_id, "conversation_examples", {"user": prompt, "mirrir": response})
        save_user_memory(user_id, memory)
if __name__ == "__main__":
    main()