from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),  
    base_url="https://api.x.ai/v1",
)

completion = client.chat.completions.create(
    model="grok-4-fast",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud"},
        {"role": "user", "content": "what is coding"}
    ]
)

print(completion.choices[0].message.content)
