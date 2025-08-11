import json
import os

user_data = {
    "name": "TestUser",
    "tone": "friendly",
    "favorite_things": ["coffee", "reading"],
    "feel_better_methods": ["nap", "walk"],
    "common_feelings": ["happy", "thoughtful"],
    "conversation_examples": ["Hello!", "How are you today?"]
}

# Make sure user_data directory exists (adjust path if needed)
os.makedirs("user_data", exist_ok=True)

# Save the user data as a JSON file
with open("user_data/testuser.json", "w") as f:
    json.dump(user_data, f, indent=4)

print("Test user JSON file created in user_data folder.")