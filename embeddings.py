from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

text="Eiffel tower is in Paris and is a famous landmark, it is 324 meters tall."

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=text
)   

print("Embedding:", response.data[0].embedding)      