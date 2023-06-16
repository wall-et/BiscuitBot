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
        return "Who's there?"  # Bot responds with "Who's there?"

    # Check the current joke stage and construct the response accordingly
    if message.channel.id in joke_stages:
        stage = joke_stages[message.channel.id]
        print(stage)
        if stage == 'setup':
            # joke_stages[message.channel.id] = 'response'  # Move to the response stage
            # return None  # Return None to prompt the user for a response
        # elif stage == 'response':
            joke_stages[message.channel.id] = 'punchline'  # Move to the punchline stage
            name = message.content  # User's response
            return f"{name} who?"  # Bot responds by quoting the user with "name who?"
        elif stage == 'punchline':
            joke_stages.pop(message.channel.id)  # Remove the joke stage entry
            await message.add_reaction('\U0001F923')  # Add laughing emoji reaction
            return None #f"{message.content}, that's a good one!"  # Bot responds with the punchline

    return None  # Return None if no response is needed