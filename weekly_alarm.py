import discord
from discord.ext import commands, tasks
import datetime
import os
import asyncio


# TODO, allow admins to give input and create alarms

def schedule_alarm():
    loop = asyncio.get_event_loop()
    loop.create_task(before_alarm())


@tasks.loop(hours=168)  # Run every minute
async def alarm():
    guild = ctx.guild
    message_content = f"@everyone Yo biatches! It's weekend. Go gamba! consolation price time..."
    
    for channel in guild.channels:
        if 'general' in channel.name.lower():
            await channel.send(message_content)
            return  # Stop after sending the message to the first matching channel
    # await channel.send(message_content)


async def before_alarm():
    # Set the target day (Saturday) and time (9 PM)
    target_day = 5  # Saturday (0-6, where Monday is 0 and Sunday is 6)
    target_time = datetime.time(hour=18, minute=00)  # 9 PM UTC

    now = datetime.datetime.utcnow()
    target_datetime = now.replace(hour=target_time.hour, minute=target_time.minute, second=0, microsecond=0)

    # Calculate the number of days until the target day
    days_ahead = (target_day - now.weekday()) % 7
    target_datetime += datetime.timedelta(days=days_ahead)

    # Calculate the time until the next scheduled alarm within the current week
    time_until_alarm = (target_datetime - now).total_seconds()
    if time_until_alarm < 0:
        time_until_alarm += 7 * 24 * 60 * 60  # Add one week

    await asyncio.sleep(time_until_alarm)
    alarm.start()
