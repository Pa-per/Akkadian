import asyncio
import discord
from discord.ext import commands
from utils.functions import get_price

class PriceCheck(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot

    @commands.command(name='price',
                      aliases=['pricecheck'],
                      description='Check the price of a product on Amazon (only tested on Amazon.co.uk atm.)',
                      usage=""
                      )
    async def price_check(self, ctx):
        try:
            await ctx.message.delete()
            message = await ctx.send("Please send your Amazon URL now.")
            try:
                response = await self.client.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60)
            except  asyncio.TimeoutError:
                await response.delete()
                await message.edit("Timed out")
            else:
                await response.delete()
                await message.edit(content="Checking...")
                price_text, product_name = get_price(response.content)
                # use this later for price comparison
                # price = price_text[1:]
                embed = discord.Embed(title=f"Amazon Price Check", description=f"{product_name}", color=0x00ff00)
                embed.add_field(name="Price", value=f"{price_text}", inline=False)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                await message.edit(content="", embed=embed)
        except Exception as e:
            print(e)
        
        
async def setup(bot: commands.Bot):
    await bot.add_cog(PriceCheck(bot))