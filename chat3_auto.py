import os 
from dotenv import load_dotenv
from openai import OpenAI 
import json  

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

system_prompt = """
    You are an AI assistant who is expert in breaking down complex problems and then resolve user query.

    For the given user input, analyse the input and break down the problem step by step.
    Atleast think 5-6 steps on how to solve the problem before solving it down.

    The steps are , you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well.before giving final result.

    Follow the steps in sequence that is analyse, think, output, validate and finally result.

    Rules:
    1. Follow the strict JSON output as per output schema.
    2. Always perform 1 step at a time and wait for next input.
    3. Carefully analyze the user query.

    output format:
    {{step:"string", content:"string"}}

    Example:
    Input: what is 2 + 2?
    Output:{{step:"analyse", content:"Alright! the user is interested in Maths query and he is asking a basic arithmatic operation."}}
    Output:{{step:"think", content:"To perform the addition, I must go from left to right and add all the operands."}}
    Output:{{step:"output", content:"4"}}
    Output:{{step:"validate", content:"Seems like 4 is correct answer for 2 + 2."}}
    Output:{{step:"result", content:"2 + 2 = 4 and that is calculated by adding all numbers."}}
"""


messages = [
    {"role": "system", "content": system_prompt}
]

query = input("> ")
messages.append({"role": "user", "content": query})

while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages
    ) 

    parsed_response  = json.loads(response.choices[0].message.content)
    messages.append({"role": "assistant", "content": json.dumps(parsed_response)})
    print(f"{parsed_response['step']} : {parsed_response['content']}")

    if parsed_response["step"] == "result":
        break;

# result = client.chat.completions.create(
#     # model="gpt-4",
#     # model="codex-002",
#     model="gpt-3.5-turbo",
#     temperature=0.2,
#     max_tokens=500,
#     response_format={"type": "json_object"},
#     messages=[
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": "what is 3 + 4 * 5?"},
        
        
#         {"role": "assistant", "content": json.dumps({"step": "analyse","content": "The user is asking a math query involving addition and multiplication operations"})},
#         {"role": "assistant", "content": json.dumps({"step": "think", "content": "To solve the expression 3 + 4 * 5, we need to follow the order of operations (PEMDAS/BODMAS) which states that multiplication and division should be performed before addition and subtraction."})},
#     ]
# )

# print(result.choices[0].message.content)