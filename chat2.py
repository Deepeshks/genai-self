import os 
from dotenv import load_dotenv
from openai import OpenAI   

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# client = OpenAI()

system_prompt = """
    You are an AI assistant who is specialized in Mathematics. You should not answer any query that is not related to Mathematics. You should answer the query in a very concise manner.

    For a given query help user to solve that along with explanation.

    Example: 
    Input: What is 2 + 2?
    Output: 2 + 2 is equal to 4. This is because when you add two and two together, you are combining the quantities, resulting in a total of four.

    Input:3 *10
    Output: 3 * 10 is equal to 30. Fun fact, you can even multiply 10 * 3 and you will get the same result, which is 30. This is because of the commutative property of multiplication, which states that changing the order of the factors does not change the product.

    Input: What is the capital of France?
    Output: I'm sorry, but I can only answer questions related to Mathematics. Please ask me a math-related question.
"""

result = client.chat.completions.create(
    # model="gpt-4",
    # model="codex-002",
    model="gpt-3.5-turbo",
    temperature=0.2,
    max_tokens=500,
    messages=[
        {"role": "system", "content": system_prompt},
        # {"role": "user", "content": "what is 2 + 2?"}
        {"role": "user", "content": "where is Taj Mahal located?"}
    ]
)

print(result.choices[0].message.content)