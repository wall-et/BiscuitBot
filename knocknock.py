import discord
from discord.ext import commands, tasks
import asyncio


joke_stages = {}


async def knock_joke(message, bot):
    
    content = message.content.lower()
    mentioned = bot.user in message.mentions
    
    # Check if the bot is mentioned and the message contains "knock knock"
    if mentioned and 'knock knock' in content:
        joke_stages[message.channel.id] = 'setup'  # Set the initial joke stage to setup
        await message.channel.send("Who's there?")

    # Check the current joke stage and respond accordingly
    if message.channel.id in joke_stages:
        stage = joke_stages[message.channel.id]
        if stage == 'setup':
            joke_stages[message.channel.id] = 'response'  # Move to the response stage
        elif stage == 'response':
            joke_stages[message.channel.id] = 'punchline'  # Move to the punchline stage
            await message.channel.send(f"{message.content} who?")
        elif stage == 'punchline':
            # await message.channel.send("Haha, that's a good one!")
            await message.add_reaction('\U0001F923')  # Add laughing emote to the response
            del joke_stages[message.channel.id]  # Remove the joke stage entry
    