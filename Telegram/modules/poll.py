import json
from pyrogram import Client, filters

POLL_FILE = "data/polls.json"

if not os.path.exists(POLL_FILE):
    with open(POLL_FILE, "w") as f:
        json.dump({}, f)

@Client.on_message(filters.command("createpoll"))
async def create_poll(client, message):
    try:
        poll_name = message.text.split(" ", 1)[1]
        with open(POLL_FILE, "r+") as f:
            polls = json.load(f)
            polls[poll_name] = {}
            f.seek(0)
            f.truncate()
            json.dump(polls, f)
        await message.reply(f"Poll created: {poll_name}")
    except IndexError:
        await message.reply("Please provide a poll name!")

@Client.on_message(filters.command("vote"))
async def vote_poll(client, message):
    try:
        poll_name, option = message.text.split(" ", 2)[1:]
        with open(POLL_FILE, "r+") as f:
            polls = json.load(f)
            if poll_name not in polls:
                await message.reply("Poll not found!")
                return
            if option not in polls[poll_name]:
                polls[poll_name][option] = 0
            polls[poll_name][option] += 1
            f.seek(0)
            f.truncate()
            json.dump(polls, f)
        await message.reply(f"Voted for: {option} in poll: {poll_name}")
    except IndexError:
        await message.reply("Usage: .vote <poll_name> <option>")

@Client.on_message(filters.command("viewpoll"))
async def view_poll(client, message):
    try:
        poll_name = message.text.split(" ", 1)[1]
        with open(POLL_FILE, "r") as f:
            polls = json.load(f)
            if poll_name not in polls:
                await message.reply("Poll not found!")
                return
            result = "\n".join([f"{opt}: {votes}" for opt, votes in polls[poll_name].items()])
        await message.reply(f"Poll: {poll_name}\n\n{result}")
    except IndexError:
        await message.reply("Please provide a poll name!")
