from mirrir.chat import respond_to_user

def main():
    print("Say hello to yourself.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        response = respond_to_user(user_input)
        print("Mirrir:", response)

if __name__ == "__main__":
    main()