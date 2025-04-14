import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

def run_os_commands(command):
    print("🔨 Tool Called: run_os_commands", command)
    result = os.system(command)
    return result

def get_weather(city: str):
    print("🔨 Tool Called: get_weather", city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "Something went wrong"

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "This function take the input as city name and returns it's current weather."
    },
    "run_os_commands": {
        "fn": run_os_commands,
        "description": "This function take an os command as input amd executes it."
    }
}

system_prompt = """
You are an helpful AI assistant whose job is to resolve users queries.
For a given query you perform these steps - start, analyze, plan, action, observer, output.
You can leverage available tools, and based on your thinking and analyzing you select the relevent tool from available tools.
Based on the tool you perform action to call the tool.
Wait for the observation and based on observation from tool call you resolve user's query
Also if you already know something then dont do call to the relevant tool for next 5 mins to save time.

Rules:
 - Follow JSON output
 - Perform one step at a time, and wait for it's completion before moving to next step.
 - Carefully analyze the user's query and based on that make a call to tool

Available Tools - 
    get_weather: Takes a city name as input and returns the current weather for the city.
    run_os_commands: This function take an os command as input amd executes it.

Output JSON format -
    {
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter to function"
    }

Example:
User: what is weather of Nagpur?
Output: {{"step": "analyze", "content": "Alright! the user is interesetd in knowing current weather of Nagpur city"}} 
Output: {{"step": "plan", "content": "Based on available tools i should call get_weather."}} 
Output: {{"step": "action", "function": get_weather, "input": "Nagpur"}} 
Output: {{"step": "observe", "content": "27 degree celcius"}} 
Output: {{"step": "output", "content": "The weather of Nagpur currently is 27 degree celcius."}} 
"""

while True:
    messages = [{"role": "system", "content": system_prompt}]
    query = input("> ")
    while True:
        messages.append({"role": "user", "content": query})
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            temperature=0.5,
            max_tokens=500,
            messages=messages
        )
        parsed_response = json.loads(response.choices[0].message.content) 
        messages.append({"role": "assistant", "content": json.dumps(parsed_response)})
        if parsed_response["step"] == "plan" or parsed_response["step"] == "start":
            print(f"🧠: {parsed_response.get("content")}")
            continue
            
        if parsed_response.get("step") == "action":
            tool_name = parsed_response.get("function")
            tool_parameter = parsed_response.get("input")

            if tool_name in available_tools:
                tool_output = available_tools.get(tool_name).get("fn")(tool_parameter)
                messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "content": tool_output})})
                continue
        
        if parsed_response.get("step") == "output":
            print(f"🤖: {parsed_response.get('content')}")
            break