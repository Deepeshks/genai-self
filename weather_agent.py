import os
import requests 
from dotenv import load_dotenv
from openai import OpenAI 
import json  

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get(""),
)

def query_db(sql):
    pass

def run_command(command):
    result = os.system(command=command)
    return result

print(run_command("ls -l"))

def get_weather(city):
    ##TODO : make an actual API call to get the weather information for the city
    print(f"Getting weather for {city}")
    url = f"https://wttr.in/{city}?format=%C+%t"
    # print(url)
    response  =  requests.get(url)
    if response.status_code == 200:
        return response.text
    
    return "Unable to get weather information at the moment"

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for the city"
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns ouput"
    }
}

system_prompt = f"""
    You are an helpfull AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - get_weather: Takes a city name as an input and returns the current weather for the city
    - run_command: Takes a command as input to execute on system and returns ouput

    
    
    Example:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interested in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}
"""


messages = [
    {"role": "system", "content": system_prompt}
]

while True:
    query = input("> ")
    messages.append({"role": "user", "content": query})
    while True:
        response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages
        )
        parsed_output  = json.loads(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(parsed_output)})

        if parsed_output["step"] == "plan":
            print(f"Planning : {parsed_output['content']}")
            continue
        elif parsed_output["step"] == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")
            print(f"Action : Calling tool {tool_name} with input {tool_input}")
            if available_tools.get(tool_name, False) != False:
                output = available_tools[tool_name].get("fn")(tool_input)
                print(f"Observation : {output}")
                messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                continue
        elif parsed_output["step"] == "output":
            print(f"Output : {parsed_output['content']}")
            break;

            

# response = client.chat.completions.create(
#     model="gpt-4o",
#     response_format={"type": "json_object"},
#     messages=[
#         {"role": "system", "content": system_prompt},
#         # {"role": "user", "content": query},
#         {"role": "user", "content": "what is the weather of halifax?"},
#         {"role": "assistant", "content": json.dumps({"step": "plan","content": "The user is interested in weather data for Halifax."})},
#         {"role": "assistant", "content": json.dumps({"step": "plan", "content": "From the available tools I should call get_weather."})},
#         {"role": "assistant", "content": json.dumps({"step": "action", "function": "get_weather", "input": "halifax"})},
#         {"role": "assistant", "content": json.dumps({"step": "observe", "output": "10 Degree Cel"})},
#     ]
# ) 

    # parsed_response  = json.loads(response.choices[0].message.content)
    # messages.append({"role": "assistant", "content": json.dumps(parsed_response)})
    # print(f"{parsed_response['step']} : {parsed_response['content']}")

    # if parsed_response["step"] == "result":
    #     break;


# print(response.choices[0].message.content)