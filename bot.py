# bot.py
import os
import discord
import re
import aiohttp
import asyncio
import random
from datetime import date

_token = os.getenv("DISCORD_TOKEN")
client = discord.Client()
phrases = ["rickroll", "rick roll", "rick astley", "never gonna give you up"]


def get_random_response():
    responses = []
    current_date = date.today()
    responses.append(f"Bruh.. its {current_date.year}!!")
    responses.append("Nice try..")
    responses.append("Maybe next time...")
    responses.append("Nope ❌")
    return random.choice(responses)


async def check_one_rickroll_present(session, url):
    try:
        async with session.get(url) as response:
            content = str(await response.content.read()).lower()
            return bool(re.findall("|".join(phrases), content, re.MULTILINE))
    except Exception:
        return False


async def check_all_rickroll_present(urls):
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *[check_one_rickroll_present(session, url) for url in urls]
        )
        return True in results


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    links = re.findall(r"(https?://\S+)", message.content)
    if len(links) == 0:
        return

    if await check_all_rickroll_present(links):
        await message.add_reaction("🚫")
        await message.reply(get_random_response())


client.run(_token)
