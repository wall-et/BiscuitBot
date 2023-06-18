import discord
from discord.ext import commands, tasks
import datetime
import os
import asyncio

from weekly_alarm import schedule_alarm
from knocknock import knock_joke


intents = discord.Intents.default()  # Create an instance of the Intents class
intents.typing = False  # Disable the typing event (optional)
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)  # Pass the intents argument

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
    # print(message)
    # print(message.content)
    if message.author.bot:
        return

    response = await knock_joke(message, bot)

    if response:
        await message.channel.send(response)

    await bot.process_commands(message)

# Command: !set_alarm
@bot.command()
async def set_alarm(ctx):
    duration = ctx.content.split(' ')[1]
    alarm_time = datetime.now() + datetime.timedelta(minus=int(duration))
    alarm_time_str = alarm_time.strftime('%d-%m-%Y %H:%M:%S')
    await ctx.send(f'Alarm set for {alarm_time_str}')
    await asyncio.sleep(int(duration) * 60)
    await ctx.send(f'@{ctx.author.mention} Wake up! It\'s time!')

# Run the bot
with open("./secrets") as f:
    _token = f.read().strip()

bot.run(_token)

# reminder, coin, news, sttime