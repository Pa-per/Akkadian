import json
import os

from discord.ext import commands
from discord.ext.commands import ExtensionError

with open("config.json") as file:
    data = json.load(file)
    owner_id = data["bot"]["owner"]


class owner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot

    @commands.command(name= "reloadall")
    async def reload(self, ctx: commands.Context):
        if ctx.author.id == int(owner_id):
            try:
                for filename in os.listdir("commands") and os.listdir("events"):
                    if filename.endswith(".py"):
                        try:
                            await self.client.unload_extension(f"commands.{filename[:-3]}")
                        except ExtensionError:
                            await self.client.unload_extension(f"events.{filename[:-3]}")
                for filename in os.listdir("commands") and os.listdir("events"):
                    if filename.endswith(".py"):
                        try:
                            await self.client.load_extension(f"commands.{filename[:-3]}")
                        except ExtensionError:
                            await self.client.load_extension(f"events.{filename[:-3]}")
                await ctx.send("Reloaded all cogs")
            except Exception as e:
                print(e)
        else:
            return


async def setup(bot: commands.Bot):
    await bot.add_cog(owner(bot))
