import os

import discord
from discord.ext import commands
from utils.functions import download_avatar


class DownloadAV(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return
        avatar_url = member.avatar.url
        channel = self.bot.get_channel(969971223931007056)
        image = download_avatar(avatar_url)
        if image is True:
            embed = discord.Embed(
                title=f"New Member! 👨‍🚀",
                color=0xc6ea7e
            )
            embed.set_image(url=f"attachment://welcome_with_avatar.png")
            embed.description = f"{member.mention} has joined the server!"
            embed.set_footer(text=f"{member.guild.name}", icon_url=member.guild.icon.url)
            make_welcome_image(self, member=member)
            await channel.send(file=discord.File(f"assets/welcome_with_avatar.png"), embed=embed)
            os.remove('assets/avatar.png')
            os.remove('assets/welcome_with_avatar.png')
        else:
            return


def make_welcome_image(self, member):
    from easy_pil import Editor, Font
    poppins = Font.poppins(size=50, variant="bold")
    poppins_regular = Font.poppins(variant="regular", size=30)
    poppins_mediam = Font.poppins(variant="bold", size=40)
    board = Editor('assets/welcome.png')
    profile = Editor("assets/avatar.png").resize((200, 200)).circle_image()
    board.paste(profile, (100, 30))
    board.ellipse((100, 30), 200, 200, outline="#c6ea7e", stroke_width=4)
    board.text((205, 250), "WELCOME", color="#c6ea7e", font=poppins, align="center")
    board.text((205, 300), f"{member.name}#{member.discriminator}", color="#c6ea7e", font=poppins_mediam, align="center")
    members = len(self.bot.get_guild(member.guild.id).members)
    board.text((190, 350), f"YOU ARE MEMBER ", font=poppins_regular, color="white", align="center")
    board.text((355, 350), f"#{members}", font=poppins_mediam, color="#c6ea7e", align="center")
    board.save("assets/welcome_with_avatar.png")

async def setup(bot: commands.Bot):
    await bot.add_cog(DownloadAV(bot))
