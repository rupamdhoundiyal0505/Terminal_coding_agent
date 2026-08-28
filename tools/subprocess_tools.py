import subprocess

def run_command(command: str) -> str:
    dangerous = ["rm -rf", "sudo", ":(){:|:&};:"]
    if any(bad in command for bad in dangerous):
        return "Blocked: command matched a dangerous pattern."
    confirm = input(f"\n⚠️  AI wants to RUN: '{command}'. Allow? (y/n): ")
    if confirm.lower() != "y":
        return "User denied permission to run this command."
    
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=10
        )
        return f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"

        
    except subprocess.TimeoutExpired:
        return "Command timed out after 10 seconds."