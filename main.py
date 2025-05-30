from mirrir.chat import respond_to_user
from mirrir.persona import get_default_persona

def main():
    print("Say hello to yourself.")
    persona = get_default_persona()
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        response = respond_to_user(user_input, persona)
        print("Mirrir:", response)

if __name__ == "__main__":
    main()