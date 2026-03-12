import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


# client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
client = genai.Client(api_key="AIzaSyDyWOlhAc_RrRC18owOZQEYLvexMF0EeqQ")


response = client.models.generate_content(
    model='gemini-2.5-flash', contents='Why is the sky blue?'
)
print(response.text)