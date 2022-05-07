import aiohttp
import discord
from discord.ext import commands
from utils.functions import check_exists
from utils.responses import (found_embed, not_found, searching,
                             something_went_wrong)


class MinecraftAccount(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot

    @commands.command(name="skin",
                      usage="<account name>",
                      description="Retrieves the users minecraft account skin (if it exists).")
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def skin(self, ctx: commands.Context, name: str):
        """Command that retrieves the users minecraft account skin
        Args:
            name (str, optional): A Mojang/Microsoft account username. Defaults to None.
        """
        await ctx.trigger_typing()
        msg = await ctx.reply(embed=searching, mention_author=False)
        data = await check_exists(name)
        if data is False:
            return await msg.edit(embed=not_found)
        uuid = data["id"]
        name_ = data["name"]
        image = f"https://crafthead.net/armor/body/{uuid}"
        found_embed.description = f"[`{name_}`]"
        found_embed.set_image(url=image)
        await msg.edit(embed=found_embed)

    @commands.command(name="names",
                      usage="<account name>",
                      description="Retrieves a users name history."
                      )
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def names(self, ctx: commands.Context, name: str):
        """Command that retrieves a users previous usernames if any.

        Args:
            name (str, optional): The Mojang/Microsoft username to search. Defaults to None.
        """
        await ctx.trigger_typing()
        msg = await ctx.reply(embed=searching, mention_author=False)
        data = await check_exists(name)
        if data is False:
            return await msg.edit(embed=not_found)
        else:
            UUID = data["id"]
            session = aiohttp.ClientSession()
            async with session.get(f"https://api.mojang.com/user/profiles/{UUID}/names") as response:
                if response.status != 200:
                    await session.close()
                    await msg.edit(embed=something_went_wrong)
                else:
                    data = await response.json()
                    await session.close()
                    found_names = len(data) - 1
                    current_name = data.pop()
                    found_names_embed = discord.Embed(
                        title="Name Search | ✅", description=f"Found a total of {found_names} previous name(s)", color=discord.Color.from_rgb(0, 255, 154))
                    found_names_embed.set_thumbnail(
                        url=f"https://minotar.net/armor/bust/{name}/190.png")
                    if "changedToAt" in current_name:
                        timestamp = current_name["changedToAt"] / 1000
                        found_names_embed.add_field(
                            name="Current Name", value=f"`{current_name['name']}` - <t:{int(timestamp)}:R>", inline=False)
                    else:
                        found_names_embed.add_field(
                            name="Current Name", value=f"`{current_name['name']}` - Original", inline=False)
                    if found_names != 0:
                        names = ""
                        for name in data:
                            if "changedToAt" in name:
                                timestamp = name["changedToAt"] / 1000
                                name = name['name']
                                names += f"`{name}` - <t:{int(timestamp)}:R>\n"
                            else:
                                original_name = name['name']
                                names += f"`{original_name}` - Original\n"
                        found_names_embed.add_field(
                            name="Names Found", value=names)
                    await msg.edit(embed=found_names_embed)

    @commands.command(name="uuid",
                      usage="<account name>",
                      description="Retrieves a users UUID.")
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def uuid(self, ctx: commands.Context, name: str):
        """Command that retrieves a users UUID.
        Args:
            name (str, optional): The Mojang/Microsoft username to search. Defaults to None.
        """
        await ctx.trigger_typing()
        msg = await ctx.reply(embed=searching, mention_author=False)
        data = await check_exists(name)
        if data is False:
            return await msg.edit(embed=not_found)
        else:
            UUID = data["id"]
            found_embed = discord.Embed(title="UUID Search | ✅",
                                        color=discord.Color.from_rgb(0, 255, 154))
            found_embed.description = f"[`{name}`]"
            found_embed.set_thumbnail(
                url=f"https://minotar.net/armor/bust/{name}/190.png")
            found_embed.add_field(
                name="UUID", value=f"`{UUID}`", inline=False)
            await msg.edit(embed=found_embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(MinecraftAccount(bot))
