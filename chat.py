import os 
from dotenv import load_dotenv
from openai import OpenAI   

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# client = OpenAI()

result = client.chat.completions.create(
    # model="gpt-4",
    # model="codex-002",
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hey there"}
    ]
)

print(result.choices[0].message.content)
# print(result.choices)