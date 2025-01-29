tasks = []

def handle_tasks(command: str) -> str:
    """
    Process task management commands.
    :param command: The text of the user's command.
    :return: A response message.
    """
    global tasks
    if command.startswith(".tasks add"):
        task = command.replace(".tasks add", "").strip()
        tasks.append(task)
        return f"Task added: {task}"
    elif command.startswith(".tasks list"):
        if tasks:
            return "\n".join([f"{i+1}. {task}" for i, task in enumerate(tasks)])
        else:
            return "No tasks found."
    elif command.startswith(".tasks clear"):
        tasks.clear()
        return "All tasks cleared."
    else:
        return "Invalid command. Use `.tasks add <task>`, `.tasks list`, or `.tasks clear`."
