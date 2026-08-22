
# from aifc import Aifc_read
import requests
import json
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5-coder:3b"

messages = []

def chat(messages: list[dict]):
    

    response = requests.post(
        OLLAMA_URL,
        json = {
            "model": MODEL,
            "messages" : messages,
            "stream" : True
        },
        stream = True
    )
    # AI_msg = response.json()["message"]["content"]
    print("\nAI: ")
    ai_res = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            content = data["message"]["content"]
            ai_res+=content
            print(content, end="", flush = True)

    print("\n")
    messages.append({
        "role" : "assistant",
        "content" : ai_res
    })
    # return history


while True:
    user_input = input("You: \n")
    messages.append(
        {"role":"user","content": user_input }
    )
    if user_input.lower().strip() in ("exit", "quit", "bye"):
        break
    chat(messages)


    
    
    

