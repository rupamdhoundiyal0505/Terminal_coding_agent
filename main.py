import os
import json
from re import M
# from token import OP
from openai import OpenAI
from tools.file_tools import read_file, write_file
from dotenv import load_dotenv
from tools.subprocess_tools import run_command


load_dotenv()
client = OpenAI()
MODEL = "gpt-4o-mini"

messages = [
    {
        "role": "system",
        "content": (
            "You are a coding assistant with access to tools. "
            "When you receive a tool result, treat it as accurate and directly available to you — "
            "never say you cannot access something after a tool has already returned its content. "
            "Answer using the actual tool result data."
        )
    }
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "1. Read the contents of a file at a given path 2. if file is empty that is len(content)==0 then you should say the file is empty",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to read"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file at a given path. Creates the file if it doesn't exist, overwrites if it does.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to write"},
                    "content": {"type": "string", "description": "The content to write into the file"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a shell command and return its stdout/stderr output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The shell command to execute"}
                },
                "required": ["command"]
            }
        }
    }
]
total_tokens = {"prompt": 0, "completion": 0}
def chat(messages: list) -> list:
    # print(messages)

    while True:
        response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools
        )
        total_tokens["prompt"] = total_tokens["prompt"] + response.usage.prompt_tokens
        total_tokens["completion"] = total_tokens["completion"] + response.usage.completion_tokens
        

        message = response.choices[0].message
        # print(f"[DEBUG] This response contains {len(message.tool_calls) if message.tool_calls else 0} tool call(s)")

        # print("\n--- RAW MESSAGE ---")
        # # print(response.choices[0])
        # print(message)
        # print("--------------------\n")

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
                    # print(f"[DEBUG] tool_result = {repr(tool_result)}")
                elif fn_name == "write_file":
                    tool_result = write_file(fn_args["path"], fn_args["content"])
                elif fn_name == "run_command":
                    tool_result = run_command(fn_args["command"])
                else:
                    tool_result = f"Error: unknown tool '{fn_name}'"
                # print("\n--- TOOL RESULT ---")
                # print(tool_result)
                # print("--------------------\n")

                messages.append({
                    "role" : "tool",
                    "tool_call_id" : call.id,
                    "content" : tool_result
                })

        # Case 2: model just replied normally
        else:
            print("AI:", message.content)
            messages.append({"role": "assistant", "content": message.content})
            print("----------Token usage---------")
            print(total_tokens)
            return messages
    


while True:
    user_input = input("You: \n")
    if user_input.lower().strip() in ("exit", "quit", "bye"):
        break

    messages.append({"role": "user", "content": user_input})
    messages = chat(messages)