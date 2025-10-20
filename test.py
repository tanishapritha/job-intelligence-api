import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Initialize OpenAI/OpenRouter client
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"  # optional, for OpenRouter
)

# Test simple text completion
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {"role": "user", "content": [{"type": "text", "text": "Hello! Can you test my API key?"}]}
    ]
)

print(response.choices[0].message.content)
