import datetime
import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot

    @commands.command(name="kick",
                      usage="<user> <reason>",
                      description="Kicks a user from the server."
                      )
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def kick(self, ctx: commands.Context, user: discord.User, *, reason: str = None):
        """Command that kicks a user from the server.
        Args:
            user (discord.User, required): The user to kick.
            reason (str, optional): The reason for the kick. Defaults to None.
        """
        await ctx.trigger_typing()
        if reason is None:
            reason = "No reason given."
        await ctx.guild.kick(user, reason=reason)
        await ctx.reply(f"{user.mention} has been kicked from the server for {reason}", mention_author=False)

    @commands.command(name="ban",
                      usage="<user> <reason>",
                      description="Bans a user from the server."
                      )
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def ban(self, ctx: commands.Context, user: discord.User, *, reason: str = None):
        """Command that bans a user from the server.
        Args:
            user (mention, required): The user to ban.
            reason (str, optional): The reason for the ban. Defaults to None.
        """
        await ctx.trigger_typing()
        if reason is None:
            reason = "No reason provided."
        try:
            await ctx.guild.ban(user, reason=reason)
            await ctx.reply(f"**{user.name}** has been banned from the server for **{reason}**.", mention_author=False)
        except discord.Forbidden:
            await ctx.send("I don't have permissions to ban users.")

    @commands.command(name="clear",
                      usage="<amount>",
                      description="Clears a certain amount of messages."
                      )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def clear(self, ctx: commands.Context, amount: int = None):
        """Command that clears a certain amount of messages.
        Args:
            amount (int, optional): The amount of messages to clear. Defaults to 10
        """
        if amount is None:
            amount = 10
        if amount > 10000:
            return await ctx.send("You can't delete more than 100 messages at a time.")
        await ctx.channel.purge(limit=amount)
        msg = await ctx.send(f"Cleared **{amount}** messages.")
        await msg.delete(delay=5)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
