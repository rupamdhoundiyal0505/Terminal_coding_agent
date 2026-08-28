
import os
def read_file(path: str) -> str:
    if not os.path.exists(path):
        return f"Error: file '{path}' does not exist."
    with open(path, "r") as f:
        return f.read()


def write_file(path : str, content : str) -> str:
    confirm = input(f"\n⚠️  AI wants to WRITE to '{path}'. Allow? (y/n): ")
    if confirm.lower() != "y":
        return "User denied permission to write this file!!"
    with open(path, "w") as f:
        f.write(content)
    return f"Successfully wrote to {path}."