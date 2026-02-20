import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY",""),
)

def Chat(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=[
            {
            "role": "user",
            "content": prompt + " Keep your response short, concise, and to the point. Maximum 2-3 sentences. Dont add any bold or italic typestyle."
            }
        ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"
