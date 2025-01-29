from pyrogram import Client, filters
from pyrogram.types import Message
import random

@Client.on_message(filters.command("game"))
async def play_game(client, message: Message):
    games = ["Rock, Paper, Scissors", "Truth or Dare", "Guess the Number"]
    await message.reply(f"Let's play: {random.choice(games)}!")

@Client.on_message(filters.command("roll"))
async def roll_dice(client, message: Message):
    dice = random.randint(1, 6)
    await message.reply(f"You rolled a {dice} 🎲")
