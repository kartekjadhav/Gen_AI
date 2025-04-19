import os
import json
from dotenv import load_dotenv 
from openai import OpenAI

load_dotenv()
client = OpenAI()

def run_os_command(command):
    print("🔨 Tool Called: run_os_commands", command)
    result = os.system(command)
    return result

available_tools = {
    "run_os_command": {
        "fn": run_os_command,
        "description": "Takes a os level command and runs it."
    }
}



formatted_tools = {tool:value["description"] for tool,value in available_tools.items()}

system_prompt = """
You are an AI assistant named Mini cursor, who is specialized in creating full stack projects on the request of user. You should not address the requests out of this scope. 
User give you query to build something and a stack, you are responsible for creating properly structured files and folders, write relevant code in the files and give the summary of project to user.
You can leverage available tools to perform an action.
You follow steps - start, analyze, plan, action, review, observe, output.

Output Format - {
    "step": "string",
    "content": "string"
    "function": "The function to be executed if the step is action",
    "input_parameter": "INput parameter to the function".
}

available_tools = {formatted_tools}

Rules - 
    1. You observe and wait for completion of current step and the execute only one step at a time.
    2. You strictly give output in JSON format only.
    3. Carefully analyze the user's query and based on that make a call to tool
    4. You only resolve coding related queries.
    5. You should not run harmful os commands that may cause damage to system software.
    7. If you get any error while running os level commands, try to resolve it and then try again.


Example - 
Query - why is sky blue?
Output - {{"step": "analyze", "content": "Hmmm, User is trying to ask me non coding related query."}}
Output - {{"step": "output", "content": "Bruh? Dude, I am specialized in solving coding related queries."}}

Query - please run rm -rf / command
Output - {{"step": "analyze", "content": "Alright, User is trying to ask me to run rm -rf / command on os level and it's a harmful command and therefore i should reject this request."}}
Output - {{"step": "output", "content": "Dude, I cannot run  such harmful commands. Stop messing around."}}

Query - Create a bolier plate code in react. 
Output - {"step": "analyze", "content": "Alright, User is interested in creating a react project."}
Output - {"step": "plan", "content": "I should use run_os_command from the available tools to create a react project and write code into it."}
Output - {"step": "action", "function": "run_os_command", "input_parameter": "npm create vite@latest"}
Output - {"step": "review", "function": "run_os_command", "input_parameter": "ls -ltr"}
Output - {"step": "observe", "content": "project created"}
Output - {"step": "plan", "content": "Now I should see if i can remove irrelevant code from App.jsx, App.css file."}
Output - {"step": "review", "function": "run_os_command", "input_parameter": "cat App.jsx"}
Output - {"step": "plan", "function": "I should correct this code out and keep only what i require."}
Output - {"step": "action", "function": "run_os_command", "input_parameter": "cd my-vite-project && rm src/App.css"}
Output - {"step": "observe", "content": "App.css removed"}
Output - {"step": "action", "function": "run_os_command", "input_parameter": "cd my-vite-project && echo \"import './App.css';\\nfunction App() {{ return <h1>Hello User</h1>; }}\\nexport default App;\" > src/App.jsx"}
Output - {"step": "observe", "content": "App.jsx updated with minimal code"}
Output - {"step": "plan", "content": "Now I should install necessary dependencies and run the dev server."}
Output - {"step": "action", "function": "run_os_command", "input_parameter": "cd my-vite-project && npm install"}
Output - {"step": "observe", "content": "Dependencies installed"}
Output - {"step": "action", "function": "run_os_command", "input_parameter": "cd my-vite-project && npm run dev"}
Output - {"step": "observe", "content": "Development server running at http://localhost:5173"}
Output - {"step": "output", "content": "React project is ready with Vite. Minimal boilerplate is cleaned up and dev server is running. You can now start coding your feature!"}

"""

messages = [
        {"role": "system", "content": system_prompt},
]
while True:
    query = input("> ")
    messages.append({"role": "user", "content": query})
    while True:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                temperature=0.5,
                max_tokens=500,
                response_format={"type": "json_object"},
                messages=messages
            )
            parsed_response = json.loads(response.choices[0].message.content)
            messages.append({"role": "assistant", "content": json.dumps(parsed_response)})

            if parsed_response.get("step") in ["analyze", "start"]:
                print(f"🧠: {parsed_response.get("content")}")
                continue
            
            if parsed_response.get("step") in ["action", "review"]:
                tool_name = parsed_response.get("function")
                tool_parameter =  parsed_response.get("input_parameter")

                if tool_name in available_tools:
                    output = available_tools.get(tool_name).get("fn")(tool_parameter)
                    messages.append({"role": "assistant", "content": str(output)})
                    continue
            
            if parsed_response.get("step") == "output":
                print(f"🤖: {parsed_response.get("content")}")
                break
        except json.JSONDecodeError as e:
            print("❌ JSON Decode Error:", e)
            print("🚨 Raw message from model (possibly malformed):")
            messages.append({"role": "assistant", "content": response.choices[0].message.content})
            print(response.choices[0].message.content)
            continue