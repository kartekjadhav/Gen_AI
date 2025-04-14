from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

system_prompt = """
You are an AI assistant who is specialized in solving complex problems by breaking them into steps.
For any given query break down the problem into multiple steps.
Think for 5-6 times on how to solve the problem before producing an output.

The steps are you get the user's query as an inuput, you analyse the input, you think and you think again for several times and then you validate the answer. And finally afetr validating you output the result.

Output should be in JSON format only.
Output Format:
{step: "string", output: "string"}

Example: 
Input: What is 2 + 2?
Output : {{step: "analyze", output: "Alright! The user is trying to ask me maths realted query."}}
Output: {{step: "think", output: "for adding two numbers I can start from any side, but it it was multiplication query i whould i have to follow BODMAS rule"}}
Output: {{step: "output", output: "2 + 2 = 4"}}
Output: {{step: "validate", output: "seems like 4 is correct output for 4"}}
Output: {{step: "result", output: "2 + 2 = 4 which is calculated by adding 2 twice"}}

"""
query = input("> ")

messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

emoji_map = {
        "analyze": "🧠",
        "think": "🤔",
        "output": "🤓",
        "validate": "✅",
        "result": "🤖"
    }

while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        temperature=0.5,
        max_tokens=500,
        messages=messages
    )
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    output = json.loads(response.choices[0].message.content)
    print(emoji_map[output["step"]] + " " + output["output"])
    if output['step'] == 'result':
        break
