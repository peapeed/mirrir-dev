import json
import os
import sys

def extract_username(message):
    # A simple example: looks for a name mentioned in common phrases
    if "you can call me" in message.lower():
        return message.split("call me")[-1].strip(" .!").capitalize()
    if "my name is" in message.lower():
        return message.split("my name is")[-1].strip(" .!").capitalize()
    return None

def split_conversations(input_file, output_dir):
    with open(input_file, "r") as f:
        data = json.load(f)

    user_data = {}

    for message in data.get("conversation_examples", []):
        name = extract_username(message)
        if name:
            current_user = name.lower()
            if current_user not in user_data:
                user_data[current_user] = {
                    "name": current_user.capitalize(),
                    "tone": "casual",
                    "favorite_things": [],
                    "feel_better_methods": [],
                    "common_feelings": [],
                    "conversation_examples": []
                }
        if 'current_user' in locals():
            user_data[current_user]["conversation_examples"].append(message)

    os.makedirs(output_dir, exist_ok=True)

    for user, content in user_data.items():
        file_path = os.path.join(output_dir, f"{user}.json")
        with open(file_path, "w") as f:
            json.dump(content, f, indent=4)

    print(f"Done! Saved {len(user_data)} user files to '{output_dir}'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 split_memory.py <input_json> <output_dir>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    split_conversations(input_file, output_dir)