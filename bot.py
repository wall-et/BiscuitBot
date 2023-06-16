import discord
from discord.ext import commands, tasks
import datetime
import os
import asyncio

from weekly_alarm import schedule_alarm
from knocknock import knock_joke

# Create a new bot instance
bot = commands.Bot(command_prefix='!')

# Command: !hello
@bot.command()
async def hello(ctx):
    await ctx.send('Hello, world!')


# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await bot.wait_until_ready()
    schedule_alarm() 

@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore messages from bots

    await knock_joke(message, bot)

    await bot.process_commands(message)



# Run the bot
with open("./secrets") as f:
    _token = f.read().strip()

bot.run(_token)

# reminder, coin, news, sttime