import json
import platform

import discord
from colorama import Fore
from discord.ext import commands
from pymongo import MongoClient

from utils.functions import load_cogs, set_status

intents = discord.Intents.all()

with open("config.json") as file:
    data = json.load(file)
    bot_version = data["bot"]["version"]
    creators = data["bot"]["creator"]
    token = data["bot"]["token"]
    owner = data["bot"]["owner"]
    cluster = MongoClient(data["mongodb"]["cluster"])
    db = cluster["Akkadian"]
    serverConfigs = db["Guilds"]


async def get_prefix(self, message):

    query = {"_id": message.guild.id}

    guilds = serverConfigs.find(query)

    for result in guilds:

        return result["prefix"]

client = commands.Bot(command_prefix=get_prefix, intents=intents)


class Greetings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


@client.event
async def on_ready():

    await load_cogs(client)

    await set_status(client)

    print(Fore.CYAN +
          f" 「 {bot_version} 」|「 Created by: {creators} 」" + Fore.RESET)

    print(Fore.LIGHTYELLOW_EX +
          f" 「 d.py: {discord.__version__}  」|「 py: {platform.python_version()} 」" + Fore.RESET)


@client.event
async def on_guild_join(guild: discord.Guild):
    query = {"_id": guild.id}

    if serverConfigs.count_documents(query) == 0:

        default_prefix = "."

        new_prefix = {"_id": guild.id, "prefix": default_prefix}

        serverConfigs.insert_one(new_prefix)


@client.event
async def on_guild_remove(guild: discord.Guild):
    query = {"_id": guild.id}

    if serverConfigs.count_documents(query) == 1:

        serverConfigs.delete_one(query)

        print("Removed guild from database")


@client.event
async def on_message(message):

    if not message.guild:
        return

    if message.content.startswith(
        f"<@!{client.user.id}>"
    ) or message.content.startswith(f"<@{client.user.id}>"):

        query = {"_id": message.guild.id}

        if serverConfigs.count_documents(query) == 0:

            default_prefix = "-"

            new_prefix = {"_id": message.guild.id,
                          "prefix": default_prefix}

            serverConfigs.insert_one(new_prefix)

            await message.reply(
                f"**Hello!**\nMy prefix for this server is: `{default_prefix}`"
            )

        else:

            query = {"_id": message.guild.id}

            guild = serverConfigs.find(query)

            for result in guild:

                prefix = result["prefix"]

                await message.reply(
                    f"**Hello!**\nMy prefix for this server is: `{prefix}`"
                )

    await client.process_commands(message)


client.run(token)
