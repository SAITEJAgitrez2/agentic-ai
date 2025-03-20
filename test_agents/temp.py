import os
from dotenv import load_dotenv
from openai import OpenAI

# Load from .env
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # or "gpt-4"
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"},
    ]
)

print("✅ API Call Successful!")
print("Assistant:", response.choices[0].message.content)
