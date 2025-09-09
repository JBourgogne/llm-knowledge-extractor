# test_openai.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key: {api_key[:7]}..." if api_key else "No API key found")

try:
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello"}],
        max_tokens=10
    )
    print("OpenAI works!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"OpenAI failed: {e}")