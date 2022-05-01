from discord.ext import commands


class commandErrors(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply(f"The argument you entered was not found. Please check your spelling and try again.", mention_author=False)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(f"You do not have the required permissions to use this command.", mention_author=False)
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"You are on cooldown. Please wait {error.retry_after:.2f} seconds and try again.", mention_author=False)
        elif isinstance(error, commands.CheckFailure):
            await ctx.reply(f"You are not allowed to use this command.", mention_author=False)


async def setup(bot: commands.Bot):
    await bot.add_cog(commandErrors(bot))
