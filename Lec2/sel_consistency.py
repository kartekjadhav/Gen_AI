from collections import Counter
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

emoji_map = {
        "analyze": "🧠",
        "think": "🤔",
        "output": "🤓",
        "validate": "✅",
        "result": "🤖"
    }

paths = 5
responses = []
for _ in range(paths):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]
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
            responses.append(output["output"])
            break

results_counter = Counter(responses)
most_common_result, count = results_counter.most_common(1)[0]

print("================ Self Consistency Analysis ================")
print(f"Generated {paths} reasoning paths")
print(f"Most common result (appeared {count} times):")
print(most_common_result)
    
# Calculate consistency percentage
consistency = (count / paths) * 100
print(f"\nConsistency: {consistency:.1f}%")

if consistency < 60:
    print("Warning: Low consistency in answers. The problem might be ambiguous or complex.")
else:
    print("No results were generated.")