import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client using your API key from .env
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization="org-OdrHi0Qx9blJ3wmMVDcg4sos"  # replace with your org ID
)

models = client.models.list()
print([model.id for model in models])

# Test function
def test_openai_response():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What's the capital of Japan?"}
        ]
    )
    print(response.choices[0].message.content)

# Run the test
if __name__ == "__main__":
    test_openai_response()