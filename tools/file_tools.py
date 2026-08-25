
import os
def read_file(path: str) -> str:
    if not os.path.exists(path):
        return f"Error: file '{path}' does not exist."
    with open(path, "r") as f:
        return f.read()