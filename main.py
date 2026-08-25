import os
import json
from re import M
# from token import OP
from openai import OpenAI
from tools.file_tools import read_file
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
MODEL = "gpt-4o-mini"

messages = []

tools =[
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file at a given path",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to read"
                    }
                },
                "required": ["path"]
            }
        }
    }
]

def chat(messages: list) -> list:
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools
    )

    message = response.choices[0].message

    print("\n--- RAW MESSAGE ---")
    print(message)
    print("--------------------\n")

    # Case 1: model wants to call a tool
    if message.tool_calls:
        # append the assistant's tool-call message first (required by OpenAI's format)
        messages.append(message)

        for call in message.tool_calls:
            fn_name = call.function.name
            fn_args = json.loads(call.function.arguments)  # arguments come as a JSON string here

            print(f"AI wants to call: {fn_name}({fn_args})")

            if fn_name == "read_file":
                tool_result = read_file(fn_args["path"])
                print("\n--- TOOL RESULT ---")
                print(tool_result)
                print("--------------------\n")

        # NOTE: not feeding tool_result back yet — that's the next step

    # Case 2: model just replied normally
    else:
        print("AI:", message.content)
        messages.append({"role": "assistant", "content": message.content})

    return messages


while True:
    user_input = input("You: \n")
    if user_input.lower().strip() in ("exit", "quit", "bye"):
        break

    messages.append({"role": "user", "content": user_input})
    messages = chat(messages)