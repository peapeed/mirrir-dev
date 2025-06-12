import json
import os

MEMORY_DIR = "user_data"

# Ensure the user data directory exists
if not os.path.exists(MEMORY_DIR):
    os.makedirs(MEMORY_DIR)

def get_user_memory_path(user_id):
    return os.path.join(MEMORY_DIR, f"{user_id}.json")


def load_user_memory(user_id):
    path = get_user_memory_path(user_id)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    else:
        return {
            "name": None,
            "tone": "",
            "favorite_things": [],
            "feel_better_methods": [],
            "common_feelings": [],
            "conversation_examples": []  # optional: keep snippets of how user talks
        }


def save_user_memory(user_id, memory):
    path = get_user_memory_path(user_id)
    with open(path, "w") as f:
        json.dump(memory, f, indent=4)


def update_user_memory(user_id, key, value):
    memory = load_user_memory(user_id)
    if key in memory:
        if isinstance(memory[key], list) and value not in memory[key]:
            memory[key].append(value)
        elif not isinstance(memory[key], list):
            memory[key] = value
        save_user_memory(user_id, memory)
    return memory