import re

def validate_command(command):
    # Simple validation for commands
    pattern = r"^[a-zA-Z0-9_]+$"
    return re.match(pattern, command)
