from dotenv import load_dotenv
load_dotenv()
from mirrir.chat import respond_to_user
from mirrir.user_memory import (
    load_user_memory,
    update_user_memory,
    save_user_memory
)

def main():
    print("Welcome to Mirrir. You can exit anytime by saying 'goodbye'.")
    user_id = input("Before we begin... what should I call you? ").strip().lower().replace(" ", "_")
    memory = load_user_memory(user_id)

    while True:
        prompt = input("You: ").strip()
        if prompt.lower() in ["quit", "exit", "goodbye"]:
            print("Mirrir: goodbye")
            break

        if not prompt:
            continue  # Skip empty input


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