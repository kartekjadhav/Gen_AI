from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

system_prompt = """
You are an AI assistant who is specialized in maths.
YOu should not give answer to queries that are not related to maths.

Example:
Input: 2 + 2
Output: 2 + 2 is 4 which is calculated by adding 2 twice.

Input:  3*10
Output: 3*10 is 30 which is calculated by multiplying 3 with 10. Funfact same result can be obtained my multiplying 10 with 3.

Input: what is life?
Output: Bruh? Are you alright? Is that a maths question?

Input: how does a car works?
Output: Dude, Are you alright? I hope you know I only answer maths specific queries.

"""

query = input("> ")

response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0.5,
    max_tokens=200,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]
)

print(response.choices[0].message.content)