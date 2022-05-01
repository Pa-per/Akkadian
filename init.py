import json
import os
import platform

import discord
from colorama import Fore
from discord.ext import commands

intents = discord.Intents.all()

client = commands.Bot(command_prefix="#", intents=intents)

with open("config.json") as file:
    data = json.load(file)
    bot_version = data["bot"]["version"]
    creators = data["bot"]["creator"]
    token = data["bot"]["token"]
    owner = data["bot"]["owner"]

class Greetings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

@client.event
async def on_ready():
    for filename in os.listdir("commands"):
        if filename.endswith(".py"):
            await client.load_extension(f"commands.{filename[:-3]}")
    for filename in os.listdir("events"):
        if filename.endswith(".py"):
            await client.load_extension(f"events.{filename[:-3]}")
    print(Fore.GREEN + "MODERATION Initialised" + Fore.RESET)
    print(Fore.GREEN + "MINECRAFT Initialised" + Fore.RESET)
    print(Fore.GREEN + "ERRORS Initialised" + Fore.RESET)
    print(Fore.MAGENTA + f"""
─█▀▀█ █─█ █─█ █▀▀█ █▀▀▄ ─▀─ █▀▀█ █▀▀▄ 
░█▄▄█ █▀▄ █▀▄ █▄▄█ █──█ ▀█▀ █▄▄█ █──█ 
░█─░█ ▀─▀ ▀─▀ ▀──▀ ▀▀▀─ ▀▀▀ ▀──▀ ▀──▀


       █▀█ █▄░█ █░░ █ █▄░█ █▀▀
       █▄█ █░▀█ █▄▄ █ █░▀█ ██▄

―――――――――――――――――――――――――――――――――――――""")
    print(Fore.CYAN +
          f" 「 {bot_version} 」|「 Created by: {creators} 」" + Fore.RESET)
    # print only the version number that i am using
    print(Fore.LIGHTYELLOW_EX + f" 「 d.py: {discord.__version__}  」|「 py: {platform.python_version()} 」" + Fore.RESET)
    await client.change_presence(activity=discord.Streaming(platform= "Twitch", name='brokeback mountain', url='https://www.twitch.tv/monstercat'))


# reload all cogs if the bot owner runs the command
@client.command()
async def reload(ctx):
    if ctx.author.id == int(owner):
        for filename in os.listdir("commands"):
            if filename.endswith(".py"):
                await client.unload_extension(f"commands.{filename[:-3]}")
        for filename in os.listdir("events"):
            if filename.endswith(".py"):
                await client.unload_extension(f"events.{filename[:-3]}")
        for filename in os.listdir("commands"):
            if filename.endswith(".py"):
                await client.load_extension(f"commands.{filename[:-3]}")
        for filename in os.listdir("events"):
            if filename.endswith(".py"):
                await client.load_extension(f"events.{filename[:-3]}")
        await ctx.send("Reloaded all cogs")
    else:
        return

client.run(token)
