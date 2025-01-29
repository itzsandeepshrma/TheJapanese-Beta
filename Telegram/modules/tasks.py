from pyrogram import Client, filters
from pyrogram.types import Message
import json
import os

TASKS_FILE = "data/tasks.json"

# Ensure the file exists
if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, "w") as f:
        json.dump({}, f)

@Client.on_message(filters.command("addtask"))
async def add_task(client, message: Message):
    task = message.text.split(" ", 1)[1] if " " in message.text else None
    if not task:
        await message.reply("Please provide a task.")
        return
    
    user_id = str(message.from_user.id)
    with open(TASKS_FILE, "r+") as f:
        tasks = json.load(f)
        if user_id not in tasks:
            tasks[user_id] = []
        tasks[user_id].append(task)
        f.seek(0)
        json.dump(tasks, f)
    
    await message.reply(f"Task added: {task}")

@Client.on_message(filters.command("viewtasks"))
async def view_tasks(client, message: Message):
    user_id = str(message.from_user.id)
    with open(TASKS_FILE, "r") as f:
        tasks = json.load(f)
        user_tasks = tasks.get(user_id, [])
        if user_tasks:
            reply = "\n".join([f"{i+1}. {task}" for i, task in enumerate(user_tasks)])
        else:
            reply = "You have no tasks."
    await message.reply(reply)

@Client.on_message(filters.command("deltask"))
async def delete_task(client, message: Message):
    try:
        task_number = int(message.text.split(" ")[1]) - 1
    except (IndexError, ValueError):
        await message.reply("Please provide a valid task number.")
        return
    
    user_id = str(message.from_user.id)
    with open(TASKS_FILE, "r+") as f:
        tasks = json.load(f)
        user_tasks = tasks.get(user_id, [])
        if 0 <= task_number < len(user_tasks):
            deleted_task = user_tasks.pop(task_number)
            f.seek(0)
            f.truncate()
            json.dump(tasks, f)
            await message.reply(f"Deleted task: {deleted_task}")
        else:
            await message.reply("Invalid task number.")
