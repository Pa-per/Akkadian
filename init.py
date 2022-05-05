import json
import os
import platform

import discord
from colorama import Fore
from discord.ext import commands
from discord.ext.commands import ExtensionError

intents = discord.Intents.all()

client = commands.Bot(command_prefix="#", intents=intents)

with open("config.json") as file:
    data = json.load(file)
    bot_version = data["bot"]["version"]
    creators = data["bot"]["creator"]
    token = data["bot"]["token"]
    owner = data["bot"]["owner"]
    streaming = data["bot"]["status"]["streaming"]["boolean"]
    watching = data["bot"]["status"]["watching"]["boolean"]
    playing = data["bot"]["status"]["playing"]["boolean"]

class Greetings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

@client.event
async def on_ready():
    print(str(os.listdir))
    for filename in os.listdir("commands"):
        if filename.endswith(".py"):
            await client.load_extension(f"commands.{filename[:-3]}")
            print(f"Loaded {filename[:-3]}")
    for filename in os.listdir("events"):
        if filename.endswith(".py"):
            await client.load_extension(f"events.{filename[:-3]}")
            print(f"Loaded {filename[:-3]}")
    print(Fore.CYAN +
          f" 「 {bot_version} 」|「 Created by: {creators} 」" + Fore.RESET)
    print(Fore.LIGHTYELLOW_EX +
          f" 「 d.py: {discord.__version__}  」|「 py: {platform.python_version()} 」" + Fore.RESET)
    status = data["bot"]["status"]["status"]
    if streaming == "True":
        platform_ = data["bot"]["status"]["streaming"]["type"]
        name = data["bot"]["status"]["streaming"]["game"]
        url = data["bot"]["status"]["streaming"]["url"]
        await client.change_presence(activity=discord.Streaming(platform=platform_, name=name, url=url))
    elif watching == "True":
        activity = data["bot"]["status"]["watching"]["watching"]
        if status == "online":
            await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=activity))
        elif status == "dnd":
            await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=activity))
        elif status == "idle":
            await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=activity))
    elif playing == "True":
        game = data["bot"]["status"]["playing"]["game"]
        if status == "online":
            await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=game))
        elif status == "dnd":
            await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name=game))
        elif status == "idle":
            await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.playing, name=game))

client.run(token)